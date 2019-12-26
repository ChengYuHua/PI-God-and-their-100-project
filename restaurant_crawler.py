import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def parser():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", attrs={"class": "dbg0pd"})
    # print(soup.prettify())
    items = [i.text for i in items]
    return items


user_agents = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'
driver = webdriver.Chrome(executable_path="/Users/evacheng/Desktop/chromedriver")


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

print(restaurants)
driver.close()
