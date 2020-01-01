from processor.Processor import Processor
from copy import deepcopy
import pickle
import gensim
from pyvi import ViTokenizer
import os


class ProcessorByNaiveBayes(Processor):
    def __init__(self):
        Processor.__init__(self)
        self.mapping = {
            0: 'irrelevant',
            1: 'related'
        }
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path = dir_path.replace("processor\\IrrelevantProcessor", "")
        self.nb_model = pickle.load(open(os.path.join(self.path, "model/NB_relevant/naive_bayes_model.pkl"), "rb"))
        self.tf_idf_vec = pickle.load(open(os.path.join(self.path, "model/NB_relevant/tf_idf_vec.pkl"), "rb"))

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
            cate_name = self.mapping[self.nb_model.predict(text_tf_idf)[0]]

            new_item["processor_irrelevant"] = cate_name
            self.num_processed += 1
            return new_item
        else:
            new_item["processor_irrelevant"] = "skipped"
            self.num_skip += 1
            return new_item
