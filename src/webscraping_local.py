from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests

def get_download_link(nusmods_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(nusmods_url)
    driver.implicitly_wait(15)
    frame = driver.find_element(By.ID, 'downshift-1-item-0')
    return frame.get_attribute('href')

def save_image(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)