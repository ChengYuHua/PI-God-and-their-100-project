import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from lxml import etree
"""
1.前置作業
import 需要的 library
用excel建置六面向和總評的精準、模糊語料庫來判斷正、負評
讀入csv

服務：service_good、service_bad
餐點：food_good、food_bad
CP值：cp_good、cp_bad
環境：environment_good、environment_bad
交通易達性：reachable_good、reachable_bad
等待時間：speed_good、speed_bad

建餐聽的 class，專門計算細項分數
class Restaraunt:
# 第一個位置放累積正評數，第二個位置放累積中立數，第三個位置放累積負評數
# articles是累積文章數
    service = [0, 0, 0]
    food = [0, 0, 0]
    cp = [0, 0, 0]
    environment = [0, 0, 0]
    reachable = [0, 0, 0]
    speed = [0, 0, 0]
    total = [0, 0]  # 中立就跳過不要計
    articles = 0
    ptt_url = []  # ppt網址
    dcard_url = []  # dcard網址
    ifoodie_url = []  # ifoodie網址
    pixnet_url = []  # pixnet網址

    # 函數呼叫時，依序回傳該細項正評總分、中立總分和負評總分

    def total_service(self):
        return (self.service[0] / articles), (self.service[1] / articles) , (self.service[2] / articles)
    # 這邊只列一個，其他略過

建文章的class，用來計算單篇文章的各項分數
class Article:
    # 這邊放計算單篇文章的分數和細項的函數
    # aka語料庫比對的部分

讓使用者依序輸入地點和食物種類
location = input()
category = input()
建一個 all_score 的 list，之後會拿來存所有餐廳的評分和資訊

2.程式動起來
"""
class Restaurant:


A = Restaurant()
B = Restaurant()
C = Restaurant()
D = Restaurant()
E = Restaurant()
F = Restaurant()
G = Restaurant()
H = Restaurant()
I = Restaurant()
J = Restaurant()
K = Restaurant()
L = Restaurant()
M = Restaurant()
N = Restaurant()
O = Restaurant()
P = Restaurant()
Q = Restaurant()
R = Restaurant()
S = Restaurant()
T = Restaurant()
U = Restaurant()
V = Restaurant()
W = Restaurant()
X = Restaurant()
Y = Restaurant()
Z = Restaurant()
restaurant_objects = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z]


# 從google map爬餐廳會用到的函數：parser、restaurant_crawler
def parser():
    html = driver.page_source
    parser_soup = BeautifulSoup(html, 'html.parser')
    items = parser_soup.find_all("div", attrs={"class": "dbg0pd"})
    items = [parser_i.text for parser_i in items]
    return items


user_agents = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'
driver = webdriver.Chrome(executable_path="chromedriver")

foodType = input()
place = input()


def restaurant_crawler(food_local, place_local):
    restaurants = []
    last_page = False

    google_url = 'https://www.google.com.tw/search?q='
    driver.get(google_url+food_local+"+"+place_local)
    time.sleep(2)

    more_place = driver.find_element_by_class_name("i0vbXd").click()
    restaurants += parser()  # +=還是append？

    while last_page is False:
        try:
            next_page = driver.find_element_by_id("pnnext").click()
            restaurants += parser()  # +=還是append？
            time.sleep(2)
        except:
            last_page = True

    driver.close()
    return restaurants


sites = ["www.ptt.cc"]


def google_crawler(keywords):  # 餐廳的一個屬性，keywords為查詢的關鍵字
    google_url = 'https://www.google.com.tw/search?q='
    google_results = requests.get(google_url+keywords, user_agents)
    google_soup = BeautifulSoup(google_results.text, 'html.parser')

    items = google_soup.find_all("div", attrs={"class": "kCrYT"})
    urls = []
    for item in items:
        try:
            temp = item.find("a")["href"]
            urls.append(temp[temp.find("h"):temp.find("&s")])
        except:
            pass
    return urls


