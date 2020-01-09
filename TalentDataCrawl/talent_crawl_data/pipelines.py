import hashlib
import elasticsearch
from elasticsearch import Elasticsearch
from scrapy.utils.project import get_project_settings
from talent_crawl_data.utils.TimeUtils import get_instance_time_iso_format
from client_elasticsearch.MappingElasticSearch import MappingElasticSearch
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from comon.constant import SERVER_HOST_NAME, create_client_elastic_search, talent_crawled_index


class TalentCrawledDataPipeline(object):
    def __init__(self):
        self.settings = get_project_settings()
        if self.settings['ELASTIC_SEARCH_PORT']:
            uri = "%s:%d" % (self.settings['ELASTIC_SEARCH_SERVER'], self.settings['ELASTIC_SEARCH_PORT'])
        else:
            uri = "%s" % (self.settings['ELASTIC_SEARCH_SERVER'])
        self.es = Elasticsearch([uri])
        # self.mapES = MappingElasticSearch()

    def process_item(self, item, spider):
        if "TalentCrawledDataPipeline" in getattr(spider, 'pipelines', []):
            index_id = create_item_id(item)
            item["indexed_date"] = get_instance_time_iso_format()
            if "https://baomoi.com/404" != item['url']:
                try:
                    # self.es.index(index=self.settings['ELASTIC_SEARCH_INDEX'], id=index_id, body=dict(item))
                    host = create_client_elastic_search(SERVER_HOST_NAME)
                    host.index(index=talent_crawled_index, id=index_id, body=dict(item))
                except elasticsearch.exceptions.NotFoundError:
                    MappingElasticSearch.mappingIndicesToHost(index=self.settings['ELASTIC_SEARCH_INDEX'], host_type=SERVER_HOST_NAME)
                    ElasticSearchUtils.settingMaxResultSearch(index=self.settings['ELASTIC_SEARCH_INDEX'], host_type=SERVER_HOST_NAME, max_result= 5000000)
            return item
        else:
            pass


def create_item_id(item):
    return hashlib.md5(str(item['url']).encode('utf-8')).hexdigest()
