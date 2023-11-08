import re
import nltk
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dropout, Dense
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

# Constants for text preprocessing
VOCAB_SIZE = 50000
EMBEDDING_DIM = 128
MAX_SEQUENCE_LENGTH = 200
TRUNCATION_TYPE = 'post'
PADDING_TYPE = 'post'
OOV_TOKEN = '<OOV>'

# Load and preprocess the dataset
DATASET_PATH = '/content/occupation.csv'

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    text = ' '.join(stemmer.stem(word) for word in text.split())
    return text

# Load and preprocess the dataset
dataset = pd.read_csv(DATASET_PATH)
dataset.dropna(subset=["occupation"], inplace=True)
valid_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
dataset = dataset[dataset['occupation_type_new'].isin(valid_labels)]
dataset["occupation"] = dataset["occupation"].apply(clean_text)
dataset = dataset.sample(frac=1)

# Split data into features and labels
complaints = dataset["occupation"].values
labels = dataset["occupation_type_new"].values

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(complaints, labels, test_size=0.20, random_state=42)

# Tokenization
tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token=OOV_TOKEN)
tokenizer.fit_on_texts(X_train)
word_index = tokenizer.word_index

# Text sequences and padding
train_seq = tokenizer.texts_to_sequences(X_train)
train_padded = pad_sequences(train_seq, maxlen=MAX_SEQUENCE_LENGTH, padding=PADDING_TYPE, truncating=TRUNCATION_TYPE)

# One-hot encoding of labels
encode = OneHotEncoder()
training_labels = encode.fit_transform(y_train.reshape(-1, 1)).toarray()

# Create and compile the model
model = Sequential()
model.add(Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
model.add(Conv1D(48, 5, activation='relu', padding='valid'))
model.add(GlobalMaxPooling1D())
model.add(Dropout(0.5))
model.add(Dense(11, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Define training parameters and callbacks
EPOCHS = 50
BATCH_SIZE = 32

callbacks = [
    ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.0001),
    EarlyStopping(monitor='val_loss', mode='min', patience=2, verbose=1),
    EarlyStopping(monitor='val_accuracy', mode='max', patience=5, verbose=1)
]

# Train the model
history = model.fit(
    train_padded, training_labels, shuffle=True,
    epochs=EPOCHS, batch_size=BATCH_SIZE,
    validation_split=0.2,
    callbacks=callbacks
)
