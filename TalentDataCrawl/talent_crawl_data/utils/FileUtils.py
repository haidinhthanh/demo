def find_last_index(file_path):
    with open(file_path, "r") as f:
        last_line = f.read().splitlines()[-1]
        last_index = last_line.split()[0]
    return last_index


def get_start_urls(file_path, start_index, last_index, num_url):
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
    if start_index + num_url <= last_index:
        return [line.split()[1] for line in lines[start_index:start_index + num_url]]
    elif start_index > last_index:
        return []
    else:
        return [line.split()[1] for line in lines[start_index:last_index+1]]


def get_last_crawl_index(start_index, last_index, num_url):
    if start_index + num_url <= last_index:
        return start_index + num_url -1
    else:
        return last_index


def get_config_last_index(config, file_name):
    for item in config:
        if file_name in item.keys():
            return item
