import { Builder, By } from 'selenium-webdriver';
import chrome from 'selenium-webdriver/chrome.js';
import fetch from 'node-fetch';  // Use node-fetch instead of axios
import { performance } from 'perf_hooks';
import pLimit from 'p-limit';  // Import p-limit

const limit = pLimit(7); // Increase concurrency limit to 10

(async function getImageDetails(url) {
  // Set Chrome options for headless mode
  let options = new chrome.Options();
  options.addArguments('--headless');
  options.addArguments('--disable-gpu');
  options.addArguments('--no-sandbox');

  // Start the Chrome WebDriver
  const driver = await new Builder()
    .forBrowser('chrome')
    .setChromeOptions(options)
    .build();

  try {
    // Navigate to the URL
    await driver.get(url);

    // Execute a script to retrieve all image sources at once (bypass individual getAttribute calls)
    const imageUrls = await driver.executeScript(() => {
      const images = Array.from(document.querySelectorAll('img'));
      return images.map(img => img.src).filter(src => src); // Only return non-null/undefined URLs
    });

    console.log(`Found ${imageUrls.length} image URLs on ${url}.`);

    const filteredImages = [];  // Array to store filtered images
    const imageRequests = [];  // Array to store the image requests

    // Process the image URLs with concurrency control
    for (let imgUrl of imageUrls) {
      // Limit concurrent requests
      imageRequests.push(limit(() => fetchImageDetails(imgUrl, filteredImages)));
    }

    // Wait for all image requests to finish
    await Promise.all(imageRequests);

    console.log("\nImages with reload time > 0.1s or size > 1MB:");
    filteredImages.forEach(image => {
      console.log(`Image: ${image.url} | Size: ${image.size.toFixed(2)} KB | Type: ${image.type} | Load Time: ${image.load_time} s`);
    });

  } catch (error) {
    console.log(`Error during WebDriver operation: ${error}`);
  } finally {
    await driver.quit(); // Ensure driver quits after the operation
  }
})('https://crocobet.com');

// Function to fetch image details asynchronously
async function fetchImageDetails(imgUrl, filteredImages) {
  const startTime = performance.now();

  try {
    // Use fetch to get image data
    const response = await fetch(imgUrl);
    const buffer = await response.buffer();

    const imgSize = buffer.length / 1024; // Image size in KB
    const imgType = imgUrl.split('.').pop(); // Extract file extension as image type
    const loadTime = (performance.now() - startTime) / 1000; // Load time in seconds

    // Filter based on load time > 0.1s or size > 1MB
    if (loadTime > 0.1 || imgSize > 1024) {  // 1024 KB = 1MB
      filteredImages.push({
        url: imgUrl,
        size: imgSize,
        type: imgType,
        load_time: loadTime.toFixed(2)
      });
    }
  } catch (err) {
    console.log(`Error loading image ${imgUrl}: ${err}`);
  }
}
