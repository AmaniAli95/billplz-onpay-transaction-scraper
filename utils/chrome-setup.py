from selenium import webdriver

def setup_chrome_options(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    return options
