import ahocorasick
import re
from copy import deepcopy
from processor.Processor import Processor
from comon.constant import pattern_search, pattern_key
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from comon.constant import local_elastic
import gensim


class ProcessorByKeyAndPattern(Processor):
    def __init__(self):
        Processor.__init__(self)
        self.name = "ProcessorByKeyAndPattern_TalentInfo"
        self.keywords = ["Salary", "Environment", "Regime"]

    def process(self, item):
        new_item = deepcopy(item)
        new_item["processor_talent_info"] = {
            "Salary": [],
            "Environment": [],
            "Regime": []
        }
        if 'content' in item and 'title' in item:
            if 'summary' in item:
                text = item['title'] + "." + item['summary'] + "." + item['content']
            else:
                text = item['title'] + "." + item['content']
            keys = []
            for keyword in self.keywords:
                key = self.checkKeyWordExist(text, keyword)
                if key is not None:
                    keys.append(key)
            if keys:
                sentences = self.splitSentences(text)
                for key in keys:
                    ext_sen = self.extractSentences(sentences, key)

                    new_item["processor_talent_info"][key] += ext_sen

            self.num_processed += 1
            return new_item
        else:
            self.num_skip += 1
            return new_item

    @staticmethod
    def splitSentences(text):
        text = text.replace("\n", "")
        sentences = []
        sentence = ""
        for i in range(len(text)):
            if i == len(text) - 3:
                sentences.append(sentence)
                break
            if text[i] == '\n':
                continue
            if (text[i] == '.' and text[i + 1].isupper()) or (
                    text[i] == '.' and text[i + 1] == " " and text[i + 2].isupper()):
                sentences.append(sentence + ".")
                sentence = ""
            else:
                sentence += text[i]
        return sentences

    @staticmethod
    def checkKeyWordExist(text, keyword):
        keywords = pattern_key[keyword]
        aho_cora_dict = ahocorasick.Automaton()
        for index, value in enumerate(keywords):
            aho_cora_dict.add_word(value, (index, value))
        aho_cora_dict.make_automaton()
        valid = False
        for item in aho_cora_dict.iter(str(text).lower()):
            if item:
                valid = True
                break
        if valid:
            return keyword
        else:
            return None

    @staticmethod
    def extractSentences(sentences, key_pattern):
        ext_arr = []
        patterns = pattern_search[key_pattern]
        for pattern in patterns:
            for sentence in sentences:
                matchObj = re.search(pattern, sentence)
                if matchObj:
                    ext_str = matchObj.group()
                    ext_str = " ".join(gensim.utils.simple_preprocess(ext_str))
                    if ext_str in ext_arr:
                        continue
                    else:
                        ext_arr.append(ext_str)
        return ext_arr

    @staticmethod
    def checkExistInfoExtract(item):
        keys = dict(item["processor_talent_info"]).keys()
        for key in keys:
            if item["processor_talent_info"][key]:
                return True
        return False
