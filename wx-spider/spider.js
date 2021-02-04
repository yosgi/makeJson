'use strict';

const rds = require('ali-rds');
const config = require('./config');
const sapi = require('./' + config.spider.default);
const MongoClient = require('mongodb').MongoClient;
const moment = require('moment');
const md5 = require("crypto-js/md5");
const sanitizeHtml = require('sanitize-html');
const cheerio = require('cheerio');
const image = require('./image');

const db = rds(config.db);

async function taskBegin(command) {
    console.log('fetch article begin')
    const client = await MongoClient.connect(config.mongo.url, {useUnifiedTopology: true});
    const mdb = await client.db('wxspider');
    await sapi.setMongo(mdb);
    const articleTable = await mdb.collection('article');
    const accountTable = await mdb.collection('account');

    let skip = 0;
    const limit = 10;
    while(1) {
        const accountList = await accountTable.find({}, {
            sort: {_id: 1},
            limit,
            skip,
        }).toArray();
        skip += limit;
        if (!accountList || accountList.length <= 0) {
            break;
        }
        for (let i = 0; i < accountList.length; i++) {
            await fetch(accountList[i], articleTable, accountTable, command);
            if (command != 'test') {
                await image.download();
            }
        }
    }
    client.close()
    db.getConnection().then(conn => {
        conn.conn.destroy()
    });
    console.log('fetch article finish')
}

async function fetchAll(accountList) {
    if (config.spider.default !== 'tianapi') {
        console.log('api not supported')
        return
    }
    console.log('fetch article begin')
    const client = await MongoClient.connect(config.mongo.url, {useUnifiedTopology: true});
    const mdb = await client.db('wxspider');
    await sapi.setMongo(mdb);
    const articleTable = await mdb.collection('article');

    for (let i = 0; i < accountList.length; i++) {
        const wxAccount = accountList[i];
        let page = 0

        while (1) {
            console.log(`${wxAccount.name} - page ${page}`)
            const [hasNext, articles] = await sapi.articles({wxAccount,page});
            if (articles.length > 0) {
                const addList = [];
                articles.forEach(article => {
                    addList.push(addArticle(article, wxAccount, articleTable, {"detailInfo.contentUrl": article.data.detailInfo.contentUrl}))
                });
                await Promise.all(addList);
            }
            if (!hasNext) {
                break;
            }
            page++
        }
    }
    client.close()
    db.getConnection().then(conn => {
        conn.conn.destroy()
    });
    console.log('fetch article finish')
}

async function fetch(wxAccount, articleTable, accountTable, command) {
    if (!wxAccount.lastTime || wxAccount.lastTime == 0) {
        wxAccount.lastTime = parseInt(moment().subtract(1, 'days').startOf('day').format('x') / 1000);
    }

    let offset = 0;
    const curTime = parseInt(moment().format('x') / 1000);
    const start = moment().toISOString();
    if (curTime - wxAccount.lastTime < 1800) {
        return;
    }

    if (config.spider.default == 'tuotu') {
        // use history api
        try {
            while(1) {
                let { articles, nextOffset } = await sapi.history(wxAccount, offset, start, command);
                if (command == 'test') {
                    return;
                }
                nextOffset = parseInt(nextOffset);
                if (articles.length > 0) {
                    const addList = [];
                    articles.forEach(article => {
                        addList.push(addArticle(article, wxAccount, articleTable, {"baseInfo.appMsgId": article.data.baseInfo.appMsgId, "detailInfo.itemIndex": article.data.detailInfo.itemIndex}))
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
        } catch (error) {
            // use articles api
            console.log(wxAccount.name)
            const articles = await sapi.articles(wxAccount, command);
            if (command == 'test') {
                return;
            }
    
            if (articles.length > 0) {
                const addList = [];
                articles.forEach(article => {
                    addList.push(addArticle(article, wxAccount, articleTable, {"detailInfo.contentUrl": article.data.detailInfo.contentUrl}))
                });
                await Promise.all(addList);
            }
        }
    } else if (config.spider.default == 'tianapi') {
        // use articles api
        console.log(wxAccount.name)
        const [hasNext, articles] = await sapi.articles({wxAccount}, command);
        if (command == 'test') {
            return;
        }

        if (articles.length > 0) {
            const addList = [];
            articles.forEach(article => {
                addList.push(addArticle(article, wxAccount, articleTable, {"detailInfo.contentUrl": article.data.detailInfo.contentUrl}))
            });
            await Promise.all(addList);
        }
    }
    await accountTable.updateOne({
        userName: wxAccount.userName,
    }, {
        $set: { lastTime : curTime }
    });
}

async function addArticle(article, wxAccount, articleTable, existsWhere = null) {
    let articleTitle = `${article.title} - ${wxAccount.name}`;
    if (article.author != '') {
        articleTitle += ' - ' + article.author;
    }
    if (existsWhere) {
        const articleExist = await articleTable.find(existsWhere).count();

        if (articleExist > 0) {
            return;
        }
    }
    const addData = {
        subject: articleTitle,
        subtitle: wxAccount.subtitle,
        source: 'EEFOCUS',
        channel: wxAccount.channel,
        author: wxAccount.eefAuthorId,
        user: config.eefUserId,
        category: 2,
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
    let content = article.content.replace(new RegExp('^(?:\s|<(?:p|div)>(?:&nbsp;|\s)*</(?:p|div)>)*(<p class="pagebreak page-title">[^>]*</p>\s)?(?:\s|<(?:p|div)>(?:&nbsp;|\s)*</(?:p|div)>)*', 'gi'), '$1')
        // .replace(new RegExp('([\u4e00-\u9fa5])([a-zA-Z0-9\._\\-\/\\\\]+)', 'gi'), '$1 $2')
        // .replace(new RegExp('([a-zA-Z0-9\._\\-\/\\\\]+)([\u4e00-\u9fa5])', 'gi'), '$1 $2')
        .replace(/data-src="(.*?)"/g, function(match, url) {
            return 'src="' + config.imgUrl + 'url=' + encodeURIComponent(url) + '&s=' + md5(url + 'F5WDkx1NpyvNolBD').toString().substr(2, 6) + '"';
        });
    content = sanitizeHtml(content, {
        allowedTags: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'ul', 'ol',
        'nl', 'b', 'i', 'em', 'strike', 'code', 'hr', 'br', 'div', 'img',
        'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td', 'pre'],
        allowedAttributes: {
            img: ['src']
        },
    });
    const $ = cheerio.load(content, {
        decodeEntities: false
    })
    $('img').each(function(i, elem) {
        // const imgWidth = $(this).data('w')
        // if (imgWidth) {
        //     if (imgWidth > 400) {
        //         $(this).css('width', '400px');
        //     }
        //     $(this).removeAttr('data-w');
        // }
        if ($(this).parents('p').length == 0) {
            $(this).wrap('<p style="text-align: center;"></p>');
        } else if ($(this).parent('p').length == 1) {
            if ($(this).parent('p').children().length == 1) {
                $(this).parent('p').css('text-align', 'center');
            } else if ($(this).parent('p').children().length <= 3 && $(this).parent('p').children('br').length == $(this).parent('p').children().length - 1) {
                $(this).parent('p').css('text-align', 'center');
            }
        }
    });
    addData.content = $('body').html();
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
    await articleTable.insertOne({ ...article.data, articleId: result.insertId, wxAccountId: wxAccount._id});
}

module.exports = {
    taskBegin,
    fetchAll
}