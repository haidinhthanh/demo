from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from comon.constant import root_path, pipeline_config
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
from comon.constant import local_elastic
import os
import json


class EvaluatePipeline():
    def __init__(self):
        with open(os.path.join(root_path, pipeline_config)) as f:
            data = json.load(f)
            self.pipeline = data["pipeline"]

    def evaluate_classify(self, predict_arr):
        pass
    def evaluate_each_pipeline(self):
        pass


if __name__ == "__main__":
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