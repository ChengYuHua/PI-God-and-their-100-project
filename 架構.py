import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from lxml import etree
import re
import numpy as np
import jieba
import csv

foodType = input()  # 輸入食物種類
place = input()  # 輸入地點

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


# clean all the punctuation and others 把文章斷詞的def（已經debug）
def text_clean(text):
    text = text.lower()
    text = re.sub('<br>', ' ', text)
    text = re.sub("http://[a-zA-z./\d]*", " ", text)
    text = re.sub('[0-9]+', ' ', text)
    text = re.sub('_+', ' ', text)
    text = re.sub('[^\w\s]', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\r', ' ', text)
    text = re.sub(r'[ぁ-ゟ]', ' ', text)
    text = re.sub(r'[゠-ヿ]', ' ', text)
    text = re.sub(' +', ' ', text)
    seg_list = jieba.cut(text)
    clean_text = []
    for term in list(seg_list):
        if (term.isalpha()):
            clean_text.append(term)
    return clean_text


# 檢查一篇文章裡，六個面向的正負詞的計數，確定可以用的 def（已經debug）
def determine_amount(clean_text, i, topic, corpus):
    cnt = 0
    if clean_text[i] in corpus[topic]:
        flag_exist = 0
        flag_good = 0
        flag_bad = 0
        for j in range(1, 4):
            if clean_text[i + j] in corpus['good']:
                flag_exist = 1
                if clean_text[i + j - 1] in corpus['negative']:
                    flag_good = 1
            elif clean_text[i + j] in corpus['bad']:
                flag_exist = -1
                if clean_text[i + j - 1] in corpus['negative']:
                    flag_bad = 1
        if flag_exist == 1 and flag_good == 0:
            cnt += 1
        elif flag_exist == 1 and flag_good == 1:
            cnt -= 1
        elif flag_exist == -1 and flag_bad == 0:
            cnt -= 1
        elif flag_exist == -1 and flag_bad == 1:
            cnt += 1
    elif clean_text[i] in corpus[topic + "_good"]:
        if i > 0:
            if clean_text[i - 1] in corpus['negative']:
                cnt -= 1
            else:
                cnt += 1
        else:
            cnt += 1
    elif clean_text[i] in corpus[topic + "_bad"]:
        if i > 0:
            if clean_text[i - 1] in corpus['negative']:
                cnt += 1
            else:
                cnt -= 1
        else:
            cnt -= 1
    return cnt

# 把文章計數轉換成001 100 010 等等 的def（已debug）
# Check if the cnt is positive and return np.array
def check_pos_neg(cnt):
    if cnt > 0:
        return np.array([1, 0, 0])
    elif cnt == 0:
        return np.array([0, 1, 0])
    elif cnt < 0:
        return np.array([0, 0, 1])


# build the restaurant class and store all the parameters
class Restaurant:
    total = np.array([0, 0])
    service = np.array([0, 0])
    food = np.array([0, 0])
    cp = np.array([0, 0])
    env = np.array([0, 0])
    reach = np.array([0, 0])
    speed = np.array([0, 0])
    name = ' '


# 為了檢查計數def能不能用而寫出的爬蟲程式，可省
url = (
    'http://gotwtop1.pixnet.net/blog/post/326852833-%E3%80%90%E5%8F%B0%E5%8C%97-%E4%B8%AD%E6%AD%A3%E3%80%91%E7%99%BC%E7%8F%BE%E7%BE%A9%E5%A4%A7%E5%88%A9%E9%BA%B5-%E5%85%AC%E9%A4%A8%E5%95%86%E5%9C%88-%E5%8F%B0%E5%A4%A7-')
r = requests.get(url)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')

total_text = ""
p_tags = soup.find_all('p')
for tag in p_tags:
    total_text += tag.get_text()
    print(tag.get_text())
clean_text = text_clean(total_text)

# loading the corpus  # 開csv檔的程式
corpus = {}
with open('/Users/mac/Desktop/Corpus.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        temp = []
        key = ""
        for i, term in enumerate(row):
            if term == '\ufeffgood':
                key += 'good'
            elif i == 0:
                key += term
            elif term.isalpha():
                temp.append(term)
        corpus[key] = temp



# Complete Structure below
total_cnt = 0
service_cnt = 0
food_cnt = 0
cp_cnt = 0
speed_cnt = 0
environment_cnt = 0
reachable_cnt = 0
# 六面向+總體的矩陣，算累績分數
total_score = np.array([0, 0, 0])
service_score = np.array([0, 0, 0])
food_score = np.array([0, 0, 0])
cp_score = np.array([0, 0, 0])
speed_score = np.array([0, 0, 0])
environment_score = np.array([0, 0, 0])
reachable_score = np.array([0, 0, 0])

# 一家餐廳在各篇文章中，六面向的正負比例
total = np.array([0, 0])
service = np.array([0, 0])
food = np.array([0, 0])
cp = np.array([0, 0])
env = np.array([0, 0])
reach = np.array([0, 0])
speed = np.array([0, 0])

    # 第二層會是針對該餐廳的文章
    for clean_text in articles['res']: # articles也是dict，裡面也是餐廳的名詞，values是各篇文章
        #第三層會是針對個別的文章 先比較一篇文章的正負評，比大小算出100 010 001那些，然後累加到xx_score的矩陣中
        for i, term in enumerate(clean_text):
                total_cnt = service_cnt + food_cnt + cp_cnt + speed_cnt + environment_cnt + reachable_cnt
                service_cnt += determine_amount(clean_text, i, "service", corpus)
                food_cnt += determine_amount(clean_text, i, "food", corpus)
                cp_cnt += determine_amount(clean_text, i, "cp", corpus)
                speed_cnt += determine_amount(clean_text, i, "speed", corpus)
                environment_cnt += determine_amount(clean_text, i, "environment", corpus)
                reachable_cnt += determine_amount(clean_text, i, "reachable", corpus)
        total_score += check_pos_neg(total_cnt)
        service_score += check_pos_neg(service_cnt)
        food_score += check_pos_neg(food_cnt)
        cp_score += check_pos_neg(cp_cnt)
        speed_score += check_pos_neg(speed_cnt)
        environment_score += check_pos_neg(environment_cnt)
        reachable_score += check_pos_neg(reachable_cnt)

# 最後會輸出的是 一間餐廳的總文章正負比例
    total[0] = total_score[0]/(total_score[0] + total_score[1] + total_score[2])
    total[1] = total_score[1] / (total_score[0] + total_score[1] + total_score[2])
    service[0] = service_score[0]/(service_score[0] + service_score[1] + service_score[2])
    service[1] = service_score[1] / (service_score[0] + service_score[1] + service_score[2])
    food[0] = food_score[0] / (food_score[0] + food_score[1] + food_score[2])
    food[1] = food_score[1] / (food_score[0] + food_score[1] + food_score[2])
    cp[0] = cp_score[0] / (cp_score[0] + cp_score[1] + cp_score[2])
    cp[1] = cp_score[1] / (cp_score[0] + cp_score[1] + cp_score[2])
    speed[0] = speed_score[0] / (speed_score[0] + speed_score[1] + speed_score[2])
    speed[1] = speed_score[1] / (speed_score[0] + speed_score[1] + speed_score[2])
    env[0] = environment_score[0] / (environment_score[0] + environment_score[1] + environment_score[2])
    env[1] = environment_score[1] / (environment_score[0] + environment_score[1] + environment_score[2])
    reach[0] = reachable_score[0] / (reachable_score[0] + reachable_score[1] + reachable_score[2])
    reach[1] = reachable_score[1] / (reachable_score[0] + reachable_score[1] + reachable_score[2])




# 驊有更好的寫法
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


def restaurant_crawler(food_local, place_local):
    restaurants = []
    last_page = False

    google_url = 'https://www.google.com.tw/search?q='
    driver.get(google_url+food_local+"+"+place_local)
    time.sleep(2)

    more_place = driver.find_element_by_class_name("i0vbXd").click()
    restaurants += parser()

    while last_page is False:
        try:
            next_page = driver.find_element_by_id("pnnext").click()
            restaurants += parser()
            time.sleep(2)
        except:
            last_page = True

    driver.close()
    return restaurants


def google_crawler(keywords, site):  # 餐廳的一個屬性，keywords為查詢的關鍵字
    google_url = 'https://www.google.com.tw/search?q='
    google_results = requests.get(google_url+keywords+site, user_agents)
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


sites = ["site:www.ptt.cc", "site:www.dcard.tw", "site:ifoodie.tw", "痞客邦"]
'''
all_urls = []
for a_site in sites:  # 在主程式碼
    all_urls.append(google_crawler(keywords, a_site))
'''

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


def ptt_crawler(ptt_soup, ptt_selector, restaurant_name):  # 餐廳的一個屬性
    title = ptt_soup.find_all("span", attrs={"class": "article-meta-value"})[2].text
    first_floor = ptt_selector.xpath('//*[@id="main-content"]/text()[1]')
    check_item = title+first_floor[0]
    if check_content(check_item, restaurant_name) is True:
        push = soup.find_all("span", attrs={"class": "f3 push-content"})
        push = [ptt_p.text for ptt_p in push]
        article = check_item+''.join(push)
        return article
    else:
        return None


def dcard_crawler(dcard_soup, restaurant_name):  # 餐廳的一個屬性
    title = dcard_soup.find_all("h1", attrs={"class": "Post_title_2O-1el"})[0].text
    first_floor = dcard_soup.find_all("div", attrs={"class": "Post_content_NKEl9d"})[0].text
    check_item = title+first_floor
    if check_content(check_item, restaurant_name) is True:  # 還要傳keyword進去
        push = dcard_soup.find_all("div", attrs={"class": "CommentEntry_content_1ATrw1"})
        push = [p.text for p in push]
        article = check_item+''.join(push)
        return article
    else:
        return None


url = 'https://ifoodie.tw/post/5dea600d2261390a2235125d-%E5%8F%B0%E5%8C%97%E8%90%AC%E8%8F%AF%E6%96%B0%E5%8C%97%E4%B8%89%E9%87%8D%E8%B6%85%E5%A5%BD%E5%90%83%E8%8A%B1%E7%94%9F%E6%B2%BE%E9%86%AC%E7%9F%B3%E9%A0%AD%E7%81%AB%E9%8D%8B%E6%8E%A8'
results = requests.get(url)
results.encoding='utf-8'
soup = BeautifulSoup(results.text, 'html.parser')
selector = etree.HTML(results.text)  # 只有ptt會用到

def ifoodie_crawler(ifoodie_soup):
    p_tags = ifoodie_soup.find_all('p')
    article = str()
    for tag in p_tags:
        article += tag.get_text()
    return article

def pixnet_crawler(pixnet_soup):
    p_tags = pixnet_soup.find_all('p')
    article = str()
    for tag in p_tags:
        article += tag.get_text()
    return article

restaurants_list = restaurant_crawler(foodType, place)  # 使用爬蟲從google map找出所有符合條件的餐廳，用list的形式存入restaurants 的 list
for i in restaurants_list: # 使用 for 迴圈從 restaurants 的 list 裡，一家一家餐廳抓出來
    if i <= 25:
        restaurant_objects[i].name = i  # restaurant_objects[i] 是 class
        all_urls = []
        for a_site in sites:
            all_urls.append(google_crawler(i, a_site))
        for j in range(len(all_urls)):
            for k in range(len(all_urls[j])):
                results = requests.get(url)
                results.encoding = 'utf-8'
                soup = BeautifulSoup(results.text, 'html.parser')
                if j == 0:
                    selector = etree.HTML(results.text)
                    article = ptt_crawler(soup, selector, i)
                elif j == 1:
                    article = dcard_crawler(soup, i)
                elif j == 2:
                    article = ifoodie_crawler(soup)
                elif j == 3:
                    article = pixnet_crawler(soup)
                else:
                    break
                restaurant_objects[i].total, restaurant_objects[i].service, restaurant_objects[i].food, restaurant_objects[i].cp, restaurant_objects[i].env, restaurant_objects[i].reach, restaurant_objects[i].speed += rest_count()

    else:
        break

# 下列各list會裝各家餐廳的各項總分
all_total = []
all_service = []
all_food = []
all_cp = []
all_env = []
all_reach = []
all_speed = []
for i in restaurant_objects:
    all_total.append(restaurant_objects[i].total)
    all_service.apppend(restaurant_objects[i].service)
    all_food.append(restaurant_objects[i].food)
    all_cp.append(restaurant_objects[i].cp)
    all_env.append(restaurant_objects[i].env)
    all_reach.append(restaurant_objects[i].reach)
    all_speed.append(restaurant_objects[i].speed)

# 下列各list會裝排序過後的餐廳總分，用index表示是第幾個object
total_sort = []
service_sort = []
food_sort = []
cp_sort = []
env_sort = []
reach_sort = []
speed_sort = []

for i in range(len(all_total)):  # 每跑一個迴圈可以找到未被選取過的數值中的最大值
    max_total = -1
    max_service = -1
    max_food = -1
    max_cp = -1
    max_env = -1
    max_reach = -1
    max_speed = -1
    for j in range(len(total)):  # 把每一個數字和現有的最大值比較，找出最大的數值
        if all_total[j] > max_total:
            max_total = all_total[i]
            total_index = i
        if all_service[j] > max_service:
            max_service = all_service[i]
            service_index = i
        if all_food[j] > max_food:
            max_food = all_food[i]
            food_index = i
        if all_cp[j] > max_cp:
            max_cp = all_cp[i]
            cp_index = i
        if all_env[j] > max_env:
            max_env = all_env[i]
            env_index = i
        if all_reach[j] > max_reach:
            max_reach = all_reach[i]
            reach_index = i
        if all_speed[j] > max_speed:
            max_speed = all_speed[i]
            speed_index = i
    # 找到最大值後，存取index，並把最大值的位置改寫為０
    total_sort.append(total_index)
    service_sort.append(service_index)
    food_sort.append(food_index)
    cp_sort.append(cp_index)
    env_sort.append(env_index)
    reach_sort.append(reach_index)
    speed_sort.append(speed_index)

    all_total[total_index] = 0
    all_service[service_index] = 0
    all_food[food_index] = 0
    all_cp[cp_index] = 0
    all_env[env_index] = 0
    all_reach[reach_index] = 0
    all_speed[speed_index] = 0


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
