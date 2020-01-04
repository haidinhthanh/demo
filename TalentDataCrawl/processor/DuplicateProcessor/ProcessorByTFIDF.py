from processor.Processor import Processor
import re
from pyvi import ViTokenizer
from py_stringmatching.similarity_measure.soft_tfidf import SoftTfIdf
import math
from copy import deepcopy
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from comon.constant import LOCAL_HOST_NAME, SERVER_HOST_NAME
import gc


class ProcessorByTFIDF(Processor):
    def __init__(self,  index_elasic, num_of_fields=3, jaccard_measure=0.8, similarity_threshold=0.9):
        Processor.__init__(self)
        self.num_of_fields = num_of_fields
        self.jaccard_measure = jaccard_measure
        self.similarity_threshold = similarity_threshold
        self.clean_news_normalize = []
        self.clean_news_index = []
        self.soft_tf_idf = []
        self.index = index_elasic
        self.last_size = -1

    def process(self, item):
        self.initialization()
        new_item = deepcopy(item)
        if self.clean_news_normalize:
            print("check duplicate")
            if 'content' in item and 'title' in item:
                if 'summary' in item:
                    new = [item["title"],
                           item["summary"],
                           item["content"]]
                else:
                    new = [item["title"],
                           item["title"],
                           item["content"]]
                match = self.is_match(new)
                if match:
                    print("Duplicated")
                    new_item["processor_duplicate"] = "duplicate"
                else:
                    new_item["processor_duplicate"] = "not duplicate"
                self.num_processed += 1
                return new_item
            else:
                new_item["processor_duplicate"] = "skipped"
                self.num_skip += 1
                return new_item
        else:
            new_item["processor_duplicate"] = "not duplicate"
            self.num_processed += 1
            return new_item

    def is_match(self, check_new):
        # normalize check_new field
        check_new_normalize = [self.word_normalize(self.word_split(field)) for field in check_new]

        # size filtering
        clean_news_size_filtering = self.size_filtering(check_new_normalize, self.clean_news_normalize)
        # position filtering
        clean_news_candidates = self.position_filtering(check_new_normalize, clean_news_size_filtering)
        # check match
        flag = False  # flag check if check new match in clean news
        for new in clean_news_candidates:
            inner_flag = True
            for i in range(self.num_of_fields):
                if self.soft_tf_idf[i].get_raw_score(check_new_normalize[i], new[i]) < self.similarity_threshold:
                    inner_flag = False
                    break
                # print("DUPLICATE______________________________________________________________")
                # print(new)
                # print(check_new_normalize)
                # print("DUPLICATE______________________________________________________________")
            if inner_flag:
                flag = True

        return flag

    def initialization(self):
        server_elastic_search = LOCAL_HOST_NAME
        clean_news_search = ElasticSearchUtils.getAllTalentNewsFromHost(server_elastic_search, self.index)
        if self.last_size != len(clean_news_search):
            self.last_size = len(clean_news_search)
            clean_news = []
            for item in clean_news_search:
                if "summary" in item["_source"].keys():
                    clean_news.append([item["_source"]["title"], item["_source"]["summary"], item["_source"]["content"]])
                else:
                    clean_news.append([item["_source"]["title"], item["_source"]["title"], item["_source"]["content"]])
            for new in clean_news:
                new_split = []
                for i in range(self.num_of_fields):
                    new_split.append(self.word_normalize(self.word_split_content(new[i])))
                self.clean_news_normalize.append(new_split)
            # Build index
            clean_news_fields = [[] for i in range(self.num_of_fields)]
            for new_normalize in self.clean_news_normalize:
                for i in range(self.num_of_fields):
                    clean_news_fields[i].append(new_normalize[i])
            for i in range(self.num_of_fields):
                self.clean_news_index.append(self.invert_index(clean_news_fields[i]))
            # Soft TF/IDF models
            for i in range(self.num_of_fields):
                self.soft_tf_idf.append(SoftTfIdf(clean_news_fields[i]))

    @staticmethod
    def word_split(sentence):
        return re.compile("[\\w_]+").findall(ViTokenizer.tokenize(sentence, ))

    @staticmethod
    def word_normalize(sentence):
        return [word.lower() for word in sentence]

    @staticmethod
    def invert_index(sentences_list):
        inverted = {}
        for index, sentences in enumerate(sentences_list):
            for word in sentences:
                locations = inverted.setdefault(word, [])
                locations.append(index)
        return inverted

    def size_filtering(self, check_new, clean_news_normalize):
        up_bound = [len(field) / self.jaccard_measure for field in check_new]
        down_bound = [len(field) * self.jaccard_measure for field in check_new]
        clean_news_size_filtering = []

        for new in clean_news_normalize:
            flag = True
            for i in range(self.num_of_fields):
                flag &= down_bound[i] <= len(new[i]) <= up_bound[i]
            if flag:
                clean_news_size_filtering.append(new)

        return clean_news_size_filtering

    def calc_prefix(self, check_new, compare_new):
        prefix_overlap = math.ceil(
            (self.jaccard_measure / (self.jaccard_measure + 1)) * (len(check_new) + len(compare_new)))
        if len(check_new) >= prefix_overlap and len(compare_new) >= prefix_overlap:
            return compare_new, prefix_overlap
        return None

    def position_filtering(self, check_new, clean_news):
        # Calc an array of tuple (clean_new, prefix) of clean_news
        clean_news_prefix = []
        ids = []

        for index, clean_new in enumerate(clean_news):
            flag_choose = True
            prefix = []
            for j in range(self.num_of_fields):
                p = self.calc_prefix(check_new[j], clean_new[j])
                prefix.append(p)
                if p is None:
                    flag_choose = False
            if flag_choose:
                clean_news_prefix.append(prefix)
                ids.append(index)

        # Calculate array of
        # clean_news_sorted_prefix = clean_news_prefix[len(clean_news_prefix) - prefix_filtering + 1]
        #                               sorted by frequency and min_prefix
        clean_news_sorted_prefix = []
        min_prefix = [10000 for i in range(self.num_of_fields)]
        for new_prefix in clean_news_prefix:
            new_sorted_prefix = []
            for i in range(self.num_of_fields):
                new_sorted_prefix.append(self.sort_by_frequency(self.clean_news_index[i], new_prefix[i][0])[
                                         :len(new_prefix[i][0]) - new_prefix[i][1] + 1])
                if new_prefix[i][1] < min_prefix[i]:
                    min_prefix[i] = new_prefix[i][1]

            clean_news_sorted_prefix.append(new_sorted_prefix)

        # Build inverted index of clean_news_sorted_prefix
        clean_news_sorted_prefix_index = []
        for i in range(self.num_of_fields):
            clean_news_sorted_prefix_index.append(self.invert_index([new[i] for new in clean_news_sorted_prefix]))

        # Sort check_new by frequency
        check_new_sorted = []
        for i in range(self.num_of_fields):
            check_new_sorted.append(self.sort_by_frequency(self.clean_news_index[i], check_new[i]))

        # Ids of clean_news_sorted_prefix satisfied
        clean_news_filtered_id = []

        for i in range(self.num_of_fields):
            filter_id = []
            for new_i in check_new_sorted[i][:len(check_new_sorted[i]) - min_prefix[i] + 1]:
                id_match = clean_news_sorted_prefix_index[i].get(new_i)
                if id_match is not None:
                    filter_id += id_match
            clean_news_filtered_id.append(filter_id)

        # set of ids clean_news_sorted_prefix satisfied
        clean_news_set_id = set(clean_news_filtered_id[0])
        for new_filter_id in clean_news_filtered_id[1:]:
            clean_news_set_id.intersection_update(new_filter_id)

        return [clean_news[ids[i]] for i in clean_news_set_id]

    @staticmethod
    def sort_by_frequency(inverted_index, arr):
        return sorted(arr,
                      key=lambda arr_i: len(inverted_index.get(arr_i) if inverted_index.get(arr_i) is not None else []))

    def word_split_content(self, content):
        sentences = str(content).split(".")
        words_of_sentences = [self.word_split(sentence) for sentence in sentences]
        words_content = []
        for words in words_of_sentences:
            words_content = words_content + words
        return words_content
