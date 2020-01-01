# import spacy
# from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
# nlp = spacy.load("model/city_ner")
# nlp1 = spacy.load("model/nation_ner")
# nlp2 = spacy.load("model/province_ner")
#
# news = ElasticSearchUtils.getAllTalentNewsCrawledFromLocalHost()
# print(len(news))
# # titles = [item for item in news if item["_source"]["url"] == "https://baomoi.com/binh-duong-chu-trong-dao-tao-nang-cao-phat-trien-nguon-nhan-luc/c/25864465.epi"]
# # item = titles[0]["_source"]
# # print(item)
# for item in news:
#     print("run")
#     if 'content' in item["_source"] and 'title' in item["_source"] and 'summary' in item["_source"]:
#         text = item["_source"]['title']+item["_source"]['summary']+item["_source"]['content']
#         doc = nlp(text)
#         for ent in doc.ents:
#             print(ent.text, ent.start_char, ent.end_char, ent.label_)
#         doc = nlp1(text)
#         for ent in doc.ents:
#             print(ent.text, ent.start_char, ent.end_char, ent.label_)
#         doc = nlp2(text)
#         for ent in doc.ents:
#             print(ent.text, ent.start_char, ent.end_char, ent.label_)
#         print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

import pickle
import gensim
import numpy as np
from pyvi import ViTokenizer

# mapping = {
#     0: 'Công nghệ',
#     1: 'Giáo dục',
#     2: 'Giải trí',
#     3: 'Khoa học',
#     4: 'Kinh tế',
#     5: 'Pháp luật',
#     6: 'Thế giới',
#     7: 'Thể thao',
#     8: 'Văn hóa',
#     9: 'Xã hội',
#     10: 'Y tế'
# }
# print("start")
# nb_model = pickle.load(open("model/naive_bayes_model.pkl", "rb"))
# with open("text.txt", 'r', encoding="utf-8") as f:
#     lines = f.readlines()
#     lines = ' '.join(lines)
#     lines = gensim.utils.simple_preprocess(lines)  # xóa các ký tự đặc biệt
#     lines = ' '.join(lines)
#     text = ViTokenizer.tokenize(lines)
# print("process")
# tf_idf_vec = pickle.load(open("model/tf_idf_vec.pkl", "rb"))
# text_tf_idf = tf_idf_vec.transform([text])
#
# print("Result:")
# predict =nb_model.predict(text_tf_idf)
# print(predict)
# maxElement = np.amax(predict)
# result = np.where(predict == maxElement)
# print(maxElement)
# print(mapping[result[0][0]])
# print(mapping[nb_model.predict(text_tf_idf)[0]])


# mapping = {
#     0: "Irrelevant",
#     1: "Relevant"
# }
# print("start")
# nb_model = pickle.load(open("model/NB_relevant/naive_bayes_model.pkl", "rb"))
# with open("test.txt", 'r', encoding="UTF-8") as f:
#     lines = f.readlines()
#     lines = ' '.join(lines)
#     lines = gensim.utils.simple_preprocess(lines)  # xóa các ký tự đặc biệt
#     lines = ' '.join(lines)
#     text = ViTokenizer.tokenize(lines)
# print(text)
# print("process")
# tf_idf_vec = pickle.load(open("model/NB_relevant/tf_idf_vec.pkl", "rb"))
# text_tf_idf = tf_idf_vec.transform([text])
# print(type(text_tf_idf))
#
# predict =nb_model.predict(text_tf_idf)[0]
# print("Result:" + mapping[predict])

# maxElement = np.amax(predict)
# result = np.where(predict == maxElement)
# print(maxElement)
# print(mapping[result[0][0]])
# print(mapping[nb_model.predict(text_tf_idf)[0]])
print("1234567")