from selenium import webdriver
import time
import os
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

# General variables
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
ROOT_DIR = os.environ.get("ROOT_DIR")

def onpay_data():
    options = webdriver.ChromeOptions()
    path = '/path/to/chromedriver'
    options.add_argument('--headless')
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    download_dir = os.path.join(ROOT_DIR, 'Deploy MYFA/Onpay')
    options.add_experimental_option('prefs', {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True
    })
    
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.get('https://mfa.myfundaction.org.my/admin/main')
    
    # Login
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    driver.find_element_by_name("login").click()
    time.sleep(3)
    
    # Navigation
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul[1]/li[3]/a").click()
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul[1]/li[4]/a").click()
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul[1]/li[4]/ul/li[8]/a").click()
    time.sleep(3)
    
    # Select options
    option_ids_to_click = [1, 2, 3]
    for option_id in option_ids_to_click:
        driver.find_element_by_css_selector(f'#options > div:nth-child(2) > div > label:nth-child({option_id})').click()
    
    driver.find_element_by_css_selector('#status > option:nth-child(1)').click()
    driver.find_element_by_css_selector('#record_limit > option:nth-child(5)').click()
    
    # Date handling
    today = date.today()
    from_date = today - timedelta(days=1)
    from_date_str = from_date.strftime('%-d-%m-%Y')
    last_date = today - timedelta(days=1)
    last_date_str = last_date.strftime('%-d-%m-%Y')
    start_date = driver.find_element_by_id('start_date')
    end_date = driver.find_element_by_id('end_date')
    start_date.clear()
    end_date.clear()
    start_date.send_keys(from_date_str)
    end_date.send_keys(last_date_str)
    
    # Download
    driver.find_element_by_css_selector('#download_csv').click()
    time.sleep(50)
    
    driver.close()
    driver.quit()
    
    main_folder_onpay = os.path.join(ROOT_DIR, 'Deploy Onpay')
    arr = os.listdir(main_folder_onpay)
    time.sleep(2)
    
    # Find CSV file
    for i in arr:
        if 'csv' in i:
            df_onpay = pd.read_csv(os.path.join(main_folder_onpay, i))
    
    return df_onpay
