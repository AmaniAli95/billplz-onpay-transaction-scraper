import pandas as pd
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import requests
from dotenv import load_dotenv

load_dotenv()
ROOT_DIR = os.environ.get("ROOT_DIR")

vocab_size = 50000
max_length = 200
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>'

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

def load_text_model(model_path, tokenizer, encode):
    # Load the pre-trained text classification model
    model = tf.keras.models.load_model(model_path)
    return model, tokenizer, encode

def load_gender_model(model_path, char_index, len_vocab):
    # Load the pre-trained gender prediction model
    model = tf.keras.models.load_model(model_path)
    return model, char_index, len_vocab

def preprocess_text(text, tokenizer, max_length):
    # Tokenize and preprocess text
    text = [text]
    seq = tokenizer.texts_to_sequences(text)
    padded = pad_sequences(seq, maxlen=max_length, padding=padding_type, truncating=trunc_type)
    return padded

def predict_occupation(text, text_model, tokenizer, encode):
    # Predict occupation type for text
    text_padded = preprocess_text(text, tokenizer, max_length)
    pred = text_model.predict(text_padded)
    predicted_label = encode.inverse_transform(pred)
    return predicted_label[0][0]

def predict_gender(name, gender_model, char_index, len_vocab):
    # Predict gender for a name
    name = prepare_X([name], max_length, char_index)
    prediction = gender_model.predict(name)
    gender_dict = {0: 'F', 1: 'M'}  # Define your mapping here
    return gender_dict[np.argmax(prediction[0])]

def process_location(ip):
    response = requests.get(f"https://geolocation.com/{ip}").json()
    dictList = []
    for key, value in response.items():
        dictList.append([key, value])
    return dictList
