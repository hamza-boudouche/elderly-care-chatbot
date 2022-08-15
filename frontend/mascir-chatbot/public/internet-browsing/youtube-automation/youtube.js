const { initBrowser, openUrl } = require("../setup")
const { By, Key } = require("selenium-webdriver")

/**
 * 
 * @param {number} ms 
 * @returns 
 */
const delay = (ms) => new Promise((res) => setTimeout(res, ms));

/**
 * 
 * @param {string} searchQuery 
 */
const getYoutubeSearchResults = async (searchQuery) => {
	const driver = await initBrowser();
	await openUrl("https://www.youtube.com", driver);
	const searchbar = await driver.findElement(By.name("search_query"));
	await searchbar.click();
	await searchbar.clear();
	await searchbar.sendKeys(searchQuery, Key.RETURN);

	await delay(5000);
	const searchResults = await driver.findElements(By.id("video-title"));
	const filteredSearchResults = []
	await Promise.all(
		searchResults.map(async (element) => {
			if ((await element.getTagName()) === "a") {
				filteredSearchResults.push({
					link: await element.getAttribute("href"),
					title: await element.getAttribute("title")
				})
			}
		})
	);
	driver.close()
	return filteredSearchResults
};

/**
 * 
 * @param {string} url 
 * @returns 
 */
const controlYoutubeVideo = async (url) => {
	const driver = await initBrowser();
	await openUrl(url, driver);
	await driver.executeScript(
		'document.getElementsByClassName("ytp-prev-button")[0].setAttribute("style", "")'
	);
	const prevButton = await driver.findElement(By.className("ytp-prev-button"));
	const nextButton = await driver.findElement(By.className("ytp-next-button"));
	const playPauseButton = await driver.findElement(
		By.className("ytp-play-button")
	);

	const playPauseVideo = async () => {
		await playPauseButton.click();
	};

	const skipForward = async () => {
		//TODO: implement this
	};

	const skipBackward = async () => {
		//TODO: implement this
	};

	const prevVideo = async () => {
		await prevButton.click();
	};

	const nextVideo = async () => {
		await nextButton.click();
	};

	const closeVideo = () => {
		driver.close()
	}

	return {
		playPauseVideo,
		skipForward,
		skipBackward,
		prevVideo,
		nextVideo,
		closeVideo
	};
};

module.exports = {
	getYoutubeSearchResults,
	controlYoutubeVideo
}