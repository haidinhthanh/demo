from keras.layers import Input, Reshape, Bidirectional, Dense, GRU, LSTM
from keras import optimizers
from keras.models import Model
from extract_xpath.load_data import load_data_train
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing, naive_bayes, metrics, svm
from os import  path


def train_model(classifier, x_data, y_data, x_test=None, y_test=None, n_epochs=1, is_neural_net=False):
    print("Training")
    x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.1, random_state=42)
    if is_neural_net:
        classifier.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=n_epochs, batch_size=512)

        val_predictions = classifier.predict(x_val)
        test_predictions = classifier.predict(x_test)
        val_predictions = val_predictions.argmax(axis=-1)
        test_predictions = test_predictions.argmax(axis=-1)
    else:
        classifier.fit(x_train, y_train)
        val_predictions = classifier.predict(x_val)
        test_predictions = classifier.predict(x_test)

    print("Validation accuracy: ", metrics.accuracy_score(val_predictions, y_val))
    print("Test accuracy: ", metrics.accuracy_score(test_predictions, y_test))


def create_bi_rnn_model():
    input_layer = Input(shape=(9000,))
    layer = Reshape((10, 900))(input_layer)
    # layer = Bidirectional(GRU(128, activation='relu'))(layer)
    layer = Bidirectional(LSTM(units=256, return_sequences=False,
                               recurrent_dropout=0.5))(layer)
    layer = Dense(512, activation='relu')(layer)
    layer = Dense(512, activation='relu')(layer)
    layer = Dense(128, activation='relu')(layer)
    output_layer = Dense(11, activation='softmax')(layer)
    classifier = Model(input_layer, output_layer)
    classifier.compile(optimizer=optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return classifier


if __name__ == "__main__":
    x_data, y_data, x_test, y_test = load_data_train()
    tf_idf_vec = TfidfVectorizer(analyzer='word', max_features=9000)
    tf_idf_vec.fit(x_data)
    pickle.dump(tf_idf_vec, open("tf_idf_vec_5.pkl", "wb"))
    # tf_idf_vec = pickle.load(open("tf_idf_vec.pkl", "rb"))
    x_data_tf_idf = tf_idf_vec.transform(x_data)
    x_test_tf_idf = tf_idf_vec.transform(x_test)
    print(np.shape(x_data_tf_idf))
    print("tf_idf convert success")
    # convert y to categorical
    encoder = preprocessing.LabelEncoder()
    y_data_n = encoder.fit_transform(y_data)
    y_test_n = encoder.fit_transform(y_test)
    print("convert success")
    if path.exists("bi_rnn_model_6.pkl"):
        print("load model")
        bi_rnn = pickle.load(open('bi_rnn_model_6.pkl', 'rb'))
    else:
        print("create model")
        bi_rnn = create_bi_rnn_model()
    train_model(bi_rnn, x_data_tf_idf, y_data_n, x_test_tf_idf, y_test_n, is_neural_net=True)
    nb_model_file_path = 'bi_rnn_model_8.pkl'
    nb_model_trained = open(nb_model_file_path, 'wb')
    pickle.dump(bi_rnn, nb_model_trained)
    nb_model_trained.close()
    print('Dump NB success')