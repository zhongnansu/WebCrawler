# WebCrawler
### Set up:
install python 3.5
pip install two packages
```
pip install beautifulsoup4
pin install requests
```
### Run:
The entry is in WebCrawler.py
```
python WebCrawler.py
```
Then the program ask input from you before it runs the crawler. You have to provide parameters such as the task name, how many urls and depths you want to crawl, whether you want to save the raw html. For example:
```
Give the task name:
t5
give a seed url:
https://en.wikipedia.org/wiki/Time_zone
Give the keyword, if you don't want focus search, press enter
time
How many urls do you want to crawl at most?
15
How many depth do you want to crawl at most?
3
Do you want to save the raw html?[y]/[n]
y
Start Crawling...

```
### Report of Depth:
- Task 1: all three seed urls takes depth 2 to reach the 1000 urls and saved as task1_1.txt, task1_2.txt and task1_3.txt
- Task3: It reached depth 6 to get 373 urls.

