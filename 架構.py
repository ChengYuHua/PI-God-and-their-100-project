import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
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


# 使用爬蟲從google map找出所有符合條件的餐廳，用list的形式存入restaraunts_list
def parser():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", attrs={"class": "dbg0pd"})
    items = [i.text for i in items]
    return items


user_agents = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'
driver = webdriver.Chrome(executable_path="chromedriver")


def restaurant_crawler(user_agents, driver):
    foodType = input()
    place = input()
    restaurants = []
    last_page = False

    google_url = 'https://www.google.com.tw/search?q='
    driver.get(google_url+foodType+"+"+place)
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

"""
使用 for 迴圈從 restaraunts_list 裡，一家一家餐廳抓出來
把餐廳變成 Restaurant class
i = Restaurant()
用爬蟲找出該餐廳的文章網址，用list的形式存入該餐廳的Restaurant class中的ppt_url、dcard_url、ifoodie_url、pixnet_url

再跑一個迴圈 run 過所有該餐廳的評論文章(會以字串形式傳入)
用Aricle class計算文章的分數
計算玩分數後，紀錄於Restaurant class中
若一篇文正負評都沒有，就跳過。有的話就Restaraunt.articles += 1

餐廳的所有文章 run 完後，將餐廳名稱、各項分數編入 a_list，為該餐廳的 list
將 a_list 放入 all_score 的 list
持續 run 到所以餐廳都跑過為止

3.輸出
視使用者要什麼（輸入什麼）從 all_restaraunt 選取該項目的 index，進行比較，由高到低輸出

"""
