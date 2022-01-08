from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

def get_download_link(nusmods_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(nusmods_url)
    driver.implicitly_wait(15)
    frame = driver.find_element_by_id('downshift-1-item-0')
    return frame.get_attribute('href')

def save_image(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)
    print('done')