import os
from selenium import webdriver
from utils.chrome-setup import setup_chrome_options
from web-scraping.billplz import login_to_billplz,download_billplz_data,read_billplz_data
from data-analysis.analyze-data import analyzedata
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.environ.get("ROOT_DIR")
LINK = os.environ.get("LINK")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
PATH = os.environ.get("PATH")

def main():
    options = setup_chrome_options()
    download_dir = os.path.join(ROOT_DIR, 'Deploy Billplz')
    driver = webdriver.Chrome(executable_path=PATH, options=options)
    login_to_billplz(driver, LINK, USERNAME, PASSWORD)
    download_billplz_data(driver, download_dir, 5)
    df_billplz_myfa = read_billplz_data(download_dir, 'm')
    df_billplz_myfa['TYPE_OF_ACCOUNT'] = 'm'
    driver.close()
    driver.quit()
    analyzedata()

if __name__ == "__main__":
    main()
