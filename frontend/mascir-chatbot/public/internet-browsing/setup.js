const { Builder, Capabilities, WebDriver } = require("selenium-webdriver")

const initBrowser = async () => {
	const driver = await new Builder()
		.withCapabilities(Capabilities.firefox())
		.build();
	return driver;
};

/**
 * 
 * @param {string} url 
 * @param {WebDriver} driver 
 * @returns 
 */
const openUrl = async (url) => {
	const driver = await initBrowser();
	try {
		await driver.get(url);
	} catch (error) {
		console.log(`error ${error}`);
	}

	const quit = () => {
		driver.quit();
	}

	return {
		quit
	}
};

module.exports = {
	openUrl,
	initBrowser
}