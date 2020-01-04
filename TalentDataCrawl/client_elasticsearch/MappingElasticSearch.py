import logging

from comon.constant import create_client_elastic_search


class MappingElasticSearch():
    @staticmethod
    def mappingIndicesToHost(index, host_type):
        mapping = {
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
            },
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
        host = create_client_elastic_search(host_type)
        response = host.indices.create(
            index=index,
            body=mapping,
            ignore=400
        )
        print("done")
        if 'acknowledged' in response:
            if response['acknowledged']:
                print("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
        elif 'error' in response:
            print("ERROR:", response['error']['root_cause'])
            print("TYPE:", response['error']['type'])
        print(response)

