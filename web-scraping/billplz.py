import time
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.environ.get("ROOT_DIR")
CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
BILLPLZ_URL = os.environ.get("BILLPLZ_URL")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

def setup_chrome_options(download_dir):
    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    })
    return options

def login_to_billplz(driver, url, username, password):
    try:
        driver.get(url)
        username_field = driver.find_element_by_id("user_email")
        password_field = driver.find_element_by_id("user_password")
        username_field.send_keys(username)
        password_field.send_keys(password)
        driver.find_element_by_xpath('//*[@id="new_user"]/input[3]').click()
        time.sleep(3)
    except Exception as e:
        print(f"Login failed: {e}")
        driver.quit()

def download_billplz_data(driver, download_dir, report_index):
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/a[1]').click()
        datepicker = driver.find_element_by_xpath('//*[@id="account_payment_search"]/div[1]/div[2]/div/div[1]/div/div/div/div/input')
        today = date.today()
        from_date = today - timedelta(1)
        from_date = from_date.strftime('%-d %b %Y')
        driver.execute_script('$("input.form-control.daterange").data("daterangepicker").setStartDate(arguments[0])', from_date)
        driver.execute_script('$("input.form-control.daterange").data("daterangepicker").setEndDate(arguments[0])', from_date)
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
    except Exception as e:
        print(f"Download failed: {e}")
        driver.quit()

def read_billplz_data(download_dir, account_type):
    main_folder = os.path.join(ROOT_DIR, f'Deploy Billplz/{account_type}')
    arr = os.listdir(main_folder)
    for i in arr:
        if i.endswith('.xlsx'):
            return pd.read_excel(os.path.join(main_folder, i))
    return None

def billplz_scraper():
    download_dir = os.path.join(ROOT_DIR, 'Deploy Billplz')
    # Configure Chrome options for downloads
    options = setup_chrome_options(download_dir)
    # Initialize the WebDriver
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    try:
        # Log in to Billplz
        login_to_billplz(driver, BILLPLZ_URL, USERNAME, PASSWORD)
        # Download Billplz data
        download_billplz_data(driver, download_dir, 5)
        # Read and process the downloaded data
        df_billplz_myfa = read_billplz_data(download_dir, 'm')
        if df_billplz_myfa is not None:
            df_billplz_myfa['TYPE_OF_ACCOUNT'] = 'm'
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the WebDriver
        driver.quit()