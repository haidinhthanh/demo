import scrapy
import time
from talent_crawl_data.utils.CrawlUtils import initial_index, scrape_google, filter_exist_url, append_file, scrape_bing

KEY_STORE = [
    {'keyword': "nhân tài", 'file_store': 'url/nhantai.url'},
    # {'keyword': "thu hút nhân tài", 'file_store': 'url/nhantai.url'},
    # {'keyword': "tìm kiếm nhân tài", 'file_store': 'url/nhantai.url'},
    # {'keyword': "đạo tạo nhân tài", 'file_store': 'url/nhantai.url'},
    # {'keyword': "chính sách nhân tài", 'file_store': 'url/nhantai.url'},
    # {'keyword': "người tài", 'file_store': 'url/nguoitai.url'},
    # {'keyword': "thu hút người tài", 'file_store': 'url/nguoitai.url'},
    # {'keyword': "đào tạo người tài", 'file_store': 'url/nguoitai.url'},
    # {'keyword': "chính sách người tài", 'file_store': 'url/nguoitai.url'},
    # {'keyword': "nguồn nhân lực", 'file_store': 'url/nguonnhanluc.url'},
    # {'keyword': "thu hút nguồn nhân lực", 'file_store': 'url/nguonnhanluc.url'},
    # {'keyword': "đào tạo nguồn nhân lực", 'file_store': 'url/nguonnhanluc.url'},
    # {'keyword': "phát triển nguồn nhân lực", 'file_store': 'url/nguonnhanluc.url'},
    # {'keyword': "yêu cầu nguồn nhân lực", 'file_store': 'url/nguonnhanluc.url'},
    # {'keyword': "thiếu nguồn nhân lực", 'file_store': 'url/nguonnhanluc.url'},
    # {'keyword': "khát nguồn nhân lực", 'file_store': 'url/nguonnhanluc.url'},
    # {'keyword': "chuẩn bị nguồn nhân lực", 'file_store': 'url/nguonnhanluc.url'},
    # {'keyword': "nâng cao nguồn nhân lực", 'file_store': 'url/nguonnhanluc.url'},
    # {'keyword': "nhân lực chất lượng", 'file_store': 'url/nhanlucchatluong.url'},
    # {'keyword': "thiếu nhân lực chất lượng", 'file_store': 'url/nhanlucchatluong.url'},
]

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}


class TalentUrlSpider(scrapy.Spider):
    name = 'TalentUrlSpider'
    start_urls = ['https://www.google.com/']
    pipelines = ['TalentUrlPipeline']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user_agent = ""
    #     self.key_store = []
    #     self.last_index = []
    #
    # def __init__(self):
    #     self.last_index = [{"keyword": file['keyword'],
    #                         "last_index": initial_index(file['file_store']),
    #                         "file_store": file['file_store']
    #                         }
    #                        for file in KEY_STORE]
    def __init__(self, domain=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_store = KEY_STORE
        self.user_agent = USER_AGENT
        self.last_index = [{"keyword": file['keyword'],
                            "last_index": initial_index(file['file_store']),
                            "file_store": file['file_store']
                            }
                           for file in self.key_store]
        self.domain = domain

    def parse(self, response):
        keywords = [keyword['keyword'] for keyword in KEY_STORE]
        datas = []
        for keyword in keywords:
            try:
                results = scrape_bing('site:'+self.domain+' '+keyword, 10, "en", self.user_agent)
                for result in results:
                    datas.append(result)
            except Exception as e:
                print(e)
            finally:
                time.sleep(10)
        print(datas)
        for keyword in keywords:
            file_store = [file['file_store'] for file in self.key_store if (file['keyword'] == keyword)][0]
            last_index = [file['last_index'] for file in self.last_index if (file['keyword'] == keyword)][0]

            # lọc các url đã tồn tại và lưu các url mới
            data_keyword = [data for data in datas if (data['keyword'] == 'site:'+self.domain+' '+keyword)]
            # print(file_store)
            # print(data_keyword)
            # filter_data = filter_exist_url(data_keyword, file_store)
            # for item in filter_data:
            #     print(item)
            # last_index = append_file(filter_data, file_store, last_index)
            #
            # # đánh lại chỉ mục sau khi lưu
            # for file in self.last_index:
            #     if file['file_store'] == file_store:
            #         file['last_index'] = last_index