# 從論壇爬文章會用到的函數：check_content、ptt_crawler、dcard_crawler、、
def check_content(content, keyword):  # 檢查該篇討論串討論主題是否為目標餐廳
    correct = 0
    for char in keyword[0:4]:
        if char in content:
            correct += 1
    if correct >= 2:
        return True
    else:
        return False


def ptt_crawler(ptt_soup, ptt_selector):  # 餐廳的一個屬性
    title = ptt_soup.find_all("span", attrs={"class": "article-meta-value"})[2].text
    first_floor = ptt_selector.xpath('//*[@id="main-content"]/text()[1]')
    check_item = title+first_floor[0]
    if check_content(check_item):
        push = soup.find_all("span", attrs={"class": "f3 push-content"})
        push = [ptt_p.text for ptt_p in push]
        article = check_item+''.join(push)
        return article
    else:
        return None


def dcard_crawler(dcard_soup):  # 餐廳的一個屬性
    title = dcard_soup.find_all("h1", attrs={"class": "Post_title_2O-1el"})[0].text
    first_floor = dcard_soup.find_all("div", attrs={"class": "Post_content_NKEl9d"})[0].text
    check_item = title+first_floor
    if check_content(check_item):  # 還要傳keyword進去
        push = dcard_soup.find_all("div", attrs={"class": "CommentEntry_content_1ATrw1"})
        push = [p.text for p in push]
        article = check_item+''.join(push)
        return article
    else:
        return None

# ifoodie
url = 'https://ifoodie.tw/post/5dea600d2261390a2235125d-%E5%8F%B0%E5%8C%97%E8%90%AC%E8%8F%AF%E6%96%B0%E5%8C%97%E4%B8%89%E9%87%8D%E8%B6%85%E5%A5%BD%E5%90%83%E8%8A%B1%E7%94%9F%E6%B2%BE%E9%86%AC%E7%9F%B3%E9%A0%AD%E7%81%AB%E9%8D%8B%E6%8E%A8'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

p_tags = soup.find_all('p')
for tag in p_tags:
  print(tag.get_text())

results = requests.get("https://www.dcard.tw/f/nccu/p/231015687")
soup = BeautifulSoup(results.text, 'html.parser')
selector = etree.HTML(results.text)

# pixnet
url = ('http://gotwtop1.pixnet.net/blog/post/326852833-%E3%80%90%E5%8F%B0%E5%8C%97-%E4%B8%AD%E6%AD%A3%E3%80%91%E7%99%BC%E7%8F%BE%E7%BE%A9%E5%A4%A7%E5%88%A9%E9%BA%B5-%E5%85%AC%E9%A4%A8%E5%95%86%E5%9C%88-%E5%8F%B0%E5%A4%A7-')
r = requests.get(url)
r.encoding='utf-8'
soup = BeautifulSoup(r.text, 'html.parser')

p_tags = soup.find_all('p')
for tag in p_tags:
  print(tag.get_text())


restaurants_list = restaurant_crawler(foodType, place)  # 使用爬蟲從google map找出所有符合條件的餐廳，用list的形式存入restaurants 的 list
for i in restaurants_list: # 使用 for 迴圈從 restaurants 的 list 裡，一家一家餐廳抓出來
    # 把餐廳變成 Restaurant class
    i = Restaurant()
    """
    用爬蟲找出該餐廳的文章網址，用list的形式存入該餐廳的Restaurant class中的ppt_url、dcard_url、ifoodie_url、pixnet_url

    再跑一個迴圈 run 過所有該餐廳的評論文章(會以字串形式傳入)
    用Article class計算文章的分數
    計算玩分數後，紀錄於Restaurant class中
    若一篇文正負評都沒有，就跳過。有的話就Restaraunt.articles += 1

    餐廳的所有文章 run 完後，將餐廳名稱、各項分數編入 a_list，為該餐廳的 list
    將 a_list 放入 all_score 的 list
    持續 run 到所以餐廳都跑過為止
    """


"""
3.輸出
視使用者要什麼（輸入什麼）從 all_restaraunt 選取該項目的 index，進行比較，由高到低輸出
"""
