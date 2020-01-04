from processor.Processor import Processor
import ahocorasick
from copy import deepcopy


class ProcessorByKeyWord(Processor):
    def __init__(self):
        Processor.__init__(self)
        self.aho_cora_dict = ahocorasick.Automaton()
        self.keyword = []
        self.initialization()

    def initialization(self):
        self.keyword = ["nguyên nhân tại", "người tài xế", "người tài sản", "người” – tài khoản",
                        "người, tài xế", "người tài sắc vẹn toàn", "tài xế", "tài – người đàn ông",
                        "thiệt hại cho người, tài sản", "thiệt hại về người, tài sản", "thay người tài tình",
                        "nhân, tài", "người tài xe"]
        for index, value in enumerate(self.keyword):
            self.aho_cora_dict.add_word(value, (index, value))
        self.aho_cora_dict.make_automaton()

    def process(self, item):
        new_item = deepcopy(item)
        if 'content' in item and 'title' in item:
            if 'summary' in item:
                text = item['title'] + "." + item['summary'] + "." + item['content']
            else:
                text = item['title'] + "." + item['content']
            valid = True
            for item in self.aho_cora_dict.iter(text):
                if item:
                    valid = False
                    break
            if valid:
                new_item["processor_irrelevant"] = "related"
            else:
                new_item["processor_irrelevant"] = "irrelevant"
            self.num_processed += 1
            return new_item
        else:
            new_item["processor_irrelevant"] = "skipped"
            self.num_skip += 1
            return new_item
