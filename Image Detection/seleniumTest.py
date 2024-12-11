# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import requests
# import time

# # Setup for headless browser using Chrome
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(options=options)

# # Function to get all image URLs from a webpage using Selenium
# def get_image_urls_dynamic(url):
#     driver.get(url)
#     time.sleep(5)  # Give time for dynamic content to load
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     img_urls = []
#     for img in soup.find_all('img'):
#         img_url = img.get('src')
#         if img_url:
#             # Convert relative URLs to absolute URLs
#             if img_url.startswith('http'):
#                 img_urls.append(img_url)
#             else:
#                 img_urls.append(f"{url.rstrip('/')}/{img_url.lstrip('/')}")
    
#     return img_urls

# # Function to check image metadata (size, content-type, etc.)
# def check_image_metadata(url):
#     try:
#         start_time = time.time()
#         response = requests.head(url, allow_redirects=True)  # Use HEAD request to fetch headers only
#         response.raise_for_status()  # Raise an exception for 4xx/5xx responses

#         # Extract content-length (size in bytes) and content-type (image format)
#         img_size = int(response.headers.get('Content-Length', 0))  # Size in bytes
#         img_type = response.headers.get('Content-Type', 'unknown')
#         load_time = time.time() - start_time  # Time in seconds
        
#         return img_size, img_type, load_time
#     except requests.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return None, None, None

# # Function to analyze and report only large images
# def analyze_large_images(website_url, size_threshold=500):
#     img_urls = get_image_urls_dynamic(website_url)
#     print(f"Found {len(img_urls)} images on {website_url}.\n")

#     # Check each image's metadata (size, type, and load time)
#     for img_url in img_urls:
#         img_size, img_type, load_time = check_image_metadata(img_url)
#         if img_size is not None and load_time is not None:
#             # Only display images larger than the threshold size (in KB)
#             if img_size > size_threshold * 1024:  # Convert KB to Bytes
#                 print(f"Large Image: {img_url} | Size: {img_size / 1024:.2f} KB | Type: {img_type} | Load Time: {load_time:.2f} s")

# # Example usage
# website_url = "https://crocobet.com"  # Replace with your target website
# analyze_large_images(website_url, size_threshold=500)  # Display only images larger than 500 KB

# # Don't forget to quit the browser after you're done
# driver.quit()



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

# Setup for headless browser using Chrome
options = Options()
options.headless = True  # Ensure headless mode is enabled
options.add_argument("--no-sandbox")  # Sometimes necessary for headless to work correctly
options.add_argument("--disable-dev-shm-usage")  # Improve stability of headless mode
driver = webdriver.Chrome(options=options)

# Function to get all image URLs from a webpage using Selenium
def get_image_urls_dynamic(url):
    driver.get(url)
    time.sleep(5)  # Give time for dynamic content to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    img_urls = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            # Convert relative URLs to absolute URLs
            if img_url.startswith('http'):
                img_urls.append(img_url)
            else:
                img_urls.append(f"{url.rstrip('/')}/{img_url.lstrip('/')}")
    
    return img_urls

# Function to check image metadata (size, content-type, etc.)
def check_image_metadata(url):
    try:
        start_time = time.time()
        response = requests.head(url, allow_redirects=True)  # Use HEAD request to fetch headers only
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses

        # Extract content-length (size in bytes) and content-type (image format)
        img_size = int(response.headers.get('Content-Length', 0))  # Size in bytes
        img_type = response.headers.get('Content-Type', 'unknown')
        load_time = time.time() - start_time  # Time in seconds
        
        return img_size, img_type, load_time
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None, None

# Function to analyze and report only large images
def analyze_large_images(website_url, size_threshold=100):
    img_urls = get_image_urls_dynamic(website_url)
    print(f"Found {len(img_urls)} images on {website_url}.\n")

    # Check each image's metadata (size, type, and load time)
    for img_url in img_urls:
        img_size, img_type, load_time = check_image_metadata(img_url)
        if img_size is not None and load_time is not None:
            # Only display images larger than the threshold size (in KB)
            if img_size > size_threshold * 1024:  # Convert KB to Bytes
                # Format the output to match the requested format
                print(f"Large Image: {img_url} | Size: {img_size / 1024:.2f} KB | Type: {img_type} | Load Time: {load_time:.2f} s")

# Example usage
website_url = "https://crocobet.com"  # Replace with your target website
analyze_large_images(website_url, size_threshold=500)  # Display only images larger than 500 KB

# Don't forget to quit the browser after you're done
driver.quit()
