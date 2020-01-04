import os
import pickle
from const_path import root_path
path = root_path
bi_rnn = pickle.load(open(os.path.join(path, "model/bi_rnn_model.pkl"), "rb"))
irr_naive_bayes = pickle.load(open(os.path.join(path, "model/NB_relevant/naive_bayes_model.pkl"), "rb"))
cate_svm = pickle.load(open(os.path.join(path, "model/svm_model.pkl"), "rb"))

# wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1WP_GQfmc1yLNYNuYD2fJV93fhVyGXVMT' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1WP_GQfmc1yLNYNuYD2fJV93fhVyGXVMT" -O svm_model.pkl && rm -rf /tmp/cookies.txt
