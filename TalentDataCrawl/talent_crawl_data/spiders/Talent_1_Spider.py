# -*- coding: utf-8 -*-
import scrapy
from .TalentUrlSpider import TalentUrlSpider
from ..utils.CrawlUtils import initial_index

KEY_STORE = [
    {'keyword': "nhân tài", 'file_store': 'url/nhantai.url'},
    # {'keyword': "thu hút nhân tài", 'file_store': 'url/nhantai.url'},
    # {'keyword': "tìm kiếm nhân tài", 'file_store': 'url/nhantai.url'},
    # {'keyword': "đạo tạo nhân tài", 'file_store': 'url/nhantai.url'},
    # {'keyword': "chính sách nhân tài", 'file_store': 'url/nhantai.url'}
]

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}


class Talent1SpiderSpider(TalentUrlSpider):
    name = 'Talent1Spider'
    start_urls = ['http://www.google.com/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_store = KEY_STORE
        self.user_agent = USER_AGENT
        self.last_index = [{"keyword": file['keyword'],
                            "last_index": initial_index(file['file_store']),
                            "file_store": file['file_store']
                            }
                           for file in self.key_store]
