'use strict';

module.exports = {
    db: {
        host: '192.168.2.82',
        port: 3309,
        user: 'pi_article',
        password: 'account#@II(+qwepi!!',
        database: 'pi_article_eefocus',
    },
    sleepMss: [3000, 7000],
    mongo: {
        url: 'mongodb://192.168.99.100:27017',
    },
    spider: {
        tuotu: {
            AccessKey: '',
            AccessSecret: '',
        }
    },
    eefUserId: 3470578,
    imgUrl: 'https://wximg.eefocus.com/forward?',
    featureImg: {
        dist: '/Users/hypnos/Work/eefocus/vhosts/article-eefocus-com/upload/article/feature/',
        forDb: 'upload/article/feature/',
    },
    wxAccount: [
        {name: '满天芯', userName: 'mantianIC', eefAuthorId: 125, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '拓墣产业研究', userName: 'TRI-topology', eefAuthorId: 126, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '汽车电子设计', userName: 'QCDZSJ', eefAuthorId: 34, channel: 1, subtitle:'《汽车电子瞭望台》系列', tags:['公众号', '《汽车电子瞭望台》系列']},
        // {name: '芯思想', userName: 'ChipInsights', eefAuthorId: 113, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '老石谈芯', userName: 'gh_5ce1d0cb1568', eefAuthorId: 128, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '痞子衡嵌入式', userName: 'pzh_mcu', eefAuthorId: 129, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '物联网智库', userName: 'iot101', eefAuthorId: 130, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'AI人工智能产业研究', userName: 'AIchanyan', eefAuthorId: 131, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '脑极体', userName: 'unity007', eefAuthorId: 132, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '大鱼半导体', userName: 'gh_50dcc483f978', eefAuthorId: 133, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '功率半导体那些事儿', userName: 'Power_semiconductors', eefAuthorId: 134, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '花边科技', userName: 'huabiankeji', eefAuthorId: 135, channel: 1, subtitle:'', tags:['公众号']},




        // {name: '满天芯', userName: 'mantianIC', eefAuthorId: 134, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '拓墣产业研究', userName: 'TRI-topology', eefAuthorId: 135, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '汽车电子设计', userName: 'QCDZSJ', eefAuthorId: 34, channel: 1, subtitle:'《汽车电子瞭望台》系列', tags:['公众号', '《汽车电子瞭望台》系列']},
        // {name: '芯思想', userName: 'ChipInsights', eefAuthorId: 113, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '老石谈芯', userName: 'gh_5ce1d0cb1568', eefAuthorId: 133, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '痞子衡嵌入式', userName: 'pzh_mcu', eefAuthorId: 136, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '物联网智库', userName: 'iot101', eefAuthorId: 137, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'AI人工智能产业研究', userName: 'AIchanyan', eefAuthorId: 138, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '脑极体', userName: 'unity007', eefAuthorId: 140, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '大鱼半导体', userName: 'gh_50dcc483f978', eefAuthorId: 141, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '功率半导体那些事儿', userName: 'Power_semiconductors', eefAuthorId: 142, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '花边科技', userName: 'huabiankeji', eefAuthorId: 143, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '智车行家', userName: 'gh_4090d6fa3eb3', eefAuthorId: 152, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'ATC汽车技术会议', userName: 'ATC-conference', eefAuthorId: 153, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '科创之道', userName: 'FinanceDL', eefAuthorId: 150, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '芯片之家', userName: 'chiphome-dy', eefAuthorId: 158, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'TsinghuaJoking', userName: 'tsinghuazhuoqing', eefAuthorId: 154, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '芯华社', userName: 'ChipNews', eefAuthorId: 113, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '芯片揭秘', userName: 'ICxpjm', eefAuthorId: 169, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '无线深海', userName: 'wuxian_shenhai', eefAuthorId: 162, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '小鱼学IC', userName: 'LF-FPGA', eefAuthorId: 159, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'CINNO', userName: 'CINNO_CreateMore', eefAuthorId: 156, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '鲜枣课堂', userName: 'xzclasscom', eefAuthorId: 163, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'SiP系统级封装技术', userName: 'SiPTechnology', eefAuthorId: 165, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '大鱼机器人', userName: 'All_best_xiaolong', eefAuthorId: 141, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'AI报道', userName: 'AI-Reporting', eefAuthorId: 144, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '志博PCB', userName: 'gh_2c41021c3d8e', eefAuthorId: 155, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'AI掘金志', userName: 'HealthAI', eefAuthorId: 166, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'AI芯天下', userName: 'World_2078', eefAuthorId: 167, channel: 1, subtitle:'', tags:['公众号']},
        // {name: 'FPGA开源工作室', userName: 'leezym0317', eefAuthorId: 164, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '史晨星', userName: 'shichenxing1', eefAuthorId: 151, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '科技茱比莉Jubilee', userName: 'IT-Jubilee', eefAuthorId: 157, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '电子产业分析', userName: 'gh_0cdc890e93ea', eefAuthorId: 161, channel: 1, subtitle:'', tags:['公众号']},
        // {name: '佐思汽车研究', userName: 'zuosiqiche', eefAuthorId: 160, channel: 1, subtitle:'', tags:['公众号']},
    ],
}