import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import *
from sklearn.svm import *
from sklearn.metrics import make_scorer, cohen_kappa_score
from model_train.load_data import load_data_train
from scipy import stats


def tuning():
    rand_list = {"C": stats.uniform(2, 10),
                 "gamma": stats.uniform(0.1, 1),
                 "kernel": ["linear", "poly", "rbf"]}
    mdl = SVC(probability=True, random_state=1)
    auc = make_scorer(cohen_kappa_score)
    grid_list = {"C": np.arange(2, 10, 2),
                 "gamma": np.arange(0.1, 1, 0.2)}
    # C_range = np.logspace(-1, 2, 4)
    # kernels = ["linear", "poly", "rbf"]
    # param_grid = dict(gamma=['auto'], C=C_range, kernel=kernels)
    # grid = GridSearchCV(SVC(), param_grid=grid_list, n_jobs=-1, verbose=2)
    grid = RandomizedSearchCV(mdl, param_distributions=rand_list, n_iter=2, n_jobs=2, cv=2, random_state=1000,
                              scoring=auc, verbose=1000)
    print("fitting")
    grid.fit(x_data_tf_idf, y_data)
    print("saving")
    pickle.dump(grid, open('model/grid_svm.model', 'wb'))


def retrain():
    print('retrain best param')
    grid = pickle.load(open('model/grid_svm.model', 'rb'))
    params = grid.best_params_
    print(grid.cv_results_)
    C = params["C"]
    kernel = params["kernel"]
    gamma = params["gamma"]
    svm = SVC(C=C, kernel=kernel, gamma=gamma)
    print("fitting")
    svm.fit(x_data_tf_idf, y_data)
    print("saving")
    pickle.dump(svm, open('model/svm_model.pkl', 'wb'))
    print('extract_xpath complete! ')


if __name__ == "__main__":
    x_data, y_data, x_test, y_test = load_data_train()
    print("Load data success")

    # tf_idf_vec = pickle.load(open("model/tf_idf_vec.pkl", "rb"))
    tf_idf_vec = TfidfVectorizer(analyzer='word', max_features=30000)
    tf_idf_vec.fit(x_data)
    print("fit success")
    x_data_tf_idf = tf_idf_vec.transform(x_data)
    x_test_tf_idf = tf_idf_vec.transform(x_test)
    tuning()
    retrain()
    svm_model = pickle.load(open('model/svm_model.pkl', 'rb'))
    acc = svm_model.score(x_test_tf_idf, y_test)
    print(acc)
