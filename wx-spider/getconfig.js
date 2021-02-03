'use strict';

const config = require('./config');
const sapi = require('./tuotu');
const MongoClient = require('mongodb').MongoClient;

const argv = process.argv
const command = argv[2];

const accountList = [
    ['嵌入式Linux系统开发','嵌入式Linux系统开发'],
    ['MATLAB的科学与工程应用','MATLAB的科学与工程应用'],
    ['射频学堂','射频学堂'],
    ['码农Xianyi','王军辉'],
];

const authorMap = new Map([
    ['嵌入式Linux系统开发','371'],
    ['MATLAB的科学与工程应用','372'],
    ['射频学堂','373'],
    ['码农Xianyi','361'],
]);

(async () => {
    try {
        const client = await MongoClient.connect(config.mongo.url, {useUnifiedTopology: true});
        const mdb = await client.db('wxspider');
        await sapi.setMongo(mdb);
        if (command == 'check') {
            await check()
        } else {
            await build()
        }
        process.exit()
    } catch (error) {
        console.error(error);
        process.exit()
    }
})();

async function check()
{
    for (let i = 0; i < accountList.length; i++) {
        if (!authorMap.has(accountList[i][1])) {
            console.log(`${accountList[i][0]}, ${accountList[i][1]} - no author`);
        }
    }
}

async function build()
{
    const prev = 0;
    for (let i = 0; i < accountList.length; i++) {
        if (i < prev) {
            continue;
        }
        const info = await sapi.wxInfo(accountList[i][0], 2);
        if (!info.Biz || !info.UserName.String) {
            console.log(`${accountList[i][0]} - ${JSON.stringify(info)} - no biz or username`);
            continue;
        }
        if (!authorMap.has(accountList[i][1])) {
            throw `${accountList[i][0]} - no author`;
        }
        const authorId = authorMap.get(accountList[i][1]);
        console.log(`${i} => {name: '${accountList[i][0]}', biz: '${info.Biz}', userName: '${info.UserName.String}', eefAuthorId: ${authorId}, channel: 1, subtitle:'', tags:['公众号']}`);
    }
}

