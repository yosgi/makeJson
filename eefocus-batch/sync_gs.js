'use strict';

const rds = require('ali-rds');
const config = require('./config');
const centerDb = rds(config.db.eefocus_center);

const moment = require('moment')
const fs = require('fs');
const readline = require('readline');
const {google} = require('googleapis');

process.env.http_proxy = config.google.proxy;
process.env.https_proxy = config.google.proxy;

// If modifying these scopes, delete token.json.
const SCOPES = ['https://www.googleapis.com/auth/spreadsheets'];
// The file token.json stores the user's access and refresh tokens, and is
// created automatically when the authorization flow completes for the first
// time.
const TOKEN_PATH = 'token.json';

// Load client secrets from a local file.
fs.readFile('credentials.json', (err, content) => {
  if (err) return console.log('Error loading client secret file:', err);
  // Authorize a client with credentials, then call the Google Sheets API.
  authorize(JSON.parse(content), main);
});

/**
 * Create an OAuth2 client with the given credentials, and then execute the
 * given callback function.
 * @param {Object} credentials The authorization client credentials.
 * @param {function} callback The callback to call with the authorized client.
 */
function authorize(credentials, callback) {
  const {client_secret, client_id, redirect_uris} = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(
      client_id, client_secret, redirect_uris[0]);

  // Check if we have previously stored a token.
  fs.readFile(TOKEN_PATH, (err, token) => {
    if (err) return getNewToken(oAuth2Client, callback);
    oAuth2Client.setCredentials(JSON.parse(token));
    callback(oAuth2Client);
  });
}

/**
 * Get and store new token after prompting for user authorization, and then
 * execute the given callback with the authorized OAuth2 client.
 * @param {google.auth.OAuth2} oAuth2Client The OAuth2 client to get token for.
 * @param {getEventsCallback} callback The callback for the authorized client.
 */
function getNewToken(oAuth2Client, callback) {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
  });
  console.log('Authorize this app by visiting this url:', authUrl);
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.question('Enter the code from that page here: ', (code) => {
    rl.close();
    oAuth2Client.getToken(code, (err, token) => {
      if (err) return console.error('Error while trying to retrieve access token', err);
      oAuth2Client.setCredentials(token);
      // Store the token to disk for later program executions
      fs.writeFile(TOKEN_PATH, JSON.stringify(token), (err) => {
        if (err) return console.error(err);
        console.log('Token stored to', TOKEN_PATH);
      });
      callback(oAuth2Client);
    });
  });
}

function getFromMap() {
    const fromMap = new Map();
    config.google.from_map.map(fromRow => {
        fromMap.set(fromRow.app, fromRow.name);
    })
    return fromMap;
}

async function main(auth){
    try {
        const sheets = google.sheets({version: 'v4', auth});
        const res = await sheets.spreadsheets.values.get({
            spreadsheetId: config.google.account_sheetid,
            range: 'A1',
        });
        const rows = res.data.values;
        const cellDefault = rows[0][0].split('-');
        let maxid = parseInt(cellDefault[1]);
        let maxRow = parseInt(cellDefault[2]);
        if (!maxid || !maxRow) {
            throw 'get <db max id>-<sheet max row> error'
        }
        const limit = 100;
        const data = [{range: 'A1'}, {}];
        const fromMap = getFromMap();
        const today = moment().startOf('day').unix();
        while(1) {
            const users = await centerDb.query(`select id,time_register,position,\`from\`,visit_province from eef_platform_auto_business_edm where id > ${maxid} and time_register < ${today} order by id asc limit ${limit}`);
            if (!users || users.length <= 0) {
                break;
            }
            const appendData = []
            users.map(user => {
                appendData.push([moment(user.time_register * 1000).format('YYYY/MM/DD HH:mm'), user.position, fromMap.has(user.from) ? fromMap.get(user.from) : 'OTHER', user.visit_province || '']);
            })
            data[1] = {
                range: `A${maxRow + 1}`,
                values: appendData,
            };
            maxid = users[users.length - 1].id;
            maxRow += users.length;
            data[0].values = [[`${cellDefault[0]}-${maxid}-${maxRow}`]];
            await sheets.spreadsheets.values.batchUpdate({
                spreadsheetId: config.google.account_sheetid,
                resource: {
                    data,
                    valueInputOption: 'RAW',
                },
            });
        }
        process.exit()
    } catch (error) {
        console.error(error);
        process.exit()
    }
}