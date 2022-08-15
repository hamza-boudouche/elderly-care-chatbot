const { app, BrowserWindow, ipcMain } = require('electron')

const path = require('path')
const isDev = require('electron-is-dev')
const { electron } = require('process')

require('@electron/remote/main').initialize()

const { openUrl } = require("./internet-browsing/setup")
const { controlYoutubeVideo, getYoutubeSearchResults } = require("./internet-browsing/youtube-automation/youtube")
const { Driver } = require('selenium-webdriver/chrome')

let controls = undefined
let youtubeControls = undefined

function createWindow() {
	// Create the browser window. 
	const win = new BrowserWindow({
		width: 700,
		height: 800,
		webPreferences: {
			nodeIntegration: true,
			contextIsolation: true,
			enableRemoteModule: false,
			preload: path.join(__dirname, "preload.js")
		}
	})

	win.loadURL(
		isDev
			? 'http://localhost:3000'
			: `file://${path.join(__dirname, '../build/index.html')}`
	)
}

app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
	// On OS X it is common for applications and their menu bar
	// to stay active until the user quits explicitly with Cmd + Q
	if (process.platform !== 'darwin') {
		app.quit()
	}
})

app.on('activate', function () {
	// On OS X it's common to re-create a window in the app when the
	// dock icon is clicked and there are no other windows open.
	if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

ipcMain.on("message.receive", async (e, { text }) => {
	console.log("message was received", text)
})

ipcMain.on("selenium.open", async (e, { url }) => {
	console.log("open selenium browser")
	controls = await openUrl(url)
})

ipcMain.on("selenium.close", async (e) => {
	controls?.quit()
	controls = undefined
	youtubeControls = undefined
})

ipcMain.on("selenium.youtube.search", async (e, { search_query }) => {
	controls?.quit()
	await getYoutubeSearchResults(search_query)
})

ipcMain.on("selenium.youtube.open", async (e, { url }) => {
	controls?.quit()
	youtubeControls = await controlYoutubeVideo(url)
	controls = {
		quit: youtubeControls.closeVideo
	}
})

ipcMain.on("selenium.youtube.playPause", async (e) => {
	await youtubeControls?.playPauseVideo()
})

ipcMain.on("selenium.youtube.skipForward", async (e) => {
	await youtubeControls?.skipForward()
})

ipcMain.on("selenium.youtube.skipBackward", async (e) => {
	await youtubeControls?.skipBackward()
})

ipcMain.on("selenium.youtube.prevVideo", async (e) => {
	await youtubeControls?.prevVideo()
})

ipcMain.on("selenium.youtube.nextVideo", async (e) => {
	await youtubeControls?.nextVideo()
})