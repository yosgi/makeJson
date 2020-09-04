'use strict';

const rds = require('ali-rds');
const config = require('./config');
const accountDb = rds(config.db.eefocus_account);
const moore8Db = rds(config.db.moore8);
const cirmallDb = rds(config.db.cirmall);
const analyticsDb = rds(config.db.analytics);
const argv = process.argv
const command = argv[2];

const limit = 100;

const moment = require('moment')

async function getOptions() {
    const options = await analyticsDb.select('options');
    const opMap = new Map();
    options.forEach(option => {
        opMap.set(option.key, option.value)
    });
    return opMap;
}

async function setOption(key, value) {
    await analyticsDb.update('options', {value}, {
        where: { key },
    });
}

switch (command) {
    case 'insertOrder':
        (async () => {
            await insertOrder();
            process.exit()
        })();
        break;
    case 'updateOrder':
        (async () => {
            await updateOrder();
            process.exit()
        })();
        break;
    case 'updateUser':
        (async () => {
            await updateUser();
            process.exit()
        })();
        break;

    default:
        break;
}

async function insertOrder() {
    try {
        const mRet = await analyticsDb.query('select max(pid_int) as pid_int from orders where type=0');
        let maxid = mRet[0].pid_int;
        maxid = maxid || 0
        let nowStamp = moment().unix();
        while(1) {
            const adds = [];
            const orderItems = await moore8Db.query(`select i.id,o.user_id,o.price,o.order_type,c.title,i.fee,c.first_published_time,o.paid_at,c.is_live from order_item as i join \`order\` as o on i.order_no=o.order_no join course as c on i.course_id=c.id where i.id > ${maxid} and o.status_code=1 order by i.id asc limit ${limit}`);
            if (!orderItems || orderItems.length <= 0) {
                break;
            }
            maxid = orderItems[orderItems.length - 1].id;
            orderItems.forEach(orderItem => {
                adds.push({
                    pid_int: orderItem.id,
                    user_id: orderItem.user_id,
                    title: orderItem.title,
                    price: orderItem.order_type == 0 ? orderItem.price : 0,
                    total_fee: orderItem.fee,
                    publish_at: moment(orderItem.first_published_time * 1000).format(),
                    paid_at: moment(orderItem.paid_at * 1000).format(),
                    type: 0,//课程
                    sub_type: orderItem.is_live,
                })
            });
            await analyticsDb.insert('orders', adds);
            console.log(maxid)
        }
        const cRet = await analyticsDb.query('select max(pid_string) as pid_string from orders where type=1');
        let maxOrder = cRet[0].pid_string;
        maxOrder = maxOrder || 0
        while(1) {
            const adds = [];
            const orderItems = await cirmallDb.query(`select order_no,user_id,price,total_fee,paid_at,circuit_id from orders where order_no > ${maxOrder} and status=1 order by order_no asc limit ${limit}`);
            if (!orderItems || orderItems.length <= 0) {
                break;
            }
            maxOrder = orderItems[orderItems.length - 1].order_no;
            let circuitIds = orderItems.map(r=>r.circuit_id);
            circuitIds = [...new Set(circuitIds)]
            const circuits = await cirmallDb.query(`select c.id,c.name,IFNULL(p.published, 0) as published from circuits as c join circuits_published as p on c.id=p.circuit_id where c.id in (${circuitIds.join(',')})`);
            const circuitMap = new Map()
            circuits.forEach(circuit => {
                circuitMap.set(circuit.id, circuit);
            });
            orderItems.forEach(orderItem => {
                adds.push({
                    pid_string: orderItem.order_no,
                    user_id: orderItem.user_id,
                    title: circuitMap.has(orderItem.circuit_id) ? circuitMap.get(orderItem.circuit_id).name : '',
                    price: orderItem.price,
                    total_fee: orderItem.total_fee,
                    publish_at: circuitMap.has(orderItem.circuit_id) ? moment(circuitMap.get(orderItem.circuit_id).published * 1000).format() : '',
                    paid_at: moment(orderItem.paid_at * 1000).format(),
                    type: 1,//电路
                    sub_type: 0,
                })
            });
            await analyticsDb.insert('orders', adds);
            console.log(maxOrder)
        }
        await setOption('last_paid', nowStamp)
    } catch (error) {
        console.error(error);
    }
}

