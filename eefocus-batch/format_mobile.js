const phoneUtil = require('google-libphonenumber').PhoneNumberUtil.getInstance();
const PNF = require('google-libphonenumber').PhoneNumberFormat;

const rds = require('ali-rds');
const config = require('./config');
const argv = process.argv

const accountDb = rds(config.db.eefocus_account);

let limit = 100;
let lastUid = parseInt(argv[2]);

function sleep(time = 0) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve();
        }, time);
    })
};

(async () => {
    while(1) {
        const users = await accountDb.query('SELECT id,mobile_phone,country_code FROM eef_core_user_account WHERE id > ? ORDER BY id ASC LIMIT ?', [ lastUid, limit]);
        if (!users || users.length == 0) {
            break;
        }

        const rows = []
        users.forEach(user => {
            if (user.mobile_phone && user.mobile_phone != '' && !/^1[0-9]{10}$/.test(user.mobile_phone)) {
                try {
                    const number = phoneUtil.parse(user.mobile_phone, 'CN');
                    const country_code = number.getCountryCode();
                    let mobile_phone = user.mobile_phone;
                    if (country_code != 86) {
                        mobile_phone = phoneUtil.format(number, PNF.E164);
                    }
                    if (mobile_phone != user.mobile_phone || country_code != user.country_code) {
                        rows.push({
                            id: user.id,
                            mobile_phone: mobile_phone,
                            country_code: country_code,
                        })
                    }
                }  catch (error) {
                }
            }
            lastUid = user.id;
        });
        if (rows.length > 0) {
            await accountDb.updateRows('eef_core_user_account', rows);
        }
        console.log(lastUid)
        await sleep(1000)
    }
    process.exit()
})();
