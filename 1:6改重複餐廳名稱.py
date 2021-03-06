import tkinter as tk
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from lxml import etree
import re
import numpy as np
import jieba
import csv
from tkinter import ttk
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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
        flag_pos_neg = 0  # 正的代表正評，富的代表富屏
        flag_small = 0
        for j in range(1, 4):  # 在第i個名詞中檢查前後j個形容詞與否定詞
            if i + j < len(clean_text):  # debug
                if clean_text[i + j] in corpus['good']:
                    if flag_pos_neg == 0:
                        flag_pos_neg = 1
                    if clean_text[i + j - 1] in corpus['negative']:
                        flag_pos_neg *= -1
                elif clean_text[i + j] in corpus['bad']:
                    if flag_pos_neg == 0:
                        flag_pos_neg = -1
                    if clean_text[i + j - 1] in corpus['negative']:
                        flag_pos_neg *= -1

            if flag_pos_neg == 1:
                flag_small += 1
            elif flag_pos_neg == -1:
                flag_small -= 1
            flag_pos_neg = 0
            if i - j >= 0:
                if clean_text[i - j] in corpus['good']:
                    if flag_pos_neg == 0:
                        flag_pos_neg = 1
                    if i - j - 1 >= 0:
                        if clean_text[i - j - 1] in corpus['negative']:
                            flag_pos_neg *= -1
                elif clean_text[i - j] in corpus['bad']:
                    if flag_pos_neg == 0:
                        flag_pos_neg = -1
                    if i - j - 1 >= 0:
                        if clean_text[i - j - 1] in corpus['negative']:
                            flag_pos_neg *= -1
            if flag_pos_neg == 1:
                flag_small += 1
            elif flag_pos_neg == -1:
                flag_small -= 1

        if flag_small > 0:
            cnt += 1
        elif flag_small < 0:
            cnt -= 1
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
    total = [0, 0]
    service = [0, 0]
    food = [0, 0]
    cp = [0, 0]
    env = [0, 0]
    reach = [0, 0]
    speed = [0, 0]
    name = ' '


# loading the corpus  # 開csv檔的程式
corpus = {}
with open('/Users/sdtaiwan/Desktop/Corpus.csv', newline='', encoding='utf-8') as f:
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


# 會是針對個別的文章 先比較一篇文章的正負評，比大小算出100 010 001那些，然後累加到xx_score的矩陣中
def rest_count(a_clean_text):
    service_cnt = 0
    food_cnt = 0
    cp_cnt = 0
    speed_cnt = 0
    environment_cnt = 0
    reachable_cnt = 0

    for abc, term in enumerate(a_clean_text):
        service_cnt += determine_amount(a_clean_text, abc, "service", corpus)
        food_cnt += determine_amount(a_clean_text, abc, "food", corpus)
        cp_cnt += determine_amount(a_clean_text, abc, "cp", corpus)
        speed_cnt += determine_amount(a_clean_text, abc, "speed", corpus)
        environment_cnt += determine_amount(a_clean_text, abc, "environment", corpus)
        reachable_cnt += determine_amount(a_clean_text, abc, "reachable", corpus)

    total_cnt = service_cnt + food_cnt + cp_cnt + speed_cnt + environment_cnt + reachable_cnt

    # 六面向+總體的矩陣，算累績分數
    # xxx_score是單篇文章的矩陣，有100、010、001
    total_score = check_pos_neg(total_cnt)
    service_score = check_pos_neg(service_cnt)
    food_score = check_pos_neg(food_cnt)
    cp_score = check_pos_neg(cp_cnt)
    speed_score = check_pos_neg(speed_cnt)
    environment_score = check_pos_neg(environment_cnt)
    reachable_score = check_pos_neg(reachable_cnt)
    return total_score, service_score, food_score, cp_score, environment_score, reachable_score, speed_score


# 從google map爬餐廳會用到的函數：parser、restaurant_crawler
def parser():
    html = driver.page_source
    parser_soup = BeautifulSoup(html, 'html.parser')
    items = parser_soup.find_all("div", attrs={"class": "dbg0pd"})
    items = [parser_i.text for parser_i in items]
    return items


