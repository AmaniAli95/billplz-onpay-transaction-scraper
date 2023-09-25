import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from utils.data-processing import process_location, predict_occupation, predict_gender

def analyzedata():
    billplz_data = pd.read_csv(os.path.join(ROOT_DIR, 'billplz_data.csv'))
    billplz_data = billplz_data.rename(columns=lambda x: f'BPL {x}')
    data_billplz = billplz_data[billplz_data['Platform'] == 'billplz']

    data_billplz['NAME'] = data_billplz['BPL NAME']
    data_billplz['EMAIL'] = data_billplz['BPL EMAIL']
    data_billplz['PAYMENT_RECEIVED'] = data_billplz['BPL PAYMENT RECEIVED']
    data_billplz['TRANSACTION_DATE'] = data_billplz['BPL TRANSACTION DATE['OP Tarikh & Masa (Dimasukkan)']
    data_billplz['CAMPAIGN'] = data_billplz['BPL COLLECTION TITLE']

    data_billplz['TRANSACTION_DATE'].fillna('N/A', inplace=True)
    data_billplz['PAYMENT_RECEIVED'].fillna(0, inplace=True)
    data_billplz['GENDER'].fillna('N/A', inplace=True)
    data_billplz['OCCUPATION'].fillna('N/A', inplace=True)

    cv_gender = CountVectorizer()
    cv_occupation = CountVectorizer()
    clf_gender = MultinomialNB()
    clf_occupation = MultinomialNB()

    names_gender = pd.read_csv(os.path.join(ROOT_DIR, 'train_gender.csv'))
    names_occupation = pd.read_csv(os.path.join(ROOT_DIR, 'train_occupation.csv'))
    X_gender = cv_gender.fit_transform(names_gender['name']).toarray()
    y_gender = names_gender['gender']
    clf_gender.fit(X_gender, y_gender)
    X_occupation = cv_occupation.fit_transform(names_occupation['name']).toarray()
    y_occupation = names_occupation['occupation']
    clf_occupation.fit(X_occupation, y_occupation)
    data_billplz['GENDER'] = data_billplz['NAME'].apply(
        lambda x: predict_gender(x, cv_gender, clf_gender)
    )
    data_billplz['OCCUPATION'] = data_billplz['NAME'].apply(
        lambda x: predict_occupation(x, cv_occupation, clf_occupation)
    )

    data_billplz['TYPE_OF_ACCOUNT'] = data_billplz['CAMP'].apply('M')

    data_billplz.to_csv(os.path.join(ROOT_DIR, 'processed_data.csv'))
    return data_billplz
