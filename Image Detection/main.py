from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu") 
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_image_details(url):
    driver.get(url)  

    images = driver.find_elements(By.TAG_NAME, 'img')
    print(f"Found {len(images)} images on {url}.")

    # images with reload time > 0.5s or size > 1MB
    filtered_images = []


    for img in images:
        img_url = img.get_attribute('src')  # Get image URL
        
        if img_url:
            if not img_url.startswith('http'):
                img_url = url + img_url
            
            try:
                #  image details
                img_response = requests.get(img_url, stream=True)
                img_size = len(img_response.content) / 1024  # Size in KB
                img_type = img_url.split('.')[-1]  # Extract image type (file extension)

                # Mock Load Time
                start_time = time.time()
                img_response = requests.get(img_url)
                load_time = round(time.time() - start_time, 2)

                # Display the image(all)
                # print(f"Image: {img_url} | Size: {img_size:.2f} KB | Type: {img_type} | Load Time: {load_time:.2f} s")
                
                
                if load_time > 0.1 or img_size > 1024:  # 1024 KB = 1MB
                    filtered_images.append({
                        "url": img_url,
                        "size": img_size,
                        "type": img_type,
                        "load_time": load_time
                    })

            except requests.exceptions.RequestException as e:
                print(f"Error loading image {img_url}: {e}")
    
    print("\nImages with reload time > 0.5s or size > 1MB:")
    for image in filtered_images:
        print(f"Image: {image['url']} | Size: {image['size']:.2f} KB | Type: {image['type']} | Load Time: {image['load_time']:.2f} s")

get_image_details('https://crocobet.com')

driver.quit()
