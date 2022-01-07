from selenium import webdriver

def get_download_link(nusmods_url):
    driver = webdriver.Chrome()
    driver.get(nusmods_url)
    driver.implicitly_wait(15)
    frame = driver.find_element_by_id('downshift-1-item-0')
    return frame.get_attribute('href')