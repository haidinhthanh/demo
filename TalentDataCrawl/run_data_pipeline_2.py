from comon.constant import talent_crawled_index
import json
import gc
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from data_pipeline.ProcessorPipeline2 import ProcessorPipeline2
from data_pipeline.DataPipelineUtils import process_news
from comon.constant import LOCAL_HOST_NAME
from log.log_service import LogService

if __name__ == "__main__":
    crawled_news = ElasticSearchUtils.getAllNewsFromHostInOneDay(talent_crawled_index, LOCAL_HOST_NAME)
    pipeline_name = "data pipeline 2"
    crawled_source_news = [item['_source'] for item in crawled_news]
    host_type = LOCAL_HOST_NAME
    i = 0
    no_news_input = len(crawled_source_news)
    no_news_process = 0
    no_news_clean = 0
    try:
        logger = LogService().configLogDataPipelineProcessData(pipeline_name)
        while True:
            pipeline = ProcessorPipeline2()
            processed_items = []
            if i > len(crawled_source_news):
                for item in crawled_source_news[i - 10:len(crawled_source_news)]:
                    print("Running: " + str(crawled_source_news.index(item)))
                    new_item = process_news(item, pipeline, host_type, logger)
                    processed_items.append(item)
                no_news_process += len(processed_items)
                print("size processed data", len(processed_items))
                clean_news = [item for item in processed_items
                              if ("processor_irrelevant" in item and "processor_duplicate" in item
                                  and item["processor_irrelevant"] == "related"
                                  and item["processor_duplicate"] == "not duplicate")]
                no_news_clean += len(clean_news)
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
                for item in crawled_source_news[i:i + 5]:
                    print("Running: " + str(crawled_source_news.index(item)))
                    new_item = process_news(item, pipeline, host_type, logger)
                    processed_items.append(new_item)
                no_news_process += len(processed_items)
                print("size processed data", len(processed_items))
                clean_news = [item for item in processed_items
                              if ("processor_irrelevant" in item and "processor_duplicate" in item
                                  and item["processor_irrelevant"] == "related"
                                  and item["processor_duplicate"] == "not duplicate")]
                no_news_clean += len(clean_news)
                print("size clean data: ", len(clean_news))
                print('Pipeline stats:\n', json.dumps(pipeline.stats(), indent=2))
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                break
                del pipeline
                del clean_news
                del processed_items
                del new_item
                gc.collect()
                i += 5
        logger = LogService().configLogDataPipelineSummary(pipeline_name)
        logger.info("number of crawled news in day :" + str(no_news_input))
        logger.info("number of crawled news processed :" + str(no_news_process))
        logger.info("number of cleaned news processed :" + str(no_news_clean))
    except MemoryError:
        print("Re run")

