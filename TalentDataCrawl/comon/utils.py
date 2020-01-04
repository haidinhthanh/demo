from const_path import root_path
from comon.constant import system_config
import os
import json
import re


def getDomainHadCrawl():
    with open(os.path.join(root_path, system_config), "r") as f:
        data = json.load(f)
        domains = data["domain"]
    return domains


def checkDomainHadCrawl(domain):
    crawl_domains = getDomainHadCrawl()
    for crawl_domain in crawl_domains:
        if crawl_domain in domain:
            return True
    return False


def getMapXpath():
    with open(os.path.join(root_path, system_config), "r") as f:
        data = json.load(f)
        return data["domain_xpath"]


date_re = [
    ["-", "\d{1,2}-\d{1,2}-\d{4}"],
    ["/", "\d{1,2}/\d{1,2}/\d{4}"],
    ["/", "\d{1,2}/\d{1,2}/\d{2}"],
    ["-", "\d{1,2}-\d{1,2}-\d{2}"],
]
time_re = [
    [":", "\d{1,2}:\d{1,2}:\d{1,2}"],
    [":", "\d{1,2}:\d{1,2}"]
]


def getTimeIso(time):
    try:
        text = str(time).strip()
        for pattern in date_re:
            date_match = re.search(pattern[1], text)
            if date_match:
                date = date_match.group()
                date_detail = date.split(pattern[0])
                if len(date_detail[2]) <= 2:
                    date_detail[2] = "20" + date_detail[2]
                date_string = "-".join(reversed(date_detail))
        for pattern in time_re:
            time_match = re.search(pattern[1], text)
            if time_match:
                time = time_match.group()
                time_detail = time.split(pattern[0])
                if len(time_detail) <= 2:
                    time_detail.append("00")
                time_string = ":".join(time_detail)
        return date_string + "T" + time_string + "Z"
    except Exception:
        return ""
