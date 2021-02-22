'use strict';

const rds = require('ali-rds');
const config = require('./config');
const axios = require('axios');
const moment = require('moment');

const articleDb = rds(config.db.eefocus_article);
const limit = 10;

async function clean()
{
    const articles = await articleDb.query(`select id,content from eef_article_article where id>=477454`)
    const rows = []
    for (let i = 0; i < articles.length; i++) {
        const article = articles[i];
        const content = article.content.replace(/<a class="article-link" href="[^"]+">([^>]+)<\/a>/g, '$1')
        if (content != article.content) {
            rows.push({
                row: { content },
                where: { id: article.id }
            })
        }
    }
    if (rows.length > 0) {
        await articleDb.updateRows('eef_article_article', rows)
    }
}

async function getFromEs(keyword, maxId)
{
    const cond = {
        index: 'eefocus_search',
        body: {
            _source: {
                excludes: [ 'body' ],
            },
            query: {
                bool: {
                    filter: [
                        {
                            terms: {
                                app_id: [
                                    1, 6, 7, 8
                                ]
                            }
                        }
                    ],
                    must:[
                        {
                            match_phrase: {
                                body: keyword
                            }
                        }
                    ]
                }
            },
            sort: {
                id: {
                    order: 'desc'
                }
            },
            size: limit
        }
    };
    //TODO for test
    // cond.body.query.bool.filter[0].terms.app_id = [1]
    // cond.body.query.bool.filter.push({
    //     range: {
    //         id: {
    //             gt: '1_477454'
    //         }
    //     }
    // })
    // end TODO
    if (maxId) {
        cond.body.query.bool.filter.push({
            range: {
                id: {
                    lt: maxId
                }
            }
        })
    }
    const res = await axios({
        url: 'https://basic.eefocus.com/search/eefocus',
        method: 'post',
        data: {
            cond: JSON.stringify(cond)
        }
    })

    if (res.status != 200) {
        throw `es error - ${res.status} ${res.statusText}`;
    } else if (res.data.code != 0) {
        throw `es error - ${res.data.code} ${res.data.message}`;
    }
    const idMap = new Map()
    const ids = []
    const hits = res.data.data.body.hits.hits
    let articles = []
    let hasNext = res.data.data.body.hits.total > limit
    if (hits.length > 0) {
        hits.forEach(element => {
            const id = parseInt(element._source.id.split('_')[1])
            ids.push(id)
            idMap.set(id, element._source.id)
        });
        const tmp = await articleDb.query(`select id,content from eef_article_article where id in (${ids.join(',')}) order by id desc`)
        tmp.forEach(element => {
            element.es_id = idMap.get(element.id)
            articles.push(element)
        });
    }
    return [articles, hasNext]
}

async function getFromDb(term, maxId)
{
    let where = ''
    if (maxId) {
        where = `and id < ${maxId}`
    }
    // todo
    const articles = await articleDb.query(`select id,content from eef_article_article where id>=477454 and content like ? ${where} order by id desc limit ?`, [`%${term}%`, limit])
    return [articles, true]
}

async function getNewArticles(term, lastId)
{
    const articles = await articleDb.query(`select id,content from eef_article_article where id>${lastId} and content like ? order by id asc limit ?`, [`%${term}%`, limit])
    return [articles, true]
}

