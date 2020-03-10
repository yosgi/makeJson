'use strict'
const fs = require('fs');
const moment = require('moment');

exports.info = function(data) {
    let fd = fs.openSync(__dirname + '/log/info.log', 'a');
    fs.writeFileSync(fd, moment().format('YYYY-MM-DD HH:mm:ss  ') + data + "\n", {flag: 'a'});
    fs.closeSync(fd);
}

exports.error = function(data) {
    let fd = fs.openSync(__dirname + '/log/error.log', 'a');
    fs.writeFileSync(fd, moment().format('YYYY-MM-DD HH:mm:ss  ') + data + "\n", {flag: 'a'});
    fs.closeSync(fd);
}