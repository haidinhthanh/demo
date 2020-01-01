from keras.layers import Input, Reshape, Bidirectional, Dense, LSTM
from keras import optimizers
from keras.models import Model
from model_train.category_classify_naive_bayes import train_model, load_data_train
import pickle
import numpy as np
from sklearn import preprocessing


def create_bi_rnn_model():
    input_layer = Input(shape=(30000,))
    layer = Reshape((10, 3000))(input_layer)
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
    tf_idf_vec = pickle.load(open("model/tf_idf_vec.pkl", "rb"))
    x_data_tf_idf = tf_idf_vec.transform(x_data)
    x_test_tf_idf = tf_idf_vec.transform(x_test)
    print(np.shape(x_data_tf_idf))
    print("tf_idf convert success")
    # convert y to categorical
    encoder = preprocessing.LabelEncoder()
    y_data_n = encoder.fit_transform(y_data)
    y_test_n = encoder.fit_transform(y_test)
    print("convert success")

    bi_rnn = create_bi_rnn_model()
    train_model(bi_rnn, x_data_tf_idf, y_data_n, x_test_tf_idf, y_test_n, is_neural_net=True)
    nb_model_file_path = 'model/bi_rnn_model.pkl'
    nb_model_trained = open(nb_model_file_path, 'wb')
    pickle.dump(bi_rnn, nb_model_trained)
    nb_model_trained.close()
    print('Dump NB success')