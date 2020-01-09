from lxml import etree
import requests
import pickle
import gensim
import numpy as np
from pyvi import ViTokenizer
from collections import Counter
import os
import json
from const_path import root_path, source_path

dir_path = os.path.dirname(os.path.realpath(__file__))
bi_rnn = pickle.load(open(os.path.join(dir_path, 'bi_rnn_model_6.pkl'), 'rb'))
tf_idf_vec = pickle.load(open(os.path.join(dir_path, "tf_idf_vec_5.pkl"), "rb"))


def getDemoUrl(domain):
    files = [name for name in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, name)) if
             ".url" in name]
    urls = []
    for file in files:
        with open(os.path.join(source_path, file), "r") as f:
            lines = f.readlines()
            urls += [item.split(" ")[1].replace("\n", "") for item in lines if domain in item.split(" ")[1] and
                     item.split(" ")[1].replace("\n", "") != ""]
    if len(urls) > 100:
        return urls[0:100]
    else:
        return urls[0:len(urls)]


def convertToImageXpath(xpath):
    xpath_el = [item for item in xpath.split("/") if item != "img"]
    size = len(xpath_el)
    if "[" in xpath_el[size - 1]:
        index = xpath_el[size - 1].index("[")
        xpath_el[size - 1] = xpath_el[size - 1][0:index]

    for item in xpath_el:
        if "tbody" in item:
            index = xpath_el.index(item)
            el = xpath_el[index]
            if "[" in el:
                index2 = el.index("[")
                xpath_el[index] = el[0:index2]
    return "/".join(xpath_el) + "/img/@src"


def cal_similarity(first_path, second_path):
    score = 0
    first_path = [item for item in first_path.split("/") if (item != "em" and item != "strong")]
    second_path = [item for item in second_path.split("/") if (item != "em" and item != "strong")]
    if len(first_path) < len(second_path):
        size = len(first_path)
    else:
        size = len(second_path)
    if len(first_path) == len(second_path):
        size = len(first_path)
        if "[" in first_path[size - 1] and "[" in second_path[size - 1]:
            new_first_path = first_path
            new_second_path = second_path
            new_first_path[size - 1] = new_first_path[size - 1][0: new_first_path[size - 1].find("[")]
            new_second_path[size - 1] = new_second_path[size - 1][0: new_second_path[size - 1].find("[")]
            if "/".join(new_first_path) == "/".join(new_second_path):
                return 0
        for i in range(len(first_path)):
            str1 = first_path[i]
            str2 = second_path[i]
            if i == size - 1 and str1 == str2:
                score += -1
            if str1 != str2:
                score += -1
    else:
        score -= abs(len(first_path) - len(second_path))
        for i in range(size):
            str1 = first_path[i]
            str2 = second_path[i]
            if str1 != str2:
                score += -1
    return score


def compare_path_similarity(first_path, second_path):
    first_path = [item for item in first_path.split("/") if (item != "em" and item != "strong")]
    second_path = [item for item in second_path.split("/") if (item != "em" and item != "strong")]
    if len(first_path) != len(second_path):
        return False
    else:
        for i in range(len(first_path)):
            str1 = first_path[i]
            str2 = second_path[i]
            if i == len(first_path) - 1:
                if "[" in first_path[i]:
                    index = first_path[i].find("[")
                    str1 = first_path[i][0: index]
                if "[" in second_path[i]:
                    index = second_path[i].find("[")
                    str2 = second_path[i][0: index]
                if str1 != str2:
                    return False
            else:
                if str1 != str2:
                    return False

    return True


def compare_img_path_similarity(first_path, second_path):
    first_path = [item for item in first_path.split("/") if (item != "img")]
    second_path = [item for item in second_path.split("/") if (item != "img")]
    if len(first_path) != len(second_path):
        return False
    else:
        for i in range(len(first_path)):
            str1 = first_path[i]
            str2 = second_path[i]

            if "[" in first_path[i]:
                index = first_path[i].find("[")
                str1 = first_path[i][0: index]
            if "[" in second_path[i]:
                index = second_path[i].find("[")
                str2 = second_path[i][0: index]
            if str1 != str2:
                return False
    return True


def getLocImg(arr, path):
    for item in arr:
        if path in item[0]:
            return item[-1]
    return -1