async function updateOrder() {
    try {
        const options = await getOptions();
        let lastPaid = options.get('last_paid');
        let maxid = 0;
        let nowStamp = moment().unix();
        while(1) {
            const adds = [];
            const updates = [];
            const pids = [];
            const orderItems = await moore8Db.query(`select i.id,o.user_id,o.price,o.order_type,c.title,i.fee,c.first_published_time,o.paid_at,c.is_live from order_item as i join \`order\` as o on i.order_no=o.order_no join course as c on i.course_id=c.id where o.paid_at>${lastPaid} and i.id > ${maxid} and o.status_code=1 order by i.id asc limit ${limit}`);
            if (!orderItems || orderItems.length <= 0) {
                break;
            }
            maxid = orderItems[orderItems.length - 1].id;
            orderItems.forEach(orderItem => {
                pids.push(orderItem.id);
            });
            const exists = await analyticsDb.select('orders', {
                where: {
                    type: 0,
                    pid_int: pids
                }
            });
            orderItems.forEach(orderItem => {
                let existId = false
                for (let i = 0; i < exists.length; i++) {
                    const element = exists[i];
                    if (orderItem.id == element.pid_int) {
                        existId = element.id
                        break;
                    }
                }
                if (existId) {
                    updates.push({
                        id: existId,
                        pid_int: orderItem.id,
                        user_id: orderItem.user_id,
                        title: orderItem.title,
                        price: orderItem.order_type == 0 ? orderItem.price : 0,
                        total_fee: orderItem.fee,
                        publish_at: moment(orderItem.first_published_time * 1000).format(),
                        paid_at: moment(orderItem.paid_at * 1000).format(),
                        type: 0,//课程
                        sub_type: orderItem.is_live,
                    })
                } else {
                    adds.push({
                        pid_int: orderItem.id,
                        user_id: orderItem.user_id,
                        title: orderItem.title,
                        price: orderItem.order_type == 0 ? orderItem.price : 0,
                        total_fee: orderItem.fee,
                        publish_at: moment(orderItem.first_published_time * 1000).format(),
                        paid_at: moment(orderItem.paid_at * 1000).format(),
                        type: 0,//课程
                        sub_type: orderItem.is_live,
                    })
                }
            });
            if (adds.length > 0) {
                console.log('add moore8 orders')
                await analyticsDb.insert('orders', adds);
            }
            if (updates.length > 0) {
                console.log('update moore8 orders')
                await analyticsDb.updateRows('orders', updates);
            }
        }
        let maxOrder = 0;
        while(1) {
            const adds = [];
            const updates = [];
            const pids = [];
            
            const orderItems = await cirmallDb.query(`select order_no,user_id,price,total_fee,paid_at,circuit_id from orders where order_no > ${maxOrder} and paid_at > ${lastPaid} and status=1 order by order_no asc limit ${limit}`);
            if (!orderItems || orderItems.length <= 0) {
                break;
            }
            maxOrder = orderItems[orderItems.length - 1].order_no;
            let circuitIds = orderItems.map(r=>r.circuit_id);
            circuitIds = [...new Set(circuitIds)]
            const circuits = await cirmallDb.query(`select c.id,c.name,IFNULL(p.published, 0) as published from circuits as c join circuits_published as p on c.id=p.circuit_id where c.id in (${circuitIds.join(',')})`);
            const circuitMap = new Map()
            circuits.forEach(circuit => {
                circuitMap.set(circuit.id, circuit);
            });
            orderItems.forEach(orderItem => {
                pids.push(orderItem.order_no);
            });
            const exists = await analyticsDb.select('orders', {
                where: {
                    type: 1,
                    pid_string: pids
                }
            });
            orderItems.forEach(orderItem => {
                let existId = false
                for (let i = 0; i < exists.length; i++) {
                    const element = exists[i];
                    if (orderItem.order_no == element.pid_string) {
                        existId = element.id
                        break;
                    }
                }
                if (existId) {
                    updates.push({
                        id: existId,
                        pid_string: orderItem.order_no,
                        user_id: orderItem.user_id,
                        title: circuitMap.has(orderItem.circuit_id) ? circuitMap.get(orderItem.circuit_id).name : '',
                        price: orderItem.price,
                        total_fee: orderItem.total_fee,
                        publish_at: circuitMap.has(orderItem.circuit_id) ? moment(circuitMap.get(orderItem.circuit_id).published * 1000).format() : '',
                        paid_at: moment(orderItem.paid_at * 1000).format(),
                        type: 1,//电路
                        sub_type: 0,
                    })
                } else {
                    adds.push({
                        pid_string: orderItem.order_no,
                        user_id: orderItem.user_id,
                        title: circuitMap.has(orderItem.circuit_id) ? circuitMap.get(orderItem.circuit_id).name : '',
                        price: orderItem.price,
                        total_fee: orderItem.total_fee,
                        publish_at: circuitMap.has(orderItem.circuit_id) ? moment(circuitMap.get(orderItem.circuit_id).published * 1000).format() : '',
                        paid_at: moment(orderItem.paid_at * 1000).format(),
                        type: 1,//电路
                        sub_type: 0,
                    })
                }
            });
            if (adds.length > 0) {
                console.log('add cirmall orders')
                await analyticsDb.insert('orders', adds);
            }
            if (updates.length > 0) {
                console.log('update cirmall orders')
                await analyticsDb.updateRows('orders', updates);
            }
        }
        await setOption('last_paid', nowStamp)
    } catch (error) {
        console.error(error);
    }
}

