import time
from datetime import date, timedelta
from selenium import webdriver
import os
import pandas as pd

ROOT_DIR = '/your/root/path' 
def login_to_billplz(driver, url, username, password):
    driver.get(url)
    username_field = driver.find_element_by_id("user_email")
    password_field = driver.find_element_by_id("user_password")
    username_field.send_keys(username)
    password_field.send_keys(password)
    driver.find_element_by_xpath('//*[@id="new_user"]/input[3]').click()
    time.sleep(3)

def download_billplz_data(driver, download_dir, report_index):
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/a[1]').click()
    datepicker = driver.find_element_by_xpath('//*[@id="account_payment_search"]/div[1]/div[2]/div/div[1]/div/div/div/div/input')
    today = date.today()
    from_date = today - timedelta(1)
    from_date = from_date.strftime('%-d %b %Y')
    driver.execute_script('$("input.form-control.daterange").data("daterangepicker").setStartDate(arguments[0])',from_date)
    driver.execute_script('$("input.form-control.daterange").data("daterangepicker").setEndDate(arguments[0])',from_date)    
    driver.find_element_by_css_selector('input.form-control.daterange').click()
    driver.find_element_by_css_selector('div.range_inputs > button.applyBtn').click()
    time.sleep(3)    
    driver.find_element_by_xpath('//*[@id="account_payment_search"]/div[2]/div[2]/div[1]/div/ul/li/button/span[2]').click()    
    time.sleep(5)
    driver.refresh()
    while driver.find_element_by_css_selector('#report_downloads > tr:nth-child(1) > td:nth-child(4)').text != 'completed':
        time.sleep(10)
        driver.refresh()
    download_data = driver.find_element_by_css_selector(f'#report_downloads > tr:nth-child(1) > td:nth-child({report_index}) > a')
    download_data.click()
    time.sleep(10)

def read_billplz_data(download_dir, account_type):
    main_folder = os.path.join(ROOT_DIR, f'Deploy Billplz/{account_type}')
    arr = os.listdir(main_folder)
    for i in arr:
        if 'xlsx' in i:
            return pd.read_excel(os.path.join(main_folder, i))

def billplz_m():
    options = setup_chrome_options()
    download_dir = os.path.join(ROOT_DIR, 'Deploy Billplz')
    path = '/path/to/your/chromedriver'
    driver = webdriver.Chrome(executable_path=path, options=options)
    login_to_billplz(driver, link, username, password)
    download_billplz_data(driver, download_dir, 5)
    df_billplz_myfa = read_billplz_data(download_dir, 'm')
    df_billplz_myfa['TYPE_OF_ACCOUNT'] = 'm'
    driver.close()
    driver.quit()
    return df_billplz_myfa
