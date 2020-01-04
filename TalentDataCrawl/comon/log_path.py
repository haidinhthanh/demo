from comon.constant import root_path
import os
import json

with open(os.path.join(root_path, "pipeline_config.json"), "r", encoding="UTF-8") as f:
    pipeline = json.load(f)["pipeline"]
log_crawl_link = os.path.join(root_path, "log/crawl_link")
log_crawl_news = os.path.join(root_path, "log/crawl_news")
log_process_detail = [os.path.join(root_path, "log/process_data_detail/" + item["name"]) for item in pipeline]
log_process_summary = [os.path.join(root_path, "log/process_data_summary/" + item["name"]) for item in pipeline]
log_evaluate = os.path.join(root_path, "log/evaluate_data")