user_agents = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'
driver = webdriver.Chrome(executable_path="/Users/sdtaiwan/Desktop/chromedriver")


def restaurant_crawler(food_local, place_local):
    restaurants = []
    last_page = False

    google_url = 'https://www.google.com.tw/search?q='
    driver.get(google_url + food_local + "+" + place_local)
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
    google_results = requests.get(google_url + keywords + site, user_agents)
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
    try:
        title = ptt_soup.find_all("span", attrs={"class": "article-meta-value"})[2].text
        first_floor = ptt_selector.xpath('//*[@id="main-content"]/text()[1]')
        check_item = title + first_floor[0]
        if check_content(check_item, restaurant_name) is True:
            push = soup.find_all("span", attrs={"class": "f3 push-content"})
            push = [ptt_p.text for ptt_p in push]
            article = check_item + ''.join(push)
            return article
        else:
            return None
    except:
        return None


def dcard_crawler(dcard_soup, restaurant_name):  # 餐廳的一個屬性
    try:
        title = dcard_soup.find_all("h1", attrs={"class": "Post_title_2O-1el"})[0].text
        first_floor = dcard_soup.find_all("div", attrs={"class": "Post_content_NKEl9d"})[0].text
        check_item = title + first_floor
        if check_content(check_item, restaurant_name) is True:  # 還要傳keyword進去
            push = dcard_soup.find_all("div", attrs={"class": "CommentEntry_content_1ATrw1"})
            push = [p.text for p in push]
            article = check_item + ''.join(push)
            return article
        else:
            return None
    except:
        return None


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


def find_rest(food_type, place):
    restaurants_list = restaurant_crawler(food_type, place)  # 使用爬蟲從google map找出所有符合條件的餐廳，用list的形式存入restaurants 的 list
    number = 0  # 計算餐廳數
    for i in range(len(restaurants_list)):  # 使用 for 迴圈從 restaurants 的 list 裡，一家一家餐廳抓出來
<<<<<<< HEAD:1:6改重複餐廳名稱.py
        if i <= 4:  # 可改參數
            number += 1
=======
        if i <= 5:  # 可改參數
            number += 1  # 餐廳數+1
