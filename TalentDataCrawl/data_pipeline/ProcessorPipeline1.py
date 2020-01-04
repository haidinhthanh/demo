import hashlib
import json
import elasticsearch
from elasticsearch import helpers
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from client_elasticsearch.MappingElasticSearch import MappingElasticSearch
from processor.IrrelevantProcessor.ProcessorByKeyWord import ProcessorByKeyWord
from processor.DuplicateProcessor.ProcessorByTFIDF import ProcessorByTFIDF
from processor.LocationExtractProcessor.ProcessorBySpacyModel import ProcessorBySpacyModel
from processor.CategoryClassifyProcessor.ProcessorByBiRnn import ProcessorByBiRnn
from processor.TalentInfoProcessor.ProcessorByKeyAndPattern import ProcessorByKeyAndPattern
from talent_crawl_data.utils.TimeUtils import get_instance_time_iso_format
from comon.constant import local_elastic, server_elastic, LOCAL_HOST_NAME
import time
import gc


class ProcessorPipeline1:
    def __init__(self):
        self.name = "data pipeline 1"
        self.elastic_search_index = "talent-cleaned-e1"
        processor_irrelevant_keyword = ProcessorByKeyWord()
        processor_duplicate_tf_idf = ProcessorByTFIDF("talent-cleaned-e1")
        processor_ner_spacy_model = ProcessorBySpacyModel()
        processor_cate_classify = ProcessorByBiRnn()
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


