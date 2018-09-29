import time
from bs4 import BeautifulSoup as sp
import requests
from queue import Queue

q = Queue()
result_url = []

seed_url = "https://en.wikipedia.org/wiki/Time_zone"
q.put(seed_url)
depth = 1

def BFS():
    while not q.empty() :
        size = q.qsize()
        for i in range (0, size):
            cur = q.get()
            response = requests.get(cur).text
            time.sleep(1)

            root = sp(response, "html.parser")
            content = root.find('div', id='bodyContent')
            print(content)



BFS()

