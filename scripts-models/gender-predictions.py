import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Bidirectional, LSTM, Dense, Activation, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2

# Step 1: Load and preprocess the dataset
def load_and_preprocess_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    df['Name'] = df['Name'].str.lower()
    labels = LabelEncoder().fit_transform(df['Gender'])
    vocab = set(' '.join(df['Name']))
    vocab.add('END')
    len_vocab = len(vocab)
    char_index = dict((c, i) for i, c in enumerate(vocab))
    return df, labels, len_vocab, char_index

# Step 2: Prepare data for training
def prepare_data(df, max_name_length, len_vocab, char_index):
    X, y = [], []
    
    def set_flag(i):
        tmp = np.zeros(len_vocab)
        tmp[i] = 1
        return list(tmp)

    def prepare_X(names):
        X = []
        for name in names:
            trunc_name = str(name)[:max_name_length]
            tmp = [set_flag(char_index[c]) for c in trunc_name]
            for _ in range(max_name_length - len(trunc_name)):
                tmp.append(set_flag(char_index['END']))
            X.append(tmp)
        return X

    X = prepare_X(df['Name'])
    y = np.array([[1, 0] if gender == 'M' else [0, 1] for gender in df['Gender']])
    return X, y

# Step 3: Create and compile the LSTM model
def create_and_compile_model(max_name_length, len_vocab):
    model = Sequential()
    model.add(Bidirectional(LSTM(512, return_sequences=True), backward_layer=LSTM(512, return_sequences=True, go_backwards=True), input_shape=(max_name_length, len_vocab)))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(512)))
    model.add(Dropout(0.2))
    model.add(Dense(2, activity_regularizer=l2(0.002))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Step 4: Define callbacks for model training
def define_callbacks():
    callback = EarlyStopping(monitor='val_loss', patience=5)
    mc = ModelCheckpoint('best_model.h5', monitor='val_loss', mode='min', verbose=1)
    reduce_lr_acc = ReduceLROnPlateau(monitor='val_accuracy', factor=0.1, patience=2, verbose=1, min_delta=1e-4, mode='max')
    return [callback, mc, reduce_lr_acc]

# Step 5: Train the model
def train_model(model, X_train, y_train, X_test, y_test, batch_size, epochs, callbacks):
    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_test, y_test), callbacks=callbacks)
    return history

# Step 6: Save the trained model
def save_model(model, model_path):
    model.save(model_path)

if __name__ == "__main__":
    dataset_path = 'names.csv'
    max_name_length = 20
    batch_size = 256
    epochs = 35

    # Step 1: Load and preprocess the dataset
    df, labels, len_vocab, char_index = load_and_preprocess_dataset(dataset_path)

    # Step 2: Prepare data for training
    X, y = prepare_data(df, max_name_length, len_vocab, char_index)

    # Step 3: Create and compile the LSTM model
    model = create_and compile_model(max_name_length, len_vocab)

    # Step 4: Define callbacks for model training
    callbacks = define_callbacks()

    # Step 5: Train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    history = train_model(model, X_train, y_train, X_test, y_test, batch_size, epochs, callbacks)

    # Step 6: Save the trained model
    model_path = 'gender_prediction_model.h5'
    save_model(model, model_path)
