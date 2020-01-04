from processor.Processor import Processor
import spacy
from copy import deepcopy
import os
import json
from const_path import root_path


class ProcessorBySpacyModel(Processor):
    def __init__(self):
        Processor.__init__(self)
        self.loc_data = {}
        dir_path = root_path
        self.city_nlp = spacy.load(os.path.join(dir_path, "model/city_ner"))
        self.nation_nlp = spacy.load(os.path.join(dir_path, "model/nation_ner"))
        self.province_nlp = spacy.load(os.path.join(dir_path, "model/province_ner"))
        self.initLocData()

    def process(self, item):
        new_item = deepcopy(item)
        if 'content' in item and 'title' in item:
            if 'summary' in item:
                news_info = item['title'] + "." + item['summary'] + "." + item['content']
            else:
                news_info = item['title'] + "." + item['content']
            doc_city = self.city_nlp(news_info)
            doc_nation = self.nation_nlp(news_info)
            doc_province = self.province_nlp(news_info)
            cities = []
            provinces = []
            nations = []
            for ent in doc_city.ents:
                cities.append(str(ent.text).replace("_", " "))
            for ent in doc_nation.ents:
                nations.append(str(ent.text).replace("_", " "))
            for ent in doc_province.ents:
                provinces.append(str(ent.text).replace("_", " "))
            new_item["processor_ner_loc"] = \
                {"cities": self.filterExceptionLoc(removeDuplicateFromList(cities), "cities"),
                 "provinces": self.filterExceptionLoc(removeDuplicateFromList(provinces), "provinces"),
                 "nations": self.filterExceptionLoc(removeDuplicateFromList(nations), "nations")}
            self.num_processed += 1
            return new_item
        else:
            new_item["processor_ner_loc"] = {"cities": [], "provinces": [], "nations": []}
            self.num_skip += 1
            return new_item

    def initLocData(self):
        path = os.path.join(root_path, "data_train/DataLocation")
        files = ["cities.jl", "nations.jl", "provinces.jl"]
        for file in files:
            with open(os.path.join(path, file), "r", encoding="UTF-8") as f:
                key = file.replace(".jl", "")
                data = json.load(f)
                arr_loc = data[key]
                self.loc_data[key] = arr_loc

    def filterExceptionLoc(self, arr, type_loc):
        loc = self.loc_data[type_loc]
        return [item for item in arr if item in loc]


def removeDuplicateFromList(listItems):
    return list(dict.fromkeys(listItems))
