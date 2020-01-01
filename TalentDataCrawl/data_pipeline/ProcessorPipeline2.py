import hashlib
import json
import elasticsearch
from elasticsearch import helpers
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from client_elasticsearch.MappingElasticSearch import MappingElasticSearch
from processor.IrrelevantProcessor.ProcessorByNaiveBayes import ProcessorByNaiveBayes
from processor.DuplicateProcessor.ProcessorByTFIDF import ProcessorByTFIDF
from processor.LocationExtractProcessor.ProcessorBySpacyModel import ProcessorBySpacyModel
from processor.CategoryClassifyProcessor.ProcessorBySVM import ProcessorBySVM
from processor.TalentInfoProcessor.ProcessorByKeyAndPattern import ProcessorByKeyAndPattern
from talent_crawl_data.utils.TimeUtils import get_instance_time_iso_format
from comon.constant import local_elastic, server_elastic
import time
import gc


class ProcessorPipeline2:
    def __init__(self):
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


def create_index(index, index_id, new_item):
    try:
        actions = []
        doc = {
            '_index': index,
            '_id': index_id,
            '_source': dict(new_item)
        }
        actions.append(doc)
        server_elastic_search = local_elastic()
        helpers.bulk(server_elastic_search, actions, chunk_size=1000, request_timeout=200)
        time.sleep(3)
        del server_elastic_search
        del doc
        del actions
        gc.collect()
    except elasticsearch.exceptions.NotFoundError:
        mappingElasticSearch = MappingElasticSearch()
        mappingElasticSearch.mappingIndicesToHost(index=index, host=local_elastic())


def process_news(item, pipeline):
    print("runing process")
    new_item = pipeline.process(item)
    print(new_item)
    if "processor_irrelevant" in new_item and "processor_duplicate" in new_item:
        if new_item["processor_irrelevant"] == "related" and new_item["processor_duplicate"] == "not duplicate":
            print("indexing..................")
            index_id = hashlib.md5(str(new_item['url']).encode('utf-8')).hexdigest()
            new_item["indexed_date"] = get_instance_time_iso_format()
            # server_elastic().index(index="talent-cleaned-e1", id=index_id, body=dict(new_item))
            create_index("talent-cleaned-e2", index_id, new_item)
        else:
            print("not indexing because not valid.............")
    else:
        print("not indexing because not enough field.............")
    print("==================================================================================================")
    return new_item

# def writeToFileJson(new_item):
#     with open("data_processed.json", "r") as f:
#         data = json.load(f)
#         data["data"].append(new_item)
#     f.close()
#     with open("data_processed.json", "w") as f:
#         json.dump(data, f)
#     f.close()
#
# def readFileJson():
#     with open("data_processed.json", "r") as f:
#         data = json.load(f)
#     f.close()
#     return data["data"]


if __name__ == "__main__":
    # no_crawled_news = ElasticSearchUtils.getNumOfCrawledNewsInOneDay(local_elastic(), "talent-crawled")
    no_crawled_news = ElasticSearchUtils.getNODoc(local_elastic(), "talent-crawled")
    print(no_crawled_news)
    from_new_index = 0
    size_new_index = 100

    crawled_news = []
    while True:
        if from_new_index > no_crawled_news:
            break
        crawled_new = ElasticSearchUtils.getCrawledNewsFormHostInOneDay(local_elastic(), "talent-crawled",
                                                                        from_new_index, size_new_index)
        if not crawled_new:
            break
        crawled_news += crawled_new
        from_new_index += size_new_index
    # run through processor
    crawled_source_news = [item["_source"] for item in crawled_news]
    i = 0
    try:
        while True:
            pipeline = ProcessorPipeline2()
            processed_items = []
            if i > len(crawled_source_news):
                for item in crawled_source_news[i-10:len(crawled_source_news)]:
                    print("Running: " + str(crawled_source_news.index(item)))
                    new_item = process_news(item, pipeline)
                    processed_items.append(item)
                print("size processed data", len(processed_items))
                clean_news = [item for item in processed_items
                              if ("processor_irrelevant" in item and "processor_duplicate" in item
                                  and item["processor_irrelevant"] == "related"
                                  and item["processor_duplicate"] == "not duplicate")]
                print("size clean data: ", len(clean_news))
                print('Pipeline stats:\n', json.dumps(pipeline.stats(), indent=2))
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                del pipeline
                del clean_news
                del processed_items
                del new_item
                gc.collect()
                break
            else:
                for item in crawled_source_news[i:i+10]:
                    print("Running: " + str(crawled_source_news.index(item)))
                    new_item = process_news(item, pipeline)
                    processed_items.append(new_item)
                print("size processed data", len(processed_items))
                clean_news = [item for item in processed_items
                              if ("processor_irrelevant" in item and "processor_duplicate" in item
                                  and item["processor_irrelevant"] == "related"
                                  and item["processor_duplicate"] == "not duplicate")]
                print("size clean data: ", len(clean_news))
                print('Pipeline stats:\n', json.dumps(pipeline.stats(), indent=2))
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                del pipeline
                del clean_news
                del processed_items
                del new_item
                gc.collect()
                i += 10
    except MemoryError:
        print("Re run")
    # i = 0
    # for item in crawled_source_news[1060:]:
    #     print("Running: " + str(crawled_source_news.index(item)))
    #     if i == 50:
    #         time.sleep(600)
    #         i = 0
    #     new_item = pipeline.process(item)
    #     processed_items.append(new_item)
    #     if "processor_irrelevant" in new_item and "processor_duplicate" in new_item:
    #         if new_item["processor_irrelevant"] == "related" and new_item["processor_duplicate"] == "not duplicate":
    #             print("indexing..................")
    #             index_id = hashlib.md5(str(new_item['url']).encode('utf-8')).hexdigest()
    #             new_item["indexed_date"] = get_instance_time_iso_format()
    #             server_elastic().index(index="talent-cleaned-e1", id=index_id, body=dict(new_item))
    #             time.sleep(5)
    #         else:
    #             print(new_item)
    #             print("not indexing because not valid.............")
    #     else:
    #         print("not indexing because not enough field.............")
    #     print("==================================================================================================")
    #     i += 1
    # print("size processed data", len(processed_items))
    # clean_news = [item for item in processed_items
    #                   if (item["processor_irrelevant"] == "related"
    #                       and item["processor_duplicate"] == "not duplicate")]
    # print("size clean data: ", len(clean_news))
    # print('Pipeline stats:\n', json.dumps(pipeline.stats(), indent=2))
