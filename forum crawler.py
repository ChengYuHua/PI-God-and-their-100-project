import requests
from bs4 import BeautifulSoup
from lxml import etree


def check_content(content):  # 待討論！
    return True


def ptt_crawler(results, soup, selector):  # 餐廳的一個屬性
    title = soup.find_all("span", attrs={"class": "article-meta-value"})[2].text
    firstFloor = selector.xpath('//*[@id="main-content"]/text()[1]')
    checkItem = title+firstFloor[0]
    checkedTopic = check_content(checkItem)
    push = soup.find_all("span", attrs={"class": "f3 push-content"})
    push = [p.text for p in push]
    article = checkItem+''.join(push)
    return article


def dcard_crawler(results, soup):  # 餐廳的一個屬性
    title = soup.find_all("h1", attrs={"class": "Post_title_2O-1el"})[0].text
    firstFloor = soup.find_all("div", attrs={"class": "Post_content_NKEl9d"})[0].text
    checkItem = title+firstFloor
    checkedTopic = check_content(checkItem)
    push = soup.find_all("div", attrs={"class": "CommentEntry_content_1ATrw1"})
    push = [p.text for p in push]
    article = checkItem+''.join(push)
    return article


results = requests.get("https://www.dcard.tw/f/nccu/p/231015687")
soup = BeautifulSoup(results.text, 'html.parser')
selector = etree.HTML(results.text)

print(dcard_crawler(results, soup))
