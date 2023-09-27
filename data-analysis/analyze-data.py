import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from utils.data-processing import process_location, predict_occupation, predict_gender

def analyze_data(ROOT_DIR):
    billplz_data = pd.read_csv(ROOT_DIR + '/path/to/billplz_data.csv')
    onpay = pd.read_csv(ROOT_DIR + '/path/to/onpay_data.csv')
    billplz_data.rename(columns=lambda col: 'BPL ' + col, inplace=True)
    onpay.rename(columns=lambda col: 'OP ' + col, inplace=True)
    onpay = onpay.apply(process_location, axis=1)
    merged_data = pd.merge(onpay, billplz_data, how='outer', left_on='OP Billplz - Bill ID', right_on='BPL BILL ID', indicator=True)
    merged_data.to_csv(ROOT_DIR + '/path/to/merged_data.csv')
    merged_data.rename(columns={'_merge': 'Platform'}, inplace=True)
    merged_data['Platform'] = merged_data['Platform'].map({'both': 'onpay_billplz', 'right_only': 'billplz', 'left_only': 'Onpay'})

    data_billplz = merged_data[merged_data['Platform'] == 'billplz']
    data_onpay = merged_data[merged_data['Platform'] == 'Onpay']
    data_onpay_billplz = merged_data[merged_data['Platform'] == 'onpay_billplz']
    data_onpay['NAME'] = data_onpay['OP Nama']
    data_billplz['NAME'] = data_billplz['BPL NAME']
    data_onpay_billplz['NAME'] = data_onpay_billplz['BPL NAME']
    df_merge_onpay_billplz = pd.concat([data_onpay, data_billplz, data_onpay_billplz])
    df_merge_onpay_billplz['BPL TYPE_OF_ACCOUNT'] = df_merge_onpay_billplz['BPL TYPE_OF_ACCOUNT'].fillna('UNKNOWN')
    df_merge_onpay_billplz['OP Status Jualan'] = df_merge_onpay_billplz['OP Status Jualan'].fillna('DISAHKAN')
    df_merge_onpay_billplz['OP_IP_Country'] = df_merge_onpay_billplz['OP_IP_Country'].fillna('UNKNOWN')
    df_merge_onpay_billplz['OP_IP_City'] = df_merge_onpay_billplz['OP_IP_City'].fillna('UNKNOWN')
    df_merge_onpay_billplz['OP_IP_State'] = df_merge_onpay_billplz['OP_IP_State'].fillna('UNKNOWN')
    df_merge_onpay_billplz['OP_IP_Latitude'] = df_merge_onpay_billplz['OP_IP_Latitude'].fillna('UNKNOWN')
    df_merge_onpay_billplz['OP_IP_Longitude'] = df_merge_onpay_billplz['OP_IP_Longitude'].fillna('UNKNOWN')
    df_merge_onpay_billplz['OP_IP_Postal'] = df_merge_onpay_billplz['OP_IP_Postal'].fillna('UNKNOWN')
    df_merge_onpay_billplz['CAMPAIGN'] = df_merge_onpay_billplz['CAMPAIGN'].fillna('UNKNOWN')
    df_merge_onpay_billplz = df_merge_onpay_billplz.apply(predict_gender, axis=1)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df_merge_onpay_billplz['CAMPAIGN'])
    X_train, X_test, y_train, y_test = train_test_split(X, df_merge_onpay_billplz['PAYMENT_RECEIVED'], test_size=0.2, random_state=42)
    model = MultinomialNB()
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    return accuracy