def getImageXpath(arrXpath, content_xpath, doc_classify):
    compare_path = content_xpath.replace("/descendant-or-self::*[not(self::script)]/text()", "")
    doc_loc = [item for item in doc_classify if compare_path in item[0]]
    start_index = doc_loc[0][-1]
    last_index = doc_loc[-1][-1]
    i = 0
    while True:
        if i >= len(arrXpath):
            break
        loc_img = getLocImg(doc_classify, arrXpath[i][0])
        if compare_img_path_similarity(arrXpath[i][0], compare_path) and \
                start_index <= loc_img <= last_index:
            return convertToImageXpath(arrXpath[i][0])
        i += 1
    score_sim = [[cal_similarity(item[0], compare_path), item[0]] for item in arrXpath
                 if cal_similarity(item[0], compare_path) not in [0, -1] and
                 start_index <= getLocImg(doc_classify, item[0]) <= last_index
                 ]

    score_arr = [item[0] for item in score_sim]
    if not score_arr:
        return "empty"
    max_score = max(score_arr)
    max_index = score_arr.index(max_score)
    img_xpath = convertToImageXpath(score_sim[max_index][1])
    return img_xpath


def getPublishedDateXpath(arrXpathDate):
    if arrXpathDate:
        return arrXpathDate[0][0] + "/text()"
    else:
        return "empty"


def getSourceXpath(arrSourceXpath):
    if arrSourceXpath and "img" not in arrSourceXpath[0][0]:
        return arrSourceXpath[0][0] + "/text()"
    else:
        return "empty"


def getContentXpath(arrXpath):
    summary_xpath = "empty"
    content_xpath = "empty"
    i = 0
    while True:
        if i >= len(arrXpath) - 1:
            break
        if compare_path_similarity(arrXpath[i][0], arrXpath[i + 1][0]) and \
                cal_similarity(arrXpath[i][0], arrXpath[i + 1][0]) >= 0 and \
                "Nghe VietNamNet" not in arrXpath[i][1]:
            if i - 1 >= 0:
                content_xpath = [item for item in arrXpath[i][0].split("/")
                                 if "span" not in item and "em" not in item and "strong" not in item or item == "i"
                                 ]
                index = content_xpath[len(content_xpath) - 1].find("[")
                content_xpath[len(content_xpath) - 1] = content_xpath[len(content_xpath) - 1][
                                                        0:index] + "/descendant-or-self::*[not(self::script)]/text()"
                content_xpath = "/".join(content_xpath)

                score_sim = [[cal_similarity(arrXpath[i][0], item[0]), item[0], item[1]] for item in arrXpath
                             if cal_similarity(arrXpath[i][0], item[0]) not in [0, -1]]
                score_arr = [item[0] for item in score_sim]
                if not score_arr:
                    summary_xpath = "empty"
                else:
                    max_score = max(score_arr)
                    max_index = score_arr.index(max_score)
                    if max_score >= -2:
                        summary_xpath = score_sim[max_index][1] + "/text()"
                    else:
                        summary_xpath = "empty"
                    break
        i += 1
    return summary_xpath, content_xpath


def getTitleXpath(arrXpath):
    if arrXpath:
        arr_sim = []
        for item in arrXpath:
            sim_arr = [cal_similarity(item[0], compare_item[0]) for compare_item in arrXpath if
                       item[0] != compare_item[0]]
            arr_sim.append(sim_arr)
        dict_compare = dict(Counter(tuple(item) for item in arr_sim))
        min_val = min(dict_compare.values())
        valid_path_sim = [k for k, v in dict_compare.items() if v == min_val]
        valid_path = []
        for i in valid_path_sim:
            valid_path.append(arrXpath[arr_sim.index(list(i))])
        for item in valid_path:
            if "h1" in item[0]:
                return item[0] + "/text()"
        return "empty"
    else:
        return "empty"


mapping = {
    0: "content",
    1: "date",
    2: "image",
    3: "irrelevant",
    4: "title",
    5: "url"
}


def extract_xpath(url):
    try:
        response = requests.get(url)
        tree = etree.HTML(response.text)
        data = []
        for node in tree.xpath('//head | //style | //script | //footer | //nav | //select'):
            node.getparent().remove(node)
        for node in tree.iter():
            if node.text is not None and node.text.strip() != "":
                data.append([node.getroottree().getpath(node), node.text.strip()])
            else:
                if node.get('src') is not None and \
                        ("jpg" in node.get('src') or "jpeg" in node.get('src') or "png" in node.get('src')):
                    data.append([node.getroottree().getpath(node), node.get('src')])

        doc_classify = []
        news_content_xpath = []
        img_xpath = []
        published_date_xpath = []
        source_xpath = []
        title_xpath = []
        index = 0
        for item in data:
            text = item[1]
            text = gensim.utils.simple_preprocess(text)
            text = ' '.join(text)
            text_tokens = ViTokenizer.tokenize(text)
            text_tf_idf = tf_idf_vec.transform([text_tokens])
            predict = bi_rnn.predict(text_tf_idf)[0]
            max_element = np.amax(predict)
            result = np.where(predict == max_element)
            # print([item[0], item[1], mapping[result[0][0]]])
            doc_classify.append([item[0], item[1], mapping[result[0][0]], index])
            index += 1
            if mapping[result[0][0]] == "title" \
                    or ("h1" in item[0].split("/")):
                title_xpath.append(item)
            elif mapping[result[0][0]] == "image" \
                    or (mapping[result[0][0]] == "content" and "img" in item[0].split("/")):
                img_xpath.append(item)
            elif mapping[result[0][0]] == "date":
                published_date_xpath.append(item)
            elif mapping[result[0][0]] == "url":
                source_xpath.append(item)
            elif mapping[result[0][0]] == "content":
                news_content_xpath.append(item)
        published_date_xpath = getPublishedDateXpath(published_date_xpath)
        source_xpath = getSourceXpath(source_xpath)
        summary_xpath, content_xpath = getContentXpath(news_content_xpath)
        title_xpath = getTitleXpath(title_xpath)
        img_xpath = getImageXpath(img_xpath, content_xpath, doc_classify)
        # print((published_date_xpath, source_xpath, title_xpath, summary_xpath, content_xpath, img_xpath))
        return published_date_xpath, source_xpath, title_xpath, summary_xpath, content_xpath, img_xpath
    except Exception:
        return "empty", "empty", "empty", "empty", "empty", "empty"


