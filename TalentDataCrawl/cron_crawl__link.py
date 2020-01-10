from crontab import CronTab
import os
import datetime
import json

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d")
    return current_time


cron = CronTab(user='haidt')
root_path = os.path.dirname(os.path.realpath(__file__))


command1 = "00 12 * * * python3 -m " + os.path.join(root_path, "run_data_pipeline_1")
job1 = cron.new(command=command1)

command2 = "00 12 * * * python3 -m " + os.path.join(root_path, "run_data_pipeline_2")
job2 = cron.new(command=command2)

command3 = "00 18 * * * python3 -m " + os.path.join(root_path, "run_evaluate")
job3 = cron.new(command=command3)

with open(os.path.join(root_path,"domain.json"), "r") as f:
    domains = json.load(f)["data"]
    for domain in domains:
        command4 = "00 01 * * * cd /home/haidt/project/demo/TalentDataCrawl && scrapy crawl -a domain=" +domain + " TalentUrlSpider"
        job4 = cron.new(command=command4)

command5 = "00 02 * * * cd /home/haidt/project/demo/TalentDataCrawl && scrapy crawl NewspaperSpider"
job5 = cron.new(command=command2)

cron.write()
