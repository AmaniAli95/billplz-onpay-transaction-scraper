import requests
import re
import nltk
import tensorflow as tf
import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from numpy.random import seed
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix, classification_report
from mlxtend.plotting import plot_confusion_matrix
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dropout, Dense
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from dotenv import load_dotenv

load_dotenv()
seed(1)
tf.random.set_seed(2)
nltk.download('stopwords')
nltk.download('punkt')

# Replace with your dataset and model file paths
DATASET_PATH = os.environ.get("DATASET_PATH")
MODEL_PATH = os.environ.get("MODEL_PATH")

vocab_size = 50000
embedding_dim = 128
max_length = 200
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>'

def process_location(ip):
    response = requests.get(f"https://geolocation.com/{ip}").json()
    dictList = []
    for key, value in response.items():
        dictList.append([key, value])
    return dictList

def clean_text(text):
    """
    Clean and preprocess text data.

    Args:
        text (str): Input text to clean.

    Returns:
        str: Cleaned text.
    """
    text = text.lower()
    text = re.sub('[/(){}\[\]\|@,;]', ' ', text)
    text = text.replace('x', '')
    text = re.sub('[^0-9a-z #+_]', '', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    text = ' '.join(word for word in text.split() if 2 <= len(word) <= 21)
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text

def load_dataset(dataset_path):
    """
    Load the dataset.

    Args:
        dataset_path (str): Path to the dataset CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    dataset = pd.read_csv(dataset_path)
    return dataset

def preprocess_data(dataset):
    """
    Preprocess dataset, split, and tokenize text.

    Args:
        dataset (pd.DataFrame): Input dataset.

    Returns:
        tuple: Training and validation data.
    """
    dataset["occupation"] = dataset["occupation"].apply(clean_text)
    dataset = dataset.sample(frac=1)
    complaints = dataset["occupation"].values
    labels = dataset[["occupation_type"]].values
    X_train, X_test, y_train, y_test = train_test_split(
        complaints, labels, test_size=0.20, random_state=42
    )

    tokenizer = Tokenizer(num_words=vocab_size, oov_token='<OOV>')
    tokenizer.fit_on_texts(X_train)
    word_index = tokenizer.word_index
    train_seq = tokenizer.texts_to_sequences(X_train)
    train_padded = pad_sequences(train_seq, maxlen=max_length, padding=padding_type, truncating=trunc_type)
    validation_seq = tokenizer.texts_to_sequences(X_test)
    validation_padded = pad_sequences(validation_seq, maxlen=max_length, padding=padding_type, truncating=trunc_type)

    encode = OneHotEncoder()
    training_labels = encode.fit_transform(X_test).toarray()
    validation_labels = encode.transform(y_test).toarray()

    return train_padded, training_labels, validation_padded, validation_labels

def load_model(model_path):
    """
    Load a pre-trained model.

    Args:
        model_path (str): Path to the model HDF5 file.

    Returns:
        tf.keras.Model: Loaded model.
    """
    model = tf.keras.models.load_model(model_path)
    return model

def predict_occupation(model, tokenizer, text):
    """
    Predict occupation type for a given text.

    Args:
        model (tf.keras.Model): Loaded model.
        tokenizer (Tokenizer): Tokenizer used for text preprocessing.
        text (str): Input text for prediction.

    Returns:
        str: Predicted occupation type.
    """
    text = clean_text(text)
    new_complaint = [text]
    seq = tokenizer.texts_to_sequences(new_complaint)
    padded = pad_sequences(seq, maxlen=max_length, padding=padding_type, truncating=trunc_type)
    pred = model.predict(padded)
    predicted_label = encode.inverse_transform(pred)
    label = predicted_label[0]
    if highestNumber(pred[np.argmax(label)]) > 0.7:
        result = label[0]
    else:
        result = 'K'
    return result
    
def load_trained_model(model_path):
    return tf.keras.models.load_model(model_path, custom_objects=None, compile=True)

# Preprocess the dataset
def preprocess_dataset(data_path, maxlen=20):
    df = pd.read_csv(data_path)
    df['name'] = df['name'].apply(lambda x: str(x).lower())
    df = df[[len(e) > 1 for e in df.name]]
    df = df.drop_duplicates()
    names = df['name'].apply(lambda x: x.lower())
    gender = df['gender']
    vocab = set(' '.join([str(i) for i in names]))
    vocab.add('END')
    len_vocab = len(vocab)
    char_index = dict((c, i) for i, c in enumerate(vocab))
    X = prepare_X(names, maxlen, char_index)
    y = prepare_y(gender)
    return X, y

def prepare_X(names, maxlen, char_index):
    X = []
    for name in names.values:
        trunc_name = name[0:maxlen]
        tmp = [set_flag(char_index[j], len_vocab) for j in str(trunc_name)]
        for _ in range(0, maxlen - len(str(trunc_name))):
            tmp.append(set_flag(char_index["END"], len_vocab))
        X.append(tmp)
    return X

def prepare_y(gender):
    y = []
    for g in gender:
        if g == 'M':
            y.append([1, 0])
        else:
            y.append([0, 1])
    return y

def set_flag(i, len_vocab):
    tmp = np.zeros(len_vocab)
    tmp[i] = 1
    return list(tmp)

def predict_gender(new_names, prediction, dict_answer):
    return_results = []
    for i in prediction:
        if max(i) < 0.50:
            return_results.append([new_names, "N"])
        else:
            return_results.append([new_names, dict_answer[np.argmax(i)]])
    return return_results
