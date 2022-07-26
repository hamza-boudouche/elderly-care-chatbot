const fs = require('fs');
const readline = require('readline');
const { google } = require('googleapis');
const path = require('path');

const SCOPES = ['https://www.googleapis.com/auth/calendar'];
const TOKEN_PATH = path.join(__dirname, '../../token.json');

/**
 * parse credentials from json credentials file
 */
function credentials() {
	return new Promise((resolve, reject) => {
		fs.readFile(path.join(__dirname, "credentials.json"), (err, content) => {
			if (err) reject("error loading credentials")
			resolve(JSON.parse(content))
		})
	})
}

/**
 * Create and return OAuth2 client with the given credentials
 * @param {Object} credentials 
 */
function authorize(credentials) {
	return new Promise((resolve, reject) => {
		const { client_secret, client_id, redirect_uris } = credentials.web;
		const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
		// Check if we have previously stored a token.
		fs.readFile(TOKEN_PATH, (err, token) => {
			if (err) {
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
					oAuth2Client.getToken(code, (err2, newToken) => {
						if (err2) reject('Error retrieving access token', err);
						oAuth2Client.setCredentials(newToken);
						// Store the token to disk for later program executions
						fs.writeFile(TOKEN_PATH, JSON.stringify(token), (err) => {
							if (err) reject(err);
							console.log('Token stored to', TOKEN_PATH);
						});
					});
				});
			}
			else {
				oAuth2Client.setCredentials(JSON.parse(token));
			}
			resolve(oAuth2Client)
		});
	})
}

/**
 * 
 * @param {google.auth.OAuth2} auth 
 */
function refreshAccessToken(auth) {
	return new Promise((resolve, reject) => {
		oAuth2Client.refreshAccessToken(function (err, tokens) {
			resolve(tokens.access_token)
		});
	})
}

module.exports = {
	credentials,
	authorize,
	refreshAccessToken
}