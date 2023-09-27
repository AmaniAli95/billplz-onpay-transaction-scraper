# Billplz Onpay Transaction Scrapper
## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [Data Analysis](#data-analysis)
- [Output](#output)
- [Acknowledgments](#acknowledgments)
  
## Overview
This repository contains a Python script that automates the extraction and analysis of data from the Billplz and Onpay payment gateways. The script streamlines the entire process, including:

- **Authentication:** Logging into Billplz using your credentials.
- **Data Retrieval:** Navigating the transaction and reporting pages and downloading transaction data as CSV files.
- **Data Preprocessing:** Cleaning and preprocessing the raw data.
- **Data Analysis:** Conducting analysis on transaction trends, payment volumes, user demographics, etc., using machine learning models.
- **Data Export:** Exporting the final analyzed dataset to Google BigQuery.
  
The script uses Selenium and ChromeDriver to automate logging into Billplz and exporting the transaction data. This eliminates the need to manually download reports from the Billplz dashboard. The script does not perform any in-depth data analysis or machine learning. It is focused solely on automating the extraction of transaction data as CSVs from Billplz and Onpay.
The final cleaned data ingests to BigQuery provides the raw transaction data in a structured format for further analysis as needed. This script solves the problem of manually gathering data, acting as a data collection automation tool for Billplz and Onpay.

## Prerequisites
Before you dive in and use the script, make sure you have the following prerequisites set up on your machine:
- Python 3.x
- Google Chrome web browser
- Chromedriver
- The necessary Python packages (you can install them with `pip install -r requirements.txt`)

## Installation
Follow these simple steps to get started:
1. Clone the repository to your local machine:
```bash
git clone git@github.com:AmaniAli95/web-data-automation.git
```
2. Navigate to the project directory:
```bash
cd web-data-automation
```
3. Install the Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Configure Chrome Options (Optional):
You can customize the Chrome browser settings by modifying the `setup_chrome_options()` function in the `main.py` script. By default, it runs in headless mode for a smoother experience.
2. Set Up Chromedriver:
Replace the `path` variable in the `main.py` script with the correct path to your Chromedriver executable.
3. Run the Script:
Execute the following command to run the script:
```bash
python main.py
```
The script will handle everything, from logging into your Billplz and Onpay account to downloading data, conducting a thorough analysis, and saving the result

## File Structure
This section outlines the organization of key script components for automating the extraction and analysis of transaction data from the Billplz payment gateway. The repository includes Python scripts for various tasks related to data analysis, Chrome setup, data processing, and web scraping. Below is a brief overview of each component:
### data analysis
- **analyze-data.py:** This Python script provides automation for extracting and analyzing transaction data from Billplz and Onpay payment gateways. It covers functions for logging into Billplz and Onpay, navigating to transaction reporting pages, downloading data in CSV format, data preprocessing, and performing analysis using machine learning models to predict occupation and gender. The analyzed dataset can be exported to BigQuery for further analysis. To use this script, clone the repository, install Python dependencies, configure Chrome options if necessary, and specify the Chromedriver path. Running the script automates the entire data collection, analysis, and export process, reducing the need for manual data gathering.

### utils
- **chrome-setup.py:** This Python script, `chrome-setup.py`, configures Chrome browser options using Selenium. By default, it sets Chrome to run in headless mode for a smoother automated experience. It also disables certain browser features like infobars, extensions, and notifications to ensure seamless data extraction.
- **data-processing.py:** It utilizes the `requests` library to process IP location data and two machine learning models for occupation and gender prediction. It queries geolocation data for an IP address, extracts relevant information, and returns it as a list of key-value pairs. The script also employs scikit-learn's `CountVectorizer` and `MultinomialNB` to predict occupation and gender based on input text. Given a name, it predicts the occupation and gender by transforming the input text into feature vectors and then using `MultinomialNB` for classification. These functions can be integrated into your data processing pipeline for further analysis and enrichment.

### web scraping
- **billplz.py:** Streamlines data extraction from the Billplz payment gateway. The script automates the login process, navigation to relevant pages, and downloading of transaction data in CSV format. To use it, configure the appropriate `ROOT_DIR`, provide the path to Chromedriver, and enter your Billplz login credentials. Ensure you have Python 3.x, Google Chrome, and Chromedriver installed. Upon execution, it logs in, downloads the data, and returns it as a Pandas DataFrame, facilitating data collection and automation.
- **onpay.py:** It automates data extraction from the Onpay payment gateway using Selenium. It securely logs into your Onpay account, navigates to transaction data, applies filters, and downloads CSV files. Replace 'YourUsername,' 'YourPassword,' and '/path/to/your/root/directory' with your Onpay account credentials and desired download directory. The script utilizes ChromeDriver, headless browsing, and custom download settings for seamless automation. After downloading the data, it reads the CSV file, allowing for further data processing and analysis. Make sure you have Selenium, Pandas, and ChromeDriver installed to run this script successfully.

## Configuration
`main.py`: This is the main script that orchestrates the entire automation process. It contains functions for web scraping, data analysis, and data processing.

## Data Analysis
The data analysis is performed using machine learning models for the prediction of occupation and gender. The trained models are defined in separate functions, `predict_occupation()` and `predict_gender()`.

## Output
The script generates and stores the analyzed data in a format defined in `analyzedata()`. You can customize this function to save the data in your desired format.

## Acknowledgments
- **Selenium** - Web automation framework.
- **Scikit-Learn** - Machine learning library for Python.
- **Chromedriver** - WebDriver for Chrome.