async function updateUser() {
    try {
        const uRet = await analyticsDb.query('select max(user_id) as user_id from users');
        let maxid = uRet[0].user_id;
        maxid = maxid || 0
        while(1) {
            const adds = [];
            const users = await accountDb.query(`select id,time_created from eef_core_user_account where id > ${maxid} order by id asc limit ${limit}`);
            if (!users || users.length <= 0) {
                break;
            }
            maxid = users[users.length - 1].id;
            const uids = users.map(r=>r.id);
            const profiles = await accountDb.select('eef_user_profile', {
                where: {
                    uid: uids
                }
            });
            const profileMap = new Map()
            profiles.forEach(profile => {
                profileMap.set(profile.uid, profile);
            });
            const datas = await accountDb.select('eef_core_user_data', {
                where: {
                    uid: uids,
                    module: 'user',
                    name: 'last_login'
                }
            });
            const dataMap = new Map()
            datas.forEach(data => {
                dataMap.set(data.uid, data);
            });
            users.forEach(user => {
                adds.push({
                    user_id: user.id,
                    created_at: moment(user.time_created * 1000).format('YYYY-MM-DD HH:mm:ss'),
                    last_login: dataMap.has(user.id) ? moment(dataMap.get(user.id).value_int * 1000).format('YYYY-MM-DD HH:mm:ss') : '1990-01-01 00:00:00',
                    reg_from: profileMap.has(user.id) ? profileMap.get(user.id).registered_source : null,
                })
            });
            await analyticsDb.insert('users', adds);
            console.log(maxid)
        }
        const options = await getOptions();
        let lastTime = options.get('last_login');
        let nowStamp = moment().unix();
        maxid = 0
        while(1) {
            const updates = [];
            const datas = await accountDb.query(`select uid,value_int from eef_core_user_data where uid > ${maxid} and module='user' and name='last_login' and value_int > ${lastTime} order by uid asc limit ${limit}`);
            if (!datas || datas.length <= 0) {
                break;
            }
            maxid = datas[datas.length - 1].uid;
            datas.forEach(data => {
                if (lastTime < data.value_int) {
                    lastTime = data.value_int;
                }
                updates.push({
                    row: {last_login: moment(data.value_int * 1000).format('YYYY-MM-DD HH:mm:ss')},
                    where: {user_id: data.uid}
                })
            });
            if (updates.length > 0) {
                await analyticsDb.updateRows('users', updates);
            }
        }
        await setOption('last_login', nowStamp)
    } catch (error) {
        console.error(error);
    }
}