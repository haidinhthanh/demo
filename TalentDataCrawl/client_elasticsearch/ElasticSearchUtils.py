import logging
import elasticsearch
from elasticsearch import Elasticsearch
from comon.constant import local_elastic, server_elastic


class ElasticSearchUtils:
    @staticmethod
    def createIndex(index, host):
        host.indices.create(index=index, ignore=400)

    @staticmethod
    def deleteIndex(index, host):
        host.indices.delete(index=index, ignore=[400, 404])

    # 2015-01-01 00:00:00 now-1d/d
    @staticmethod
    def getNumOfCrawledNewsInOneDay(host, index):
        res = host.search(index=index,
                          body={"query": {
                              "range": {
                                  "indexed_date": {
                                      "gte": "2015-12-10T10:17:07Z",
                                      "lte": "now/d"
                                  }
                              }
                          }, })
        return res['hits']['total']['value']

    @staticmethod
    def getCrawledNewsFormHostInOneDay(host, index, from_value, size_value):
        crawled_news = []
        res = host.search(index=index,
                          body={"query": {
                              "range": {
                                  "indexed_date": {
                                      "gte": "2015-12-10T10:17:07Z",
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
    def getAllTalentNewsCrawledFromHost(host, index):
        from_value = 0
        size_value = 100
        crawled_news = []
        while True:
            res = host.search(index=index,
                              body={"query": {"match_all": {}},
                                    "size": size_value,
                                    "from": from_value},
                              timeout=90)
            if not res['hits']['hits']:
                break
            for hit in res['hits']['hits']:
                crawled_news.append(hit)
            from_value = from_value + size_value
        return crawled_news

    @staticmethod
    def sendCrawledNewsFromHostToHost(from_host, to_host, from_index, to_index):
        crawled_news = ElasticSearchUtils.getAllTalentNewsCrawledFromHost(from_host, from_index)
        for hit in crawled_news:
            logging.info(hit)
            res = to_host.index(index=to_index, id=hit['_id'], body=hit['_source'])
            logging.info("RESPONSE: ", res)

    @staticmethod
    def sendCleanedNewsFromHostToHost(from_host, to_host, index):
        crawled_news = ElasticSearchUtils.getAllTalentNewsCleanFromHost(from_host)
        for hit in crawled_news:
            logging.info(hit)
            res = to_host.index(index=index, id=hit['_id'], body=hit['_source'])
            logging.info("RESPONSE: ", res)

    @staticmethod
    def getAllTalentNewsCleanFromHost(host, index):
        try:
            from_value = 0
            size_value = 100
            crawled_news = []
            while True:
                res = host.search(index=index,
                                  body={"query": {"match_all": {}},
                                        "size": size_value,
                                        "from": from_value}, )
                if not res['hits']['hits']:
                    break
                for hit in res['hits']['hits']:
                    crawled_news.append(hit)
                from_value = from_value + size_value
            return crawled_news
        except elasticsearch.exceptions.NotFoundError:
            ElasticSearchUtils.createIndex(index="talent-cleaned-e1", host=host)
        return []

    @staticmethod
    def getNODoc(host, index):
        res = host.count(index=index)
        return res["count"]

    @staticmethod
    def getAllDocFromIndexAndHost(index, host):
        pass
#
# if __name__ == "__main__":
#     elasticSearchUtils = ElasticSearchUtils()
#     count = elasticSearchUtils.getNODoc(local_elastic(), "talent-crawled")
#     elasticSearchUtils.sendCrawledNewsFromHostToHost(local_elastic, sever_elastic(), "talent-crawled", "talent-crawled")
#
