import time
from bs4 import BeautifulSoup as sp
import requests
from collections import deque
import os


TASK = input("Give the task name:\n")
seed_url = input("give a seed url:\n")
KEYWORD = input("Give the keyword, if you don't want focus search, press enter\n")
COUNT_THRESHOLD = int(input("How many urls do you want to crawl at most?\n"))
DEPTH_THRESHOLD = int(input("How many depth do you want to crawl at most?\n"))
if input("Do you want to save the raw html?[y]/[n]\n").lower() == "y":
    SAVE_HTML_FLAG = True
else:
    SAVE_HTML_FLAG = False


PREFIX = "https://en.wikipedia.org"
# seed_url_1 = "https://en.wikipedia.org/wiki/Time_zone"
# seed_url_2 = "https://en.wikipedia.org/wiki/Electric_car"
# seed_url_3 = "https://en.wikipedia.org/wiki/Carbon_footprint"


def bfs(seed, keyword):
    is_focus = False
    if len(keyword) != 0:
        is_focus = True

    # init
    q = deque([])
    result_url = []
    parameter_list = []

    q.appendleft(seed)
    result_url.append(seed)
    parameter_list.append("0" + "\t" + "0" + "\t" + "0")
    count = 1
    depth = 1
    url_index = 1

    while len(q) != 0 and depth <= DEPTH_THRESHOLD:
        size = len(q)

        print("Start Crawling...")
        for i in range(0, size):
            cur = q.pop()
            response = requests.get(cur).text
            time.sleep(1)
            root = sp(response, "html.parser")
            dis = 1

            content = root.find('div', id='bodyContent')
            tables = content.findAll("table")
            for table in tables:
                table.decompose()

            a_list = content.findAll('a', href=True)

            for item in a_list:

                href = item.get("href")
                url = PREFIX + href

                if (not href.startswith("/wiki")) \
                        or ("class" in item.attrs and item["class"][0] == "external text") \
                        or ":" in href:
                    continue
                # handle "#", get the base url
                if "#" in href:
                    url = PREFIX + href.split("#")[0]

                # handle redirect_url
                if "class" in item.attrs and item["class"][0] == "mw-redirect":
                    redirect_page = requests.get(url).text
                    time.sleep(1)
                    redirect = sp(redirect_page, "html.parser")
                    url = redirect.find("link", rel="canonical").get("href")

                if count < COUNT_THRESHOLD and url not in result_url:
                    if not is_focus or has_keyword(keyword, item, url):
                        result_url.append(url)
                        q.appendleft(url)
                        parameter_list.append(str(depth) + "\t" + str(url_index) + "\t" + str(dis))
                        dis += 1
                        count += 1
                        print("valid url is " + url)
                        print("depth is " + str(depth))
                        print("count is " + str(count))

                elif count == COUNT_THRESHOLD:
                    print("Url counts restriction, End Crawling...")
                    write_to_txt(result_url, parameter_list)
                    if SAVE_HTML_FLAG:
                        save_html(result_url)
                    return 0

            url_index += 1
        depth += 1
    print("Depth restriction, End Crawling...")
    write_to_txt(result_url, parameter_list)
    if SAVE_HTML_FLAG:
        save_html(result_url)


def write_to_txt(result, parameter):
    url_path = os.getcwd() + '/' + TASK + '.txt'
    f_url = open(url_path, "w")
    num = 0
    for i in result:
        f_url.write(i + "\t" + parameter[num] + "\n")
        num += 1

    f_url.close()
    print("Finished write to txt")


def save_html(result_url):
    html_folder_path = os.getcwd() + "/" + TASK + "_folder"
    os.mkdir(html_folder_path)
    index = 1
    print("Save html Begin...")
    for url in result_url:
        print("saving num " + str(index))
        response = requests.get(url).text
        time.sleep(1)
        html = str(sp(response, "html.parser"))
        html_path = html_folder_path + "/" + str(index) + ".txt"
        html_fw = open(html_path, "w")
        html_fw.write(html)
        html_fw.close()
        index += 1


def has_keyword(keyword, item, url):
    a_text = item.get_text()
    keyword = keyword.lower()
    if keyword in a_text.lower() or keyword in url.lower():
        print(a_text)
        return True
    else:
        return False


bfs(seed_url, KEYWORD)

