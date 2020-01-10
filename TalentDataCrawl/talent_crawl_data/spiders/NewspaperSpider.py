import scrapy
import json

from scrapy.loader import ItemLoader

from talent_crawl_data.items import NewspaperItem
from talent_crawl_data.utils.FileUtils import find_last_index, get_config_last_index, \
    get_start_urls, get_last_crawl_index
from comon.utils import checkDomainHadCrawl, getDomainHadCrawl, getMapXpath, getTimeIso
from extract_xpath.extract_xpath import getXpathFromNewDomain
from log.log_service import LogService

FILES_NAME = [
    "url/nguoitai.url",
    "url/nguonnhanluc.url",
    "url/nhanlucchatluong.url",
    "url/nhantai.url"
]
NUM_STEP_URL = 10000  # số url lấy mỗi file


class NewspapersSpider(scrapy.Spider):
    name = 'NewspaperSpider'
    start_urls = []
    pipelines = ["TalentCrawledDataPipeline"]

    def __init__(self):
        with open('url/index.json', 'r') as f:
            config_index = json.load(f)
        self.crawl_logger = LogService().configLogCrawlNews()
        for file_name in FILES_NAME:
            file_config = get_config_last_index(config_index['config'], file_name)
            start_index = int(file_config[file_name]) + 1
            last_index = int(find_last_index(file_name))

            # lấy url từ mỗi file và lưu vào start urls
            urls = get_start_urls(file_name, start_index, last_index, NUM_STEP_URL)
            # kiểm tra các domain của url đã kiểm tra
            for url in urls:
                domain = url.split("/")[2]
                if not checkDomainHadCrawl(domain):
                    getXpathFromNewDomain(domain, self.crawl_logger)
            self.start_urls = self.start_urls + urls

            # đánh dấu vị trí đã lấy url đến
            last_crawl_index = get_last_crawl_index(start_index, last_index, NUM_STEP_URL)
            file_config[file_name] = last_crawl_index
        with open('url/index.json', 'w') as f:
            json.dump(config_index, f)
        self.domain_crawl = getDomainHadCrawl()
        self.map_xpath = getMapXpath()

    def parse(self, response):
        item = ItemLoader(item=NewspaperItem(), response=response)
        domain = str(response.url).split("/")[2]
        # lấy xpath phù hợp với domain
        map_xpath = self.mapDomainToXpath(domain)
        title, summary, content, source, published_date, images = [], [], [], [], [], []
        # dựa vào xpath lấy dữ liệu
        if map_xpath["title"] != "empty":
            for xpath in map_xpath["title"]:
                value = response.xpath(xpath).get()
                if value is not None:
                    title.append(value)
        if map_xpath["summary"] != "empty":
            for xpath in map_xpath["summary"]:
                value = response.xpath(xpath).get()
                if value is not None:
                    summary.append(value)
        if map_xpath["content"] != "empty":
            for xpath in map_xpath["content"]:
                value = response.xpath(xpath).getall()
                if value is not None:
                    content += value
        if map_xpath["source"] != "empty":
            for xpath in map_xpath["source"]:
                value = response.xpath(xpath).get()
                if value is not None:
                    source.append(value)
        if map_xpath["published_date"] != "empty":
            for xpath in map_xpath["published_date"]:
                value = response.xpath(xpath).get()
                if value is not None:
                    published_date.append(getTimeIso(value))
        if map_xpath["images"] != "empty":
            for xpath in map_xpath["images"]:
                value = response.xpath(xpath).getall()
                value = [item for item in value if "data:image/gif" not in item]
                if value is not None or not value:
                    images += value
        title = [item for item in list(dict.fromkeys(title)) if item != ""]
        summary = [item for item in list(dict.fromkeys(summary)) if item != ""]
        content = [item for item in list(dict.fromkeys(content)) if item != ""]
        source = [item for item in list(dict.fromkeys(source)) if item != ""]
        published_date = [item for item in list(dict.fromkeys(published_date)) if item != ""]
        images = [item for item in list(dict.fromkeys(images)) if item != ""]
        item.add_value("url", str(response.url))
        item.add_value("title", title)
        item.add_value("summary", summary)
        item.add_value("content", content)
        item.add_value("source", source)
        item.add_value("published_date", published_date)
        item.add_value("images", images)
        yield item.load_item()

    def mapDomainToXpath(self, domain):
        for item in self.domain_crawl:
            if item in domain:
                match_domain = item
                break
        for item in self.map_xpath:
            if item["domain"] == match_domain:
                return item["path"]