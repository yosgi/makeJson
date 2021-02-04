'use strict';

const rds = require('ali-rds');
const config = require('./config');
const amqp = require('amqplib');
const argv = process.argv

const centerDb = rds(config.db.eefocus_center);

(async () => {
    try {
        let lastId = argv[2];

        if (!lastId) {
            console.log('command: node updateCenterUser.js {min uid}')
            return
        }
        const maxUidRow = await centerDb.query(`select max(uid) as uid from eef_platform_auto_business_edm`)
        const conn = await amqp.connect(config.amqp.url)

        const channel = await conn.createChannel();
        await channel.assertQueue(config.amqp.queue, { durable: true });
        for (let uid = lastId; uid <= maxUidRow[0].uid; uid++) {

            if (channel.sendToQueue(config.amqp.queue, Buffer.from(JSON.stringify({
                op: 'update-user',
                data: uid
            })))) {
                console.log('send data: ' + uid)
            }
        }
        channel.close();
        process.exit()
    } catch (error) {
        console.log(error);
        process.exit()
    }
})();