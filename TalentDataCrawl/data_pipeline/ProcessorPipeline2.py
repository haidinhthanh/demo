from processor.IrrelevantProcessor.ProcessorByNaiveBayes import ProcessorByNaiveBayes
from processor.DuplicateProcessor.ProcessorByTFIDF import ProcessorByTFIDF
from processor.LocationExtractProcessor.ProcessorBySpacyModel import ProcessorBySpacyModel
from processor.CategoryClassifyProcessor.ProcessorBySVM import ProcessorBySVM
from processor.TalentInfoProcessor.ProcessorByKeyAndPattern import ProcessorByKeyAndPattern


class ProcessorPipeline2:
    def __init__(self):
        self.name = "data pipeline 2"
        self.elastic_search_index = "talent-cleaned-e2"
        processor_irrelevant_keyword = ProcessorByNaiveBayes()
        processor_duplicate_tf_idf = ProcessorByTFIDF("talent-cleaned-e2")
        processor_ner_spacy_model = ProcessorBySpacyModel()
        processor_cate_classify = ProcessorBySVM()
        processor_talent_info = ProcessorByKeyAndPattern()
        self.processors = [
            processor_irrelevant_keyword,
            processor_duplicate_tf_idf,
            processor_ner_spacy_model,
            processor_cate_classify,
            processor_talent_info
        ]

    def process(self, item):
        for processor in self.processors:
            item = processor.process(item)
        return item

    def stats(self):
        stats = {}
        for processor in self.processors:
            stats[processor.name] = processor.stats()
        return stats