>>>>>>> 7a43a332826c395197df5b1f8aa3ff3ed82dfb2c:圓餅圖.py
            store_i = i
            restaurant_objects[i].name = restaurants_list[i]  # restaurant_objects[i] 是 class
            all_urls = []
            total_add = np.array([0, 0, 0])
            service_add = np.array([0, 0, 0])
            food_add = np.array([0, 0, 0])
            cp_add = np.array([0, 0, 0])
            env_add = np.array([0, 0, 0])
            reach_add = np.array([0, 0, 0])
            speed_add = np.array([0, 0, 0])
            for a_site in sites:
                all_urls.append(google_crawler(restaurants_list[i], a_site))
            for j in range(len(all_urls)):  # 輸入順序，選擇論壇
                # 一家餐廳在各篇文章中，六面向的正負比例

                for k in range(len(all_urls[j])):  # 輸入各個網址，爬出文章
                    results = requests.get(all_urls[j][k])
                    results.encoding = 'utf-8'
                    soup = BeautifulSoup(results.text, 'html.parser')
                    if j == 0:
                        selector = etree.HTML(results.text)
                        article = ptt_crawler(soup, selector, restaurants_list[i])
                    elif j == 1:
                        article = dcard_crawler(soup, restaurants_list[i])
                    elif j == 2:
                        article = ifoodie_crawler(soup)
                    elif j == 3:
                        article = pixnet_crawler(soup)
                    else:
                        continue
                    if type(article) == 'NoneType' or article is None:
                        continue
                    else:
                        clean_text = text_clean(article)

                    article_total, article_service, article_food, article_cp, article_env, article_reach, article_speed = rest_count(
                        clean_text)
                    # 單篇文章累加成一家餐廳
                    total_add += article_total
                    service_add += article_service
                    food_add += article_food
                    cp_add += article_cp
                    env_add += article_env
                    reach_add += article_reach
                    speed_add += article_speed
            i = store_i
            # 最後會輸出的是 一間餐廳的總文章正負比例
            restaurant_objects[i].total = [int(total_add[0]) / int((total_add[0] + total_add[1] + total_add[2])),
                                           int(total_add[2]) / int((total_add[0] + total_add[1] + total_add[2]))]
            restaurant_objects[i].service = [
                int(service_add[0]) / int((service_add[0] + service_add[1] + service_add[2])),
                int(service_add[2]) / int((service_add[0] + service_add[1] + service_add[2]))]
            restaurant_objects[i].food = [int(food_add[0]) / int((food_add[0] + food_add[1] + food_add[2])),
                                          int(food_add[2]) / int((food_add[0] + food_add[1] + food_add[2]))]
            restaurant_objects[i].cp = [int(cp_add[0]) / int((cp_add[0] + cp_add[1] + cp_add[2])),
                                        int(cp_add[2]) / int((cp_add[0] + cp_add[1] + cp_add[2]))]
            restaurant_objects[i].speed = [int(speed_add[0]) / int((speed_add[0] + speed_add[1] + speed_add[2])),
                                           int(speed_add[2]) / int((speed_add[0] + speed_add[1] + speed_add[2]))]
            restaurant_objects[i].env = [int(env_add[0]) / int((env_add[0] + env_add[1] + env_add[2])),
                                         int(env_add[2]) / int((env_add[0] + env_add[1] + env_add[2]))]
            restaurant_objects[i].reach = [int(reach_add[0]) / int((reach_add[0] + reach_add[1] + reach_add[2])),
                                           int(reach_add[2]) / int((reach_add[0] + reach_add[1] + reach_add[2]))]

        else:
            break

    # 排序
    # 下列各list會裝各家餐廳的各項總分
    all_total = []
    all_service = []
    all_food = []
    all_cp = []
    all_env = []
    all_reach = []
    all_speed = []
    for i in range(number):
        all_total.append(restaurant_objects[i].total[0])
        all_service.append(restaurant_objects[i].service[0])
        all_food.append(restaurant_objects[i].food[0])
        all_cp.append(restaurant_objects[i].cp[0])
        all_env.append(restaurant_objects[i].env[0])
        all_reach.append(restaurant_objects[i].reach[0])
        all_speed.append(restaurant_objects[i].speed[0])

    # 下列各list會裝排序過後的餐廳總分，用index表示是第幾個object
    total_sort = []
    service_sort = []
    food_sort = []
    cp_sort = []
    env_sort = []
    reach_sort = []
    speed_sort = []

    for i in range(len(all_total)):  # 每跑一個迴圈可以找到未被選取過的數值中的最大值
        max_total = all_total[i]
        max_service = all_service[i]
        max_food = all_food[i]
        max_cp = all_cp[i]
        max_env = all_env[i]
        max_reach = all_reach[i]
        max_speed = all_speed[i]
        total_index = i
        service_index = i
        food_index = i
        cp_index = i
        env_index = i
        reach_index = i
        speed_index = i

        for j in range(len(all_total)):  # 把每一個數字和現有的最大值比較，找出最大的數值
            if all_total[j] > max_total:
                max_total = all_total[j]
                total_index = j
            if all_service[j] > max_service:
                max_service = all_service[j]
                service_index = j
            if all_food[j] > max_food:
                max_food = all_food[j]
                food_index = j
            if all_cp[j] > max_cp:
                max_cp = all_cp[j]
                cp_index = j
            if all_env[j] > max_env:
                max_env = all_env[j]
                env_index = j
            if all_reach[j] > max_reach:
                max_reach = all_reach[j]
                reach_index = j
            if all_speed[j] > max_speed:
                max_speed = all_speed[j]
                speed_index = j
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
    return restaurant_objects, total_sort, service_sort, food_sort, cp_sort, env_sort, reach_sort, speed_sort


x = str()
y = str()
aa = []
bb = []
cc = []
dd = []
ee = []
ff = []
gg = []
hh = []

window = tk.Tk()
# 設定視窗標題、大小和背景顏色
window.title('食神')
window.geometry('600x1000')
window.configure(background='white')


