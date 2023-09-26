# Web Data Automation
## Overview
This repository contains a Python script for automating data extraction and analysis from a popular payment gateway. The script leverages Selenium for web scraping and employs machine learning models for in-depth data analysis.

## Prerequisites
Before you dive in and use the script, make sure you have the following prerequisites set up on your machine:
- Python 3.x
- Google Chrome web browser
- Chromedriver
- The necessary Python packages (you can install them with ```pip install -r requirements.txt```)

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
You can customize the Chrome browser settings by modifying the ```setup_chrome_options()``` function in the ```main.py script```. By default, it runs in headless mode for a smoother experience.

2. Set Up Chromedriver:
Replace the `path` variable in the ```main.py``` script with the correct path to your Chromedriver executable.

3. Run the Script:
Execute the following command to run the script:
```bash
python main.py
```
The script will handle everything, from logging into your Billplz account to downloading data, conducting thorough analysis, and saving the resul

## Configuration
```main.py```: This is the main script that orchestrates the entire automation process. It contains functions for web scraping, data analysis, and data processing.

## Data Analysis
The data analysis is performed using machine learning models for the prediction of occupation and gender. The trained models are defined in separate functions, ```predict_occupation()``` and ```predict_gender()```.

## Output
The script generates and stores the analyzed data in a format defined in ```analyzedata()```. You can customize this function to save the data in your desired format.

## Acknowledgments
- **Selenium** - Web automation framework.
- **Scikit-Learn** - Machine learning library for Python.
- **Chromedriver** - WebDriver for Chrome.
