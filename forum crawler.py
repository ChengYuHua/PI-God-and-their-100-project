import requests
from bs4 import BeautifulSoup
from lxml import etree


def check_content(content, keyword):  # 檢查該篇討論串討論主題是否為目標餐廳
    correct = 0
    for char in keyword[0:4]:
        if char in content:
            correct += 1
    if correct >= 2:
        return True
    else:
        return False


def ptt_crawler(results, soup, selector):  # 餐廳的一個屬性
    title = soup.find_all("span", attrs={"class": "article-meta-value"})[2].text
    firstFloor = selector.xpath('//*[@id="main-content"]/text()[1]')
    checkItem = title+firstFloor[0]
    if check_content(checkItem):
        push = soup.find_all("span", attrs={"class": "f3 push-content"})
        push = [p.text for p in push]
        article = checkItem+''.join(push)
        return article
    else:
        return None


def dcard_crawler(results, soup):  # 餐廳的一個屬性
    title = soup.find_all("h1", attrs={"class": "Post_title_2O-1el"})[0].text
    firstFloor = soup.find_all("div", attrs={"class": "Post_content_NKEl9d"})[0].text
    checkItem = title+firstFloor
    if check_content(checkItem):
        push = soup.find_all("div", attrs={"class": "CommentEntry_content_1ATrw1"})
        push = [p.text for p in push]
        article = checkItem+''.join(push)
        return article
    else:
        return None


results = requests.get("https://www.dcard.tw/f/nccu/p/231015687")
soup = BeautifulSoup(results.text, 'html.parser')
selector = etree.HTML(results.text)

print(dcard_crawler(results, soup))
