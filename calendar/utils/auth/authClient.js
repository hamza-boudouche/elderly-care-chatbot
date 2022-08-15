const fs = require('fs');
const readline = require('readline');
const { google } = require('googleapis');
const path = require('path');
const fetch = require("node-fetch")

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
					prompt: 'consent'
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
						fs.writeFile(TOKEN_PATH, JSON.stringify(newToken), (err) => {
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

async function refreshAccessToken() {
	const credentialsContent = await fs.promises.readFile(path.join(__dirname, "credentials.json"))
	const oldTokenContent = await fs.promises.readFile(TOKEN_PATH)
	const credentials = JSON.parse(credentialsContent)
	const oldToken = JSON.parse(oldTokenContent)
	const resp = await fetch("https://www.googleapis.com/oauth2/v4/token", {
		method: "POST",
		body: JSON.stringify({
			client_id: credentials.web.client_id,
			client_secret: credentials.web.client_secret,
			refresh_token: oldToken.refresh_token,
			grant_type: "refresh_token"
		}),
		headers: {
			"Content-type": "application/json; charset=UTF-8"
		}
	})
	const newTokenData = await resp.json()
	const newToken = {
		...newTokenData,
		refresh_token: oldToken.refresh_token
	}
	console.log(credentials)
	console.log(newToken)
	await fs.promises.writeFile(TOKEN_PATH, JSON.stringify(newToken))
}

module.exports = {
	credentials,
	authorize,
	refreshAccessToken
}