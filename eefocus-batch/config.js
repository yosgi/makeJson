'use strict';

module.exports = {
    db: {
        eefocus_account: {
            host: '192.168.2.82',
            port: 3309,
            user: 'pi_account',
            password: 'arti!#cle!@#123qwepi',
            database: 'pi_account_eefocus',
        },
        eefocus_center: {
            host: '192.168.2.82',
            port: 3309,
            user: 'pi_account',
            password: 'arti!#cle!@#123qwepi',
            database: 'pi_account_eefocus',
        },
        sendy: {
            host: '192.168.99.100',
            port: 3306,
            user: 'root',
            password: 'root',
            database: 'sendy',
        }
    },
    sendy_new: {
        list: 1406,//2782
        app: 19,
    },
    google: {
        account_sheetid: '1KhSXBkUCh16KisLdpItTz-ZmiaJrwg3L95PY2fSCOZs',
        from_map: [
            { app: 'pi250d', name: 'EEFocus' },
            { app: '110', name: 'Cirmall_BBS' },
            { app: '2005', name: 'Cirmall' },
            { app: '2004', name: 'Moore8' },
            { app: '2', name: 'Community_NXP' },
            { app: '6', name: 'Community_RF' },
            { app: '11', name: 'Community_ST' },
            { app: '4002', name: 'Community_ROHM' },
            { app: '3002', name: 'Community_AMS' },
        ],
        proxy: 'http://127.0.0.1:1087'
    }
}