'use strict';

const spider = require('./spider');
const image = require('./image');
const log = require('./log');

const accountList = [
    {name: '智车行家', 'biz': 'MzU3NDY4Mjk4OQ==', userName: 'gh_4090d6fa3eb3', eefAuthorId: 152, channel: 1, subtitle:'', tags:['公众号']},
];

(async () => {
    try {
        await spider.fetchAll(accountList);
        await image.download();
        process.exit()
    } catch (error) {
        log.error('exception: ' + JSON.stringify(error));
        console.error(error);
        process.exit()
    }
})();