async function addLink(links, action, lastNewId)
{
    for (let i = 0; i < links.length; i++) {
        const linkRow = links[i];
        let maxId = 0;
        const addReg = new RegExp(`${linkRow.term}(?![^<]*(>|<\/a>))`)
        const exactReg = new RegExp(`<a class="article-link" href="[^"]+">${linkRow.term}<\/a>`)
        let minId = lastNewId
        while(1) {
            const rows = []
            let articles, hasNext
            if (action == 'news') {
                [articles, hasNext] = await getNewArticles(linkRow.term, minId)
            } else {
                [articles, hasNext] = await getFromEs(linkRow.term, maxId)
            }
            if (!articles || articles.length == 0) {
                break;
            }
            for (let j = 0; j < articles.length; j++) {
                const article = articles[j]
                // if (!new RegExp(`\/[a-z-]+\/${article.id}($|[^0-9])`).test(linkRow.link)) {
                //     continue;
                // }
                let content = ''
                switch (action) {
                    case 'news':
                        minId = article.id
                    case 'add':
                        content = article.content.replace(addReg, `<a class="article-link" href="${linkRow.link}">${linkRow.term}</a>`)
                        break;
                    case 'update':
                        content = article.content.replace(exactReg, `<a class="article-link" href="${linkRow.link}">${linkRow.term}</a>`)
                        break;
                    case 'delete':
                        content = article.content.replace(exactReg, linkRow.term)
                        break;
                
                    default:
                        break;
                }

                if (content != '' && content != article.content) {
                    rows.push({
                        row: { content, time_update: moment().unix() },
                        where: { id: article.id }
                    })
                }
            }
            if (rows.length > 0) {
                await articleDb.updateRows('eef_article_article', rows)
            }
            if (!hasNext) {
                break;
            }
            if (articles[articles.length - 1].es_id) {
                maxId = articles[articles.length - 1].es_id
            } else {
                maxId = articles[articles.length - 1].id
            }
        }
    }
}

(async () => {
    try {
        // await clean()
        // process.exit()
        let offset = 0;
        const batchConfig = await articleDb.get('eef_user_batch', {type: 1})
        let lastId = batchConfig.last_id
        let lastTime = batchConfig.last_time
        await articleDb.query(`delete from eef_article_link where id > ${lastId} and time_delete > 0`);

        console.log('--- ' + moment().format('YYYY-MM-DD HH:mm:ss'))

        // new articles
        if (batchConfig.last_id > 0) {
            console.log('add link => new articles begin...')
            offset = 0;
            const maxArticleId = await articleDb.query('select max(id) as maxid from eef_article_article')
            while(1) {
                const links = await articleDb.query(`select * from eef_article_link order by id asc limit ${limit} offset ${offset}`);
                if (!links || links.length == 0) {
                    break;
                }
                offset += limit

                await addLink(links, 'news', batchConfig.last_new_id)
                console.log(`add link => new articles offset ${offset} - finished`)
            }
            batchConfig.last_new_id = maxArticleId[0].maxid
            await articleDb.update('eef_user_batch', batchConfig)
        }

        // delete
        console.log('delete link begin...')
        while(1) {
            const links = await articleDb.query(`select * from eef_article_link where time_delete > 0 limit ${limit}`);
            if (!links || links.length == 0) {
                break;
            }

            await addLink(links, 'delete')
            const delIds = links.map(r => r.id)

            await articleDb.delete('eef_article_link', {id: delIds});
        }
        // add
        console.log('add link begin...')
        offset = 0;
        while(1) {
            const links = await articleDb.query(`select * from eef_article_link where id > ${lastId} order by id asc limit ${limit} offset ${offset}`);
            if (!links || links.length == 0) {
                break;
            }
            offset += limit

            await addLink(links, 'add')
            batchConfig.last_id = links[links.length - 1].id
            console.log(`add link offset ${offset} - finished`)
        }
        await articleDb.update('eef_user_batch', batchConfig)

        // update
        console.log('update link begin...')
        offset = 0;
        while(1) {
            const links = await articleDb.query(`select * from eef_article_link where id <= ${lastId} and time_update >= ${lastTime} order by id asc limit ${limit} offset ${offset}`);
            if (!links || links.length == 0) {
                break;
            }
            offset += limit

            await addLink(links, 'update')
            console.log(`update link offset ${offset} - finished`)
        }
        batchConfig.last_time = moment().unix()
        await articleDb.update('eef_user_batch', batchConfig)

        process.exit()
    } catch (error) {
        console.error(error);
        process.exit()
    }
})();