def calculate_food():
    global x, y, aa, bb, cc, dd, ee, ff, gg, hh
    x = str(height_entry.get())
    y = str(weight_entry.get())
    aa, bb, cc, dd, ee, ff, gg, hh = find_rest(x, y)

    firstscore = str(round(aa[bb[0]].total[0], 2)*100) + "%"
    firstname = aa[bb[0]].name
    secondscore = str(round(aa[bb[1]].total[0], 2)*100) + "%"
    secondname = aa[bb[1]].name
    thirdscore = str(round(aa[bb[2]].total[0], 2) * 100) + "%"
    thirdname = aa[bb[2]].name

    result = 'No.1 推薦餐廳：{}  好評度：{}'.format(firstname,firstscore)
    result_label.configure(text=result)
    result2 = 'No.2 推薦餐廳：{}  好評度：{}'.format(secondname,secondscore)
    result_label2.configure(text=result2)
    result3 = 'No.3 推薦餐廳：{}  好評度：{}'.format(thirdscore,thirdname)
    result_label3.configure(text=result3)

# def callbackFunc():
#     if comboitem.get() == '餐點':
#         firstscore = str(round(aa[bb[0]].total[0], 2) * 100) + "%"
#         firstname = aa[bb[0]].name
#         secondscore = str(round(aa[bb[1]].total[0], 2) * 100) + "%"
#         secondname = aa[bb[1]].name
#         thirdscore = str(round(aa[bb[2]].total[0], 2) * 100) + "%"
#         thirdname = aa[bb[2]].name
#         result = 'No.1 推薦餐廳：{}  好評度：{}'.format(firstname, firstscore)
#         result_label.configure(text=result)
#         result2 = 'No.2 推薦餐廳：{}  好評度：{}'.format(secondname, secondscore)
#         result_label2.configure(text=result2)
#         result3 = 'No.3 推薦餐廳：{}  好評度：{}'.format(thirdscore, thirdname)
#         result_label3.configure(text=result3)



"""
    orange = aa[bb[1]].total[0]
    orange = str(round(float(orange), 2) * 100)
    orange += "%"
    banana = aa[bb[1]].name

    tomato = aa[bb[2]].total[0]
    tomato = str(round(float(tomato), 2) * 100)
    tomato += "%"
    pig = aa[bb[0]].name

    result = 'No.1 推薦餐廳：{} {}No.2 推薦餐廳：{} {}No.3 推薦餐廳：{} {}'.format(pineapple, apple, orange, banana, tomato, pig)"""


header_label = tk.Label(window, text='美食推薦系統')
header_label.grid(row=0,column=1,columnspan=2)

# 以下為 height_frame 群組
height_frame = tk.Frame(window)
# 向上對齊父元件
height_label = tk.Label(text='食物種類')
height_label.grid(row=1,column=0,columnspan=2,sticky=tk.E)
height_entry = tk.Entry()
height_entry.grid(row=1,column=2,columnspan=2,sticky=tk.W)

# 以下為 weight_frame 群組

weight_label = tk.Label(text='地點')
weight_label.grid(row=2,column=0,columnspan=2,sticky=tk.E)
weight_entry = tk.Entry()
weight_entry.grid(row=2,column=2,columnspan=2,sticky=tk.W)

calculate_btn = tk.Button(window, text='GO', command=calculate_food)
calculate_btn.grid(row=3,column=1,columnspan=2)
combo_item = ttk.Combobox(window, value=['總評', '服務', '餐點', 'CP值', '環境', '交通', '速度'])
combo_item.grid(row=4,column=1)
comboitem.bind("<<ComboboxSelected>>", self.callbackFunc) #下拉式選單呼叫
result_label = tk.Label(window,text='apple')
result_label.grid(row=5,column=1,sticky=tk.W)
result_label2 = tk.Label(window,text='banana')
result_label2.grid(row=6,column=1,sticky=tk.W)
result_label3 = tk.Label(window,text='car')
result_label3.grid(row=7,column=1,sticky=tk.W)

# 運行主程式
window.mainloop()
