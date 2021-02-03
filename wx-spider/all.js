'use strict';

const spider = require('./spider');
const image = require('./image');
const log = require('./log');
const moment = require('moment');

const accountList = [
    {name: 'EPIC开元通信', biz: 'Mzg5MzA3NTc1MA==', userName: 'EPICMEMS', eefAuthorId: 291, channel: 1, subtitle:'', tags:['公众号']},
    {name: 'Gopro光莆生活', biz: 'MzUzMzkxODA3Nw==', userName: 'GoproFM520', eefAuthorId: 292, channel: 1, subtitle:'', tags:['公众号']},
];

(async () => {
    try {
        const lastTime = parseInt(moment().subtract(1, 'years').startOf('day').format('x') / 1000);
        for (let i = 0; i < accountList.length; i++) {
            await spider.fetchAll([accountList[i]], lastTime);
            await image.download();
        }
        process.exit()
    } catch (error) {
        log.error('exception: ' + JSON.stringify(error));
        console.error(error);
        process.exit()
    }
})();
