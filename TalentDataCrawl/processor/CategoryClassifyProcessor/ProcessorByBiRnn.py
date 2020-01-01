from processor.Processor import Processor
from pyvi import ViTokenizer
from copy import deepcopy
import pickle
import gensim
import numpy as np
import os
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from comon.constant import local_elastic

class ProcessorByBiRnn(Processor):
    def __init__(self):
        Processor.__init__(self)
        self.mapping = {
            0: 'Công nghệ',
            1: 'Giáo dục',
            2: 'Giải trí',
            3: 'Khoa học',
            4: 'Kinh tế',
            5: 'Pháp luật',
            6: 'Thế giới',
            7: 'Thể thao',
            8: 'Văn hóa',
            9: 'Xã hội',
            10: 'Y tế'
        }
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path = dir_path.replace("processor\\CategoryClassifyProcessor", "")
        self.bi_rnn_model = pickle.load(open(os.path.join(self.path, "model/bi_rnn_model.pkl"), "rb"))
        self.tf_idf_vec = pickle.load(open(os.path.join(self.path, "model/tf_idf_vec.pkl"), "rb"))

    def process(self, item):
        new_item = deepcopy(item)
        if 'content' in item and 'title' in item:
            if 'summary' in item:
                text = item['title'] + "." + item['summary'] + "." + item['content']
            else:
                text = item['title'] + "." + item['content']
            text = gensim.utils.simple_preprocess(text)
            text = ' '.join(text)
            text_tokens = ViTokenizer.tokenize(text)
            text_tf_idf = self.tf_idf_vec.transform([text_tokens])
            predict = self.bi_rnn_model.predict(text_tf_idf)[0]

            max_element = np.amax(predict)
            result = np.where(predict == max_element)
            cate_name = self.mapping[result[0][0]]
            new_item["processor_category_classify"] = cate_name
            self.num_processed += 1
            return new_item
        else:
            new_item["processor_category_classify"] = "skipped"
            self.num_skip += 1
            return new_item


