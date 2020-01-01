from comon.constant import local_elastic, server_elastic
import logging


class MappingElasticSearch():
    def __init__(self):
        self.mapping = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "news_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "char_filter": [
                                "html_strip"
                            ],
                            "filter": [
                                "lowercase",
                                "asciifolding"
                            ]
                        }
                    }
                }
            } ,
            "mappings": {
                "properties": {
                    "url": {
                        "type": "keyword"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "news_analyzer",
                        "search_analyzer": "news_analyzer"
                    },
                    "summary": {
                        "type": "text",
                        "analyzer": "news_analyzer",
                        "search_analyzer": "news_analyzer"
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "news_analyzer",
                        "search_analyzer": "news_analyzer"
                    },
                    "source": {
                        "type": "keyword"
                    },
                    "images": {
                        "type": "keyword"
                    },
                    "published_date": {
                        "type": "date"
                    },
                    "indexed_date": {
                        "type": "date"
                    }
                }
            }
        }

    def mappingIndicesToHost(self, index, host):
        response = host.indices.create(
            index=index,
            body=self.mapping,
            ignore=400
        )
        if 'acknowledged' in response:
            if response['acknowledged']:
                logging.info("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
        elif 'error' in response:
            logging.error("ERROR:", response['error']['root_cause'])
            logging.error("TYPE:", response['error']['type'])
        logging.info(response)

# if __name__ =="__main__":
#     mappingElasticSearch = MappingElasticSearch()
#     mappingElasticSearch.mappingIndicesToHost("talent-cleaned-e1", local_elastic())
