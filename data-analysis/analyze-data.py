import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from dotenv import load_dotenv
from utils.data-processing import load_data,rename_columns,merge_data,load_text_model,load_gender_model,predict_occupation,predict_gender

# Load environment variables
load_dotenv()

# Load datasets
BILLPLZ_DATA_PATH = os.environ.get("BILLPLZ_DATA_PATH")
ONPAY_DATA_PATH = os.environ.get("ONPAY_DATA_PATH")
billplz_data = load_data(BILLPLZ_DATA_PATH)
onpay_data = load_data(ONPAY_DATA_PATH)

# Define model paths
TEXT_MODEL_PATH = 'text_classification_model.h5'
GENDER_MODEL_PATH = 'gender_prediction_model.h5'

vocab_size = 50000
max_length = 200
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>'

rename_columns(billplz_data)
rename_columns(onpay_data)
merged_data = merge_data(billplz_data, onpay_data)


tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
encode = OneHotEncoder()  # Define your encoder with appropriate settings
text_model, tokenizer, encode = load_text_model(TEXT_MODEL_PATH, tokenizer, encode)
gender_model, char_index, len_vocab = load_gender_model(GENDER_MODEL_PATH, char_index, len_vocab)

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
    
    for i in range(len(merged_data)):
        a = merged_data['GENDER'].iloc[i]
        if a == None :
            try:
                b = merged_data['NAME'].iloc[i]
                if b != 'tiada nama':
                    c = predict_gender(b, gender_model, char_index, len_vocab)
                    merged_data.loc[i,'GENDER']=c
                elif b == 'tiada nama':
                    merged_data.loc[i,'GENDER']= 'UNKNOWN'
            except:
                merged_data.loc[i,'GENDER']= 'UNKNOWN'
    
    for i in range(len(merged_data)):
        try:
            b = merged_data['occupation'].iloc[i]
            if b != 'tiada nama':
                merged_data.loc[i,'occupation_type']= predict_occupation(b, text_model, tokenizer, encode)
            elif b == 'tiada nama':
                merged_data.loc[i,'occupation_type']= 'K'
        except:
            merged_data.loc[i,'occupation_type']= 'K'  
    return merged_data