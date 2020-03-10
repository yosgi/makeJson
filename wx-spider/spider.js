'use strict';

const rds = require('ali-rds');
const config = require('./config');
const vendor = 'tuotu';
const sapi = require('./' + vendor);
const MongoClient = require('mongodb').MongoClient;
const moment = require('moment');
const md5 = require("crypto-js/md5");

const db = rds(config.db);

async function taskBegin() {
    console.log('fetch article begin')
    const client = await MongoClient.connect(config.mongo.url, {useUnifiedTopology: true});
    const mdb = await client.db('wxspider');
    await sapi.setMongo(mdb);
    const articleTable = await mdb.collection('article');
    const accountTable = await mdb.collection('account');

    const accountList = config.wxAccount;
    for (let i = 0; i < accountList.length; i++) {
        const wxAccount = accountList[i];
        await fetch(wxAccount, articleTable, accountTable);
    }
    client.close()
    db.getConnection().then(conn => {
        conn.conn.destroy()
    });
    console.log('fetch article finish')
}

async function fetch(wxAccount, articleTable, accountTable) {
    const accountRow = await accountTable.find({userName: wxAccount.userName}).toArray();
    let lastTime = parseInt(moment().subtract(7, 'days').startOf('day').format('x') / 1000);
    if (accountRow.length == 0) {
        await accountTable.insertOne({
            userName: wxAccount.userName,
            name: wxAccount.name,
        });
    } else if (accountRow[0].lastTime) {
        await accountTable.updateOne({
            userName: wxAccount.userName,
        }, {
            $set: { name : wxAccount.name }
        });
        if (accountRow[0].lastTime > lastTime) {
            lastTime = accountRow[0].lastTime;
        }
    }
    let offset = 0;
    const curTime = parseInt(moment().format('x') / 1000);
    const start = moment().toISOString();
    if (curTime - lastTime < 3600) {
        return;
    }
    while(1) {
        let { articles, nextOffset } = await sapi.history(wxAccount, offset, start, lastTime);
        nextOffset = parseInt(nextOffset);
        if (articles.length > 0) {
            const addList = [];
            articles.forEach(article => {
                addList.push(addArticle(article, wxAccount, articleTable))
            });
            await Promise.all(addList);
            console.log(`${wxAccount.name} - next offset - ${offset}`)
        } else {
            break;
        }
        if (nextOffset <= offset) {
            break;
        }
        offset = nextOffset;
    }
    await accountTable.updateOne({
        userName: wxAccount.userName,
    }, {
        $set: { lastTime : curTime }
    });
}

async function addArticle(article, wxAccount, articleTable) {
    let articleTitle = `${article.title} - ${wxAccount.name}`;
    if (article.author != '') {
        articleTitle += ' - ' + article.author;
    }
    const articleExist = await articleTable.find({"baseInfo.appMsgId": article.data.baseInfo.appMsgId, "detailInfo.itemIndex": article.data.detailInfo.itemIndex}).count();
    if (articleExist > 0) {
        return;
    }
    const addData = {
        subject: articleTitle,
        subtitle: wxAccount.subtitle,
        source: 'EEFOCUS',
        channel: wxAccount.channel,
        author: wxAccount.eefAuthorId,
        user: config.eefUserId,
        category: 2,
        content: article.content.replace(new RegExp('^(?:\s|<(?:p|div)>(?:&nbsp;|\s)*</(?:p|div)>)*(<p class="pagebreak page-title">[^>]*</p>\s)?(?:\s|<(?:p|div)>(?:&nbsp;|\s)*</(?:p|div)>)*', 'gi'), '$1')
            .replace(new RegExp('([\u4e00-\u9fa5])([a-zA-Z0-9\._\\-\/\\\\]+)', 'gi'), '$1 $2')
            .replace(new RegExp('([a-zA-Z0-9\._\\-\/\\\\]+)([\u4e00-\u9fa5])', 'gi'), '$1 $2')
            .replace(/data-src="(.*?)"/g, function(match, url) {
                return 'src="' + config.imgUrl + 'url=' + encodeURIComponent(url) + '&s=' + md5(url + 'F5WDkx1NpyvNolBD').toString().substr(2, 6) + '"';
            }),
        summary: '',
        status: 2,
        tag: JSON.stringify(wxAccount.tags),
        related: '[]',
        partnumber: '[]',
        manufacturer: '[]',
        related_type: 1,
        time_save: parseInt(moment().format('x')/1000),
        poll_url: '',
        slug: '',
        pages: 1,
    }
    let match;
    const reg = /<(?:p|span)[^>]*>([^<]+?)<\//g;
    while ((match = reg.exec(article.content)) != null) {
        const matchContent = match[1].replace('&nbsp;', '');
        if (matchContent.length > 10 || (matchContent.length > 5 && matchContent.indexOf('作者') === -1 && matchContent.indexOf('原创') === -1)) {
            addData.summary = matchContent;
            break;
        }
    }
    const result = await db.insert('eef_article_draft', addData);
    await articleTable.insertOne({ ...article.data, articleId: result.insertId});
}

module.exports = {
    taskBegin,
}