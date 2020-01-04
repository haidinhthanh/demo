from comon.constant import root_path, pipeline_config, talent_cleaned_index, LOCAL_HOST_NAME, SERVER_HOST_NAME
from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
import os
import json
from sklearn.metrics import f1_score
import pickle
import gensim
from pyvi import ViTokenizer
from log.log_service import LogService


class EvaluatePipeline:
    def __init__(self):
        self.irr_test = []
        with open(os.path.join(root_path, pipeline_config)) as f:
            data = json.load(f)
            self.pipeline = data["pipeline"]
            f.close()
        self.eval_cate_classify = pickle.load(
            open(os.path.join(root_path, "model/model_evaluate/naive_bayes_model.pkl"), "rb"))
        self.tf_idf_vec = pickle.load(open(os.path.join(root_path, "model/tf_idf_vec.pkl"), "rb"))
        self.news_processed_pipeline = []
        self.getDataProcessedPipeline()

        self.mapping_irr_pipeline = {
            'irrelevant': 0,
            'related': 1,
        }
        self.mapping_cate_pipeline = {
            'Công nghệ': 0,
            'Giáo dục': 1,
            'Giải trí': 2,
            'Khoa học': 3,
            'Kinh tế': 4,
            'Pháp luật': 5,
            'Thế giới': 6,
            'Thể thao': 7,
            'Văn hóa': 8,
            'Xã hội': 9,
            'Y tế': 10
        }
        self.logger = LogService().configLogEvaluateDataPipeline()

    @staticmethod
    def checkRelated(item):
        keys = ["nguồn nhân lực", "nhân lực chất lượng", "chính sách nhân tài", "chính sách người tài",
                "thu hút người tài", "thu hút nhân tài", "đãi ngộ người tài", "đãi ngộ nhân tài",
                "tìm kiếm người tài", "tìm kiếm nhân tài", "đào tạo nhân tài", "đào tạo người tài",
                "chính sách người tài", "chính sách nhân tài"]
        for key in keys:
            if key in item:
                return 1
        return 0

    def getDataProcessedPipeline(self):
        for item in self.pipeline:
            with open(os.path.join(root_path, "data_pipeline/" + item["name"] + ".json"), "r", encoding="UTF-*") as f:
                data = {
                    "name": item["name"],
                    "index": item["elastic_search_index"],
                    "processed_data": json.load(f)["data_processed"]
                }
                self.news_processed_pipeline.append(data)
                f.close()

    def resetDataProcessedPipeline(self):
        for item in self.pipeline:
            with open(os.path.join(root_path, "data_pipeline/" + item["name"] + ".json"), "w", encoding="UTF-*") as f:
                json.dump({"data_processed": []}, f)
                f.close()

    def evaluate_irrelevant(self, news_arr):
        predict_arr = [self.mapping_irr_pipeline[item["processor_irrelevant"]] for item in news_arr["processed_data"] if
                       item["processor_irrelevant"] != "skipped"]
        fix_true_arr = []
        for item in news_arr["processed_data"]:
            if item["processor_irrelevant"] != "skipped":
                text = item["title"] + "." + item["content"]
                if "summary" in item:
                    text = text + "." + item["summary"]
                fix_true_arr.append(self.checkRelated(text))
        average_f1 = dict()
        average_f1["micro"] = f1_score(fix_true_arr, predict_arr, average="micro")
        return average_f1["micro"]

    def evaluate_classify_content(self, news_arr):
        predict_arr = [self.mapping_cate_pipeline[item["processor_category_classify"]] for item
                       in news_arr["processed_data"] if item["processor_category_classify"] != "skipped"]
        fix_true_arr = []
        for item in news_arr["processed_data"]:
            if item["processor_category_classify"] != "skipped":
                text = item["title"] + "." + item["content"]
                if "summary" in item:
                    text = text + "." + item["summary"]
                text = gensim.utils.simple_preprocess(text)
                text = ' '.join(text)
                text_tokens = ViTokenizer.tokenize(text)
                text_tf_idf = self.tf_idf_vec.transform([text_tokens])
                fix_true_arr.append(self.eval_cate_classify.predict(text_tf_idf)[0])
        average_f1 = dict()
        average_f1["micro"] = f1_score(fix_true_arr, predict_arr, average="micro")
        return average_f1["micro"]

    def evaluate_each_pipeline(self, news_arr):
        print(news_arr["name"])
        self.logger.info(news_arr["name"])
        score_f1_irrelevant = self.evaluate_irrelevant(news_arr)
        score_f1_cate_classify = self.evaluate_classify_content(news_arr)
        print("F1-score process irrelevant " + str(score_f1_irrelevant))
        print("F1-score process classify " + str(score_f1_cate_classify))
        self.logger.info("F1-score process irrelevant " + str(score_f1_irrelevant))
        self.logger.info("F1-score process classify " + str(score_f1_cate_classify))
        return score_f1_irrelevant + score_f1_cate_classify

    def evaluate_pipeline(self):
        pipelines_score = []
        for item in self.news_processed_pipeline:
            pipelines_score.append(self.evaluate_each_pipeline(item))
        max_score = max(pipelines_score)
        index = pipelines_score.index(max_score)
        max_score_pipeline = self.news_processed_pipeline[index]
        print("data pipeline chosen " + max_score_pipeline["name"])
        self.logger.info("data pipeline chosen " + max_score_pipeline["name"])
        self.save_highest_acc_news_processed(max_score_pipeline["index"])
        self.resetDataProcessedPipeline()

    def save_highest_acc_news_processed(self, elastic_search_index):
        ElasticSearchUtils.sendCrawledNewsFromHostToHost(LOCAL_HOST_NAME, LOCAL_HOST_NAME,
                                                         elastic_search_index, talent_cleaned_index, self.logger)


if __name__ == "__main__":
    e = EvaluatePipeline()
    e.resetDataProcessedPipeline()
