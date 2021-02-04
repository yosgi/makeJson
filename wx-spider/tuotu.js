'use strict';

const axios = require('axios');
const config = require('./config');
const log = require('./log');

let mdb = false;
let configTable;

const urls = {
    history: 'https://api.xdata.tuotoo.com/v1/open/mp/history',
    articles: 'https://api.xdata.tuotoo.com/v1/open/mp/articles',
    info: 'https://api.xdata.tuotoo.com/v1/open/mp/info',
    login: 'https://api.xdata.tuotoo.com/v1/open/token',
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function setMongo(mongodb) {
    mdb = mongodb;
    configTable = await mdb.collection('config');
}

async function getToken() {
    let mconfig = await configTable.find({}).toArray();

    let token = '';
    if (mconfig.length === 0) {
        await configTable.insertOne({});
    } else {
        const nowStamp = new Date().getTime() / 1000;
        if (mconfig[0].token && mconfig[0].token.ExpireTime > nowStamp) {
            token = mconfig[0].token.AccessToken;
        }
    }
    if (token === '') {
        const response = await axios.get(urls.login, {
            params: config.spider.tuotu
        });
        if (response.data.code === 0) {
            token = response.data.data.AccessToken;
            await configTable.updateOne({}, {$set: { token : response.data.data }});
        } else {
            throw 'token获取失败: ' + JSON.stringify(response.data);
        }
    }
    return token;
}

async function history(wxAccount, offset, start, command, retry) {
    if (typeof retry == 'undefined') {
        retry = 3
    }
    const token = await getToken();
    const response = await axios.get(urls.history, {
        headers: {'Authorization': token},
        params: {'name': wxAccount.userName, 'offset': offset, 'start': start}
    });
    if (response.data.code === 0) {
        if (command == 'test') {
            console.log(JSON.stringify(response.data.data))
            return {
                articles: [],
                nextOffset: 0,
            };
        }
        const result = response.data.data;
        let articles = []
        let nextOffset = result.msgList.pagingInfo.offset;
        if (result.msgList.msg) {
            for (let idx = 0; idx < result.msgList.msg.length; idx++) {
                const msg = result.msgList.msg[idx];
                if (msg.appMsg && msg.appMsg.detailInfo) {
                    if (msg.baseInfo.dateTime < wxAccount.lastTime) {
                        nextOffset = 0;
                        break;
                    }
                    for (let idxx = 0; idxx < msg.appMsg.detailInfo.length; idxx++) {
                        const detailData = await fetchDetail(msg.appMsg.detailInfo[idxx], msg.appMsg.baseInfo, msg.baseInfo);
                        if (detailData) {
                            articles.push(detailData);
                        }
                        await sleep(Math.floor(Math.random() * (config.sleepMss[1] - config.sleepMss[0] + 1) + config.sleepMss[0]));
                    }
                }
            }
        }
        return {
            articles,
            nextOffset,
        }
    } else {
        // if (retry >= 1 && response.data.code === 104) {
        if (retry >= 1) {
            retry--;
            await sleep(3000 * (3 - retry));
            console.log(`retry ${retry}... ${wxAccount.name} ${JSON.stringify(response.data)}`)
            return history(wxAccount, offset, start, command, retry);
        } else {
            throw `history 获取失败: ${wxAccount.name} ${JSON.stringify(response.data)}`;
        }
    }
}

async function articles(wxAccount, command, retry) {
    if (typeof retry == 'undefined') {
        retry = 3
    }
    const token = await getToken();
    const response = await axios.get(urls.articles, {
        headers: {'Authorization': token},
        params: {'name': wxAccount.name, 'fetchDepth': 10}
    });
    if (response.data.code === 0) {
        if (command == 'test') {
            return [];
        }
        const result = response.data.data;
        let articles = []
        for (let idx = 0; idx < result.length; idx++) {
            const detailInfo = result[idx];
            if (detailInfo.Datetime <= wxAccount.lastTime) {
                break;
            }
            const detailData = await fetchDetail({
                itemShowType: 0,
                contentUrl: detailInfo.URL,
                title: detailInfo.Title,
                author: detailInfo.Author,
                coverImgUrl: detailInfo.Cover,
            }, {}, {dateTime: detailInfo.Datetime});
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
            return articles(wxAccount, command, retry);
        } else {
            throw `articles 获取失败: ${wxAccount.name} ${JSON.stringify(response.data)}`;
        }
    }
}

async function fetchDetail(detailInfo, baseInfo, msgBaseInfo) {
    if (detailInfo.itemShowType !== 0) {
        return false;
    }
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

async function wxInfo(wxAccountName, retry) {
    const token = await getToken();
    const response = await axios.get(urls.info, {
        headers: {'Authorization': token},
        params: {'name': wxAccountName}
    });
    if (response.data.code === 0) {
        if (retry > 0 && !response.data.Biz) {
            await sleep(3000 * (3 - retry));
            return await wxInfo(wxAccountName, --retry)
        }
        return response.data.data;
    } else {
        throw `wxinfo 获取失败: ${wxAccountName} ${JSON.stringify(response.data)}`;
    }
}

module.exports = {
    history,
    articles,
    setMongo,
    wxInfo
}