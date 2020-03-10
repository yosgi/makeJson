'use strict';

const rds = require('ali-rds');
const config = require('./config');

const accountDb = rds(config.db.eefocus_account);
const sendyDb = rds(config.db.sendy);

(async () => {
    try {
        const curTime = parseInt(new Date().getTime() / 1000);
        const batchRow = await accountDb.get('eef_user_batch', { type: 0 });
        const lastUid = batchRow.last_uid;
        const limit = 100;
        let offset = 0;
        const listRow = await sendyDb.get('lists', { id : config.sendy_new.list });
        if (!listRow) {
            throw 'sendy - list not found - list id ' + config.sendy_new.list;
        }
        let allLists = '';
        const listRows = await sendyDb.select('lists', {
            where: { app: config.sendy_new.app },
            columns: ['id']
        });
        if (listRows.length == 0) {
            throw 'sendy - lists not found - app id ' + config.sendy_new.app;
        }
        listRows.forEach(listr => {
            allLists += listr.id + ',';
        });
        allLists = allLists.substr(0, allLists.length - 1);
        const unsubscribeAllList = listRow.unsubscribe_all_list;
        while(1) {
            const users = await accountDb.query('SELECT id,email,name FROM eef_core_user_account WHERE id > ? ORDER BY id DESC LIMIT ? OFFSET ?', [ lastUid, limit, offset ]);
            if (!users || users.length == 0) {
                break;
            }
            offset += limit;
            const emails = []
            users.forEach(user => {
                if (user.email && user.email != '') {
                    emails.push(user.email)
                }
            });
            const subscribers = await sendyDb.select('subscribers', {
                where: {
                    email: emails,
                    userID: 1,
                    list: config.sendy_new.list,
                },
                columns: ['email'],
            });
            subscribers.forEach(subscriber => {
                const idx = emails.indexOf(subscriber.email);
                if (idx !== -1) {
                    emails.splice(idx, 1);
                }
            });
            const addRows = [];
            for (let i = 0; i < users.length; i++) {
                const user = users[i];
                if (emails.indexOf(user.email) !== -1) {
                    let emailExists;
                    if (unsubscribeAllList === 1) {
                        emailExists = await sendyDb.query('SELECT email from subscribers WHERE ( email = ? AND bounced = 1 ) OR ( email = ? AND list IN ('
                            + allLists
                            + ') AND (complaint = 1 OR unsubscribed = 1) )', [user.email, user.email]);
                    } else {
                        emailExists = await sendyDb.query('SELECT email from subscribers WHERE ( email = ? AND bounced = 1 ) OR ( email = ? AND list IN ('
                            + allLists
                            + ') AND complaint = 1 )', [user.email, user.email]);
                    }
                    if (emailExists.length == 0) {
                        addRows.push({
                            userID: 1,
                            name: user.name,
                            email: user.email,
                            list: config.sendy_new.list,
                            timestamp: curTime,
                        })
                    }
                }
            }
            if (addRows.length > 0) {
                await sendyDb.insert('subscribers', addRows);
            }
            batchRow.last_uid = users[0].id;
            batchRow.last_time = curTime;
            await accountDb.update('eef_user_batch', batchRow);
        }
        process.exit()
    } catch (error) {
        console.error(error);
        process.exit()
    }
})();