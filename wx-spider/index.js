'use strict';

const spider = require('./spider');
const image = require('./image');
const log = require('./log');

(async () => {
    try {
        await spider.taskBegin();
        await image.download();
        process.exit()
    } catch (error) {
        log.error('exception: ' + JSON.stringify(error));
        console.error(error);
        process.exit()
    }
})();
