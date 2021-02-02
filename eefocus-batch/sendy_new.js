'use strict';

const rds = require('ali-rds');
const config = require('./config');

const accountDb = rds(config.db.eefocus_account);
const mainDb = rds(config.db.eefocus_main);
const sendyDb = rds(config.db.sendy);

(async () => {
    try {
        const curTime = parseInt(new Date().getTime() / 1000);
        const batchRow = await mainDb.get('eef_user_batch', { type: 0 });
        let lastId = batchRow.last_id;
        const limit = 100;
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
            const profiles = await mainDb.query('SELECT id,uid,data FROM eef_survey_data WHERE id > ? and project = ? ORDER BY id ASC LIMIT ?', [ lastId, config.sendy_new.profile_form_id, limit ]);
            if (!profiles || profiles.length == 0) {
                break;
            }
            const emails = []
            const uids = []
            profiles.forEach(profile => {
                const json = JSON.parse(profile.data)
                if (json && json.contact_email) {
                    profile.email = json.contact_email;
                    emails.push(profile.email)
                    uids.push(profile.uid)
                }
            });

            if (uids.length > 0) {
                const users = await accountDb.query(`select id,name from eef_core_user_account where id in (${uids.join(',')})`)
                const userMap = new Map(users.map(r=>[r.id,r]));
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
                for (let i = 0; i < profiles.length; i++) {
                    const profile = profiles[i];
                    if (emails.indexOf(profile.email) !== -1) {
                        let emailExists;
                        if (unsubscribeAllList === 1) {
                            emailExists = await sendyDb.query('SELECT email from subscribers WHERE ( email = ? AND bounced = 1 ) OR ( email = ? AND list IN ('
                                + allLists
                                + ') AND (complaint = 1 OR unsubscribed = 1) )', [profile.email, profile.email]);
                        } else {
                            emailExists = await sendyDb.query('SELECT email from subscribers WHERE ( email = ? AND bounced = 1 ) OR ( email = ? AND list IN ('
                                + allLists
                                + ') AND complaint = 1 )', [profile.email, profile.email]);
                        }
                        if (emailExists.length == 0 && userMap.has(profile.uid)) {
                            addRows.push({
                                userID: 1,
                                name: userMap.get(profile.uid).name,
                                email: profile.email,
                                list: config.sendy_new.list,
                                timestamp: curTime,
                            })
                        }
                    }
                }
                if (addRows.length > 0) {
                    await sendyDb.insert('subscribers', addRows);
                }
            }
            batchRow.last_id = profiles[profiles.length - 1].id
            batchRow.last_time = curTime;
            await mainDb.update('eef_user_batch', batchRow);
            lastId = batchRow.last_id
        }
        process.exit()
    } catch (error) {
        console.error(error);
        process.exit()
    }
})();