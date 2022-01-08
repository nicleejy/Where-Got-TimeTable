from selenium import webdriver
import requests

def get_download_link(nusmods_url):
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")

    chrome_options.binary_location = GOOGLE_CHROME_PATH

    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    browser.get(nusmods_url)
    browser.implicitly_wait(15)
    frame = browser.find_element_by_id('downshift-1-item-0')
    return frame.get_attribute('href')

def save_image(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)
    print('done')