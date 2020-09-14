'use strict'

const config = require('./config');
const moment = require('moment');
const fs = require('fs');
const axios = require('axios');
const rds = require('ali-rds');
const MongoClient = require('mongodb').MongoClient;
const sharp = require('sharp');
const log = require('./log');

const db = rds(config.db);
const day = moment().format('YYYY/MM/DD');
const basePath = config.featureImg.dist + day;
if (!fs.existsSync(basePath)) {
    fs.mkdirSync(basePath, {recursive: true});
}
const basePathDb = config.featureImg.forDb + day;

async function download() {
    console.log('fetch image begin')
    const client = await MongoClient.connect(config.mongo.url, {useUnifiedTopology: true});
    const mdb = await client.db('wxspider');
    const articleTable = await mdb.collection('article');
    const limit = 10;

    while(1) {
        const articles = await articleTable.find({featureImg: { $exists: false }}).project({articleId: 1, detailInfo: 1}).limit(limit).toArray()
        if (articles.length == 0) {
            break;
        }
        for (let idx = 0; idx < articles.length; idx++) {
            await setFeatureImg(articles[idx], articleTable, idx);
            await sleep(Math.floor(Math.random() * (config.sleepMss[1] - config.sleepMss[0] + 1) + config.sleepMss[0]));
        }
        console.log(`done - ${limit}`)
    }

    console.log('fetch image finish')
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function setFeatureImg(article, articleTable, idx) {
    await sleep(10 * idx)
    const url = article.detailInfo.coverImgUrl;
    const match = /mmbiz\.qpic\.cn\/(?:[a-z_]*?)mmbiz_([a-z]+)\//.exec(url);
    if (!match) {
        log.error('匹配失败：' + url);
        return;
    }
    while(1) {
        const fileName = `${(new Date().getTime()).toString(16)}`;
        const filePath = `${basePath}/${fileName}.${match[1]}`;
        if (!fs.existsSync(filePath)) {
            const writer = fs.createWriteStream(filePath, {flags: 'wx'})

            const response = await axios({
                url,
                method: 'GET',
                responseType: 'stream'
            })

            response.data.pipe(writer)

            return new Promise((resolve, reject) => {
                writer.on('finish', async() => {
                    const thumbPath = `${basePath}/${fileName}-thumb.${match[1]}`;
                    await sharp(filePath)
                        .resize(260, 195)
                        .toFile(thumbPath);
                    await db.update('eef_article_draft', { image: `${basePathDb}/${fileName}.${match[1]}`}, {
                        where: { id: article.articleId },
                    });
                    await articleTable.updateOne({ articleId : article.articleId }, { $set: { featureImg : 1 } });

                    resolve();
                })
                writer.on('error', reject)
            })
        } else {
            await sleep(1)
        }
    }
}

module.exports = {
    download
}