'use strict';

const axios = require('axios');
const config = require('./config');
const log = require('./log');
const moment = require('moment');

let mdb = false;

const urls = {
    articles: 'http://api.tianapi.com/txapi/wxinfo/index',
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function setMongo(mongodb) {
    mdb = mongodb;
}


async function checkActive() {
    const response = await axios.get(urls.articles, {
        params: {'key': config.spider.tianapi.key, 'biz': 'MzI4MDI4MDE5Ng=='}
    });
    return response.data.code === 200;
}

async function articles(options, command, retry) {
    let {wxAccount, page} = options;
    if (!page) {
        page = 0;
    }
    if (typeof retry == 'undefined') {
        retry = 5
    }
    let hasNext = true;
    const params = {'key': config.spider.tianapi.key, 'biz': wxAccount.biz, 'word': wxAccount.name}
    if (page > 0) {
        params.page = page
    }
    const response = await axios.get(urls.articles, {
        params
    });
    if (response.data.code === 200) {
        if (command == 'test') {
            return [false, []];
        }
        const result = response.data.newslist;
        let articles = []
        let maxTime = 0
        if (result) {
            maxTime = parseInt(moment(result[0].ctime).format('x') / 1000);
            for (let idx = 0; idx < result.length; idx++) {
                const detailInfo = result[idx];
                const detailTime = parseInt(moment(detailInfo.ctime).format('x') / 1000);
                if (detailTime <= wxAccount.lastTime) {
                    hasNext = false
                    break;
                }
                const detailData = await fetchDetail(wxAccount, {
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
        }
        if (!result || result.length == 0) {
            hasNext = false
        }
        return [hasNext, articles, maxTime];
    } else {
        if (retry == 3) {// code 250 时重试两次
            if (page > 0 && response.data.code === 250) {
                return [false, []];
            }
            if (response.data.code === 250) {
                const apiActive = await checkActive();
                if (apiActive) {
                    return [false, []];
                }
                retry = 0;
            }
        }
        if (retry >= 1) {
            retry--;
            console.log(`retry ${retry}... ${wxAccount.name} (${wxAccount.biz}) ${JSON.stringify(response.data)}`)
            if (response.data.code === 130) {
                await sleep(60000)
            } else {
                await sleep(30000 * (5 - retry));
            }
            return articles(options, command, retry);
        } else {
            throw `articles 获取失败: ${wxAccount.name} ${JSON.stringify(response.data)}`;
        }
    }
}

async function fetchDetail(wxAccount, detailInfo, baseInfo, msgBaseInfo) {
    console.log(`get details...`, detailInfo)
    if (!detailInfo.contentUrl) {
        console.log(`detailInfo.contentUrl is empty (⛔️️) !\n`)
        return false;
    }
    const detailRes = await axios.get(detailInfo.contentUrl, {
        // proxy: {
        //     host: '122.241.218.226',
        //     port: 8888,
        // },
    });
    const html = detailRes.data;
    if (detailRes.status !== 200) {
        console.log('获取详情失败(⛔️️): ' + detailInfo.title);
    }
    if (html.indexOf('访问过于频繁，请用微信扫描二维码进行访问') !== -1) {
        console.log('微信访问过于频繁(⛔️️): '+ detailInfo.contentUrl);
    }
    const match = /<div class="rich_media_content[^\"]*"\s+id="js_content" style="visibility: hidden;">[\s]+([\s\S]+?)[\s]+<\/div>[\s]+<script[^>]*nonce/.exec(html);
    if (!match) {
        if (html.indexOf('class="price js_pay_fee"') === -1 || html.indexOf('js_share_content') === -1) {
            // 付费阅读 分享文章
            console.log('获取详情匹配有误(⛔️️): ' + detailInfo.title);
        }
        console.log('详情匹配失败(⛔️️): ' + detailInfo.title);
        return false;
    }

    const matchAuthor = /id="js_name">([\s\S]+?)<\/a>/.exec(html)
    if (matchAuthor) {
        detailInfo.author = matchAuthor[1].trim()
    }

    // 原创
    if (!wxAccount.checkOriginal || /<span id="copyright_logo" class=".*?">(Original|原创)<\/span>/.test(html)) {
        console.log(`=====（🉑️️️➕️） 原创文章抓取成功：`, detailInfo.title)
        return {
            data: { baseInfo, detailInfo, dateTime: msgBaseInfo.dateTime },
            title: detailInfo.title,
            author: detailInfo.author,
            coverImgUrl: detailInfo.coverImgUrl,
            content: match[1],
        };
    }
    else {
        console.error(`文章非原创（⛔️️🙅🏻）：`, detailInfo.title)
    }
    return false;
}

module.exports = {
    articles,
    setMongo,
}