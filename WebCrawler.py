import time
from bs4 import BeautifulSoup as sp
import requests
from collections import deque
import os

THRESHOLD = 1000
PREFIX = "https://en.wikipedia.org"
KEYWORD = "task3"
url_path = os.getcwd() + '/' + KEYWORD + '.txt'
html_folder_path = path = os.getcwd() + "/" + KEYWORD + "_folder"
seed_url_1 = "https://en.wikipedia.org/wiki/Time_zone"
seed_url_2 = "https://en.wikipedia.org/wiki/Electric_car"
seed_url_3 = "https://en.wikipedia.org/wiki/Carbon_footprint"


def bfs(seed, keyword):
    is_focus = False
    if len(keyword) != 0:
        is_focus = True

    # init
    q = deque([])
    result_url = []
    parameter_list = []

    q.appendleft(seed)
    count = 0
    depth = 1
    url_index = 1

    while len(q) != 0 and depth <= 6:
        size = len(q)
        print("size is " + str(size))
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

            a_list = content.findAll('a', title=True)

            for item in a_list:

                href = item.get("href")
                url = PREFIX + href

                if (not href.startswith("/wiki")) or (":" in href) \
                        or "class" in item.attrs and item["class"][0] == "external text" \
                        or "#" in href:
                    continue
                # handle redirect_url
                if "class" in item.attrs and item["class"][0] == "mw-redirect":
                    redirect_page = requests.get(url).text
                    time.sleep(1)
                    redirect = sp(redirect_page, "html.parser")
                    url = redirect.find("link", rel="canonical").get("href")

                if count < THRESHOLD and url not in result_url:
                    if not is_focus or has_keyword(keyword, item, url):
                        result_url.append(url)
                        q.appendleft(url)
                        parameter_list.append(str(depth) + "\t" + str(url_index) + "\t" + str(dis))
                        dis += 1
                        count += 1
                        print("valid url is " + url)
                        print("depth is " + str(depth))
                        print("count is " + str(count))

                elif count == THRESHOLD:
                    write_to_txt(result_url, parameter_list)
                    #save_html(result_url)
                    return 0

            url_index += 1
        depth += 1

    write_to_txt(result_url, parameter_list)


def write_to_txt(result, parameter):
    f_url = open(url_path, "w")
    num = 0
    for i in result:
        f_url.write(i + "\t" + parameter[num] + "\n")
        num += 1

    f_url.close()


def save_html(result_url):
    os.mkdir(html_folder_path)
    index = 1
    print("Save html Begin...")
    for url in result_url:
        print("saving num " + str(index))
        response = requests.get(url).text
        time.sleep(1)
        html = sp(response, "html.parser").text
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


bfs(seed_url_3, "green")

# response = requests.get(seed_url_1).text
# root = sp(response, "html.parser")
# content = root.find('div', id='bodyContent')
# tables = content.findAll("table")
# for table in tables:
#     table.decompose()
# print(root)