def cal_xpath_from_urls(urls):
    published_date = []
    source = []
    title = []
    summary = []
    content = []
    image = []
    for url in urls:
        published_date_xpath, source_xpath, new_title_xpath, summary_xpath, content_xpath, img_xpath = extract_xpath(
            url)
        published_date.append(published_date_xpath)
        source.append(source_xpath)
        title.append(new_title_xpath)
        summary.append(summary_xpath)
        content.append(content_xpath)
        image.append(img_xpath)
    published_date_xpath = get_max_duplicate_path(published_date)
    source_path = get_max_duplicate_path(source)
    new_title_xpath = get_max_duplicate_path(title)
    summary_xpath = get_max_duplicate_path(summary)
    img_xpath = get_max_duplicate_path(image)
    content_xpath = get_max_duplicate_path(content)
    return published_date_xpath, source_path, new_title_xpath, summary_xpath, img_xpath, content_xpath


def get_max_duplicate_path(arrXpath):
    arrXpath = [item for item in arrXpath if item.strip() not in ["", "empty"]]
    xpath = [item for item in list(dict.fromkeys(arrXpath)) if item != "empty"]
    if len(xpath) == 0:
        return "empty"
    if len(xpath) > 0:
        news_xpath = []
        for i in range(len(xpath)):
            for j in range(i + 1, len(xpath)):
                if i != j:
                    sim_path = longestSubstringFinder(xpath[i], xpath[j])
                    if sim_path:
                        news_xpath.append([xpath[i], xpath[j], sim_path])
        if not len(news_xpath):
            return xpath
        else:
            for item in news_xpath:
                if item[0] in xpath:
                    xpath.remove(item[0])
                if item[1] in xpath:
                    xpath.remove(item[1])
            filter_lst = list(dict.fromkeys(xpath + [item[2] for item in news_xpath]))
            del_item = []
            for item in filter_lst:
                for compare_item in filter_lst:
                    if item[1:] in compare_item and item != compare_item:
                        del_item.append(item)
            return [item for item in filter_lst if item not in del_item]
    return xpath


def longestSubstringFinder(string1, string2):
    answer = []
    string_1 = string1.split("/")
    string_2 = string2.split("/")
    len1, len2 = len(string_1), len(string_2)
    if len1 >= len2:
        len_u = len2
    else:
        len_u = len1
    for i in range(len_u):
        if string_1[len1 - i - 1] == string_2[len2 - i - 1]:
            answer.append(string_1[len1 - i - 1])
        else:
            break
    if len(answer) <= 3 or "/".join(reversed(answer)) == "a/img/@src":
        return []
    return "//" + "/".join(reversed(answer))


def getXpathFromNewDomain(domain, logger):
    urls = getDemoUrl(domain)
    published_date_xpath, source_path, new_title_xpath, summary_xpath, img_xpath, content_xpath = cal_xpath_from_urls(
        urls)
    dict_xpath_domain = {}
    dict_xpath_domain["published_date"] = published_date_xpath
    dict_xpath_domain["source"] = source_path
    dict_xpath_domain["title"] = new_title_xpath
    dict_xpath_domain["summary"] = summary_xpath
    dict_xpath_domain["images"] = img_xpath
    dict_xpath_domain["content"] = content_xpath

    domain_config_path = {
        "domain": domain,
        "path": dict_xpath_domain
    }
    logger.info("extract xpath from " + domain + "\n" + json.dumps(domain_config_path))
    with open(os.path.join(root_path, "system_config.json"), "r") as f:
        config = json.load(f)
        config["domain"].append(domain)
        config["domain_xpath"].append(domain_config_path)

    with open(os.path.join(root_path, "system_config.json"), "w") as f:
        json.dump(config, f)
