'use strict';

const config = require('./config');
const sapi = require('./tuotu');
const rds = require('ali-rds');
const MongoClient = require('mongodb').MongoClient;
const db = rds(config.db);

(async () => {
    try {
        const client = await MongoClient.connect(config.mongo.url, {useUnifiedTopology: true});
        const mdb = await client.db('wxspider');
        await sapi.setMongo(mdb);

        const accountList = [
            ['lhl545545','lhl545545'],
            ['strongerHuang ','strongerHuang '],
            ['吴老师聊通信','吴老师聊通信'],
            ['eWiseTech','eWiseTech'],
            ['运算放大器参数解析与LTspice应用仿真','郑荟民'],
            ['人人都是极客','人人都是极客'],
            ['放大器参数解析与LTspice仿真','放大器参数解析与LTspice仿真'],
            ['Linux阅码场','Linux阅码场'],
            ['雷锋网','雷锋网'],
            ['量子位','量子位'],
            ['智车科技','智车科技'],
            ['芯通社','芯通社'],
            ['郭静的互联网圈','郭静'],
            ['电磁兼容EMC','电磁兼容EMC'],
            ['质量提升与技术','质量提升与技术'],
            ['宽禁带半导体技术创新联盟','宽禁带联盟'],
            ['半导体综研','半导体综研'],
            ['讯石光通讯','讯石光通讯'],
            ['移远通信','移远通信'],
            ['纽迪瑞','纽迪瑞'],
            ['美信半导体','美信半导体'],
            ['Bosch Sensortec','Bosch Sensortec'],
            ['是德科技KEYSIGHT','是德科技KEYSIGHT'],
            ['Cypress赛普拉斯半导体','Cypress赛普拉斯半导体'],
            ['Dialog半导体公司','Dialog半导体公司'],
            ['BlackBerry企业级软件与服务','BlackBerry企业级软件与服务'],
            ['富昌电子','富昌电子'],
            ['紫光展锐UNISOC','紫光展锐UNISOC'],
            ['Murata村田中国','Murata村田中国'],
            ['Latticesemi','Latticesemi'],
            ['英飞凌中国','英飞凌中国'],
            ['英飞凌工业半导体','英飞凌工业半导体'],
            ['力特半导体无锡有限公司','力特半导体无锡有限公司'],
            ['安富利','安富利'],
            ['瑞士ublox','瑞士ublox'],
            ['安森美半导体','安森美半导体'],
            ['Xilinx赛灵思官微','Xilinx赛灵思官微'],
            ['英特尔FPGA','英特尔FPGA'],
            ['英特尔中国','英特尔中国'],
            ['英特尔商用频道','英特尔商用频道'],
            ['英特尔物联网','英特尔物联网'],
            ['商汤科技SenseTime','商汤科技SenseTime'],
            ['贸泽电子','贸泽电子'],
            ['贸泽电子设计圈','贸泽电子设计圈'],
            ['瑞萨电子','瑞萨电子'],
            ['知IN','知IN'],
            ['长电科技','长电科技'],
            ['欧姆龙工业自动化资讯号','欧姆龙工业自动化资讯号'],
            ['万业企业','万业企业'],
            ['东芝中国','东芝中国'],
            ['力特奥维斯Littelfuse','力特奥维斯Littelfuse'],
            ['米尔MYiR','米尔MYiR'],
            ['新思科技','新思科技'],
        ];
        for (let i = 0; i < accountList.length; i++) {
            const author = await db.get('eef_article_author', {name: accountList[i][1]});
            if (!author) {
                throw `${accountList[i][0]} - no author`;
            }
            const info = await sapi.wxInfo(accountList[i][0]);
            const matchBiz = /biz=(.*)#/.exec(info.CustomizedInfo.BrandInfo)
            if (!matchBiz) {
                throw `${accountList[i][0]} - no biz`;
            }
            console.log(`{name: '${accountList[i][0]}', 'biz': '${matchBiz[1]}', userName: '${info.Alias}', eefAuthorId: ${author.id}, channel: 1, subtitle:'', tags:['公众号']}`);
        }
        process.exit()
    } catch (error) {
        console.error(error);
        process.exit()
    }
})();
