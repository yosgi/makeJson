'use strict';

const spider = require('./spider');
const log = require('./log');
const argv = process.argv
const command = argv[2];

(async () => {
    try {
        await spider.taskBegin(command);
        process.exit()
    } catch (error) {
        log.error('exception: ' + JSON.stringify(error));
        console.error(error);
        process.exit()
    }
})();
