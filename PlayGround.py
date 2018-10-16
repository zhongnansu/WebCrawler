import time
from bs4 import BeautifulSoup as sp
import requests
from collections import deque
import os


# path = os.getcwd() + "/" + "folder"
# os.mkdir(path)
#
# # file = open(path, 'w')
#
# print(os.getcwd()
from collections import deque

# path = "test_folder/1.txt"
# html = open(path, "r")
#
# soup = sp(html, "html.parser")
# a_list = soup.findAll('a', title=True)
# for item in a_list:
#     href = item.get("href")
#     print(href)




def save_html(result_url):
    html_folder_path = os.getcwd() + "/" + "w2" + "_folder"
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

path = "w2.txt"
list = open(path, "r")
save_html(list)