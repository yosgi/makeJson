'use strict';

const rds = require('ali-rds');
const config = require('./config');
const amqp = require('amqplib');
const moment = require('moment')

const accountDb = rds(config.db.eefocus_account);
const centerDb = rds(config.db.eefocus_center);

function log(message)
{
    console.log(moment().format('YYYY-MM-DD HH:mm:ss'))
    console.log(message)
}

async function updateUser(uid)
{
    const user = await accountDb.get('eef_core_user_account', {id:uid})
    const profile = await accountDb.get('eef_user_profile', {uid})
    const work = await accountDb.get('eef_user_custom_work', {uid})
    const education = await accountDb.get('eef_user_custom_education', {uid})
    if (user && profile) {
        const data = {
            mobile_phone: user.mobile_phone,
            birthday: user.birthdate,
            email: profile.contact_email,
            country: profile.country,
            province: profile.province,
            city: profile.city,
            telephone: profile.telephone,
        }
        if (work) {
            data.company = work.company
            data.department = work.department
            data.position = work.position
            data.position_title = work.title
            data.industry = work.industry
            data.sphere = work.sector
            data.work_description = work.description
        }
        if (education) {
            data.major = education.major
            data.degree = education.degree
            data.school = education.school
            data.edu_description = education.description
        }
        await centerDb.update('eef_platform_auto_business_edm', data, {
            where: {uid: uid}
        })
    }
}

(async () => {
    try {
        const conn = await amqp.connect(config.amqp.url)

        const channel = await conn.createChannel();
        await channel.assertQueue(config.amqp.queue, { durable: true });
        await channel.prefetch(1);
        await channel.consume(config.amqp.queue, async function(msg) {
            try {
                const { op, data } = JSON.parse(msg.content.toString())

                if (op == 'update-user') {
                    await updateUser(data)
                } else {
                    log('get error msg: ' + msg.content.toString())
                }
                await channel.ack(msg);
            } catch (error) {
                log(error)
                console.log(msg.content.toString())
                await channel.ack(msg);
            }
        }, { noAck: false });
    } catch (error) {
        log(error);
        process.exit()
    }
})();