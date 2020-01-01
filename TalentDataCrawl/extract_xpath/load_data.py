from pyvi import ViTokenizer
from tqdm import tqdm
import gensim
import os
import pickle


def load_data_train():
    x_data = pickle.load(open('x_data.pkl', 'rb'))
    y_data = pickle.load(open('y_data.pkl', 'rb'))
    x_test = pickle.load(open('x_test.pkl', 'rb'))
    y_test = pickle.load(open('y_test.pkl', 'rb'))
    return x_data, y_data, x_test, y_test



def get_data(folder_path):
    X = []
    y = []
    dirs = os.listdir(folder_path)
    for path in tqdm(dirs):
        file_paths = os.listdir(os.path.join(folder_path, path))
        for file_path in tqdm(file_paths):
            with open(os.path.join(folder_path, path, file_path), 'r', encoding="utf-8") as f:
                lines = f.readlines()
                lines = ' '.join(lines)
                lines = gensim.utils.simple_preprocess(lines)  # xóa các ký tự đặc biệt
                lines = ' '.join(lines)
                lines = ViTokenizer.tokenize(lines)  # tách từ văn bản tiếng Việt
                X.append(lines)
                y.append(path)
    return X, y


# if __name__ == "__main__":
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     train_path = os.path.join(dir_path, "data_train/Train/Train_Full")
#     test_path = os.path.join(dir_path, "data_train/Test/Test_Full")
#
#     output_train_path_x = os.path.join(dir_path, "data_train/x_data.pkl")
#     output_train_path_y = os.path.join(dir_path, "data_train/y_data.pkl")
#     output_test_path_x = os.path.join(dir_path, "data_train/x_test.pkl")
#     output_test_path_y = os.path.join(dir_path, "data_train/y_test.pkl")
#
#     x_data, y_data = get_data(train_path)
#     pickle.dump(x_data, open(output_train_path_x, 'wb'))
#     pickle.dump(y_data, open(output_train_path_y, 'wb'))
#
#     x_data, y_data = get_data(test_path)
#     pickle.dump(x_data, open(output_test_path_x, 'wb'))
#     pickle.dump(y_data, open(output_test_path_y, 'wb'))
if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    train_path = os.path.join(dir_path, "Train")
    test_path = os.path.join(dir_path, "Test")

    output_train_path_x = os.path.join(dir_path, "x_data.pkl")
    output_train_path_y = os.path.join(dir_path, "y_data.pkl")
    output_test_path_x = os.path.join(dir_path, "x_test.pkl")
    output_test_path_y = os.path.join(dir_path, "y_test.pkl")

    x_data, y_data = get_data(train_path)
    pickle.dump(x_data, open(output_train_path_x, 'wb'))
    pickle.dump(y_data, open(output_train_path_y, 'wb'))

    x_data, y_data = get_data(test_path)
    pickle.dump(x_data, open(output_test_path_x, 'wb'))
    pickle.dump(y_data, open(output_test_path_y, 'wb'))
