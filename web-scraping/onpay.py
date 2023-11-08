from selenium import webdriver
import time
import os
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# General variables
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
ROOT_DIR = os.environ.get("ROOT_DIR")

def configure_chrome_options(download_dir):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_experimental_option('prefs', {
        'download.default_directory': download_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True
    })
    return options

def login(driver, url, username, password):
    driver.get(url)
    username_element = driver.find_element_by_id("username")
    password_element = driver.find_element_by_id("password")
    username_element.send_keys(username)
    password_element.send_keys(password)
    driver.find_element_by_name("login").click()
    time.sleep(3)

def navigate_to_reports_page(driver):
    # Replace these XPath expressions with more descriptive ones
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul[1]/li[3]/a").click()
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul[1]/li[4]/a").click()
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul[1]/li[4]/ul/li[8]/a").click()
    time.sleep(3)

def select_options(driver):
    option_ids_to_click = [1, 2, 3]
    for option_id in option_ids_to_click:
        driver.find_element_by_css_selector(f'#options > div:nth-child(2) > div > label:nth-child({option_id})').click()

def set_date_range(driver, start_date, end_date):
    start_date_element = driver.find_element_by_id('start_date')
    end_date_element = driver.find_element_by_id('end_date')
    start_date_element.clear()
    end_date_element.clear()
    start_date_element.send_keys(start_date)
    end_date_element.send_keys(end_date)

def download_csv(driver):
    driver.find_element_by_css_selector('#download_csv').click()
    time.sleep(50)

def find_csv_file(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            return os.path.join(directory, filename)
    return None

def scrape_onpay_data():
    download_dir = os.path.join(ROOT_DIR, 'Deploy MYFA/Onpay')
    options = configure_chrome_options(download_dir)
    # Initialize the WebDriver
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=options)
    try:
        # Log in to Onpay
        login(driver, 'https://main', USERNAME, PASSWORD)
        # Navigate to reports page
        navigate_to_reports_page(driver)
        # Select options
        select_options(driver)
        # Set date range
        today = date.today()
        from_date = today - timedelta(days=1)
        start_date = from_date.strftime('%-d-%m-%Y')
        end_date = start_date
        set_date_range(driver, start_date, end_date)
        # Download CSV
        download_csv(driver)
        # Find and read the downloaded CSV
        main_folder_onpay = os.path.join(ROOT_DIR, 'Deploy Onpay')
        csv_file = find_csv_file(main_folder_onpay)
        if csv_file:
            df_onpay = pd.read_csv(csv_file)
        else:
            print("CSV file not found.")
            df_onpay = None
    except Exception as e:
        print(f"Error: {e}")
        df_onpay = None
    finally:
        driver.quit()
    return df_onpay