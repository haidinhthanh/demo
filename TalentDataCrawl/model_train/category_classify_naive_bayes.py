import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, naive_bayes, metrics
from model_train.load_data import load_data_nb


def train_model(classifier, x_data, y_data, x_test=None, y_test=None, n_epochs=3, is_neural_net=False):
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


def train_navies_bayes_model(x_train_tf_idf, y_train, x_test_tf_idf, y_test):
    naive_bayes_model = naive_bayes.BernoulliNB()
    train_model(naive_bayes_model, x_train_tf_idf, y_train, x_test_tf_idf, y_test)
    nb_model_file_path = 'model/NB_relevant/naive_bayes_model.pkl'
    nb_model_trained = open(nb_model_file_path, 'wb')
    pickle.dump(naive_bayes_model, nb_model_trained)
    nb_model_trained.close()
    print('Dump NB success')


#
# def train_svm_model(x_train_tf_idf, y_train, x_test_tf_idf, y_test):
#     svm_model = svm.SVC()
#     train_model(svm_model, x_train_tf_idf, y_train, x_test_tf_idf, y_test)
#     nb_model_file_path = 'model/svm.pkl'
#     nb_model_trained = open(nb_model_file_path, 'wb')
#     pickle.dump(svm_model, nb_model_trained)
#     nb_model_trained.close()
#     print('Dump NB success')
#

if __name__ == "__main__":
    print("Start")
    x_data, y_data, x_test, y_test = load_data_nb()

    # word level, max number of words equal to 30000 except all words
    tf_idf_vec = TfidfVectorizer(analyzer='word', max_features=30000)
    tf_idf_vec.fit(x_data)
    pickle.dump(tf_idf_vec, open("model/NB_relevant/tf_idf_vec.pkl", "wb"))

    # tf_idf_vec = pickle.load(open("model/tf_idf_vec.pkl", "rb"))
    x_data_tf_idf = tf_idf_vec.transform(x_data)
    x_test_tf_idf = tf_idf_vec.transform(x_test)
    print("tf_idf convert success")
    # # convert y to categorical
    encoder = preprocessing.LabelEncoder()
    y_data_n = encoder.fit_transform(y_data)
    y_test_n = encoder.fit_transform(y_test)
    print("convert success")
    train_navies_bayes_model(x_data_tf_idf, y_data_n, x_test_tf_idf, y_test_n)
