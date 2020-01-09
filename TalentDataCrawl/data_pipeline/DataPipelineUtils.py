from const_path import root_path
from comon.constant import create_client_elastic_search
import elasticsearch
from elasticsearch import helpers
import time
import gc
import json
from client_elasticsearch.MappingElasticSearch import MappingElasticSearch
import hashlib
from talent_crawl_data.utils.TimeUtils import get_instance_time_iso_format
import os

def create_index(index, index_id, new_item, host_type, logger):
    try:
        server_elastic_search = create_client_elastic_search(host_type)
        if not server_elastic_search.indices.exists(index=index):
            MappingElasticSearch.mappingIndicesToHost(index, host_type)
        actions = []
        doc = {
            '_index': index,
            '_id': index_id,
            '_source': dict(new_item)
        }
        actions.append(doc)
        helpers.bulk(server_elastic_search, actions, chunk_size=1000, request_timeout=200)
        time.sleep(3)
        logger.info("index success" + json.dumps(new_item))
        del server_elastic_search
        del doc
        del actions
        gc.collect()
    except elasticsearch.exceptions.NotFoundError:
        logger.error("Not found index" + str(index) + "in host" + str(host_type))


def process_news(item, pipeline, host_type, logger):
    name_file = pipeline.name
    index = pipeline.elastic_search_index
    new_item = pipeline.process(item)
    if "processor_irrelevant" in new_item and "processor_duplicate" in new_item:
        if new_item["processor_irrelevant"] == "related" and new_item["processor_duplicate"] == "not duplicate":
            logger.info("indexing......." + json.dumps(new_item))
            index_id = hashlib.md5(str(new_item['url']).encode('utf-8')).hexdigest()
            new_item["indexed_date"] = get_instance_time_iso_format()
            create_index(index, index_id, new_item, host_type, logger)
        else:
            logger.info("not index " + json.dumps(new_item))
            logger.info("not indexing because not valid.............")
    else:
        logger.info("not index " + json.dumps(new_item))
        logger.info("not indexing because not enough field.............")
    writeProcessedData(name_file, new_item)
    logger.info("==================================================================================================")
    return new_item


def writeProcessedData(file, new_item):
    with open(os.path.join(root_path, "data_pipeline/" + file + ".json"), "r", encoding="UTF-8") as f:
        data = json.load(f)
        data["data_processed"].append(new_item)
        f.close()
    with open(os.path.join(root_path, "data_pipeline/" + file + ".json"), "w", encoding="UTF-8") as f:
        json.dump(data, f)
        f.close()
