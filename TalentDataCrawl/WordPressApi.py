# from wordpress_xmlrpc import Client, WordPressPost
# from wordpress_xmlrpc.methods import posts
# from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
# from urllib import request
#
#
# class WordPressApiClient:
#     def __init__(self):
#         self.wp = Client('https://nhantai.org/xmlrpc.php', 'haidt', 'haidt.nhantai.2019')
#
#     # def createNewsToWordPress(self):
#     #     clean_news = ElasticSearchUtils.getAllTalentNewsCleanFromServerHost()
#     #     news = clean_news[0]["_source"]
#     #     loc = news["processor_ner_loc"]
#     #
#     #     widget = WordPressPost()
#     #     widget.post_type = 'news'
#     #     widget.title = news["title"]
#     #     widget.content = news["content"]
#     #     widget.custom_fields = []
#     #     widget.custom_fields.append({
#     #         'url': news["url"],
#     #         'summary': news["summary"],
#     #         'source': news["source"],
#     #         'publish_date': news["publish_date"],
#     #         'indexed_date': news["indexed_date"],
#     #         'cities': self.convertArrayToString(loc["cities"]),
#     #         'provinces': self.convertArrayToString(loc["provinces"]),
#     #         'nations': self.convertArrayToString(loc["nations"]),
#     #         'images': self.convertArrayToString(news["images"])
#     #     })
#     #     widget.id = self.wp.call(posts.NewPost(widget))
#
#     def convertArrayToString(arr):
#         stringItem = ""
#         if len(arr):
#             for index in range(len(arr)):
#                 if index == 0 or index == len(arr) - 1:
#                     stringItem += arr[index]
#                 else:
#                     stringItem += "-" + arr[index]
#         else:
#             return stringItem
#         return stringItem
#
#
# if __name__ == "__main__":
#     wp_client = WordPressApiClient()
#     # wp_client.createNewsToWordPress()
# # from xmlrpclib import Transport
# #
# # class SpecialTransport(Transport):
# #
# #     user_agent = 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31'
# #
# # try:
# #     # Use the verbose flag for debugging
# #     server = xmlrpc_client.ServerProxy(url, transport=SpecialTransport(), verbose=True)
# #
# # except xmlrpc_client.ProtocolError as err:
# #     print "A protocol error occurred"
# #     print "URL: %s" % err.url
# #     print "HTTP/HTTPS headers: %s" % err.headers
# #     print "Error code: %d" % err.errcode
# #     print "Error message: %s" % err.errmsg

# from client_elasticsearch.ElasticSearchUtils import ElasticSearchUtils
# from comon.Constant import local_elastic
# import json
# cli = ElasticSearchUtils()
# news = cli.getAllTalentNewsCleanFromHost(local_elastic)
#
# with open("hash.txt", "w") as f:
#     f.write("[")
#     for new in news:
#         json.dump(new, f)
#         f.write(",\n")
#     f.write("]")

# from verbalexpressions import VerEx
# #
# #
# # # In[199]:
# #
# #
# # verEx = VerEx()
# #
# #
# # # In[200]:
# #
# #
# # strings = ['123Abdul233',
# #            '233Raja434',
# #            '223Ethan Hunt444']
# #
# #
# # # In[201]:
# #
# #
# # expression = verEx.range('a','z','A','Z',' ')
# #
# #
# # # In[202]:
# #
# #
# # expression.source()
# #
# #
# # # In[204]:
# #
# #
# # import re
# #
# # re_exp = expression.compile()
# #
# #
# # # In[205]:
# #
# #
# # re.findall(re_exp,strings[0])
# #
# #
# # # In[206]:
# #
# #
# # arr = [''.join(re.findall(re_exp,line)) for line in strings]
# # print(arr)
# import rstr
# import string
# import random
# import hashlib
# for i in range(5000):
#     date_in =["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy","Chủ Nhật"]
#     ine = date_in[random.randint(0,6)]
#     day = random.randint(1,32)
#     month =random.randint(1,12)
#     year = random.randint(2000, 2121)
#
#     if day < 10:
#         day = "0" + str(day)
#     if month < 10:
#         month = "0" + str(month)
#
#     hour = random.randint(0,24)
#     minute = random.randint(0,60)
#
#     if hour < 10:
#         hour = "0" + str(hour)
#     if minute < 10:
#         minute = "0" + str(minute)
#     def randomString(stringLength=10):
#         """Generate a random string of fixed length """
#         letters = string.ascii_lowercase
#         return ''.join(random.choice(letters) for i in range(stringLength))
#     rs = ine + " " + str(day)+"/"+str(month)+"/"+str(year)+ " - " + str(hour)+":"+str(minute)
#     print(rs)
#     name = hashlib.md5(str(rs + randomString(10)).encode('utf-8')).hexdigest()
#     with open("date/" + name + ".txt", "w", encoding="UTF-8") as f:
#         f.write(rs)
