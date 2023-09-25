import os
from selenium import webdriver
from utils.chrome-setup import setup_chrome_options
from web-scraping.billplz import login_to_billplz,download_billplz_data,read_billplz_data
from data-analysis.analyze-data import analyzedata

ROOT_DIR = '/your/root/path/documents'
link = 'your_link_here'
username = 'your_username_here'
password = 'your_password_here'

def main():
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
    analyzedata()

if __name__ == "__main__":
    main()
