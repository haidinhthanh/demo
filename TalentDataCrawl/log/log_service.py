import logging
from comon.log_path import log_crawl_link, log_crawl_news, log_process_detail, log_process_summary, log_evaluate
from datetime import datetime
import os


def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d")
    return current_time


class LogService:
    def __init__(self):
        self.formatter = logging.Formatter('%(asctime)s,%(msecs)d,%(name)s %(levelname)s %(message)s')
        self.log_crawl_link = log_crawl_link
        self.log_crawl_news = log_crawl_news
        self.log_process_detail = log_process_detail
        self.log_process_summary = log_process_summary
        self.log_evaluate = log_evaluate

    def configLogDataPipelineProcessData(self, pipeline_name):
        if pipeline_name == "data pipeline 1":
            path = self.log_process_detail[0]
        elif pipeline_name == "data pipeline 2":
            path = self.log_process_detail[1]
        else:
            return None
        log_name = os.path.join(path, str(getCurrentTime()) + ".log")
        return self.setup_logger("process data", log_name)

    def configLogDataPipelineSummary(self, pipeline_name):
        if pipeline_name == "data pipeline 1":
            path = self.log_process_summary[0]
        elif pipeline_name == "data pipeline 2":
            path = self.log_process_summary[1]
        else:
            return None
        log_name = os.path.join(path, str(getCurrentTime()) + ".log")
        return self.setup_logger("process data summary ", log_name)

    def configLogEvaluateDataPipeline(self):
        log_name = os.path.join(self.log_evaluate, str(getCurrentTime()) + ".log")
        return self.setup_logger("evaluate data pipeline ", log_name)

    def configLogCrawlLink(self):
        log_name = os.path.join(self.log_crawl_link, str(getCurrentTime()) + ".log")
        return self.setup_logger("crawl link scrapy", log_name)

    def configLogCrawlNews(self):
        log_name = os.path.join(self.log_crawl_news, str(getCurrentTime()) + ".log")
        return self.setup_logger("crawl news scrapy", log_name)

    def setup_logger(self, name, log_file, level=logging.DEBUG):
        handler = logging.FileHandler(log_file)
        handler.setFormatter(self.formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

