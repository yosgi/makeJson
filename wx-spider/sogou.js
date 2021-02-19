'use strict';

const axios = require('axios');
const config = require('./config');
const log = require('./log');
const moment = require('moment');

let mdb = false;
let urlTable;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function setMongo(mongodb) {
    mdb = mongodb;
    urlTable = await mdb.collection('newlist');
}

async function articles(options, command) {
    let {wxAccount, page} = options;
    if (!page) {
        page = 0;
    }
    const urls = await urlTable.find({
        account_id: wxAccount._id,
        timestamp: {$gt : wxAccount.lastTime}
    }).sort({_id: -1}).toArray();

    if (command == 'test') {
        return [false, []];
    }
    let articles = []
    if (urls && urls.length > 0) {
        for (let idx = 0; idx < urls.length; idx++) {
            const detailInfo = urls[idx];
            const detailTime = detailInfo.timestamp;
            const detailData = await fetchDetail({
                contentUrl: detailInfo.wxurl,
                title: '',
                coverImgUrl: '',
                author: '',
            }, {}, {dateTime: detailTime});
            if (detailData) {
                articles.push(detailData);
            }
            await sleep(Math.floor(Math.random() * (config.sleepMss[1] - config.sleepMss[0] + 1) + config.sleepMss[0]));
        }
    }
    return [false, articles];
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

    const match = /<h2 class="rich_media_title" id="activity-name">[\s]*([\s\S]+?)[\s]*<\/h2>[\s\S]+<div class="rich_media_content " id="js_content" style="visibility: hidden;">[\s]+([\s\S]+?)[\s]+<\/div>[\s]+<script nonce/.exec(html);
    if (!match) {
        if (html.indexOf('class="price js_pay_fee"') === -1 || html.indexOf('js_share_content') === -1) {
            // 付费阅读 分享文章
            log.error('获取详情匹配有误' + JSON.stringify(detailInfo));
        }
        return false;
    }
    detailInfo.title = match[1]
    let matchCover = null
    const patt = /<img [^>]*data-src="([^>]*?)"[^>]*>/g
    while ((matchCover = patt.exec(html)) != null) {
        if (matchCover[0].indexOf('__bg_gif') === -1) {
            const width = /data-w="(\d+)"/.exec(matchCover[0])
            if (width && width[1] > 260) {
                detailInfo.coverImgUrl = matchCover[1].trim()
                break
            }
        }
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
            content: match[2],
        };
    }
    return false;
}

module.exports = {
    articles,
    setMongo,
}