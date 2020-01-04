import os
import pickle
dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path.replace("comon", "")
bi_rnn = pickle.load(open(os.path.join(path, "model/bi_rnn_model.pkl"), "rb"))
irr_naive_bayes = pickle.load(open(os.path.join(path, "model/NB_relevant/naive_bayes_model.pkl"), "rb"))
cate_svm = pickle.load(open(os.path.join(path, "model/svm_model.pkl"), "rb"))