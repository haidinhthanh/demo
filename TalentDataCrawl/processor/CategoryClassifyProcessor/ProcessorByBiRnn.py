from processor.Processor import Processor
from pyvi import ViTokenizer
from copy import deepcopy
import pickle
import gensim
import numpy as np
import os
from comon.model_preload import bi_rnn
from const_path import root_path


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
        self.path = root_path
        self.bi_rnn_model = bi_rnn
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

            print(text_tokens)
            text_tf_idf = self.tf_idf_vec.transform([text_tokens])
            print(text_tf_idf.shape)
            print(text_tf_idf.toarray()[0][1000:2000])
            print(self.bi_rnn_model.predict(text_tf_idf))
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
if __name__ == "__main__":
    p = ProcessorByBiRnn()
    title = str("H\u00e0 N\u1ed9i: Ban h\u00e0nh C\u00f4ng \u0111i\u1ec7n kh\u1ea9n \u1ee9ng ph\u00f3 v\u1edbi b\u00e3o s\u1ed1 3")
    text = str("Ng\u00e0y 1/8, Ch\u1ee7 t\u1ecbch UBND TP H\u00e0 N\u1ed9i Nguy\u1ec5n \u0110\u1ee9c Chung \u0111\u00e3 k\u00fd C\u00f4ng \u0111i\u1ec7n kh\u1ea9n s\u1ed1 11/C\u0110-UBND y\u00eau c\u1ea7u c\u00e1c c\u1ea5p, ng\u00e0nh, c\u00e1c \u0111\u01a1n v\u1ecb ch\u1ee7 \u0111\u1ed9ng \u1ee9ng ph\u00f3 tr\u01b0\u1edbc di\u1ec5n bi\u1ebfn b\u1ea5t th\u01b0\u1eddng c\u1ee7a c\u01a1n b\u00e3o s\u1ed1 3")
    p.process({"title": title, "content": text})