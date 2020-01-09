import requests
from bs4 import BeautifulSoup
import os


def append_file(urls, file_path, index, logger):
    with open(file_path, 'a+') as f:
        for url in urls:
            if "tag" in url['link'] \
                    or url['link'] in ['https://baomoi.com/', 'https://baomoi.com'] \
                    or ("/c/" not in url['link'].replace("https://baomoi.com", "").replace(".epi", "") and "baomoi.com" in url["link"] )\
                    or "=https://baomoi.com/" in url['link'] \
                    or "/longform/" in url['link']:
                continue
            f.write(str(index) + " " + str(url['link']) + "\n")
            logger.info("add new url " + str(url['link']) + " to " + file_path)
            index += 1
    return index


def filter_exist_url(urls, file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        filter_urls = [url for url in urls if (url['link'] not in file_content)]
    return filter_urls


def fetch_results_google(search_term, number_results, language_code, user_agent):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results,
                                                                          language_code)

    response = requests.get(google_url, headers=user_agent)
    response.raise_for_status()
    return search_term, response.text


def fetch_results_bing(search_term, no_page, language_code, user_agent):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(no_page, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
    google_url = 'https://www.bing.com/search?q={}&first={}&hl={}'.format(escaped_search_term, no_page,
                                                                          language_code)

    response = requests.get(google_url, headers=user_agent)
    response.raise_for_status()
    return search_term, response.text


def scrape_google(search_term, number_results, language_code, user_agent):
    try:
        keyword, html = fetch_results_google(search_term, number_results, language_code, user_agent)
        results = parse_google_results(html, keyword)
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")


def scrape_bing(search_term, number_results, language_code, user_agent):
    try:
        results = []
        for i in range(0, number_results, 10):
            keyword, html = fetch_results_bing(search_term, i, language_code, user_agent)
            result = parse_bing_results(html, keyword)
            results += result
        return results
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")


def initial_index(file_path):
    if os.path.exists(file_path):
        if os.stat(file_path).st_size != 0:
            with open(file_path, 'r') as f:
                lines = f.read().splitlines()
                last_line = lines[-1]
                return int(last_line.split(" ")[0]) + 1
            f.close()
        else:
            return 0
    else:
        with open(file_path, 'w') as f:
            f.close()
            return 0


def parse_google_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    found_results = []
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:
        link = result.find('a', href=True)
        title = result.find('h3')
        if link and title:
            link = link['href']
            if link != '#':
                found_results.append({'keyword': keyword, 'link': link})
    return found_results


def parse_bing_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    found_results = []
    result_block = soup.find_all('li', attrs={'class': 'b_algo'})
    for result in result_block:
        link = result.find('a', href=True)
        if link:
            link = link['href']
            if link != "#":
                found_results.append({'keyword': keyword, 'link': link})
    return found_results


# def parse_baidu_results(html, keyword):
#     soup = BeautifulSoup(html, 'html.parser')
#     found_results = []
#     result_block = soup.find_all('div', attrs={'class': 'result'})
#     for result in result_block:
#         link = result.find('a', href=True)
#         if link:
#             link = link['href']
#             if link != "#":
#                 found_results.append({'keyword': keyword, 'link': link})
#     return found_results