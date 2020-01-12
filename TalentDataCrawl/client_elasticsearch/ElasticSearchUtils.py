from client_elasticsearch.MappingElasticSearch import MappingElasticSearch
from comon.constant import create_client_elastic_search, SERVER_HOST_NAME,LOCAL_HOST_NAME


class ElasticSearchUtils:
    @staticmethod
    def createIndex(index, host):
        host.indices.create(index=index, ignore=400)

    @staticmethod
    def deleteIndex(index, host):
        host.indices.delete(index=index, ignore=[400, 404])

    # 2015-01-01 00:00:00 now-1d/d
    @staticmethod
    def getNumOfCrawledNewsInOneDay(host_type, index):
        host = create_client_elastic_search(host_type)
        body = {
            "query": {
                "range": {
                    "indexed_date": {
                        "gte": "now-1d/d",
                        "lte": "now/d"
                    }
                }
            }
        }
        res = host.count(index=index, body=body)
        return res['count']

    @staticmethod
    def getCrawledNewsFormHostInOneDay(host_type, index, from_value, size_value):
        host = create_client_elastic_search(host_type)
        crawled_news = []
        res = host.search(index=index,
                          body={"query": {
                              "range": {
                                  "indexed_date": {
                                      "gte": "now-1d/d",
                                      "lte": "now/d"
                                  }
                              }
                          },
                              "size": size_value,
                              "from": from_value})
        for hit in res['hits']['hits']:
            crawled_news.append(hit)
        return crawled_news

    @staticmethod
    def sendCrawledNewsFromHostToHost(from_host_type, to_host_type, from_index, to_index, logger):
        from_host = create_client_elastic_search(from_host_type)
        to_host = create_client_elastic_search(to_host_type)
        if from_host.indices.exists(index=from_index):
            crawled_news = ElasticSearchUtils.getAllNewsFromHostInOneDay(from_index, from_host_type)
            if not to_host.indices.exists(index=to_index):
                MappingElasticSearch.mappingIndicesToHost(to_index, to_host_type)
                ElasticSearchUtils.settingMaxResultSearch(to_index, to_host_type, 5000000)
            for hit in crawled_news:
                if 'images' in hit['_source']:
                    hit['_source']['images'] = [item for item in hit['_source']['images'] if len(item) < 2000]
                res = to_host.index(index=to_index, id=hit['_id'], body=hit['_source'])
                print(res)
                # logger.info("Indexed chosen news data processed " + str(res))
        else:
            pass
            # logger.error(from_index + "not exist in host" + from_host)

    @staticmethod
    def getNODocOfIndex(host_type, index):
        host = create_client_elastic_search(host_type)
        res = host.count(index=index)
        return res["count"]

    @staticmethod
    def getAllNewsFromHostInOneDay(index, host_type):
        no_crawled_news = ElasticSearchUtils.getNumOfCrawledNewsInOneDay(host_type, index)
        from_new_index = 0
        size_new_index = 100
        crawled_news = []
        while True:
            if from_new_index > no_crawled_news:
                break
            crawled_new = ElasticSearchUtils.getCrawledNewsFormHostInOneDay(host_type, index,
                                                                            from_new_index, size_new_index)
            if not crawled_new:
                break
            crawled_news += crawled_new
            from_new_index += size_new_index
        return crawled_news

    @staticmethod
    def settingMaxResultSearch(index, host_type, max_result):
        host = create_client_elastic_search(host_type)
        body = {
            "index": {
                "max_result_window": max_result
            }
        }
        host.indices.put_settings(index=index,
                                  body=body)

    @staticmethod
    def getAllTalentNewsFromHost(host_type, index):
        try:
            from_value = 0
            size_value = 100
            crawled_news = []
            host = create_client_elastic_search(host_type)
            while True:
                res = host.search(index=index,
                                  body={"query": {"match_all": {}},
                                        "size": size_value,
                                        "from": from_value})
                if not res['hits']['hits']:
                    break
                for hit in res['hits']['hits']:
                    crawled_news.append(hit)
                from_value = from_value + size_value
            return crawled_news
        except Exception:
            MappingElasticSearch.mappingIndicesToHost(index=index,
                                                      host_type=host_type)
            ElasticSearchUtils.settingMaxResultSearch(index=index,
                                                      host_type=host_type, max_result=5000000)
            return []

#
# if __name__ == "__main__":
#     # ElasticSearchUtils.settingMaxResultSearch(index="talent-crawled", host_type=LOCAL_HOST_NAME,
#     #                                           max_result=5000000)
# #
#     ElasticSearchUtils.sendCrawledNewsFromHostToHost(from_host_type=LOCAL_HOST_NAME, to_host_type=SERVER_HOST_NAME,
#                                                      from_index="talent-cleaned-e1", to_index="talent-cleaned-e1-v2",logger=None)
