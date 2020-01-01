import hashlib
import json
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from client_elasticsearch.MappingElasticSearch import MappingElasticSearch
from processor.IrrelevantProcessor.ProcessorByKeyWord import ProcessorByKeyWord
from processor.DuplicateProcessor.ProcessorByTFIDF import ProcessorByTFIDF
from processor.LocationExtractProcessor.ProcessorBySpacyModel import ProcessorBySpacyModel
from processor.CategoryClassifyProcessor.ProcessorByBiRnn import ProcessorByBiRnn
from processor.TalentInfoProcessor.ProcessorByKeyAndPattern import ProcessorByKeyAndPattern
from talent_crawl_data.utils.TimeUtils import get_instance_time_iso_format
from comon.constant import local_elastic, server_elastic
import time
import gc
import tensorflow as tf


if __name__ == "__main__":
    # no_crawled_news = ElasticSearchUtils.getNumOfCrawledNewsInOneDay(local_elastic(), "talent-crawled")
    # no_crawled_news = ElasticSearchUtils.getNODoc(local_elastic(), "talent-crawled")
    # print(no_crawled_news)
    # from_new_index = 0
    # size_new_index = 100
    #
    # crawled_news = []
    # while True:
    #     if from_new_index > no_crawled_news:
    #         break
    #     crawled_new = ElasticSearchUtils.getCrawledNewsFormHostInOneDay(local_elastic(), "talent-crawled",
    #                                                                     from_new_index, size_new_index)
    #     if not crawled_new:
    #         break
    #     crawled_news += crawled_new
    #     from_new_index += size_new_index
    # # run through processor
    # crawled_source_news = [item["_source"] for item in crawled_news]
    # i = 0
    # try:
    #     while True:
    #         pipeline = ProcessorPipeline1()
    #         processed_items = []
    #         if i > len(crawled_source_news):
    #             for item in crawled_source_news[i-10:len(crawled_source_news)]:
    #                 print("Running: " + str(crawled_source_news.index(item)))
    #                 new_item = process_news(item, pipeline)
    #                 processed_items.append(item)
    #             print("size processed data", len(processed_items))
    #             clean_news = [item for item in processed_items
    #                           if ("processor_irrelevant" in item and "processor_duplicate" in item
    #                               and item["processor_irrelevant"] == "related"
    #                               and item["processor_duplicate"] == "not duplicate")]
    #             print("size clean data: ", len(clean_news))
    #             print('Pipeline stats:\n', json.dumps(pipeline.stats(), indent=2))
    #             print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #             del pipeline
    #             del clean_news
    #             del processed_items
    #             del new_item
    #             gc.collect()
    #             break
    #         else:
    #             for item in crawled_source_news[i:i+10]:
    #                 print("Running: " + str(crawled_source_news.index(item)))
    #                 new_item = process_news(item, pipeline)
    #                 processed_items.append(new_item)
    #             print("size processed data", len(processed_items))
    #             clean_news = [item for item in processed_items
    #                           if ("processor_irrelevant" in item and "processor_duplicate" in item
    #                               and item["processor_irrelevant"] == "related"
    #                               and item["processor_duplicate"] == "not duplicate")]
    #             print("size clean data: ", len(clean_news))
    #             print('Pipeline stats:\n', json.dumps(pipeline.stats(), indent=2))
    #             print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #             del pipeline
    #             del clean_news
    #             del processed_items
    #             del new_item
    #             gc.collect()
    #             i += 10
    # except MemoryError:
    #     print("Rerun")
    print(tf.__version__)