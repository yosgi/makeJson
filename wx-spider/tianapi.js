'use strict';

const axios = require('axios');
const config = require('./config');
const log = require('./log');
const moment = require('moment');

let mdb = false;
let configTable;

const urls = {
    articles: 'http://api.tianapi.com/txapi/wxinfo/index',
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function setMongo(mongodb) {
    mdb = mongodb;
    configTable = await mdb.collection('config');
}

async function articles(wxAccount, lastTime, command, retry) {
    if (typeof retry == 'undefined') {
        retry = 3
    }
    const response = await axios.get(urls.articles, {
        params: {'key': config.spider.tianapi.key, 'biz': wxAccount.biz, 'word': wxAccount.name}
    });
    if (response.data.code === 200) {
        if (command == 'test') {
            return [];
        }
        const result = response.data.newslist;
        let articles = []
        for (let idx = 0; idx < result.length; idx++) {
            const detailInfo = result[idx];
            const detailTime = parseInt(moment(detailInfo.ctime).format('x') / 1000);
            if (detailTime <= lastTime) {
                break;
            }
            const detailData = await fetchDetail({
                contentUrl: detailInfo.url,
                title: detailInfo.title,
                coverImgUrl: detailInfo.picUrl,
                author: '',
            }, {}, {dateTime: detailTime});
            if (detailData) {
                articles.push(detailData);
            }
            await sleep(Math.floor(Math.random() * (config.sleepMss[1] - config.sleepMss[0] + 1) + config.sleepMss[0]));
        }
        return articles;
    } else {
        if (retry >= 1) {
            retry--;
            await sleep(3000 * (3 - retry));
            return articles(wxAccount, lastTime, command, retry);
        } else {
            throw `articles 获取失败: ${wxAccount.name} ${JSON.stringify(response.data)}`;
        }
    }
}

async function fetchDetail(detailInfo, baseInfo, msgBaseInfo) {
    console.log(`get details...`)
    const detailRes = await axios.get(detailInfo.contentUrl, {
        // proxy: {
        //     host: '122.241.218.226',
        //     port: 8888,
        // },
    });
    const html = detailRes.data;
    if (detailRes.status !== 200) {
        throw '获取详情失败' + JSON.stringify(detailInfo);
    }
    if (html.indexOf('访问过于频繁，请用微信扫描二维码进行访问') !== -1) {
        throw '微信访问过于频繁';
    }
    const match = /<div class="rich_media_content " id="js_content" style="visibility: hidden;">[\s]+([\s\S]+?)[\s]+<\/div>[\s]+<script nonce/.exec(html);
    if (!match) {
        if (html.indexOf('class="price js_pay_fee"') === -1 || html.indexOf('js_share_content') === -1) {
            // 付费阅读 分享文章
            log.error('获取详情匹配有误' + JSON.stringify(detailInfo));
        }
        return false;
    }

    const matchAuthor = /id="js_name">([\s\S]+?)<\/a>/.exec(html)
    if (matchAuthor) {
        detailInfo.author = matchAuthor[1].trim()
    }

    // 原创
    if (html.indexOf('<span id="copyright_logo" class="rich_media_meta icon_appmsg_tag appmsg_title_tag">原创</span>') !== -1) {
        return {
            data: { baseInfo, detailInfo, dateTime: msgBaseInfo.dateTime },
            title: detailInfo.title,
            author: detailInfo.author,
            coverImgUrl: detailInfo.coverImgUrl,
            content: match[1],
        };
    }
    return false;
}

module.exports = {
    articles,
    setMongo,
}