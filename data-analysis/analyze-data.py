import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import requests
from dotenv import load_dotenv

from utils.data-processing import process_location, predict_occupation, predict_gender

load_dotenv()

# Define constants for file paths and sensitive information
ROOT_DIR = 'os.environ.get("ROOT_DIR")
BILLPLZ_DATA_PATH = os.environ.get("BILLPLZ_DATA_PATH")
ONPAY_DATA_PATH = os.environ.get("ONPAY_DATA_PATH")
NAMA_DATA_PATH = os.environ.get("NAMA_DATA_PATH")
OCCUPATION_DATA_PATH = os.environ.get("OCCUPATION_DATA_PATH")

def rename_columns(df):
    for column in df.columns:
        df.rename(columns={column: f'BPL {column}'}, inplace=True)

def load_data(file_path):
    return pd.read_csv(file_path)

def merge_data(billplz_data, onpay_data):
    merged_data = pd.merge(onpay_data, billplz_data, how='outer', left_on='OP Billplz - Bill ID', right_on='BPL BILL ID', indicator=True)
    merged_data.to_csv(ROOT_DIR + '/Deploy billplzonpay.csv')
    merged_data['_merge'] = merged_data['_merge'].astype(str)
    merged_data['_merge'].loc[(merged_data['_merge'] == 'both')] = 'onpay_billplz'
    merged_data['_merge'].loc[(merged_data['_merge'] == 'right_only')] = 'billplz'
    merged_data['_merge'].loc[(merged_data['_merge'] == 'left_only')] = 'Onpay'
    return merged_data

def analyze_data(merged_data):
    data_billplz = merged_data[merged_data['_merge'] == 'billplz']
    data_onpay = merged_data[merged_data['_merge'] == 'Onpay']
    data_onpay_billplz = merged_data[merged_data['_merge'] == 'onpay_billplz']

    # Rename and process columns
    data_onpay['NAME'] = data_onpay['OP Nama']
    data_billplz['NAME'] = data_billplz['BPL NAME']
    data_onpay_billplz['NAME'] = data_onpay_billplz['BPL NAME']

    data_onpay['EMAIL'] = data_onpay['OP Emel']
    data_billplz['EMAIL'] = data_billplz['BPL EMAIL']
    data_onpay_billplz['EMAIL'] = data_onpay_billplz['OP Emel']

    data_onpay['PAYMENT_RECEIVED'] = data_onpay['OP Jumlah Keseluruhan (RM)']
    data_billplz['PAYMENT_RECEIVED'] = data_billplz['BPL PAYMENT RECEIVED']
    data_onpay_billplz['PAYMENT_RECEIVED'] = data_onpay_billplz['OP Jumlah Keseluruhan (RM)']

    data_onpay['TRANSACTION_DATE'] = data_onpay['OP Tarikh & Masa (Dimasukkan)']
    data_billplz['TRANSACTION_DATE'] = data_billplz['BPL TRANSACTION DATE']
    data_onpay_billplz['TRANSACTION_DATE'] = data_onpay_billplz['OP Tarikh & Masa (Dimasukkan)']

    data_onpay['CAMPAIGN'] = data_onpay['OP Kod Borang']
    data_billplz['CAMPAIGN'] = data_billplz['BPL COLLECTION TITLE']
    data_onpay_billplz['CAMPAIGN'] = data_onpay_billplz['BPL COLLECTION TITLE']

    merged_data = data_onpay.append([data_billplz, data_onpay_billplz])
    
    # Handle missing values and preprocess gender
    merged_data['GENDER'] = None
    merged_data['NAME'] = merged_data['NAME'].str.lower()
    merged_data['FirstName'] = merged_data['NAME'].str.split().str[0]
    merged_data['Gender'].replace({'F':0,'M':1},inplace=True)
    Xfeatures =merged_data['Name']
    cv = CountVectorizer()
    X = cv.fit_transform(Xfeatures)
    y = merged_data.Gender
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    clf = MultinomialNB()
    clf.fit(X_train,y_train)
    clf.score(X_test,y_test)
    merged_data.reset_index(inplace=True)
    for i in range(len(merged_data)):
        a = merged_data['GENDER'].iloc[i]
        if a == None :
            try:
                b = merged_data['NAME'].iloc[i]
                if b != 'tiada nama':
                    c = genderpredictor(b)
                    merged_data.loc[i,'GENDER']=c
                elif b == 'tiada nama':
                    merged_data.loc[i,'GENDER']= 'UNKNOWN'
            except:
                merged_data.loc[i,'GENDER']= 'UNKNOWN'
    Xfeatures =merged_data['occupation']
    cv = CountVectorizer()
    X = cv.fit_transform(Xfeatures)
    y = merged_data['occupation_type']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    clf = MultinomialNB()
    clf.fit(X_train,y_train)
    
    merged_data.reset_index(inplace=True)
    for i in range(len(merged_data)):
        try:
            b = merged_data['occupation'].iloc[i]
            if b != 'tiada nama':
                merged_data.loc[i,'occupation_type']= occupation(b)
            elif b == 'tiada nama':
                merged_data.loc[i,'occupation_type']= 'K'
        except:
            merged_data.loc[i,'occupation_type']= 'K'  
    return merged_data

