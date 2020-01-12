from comon.constant import talent_crawled_index
import json
import gc
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from data_pipeline.ProcessorPipeline1 import ProcessorPipeline1
from data_pipeline.DataPipelineUtils import process_news
from comon.constant import LOCAL_HOST_NAME, SERVER_HOST_NAME
from log.log_service import LogService

if __name__ == "__main__":
    crawled_news = ElasticSearchUtils.getAllNewsFromHostInOneDay(talent_crawled_index, SERVER_HOST_NAME)
    pipeline_name = "data pipeline 1"
    crawled_source_news = [item['_source'] for item in crawled_news]
    host_type = SERVER_HOST_NAME
    i = 0
    no_news_input = len(crawled_source_news)
    no_news_process = 0
    no_news_clean = 0
    try:
        logger = LogService().configLogDataPipelineProcessData(pipeline_name)
        logger.info("Total news crawled today :" + str(len(crawled_news)))
        while True:
            pipeline = ProcessorPipeline1()
            processed_items = []
            if i > len(crawled_source_news):
                for item in crawled_source_news[i -3:len(crawled_source_news)]:
                    logger.info("Process url: " + str(item["url"]))
                    new_item = process_news(item, pipeline, host_type, logger)
                    processed_items.append(item)
                no_news_process += len(processed_items)
                logger.info("size processed data" + str(len(processed_items)))
                clean_news = [item for item in processed_items
                              if ("processor_irrelevant" in item and "processor_duplicate" in item
                                  and item["processor_irrelevant"] == "related"
                                  and item["processor_duplicate"] == "not duplicate")]
                no_news_clean += len(clean_news)
                logger.info("size clean data: " + str(len(clean_news)))
                logger.info('Pipeline stats:\n' + json.dumps(pipeline.stats()))
                logger.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                del pipeline
                del clean_news
                del processed_items
                del new_item
                gc.collect()
                break
            else:
                for item in crawled_source_news[i:i + 3]:
                    logger.info("Process url: " + str(item["url"]))
                    new_item = process_news(item, pipeline, host_type, logger)
                    processed_items.append(new_item)
                no_news_process += len(processed_items)
                logger.info("size processed data" + str(len(processed_items)))
                clean_news = [item for item in processed_items
                              if ("processor_irrelevant" in item and "processor_duplicate" in item
                                  and item["processor_irrelevant"] == "related"
                                  and item["processor_duplicate"] == "not duplicate")]
                no_news_clean += len(clean_news)
                logger.info("size clean data: " + str(len(clean_news)))
                logger.info('Pipeline stats:\n' + json.dumps(pipeline.stats()))
                logger.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                del pipeline
                del clean_news
                del processed_items
                del new_item
                gc.collect()
                i += 3
        logger = LogService().configLogDataPipelineSummary(pipeline_name)
        logger.info("number of crawled news in day :" + str(no_news_input))
        logger.info("number of crawled news processed :" + str(no_news_process))
        logger.info("number of cleaned news processed :" + str(no_news_clean))
    except MemoryError:
        print("Re run")

