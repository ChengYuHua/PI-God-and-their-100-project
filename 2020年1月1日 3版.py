from collections import Counter
import os
import re
import math
import numpy as np
import heapq
import pickle
import jieba
import requests
from bs4 import BeautifulSoup
import csv


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
    if (clean_text[i] in corpus[topic]):
        flag_exist = 0
        flag_good = 0
        flag_bad = 0
        for j in range(1, 4):
            if (clean_text[i + j] in corpus['good']):
                flag_exist = 1
                if clean_text[i + j - 1] in corpus['negative']:
                    flag_good = 1
            elif (clean_text[i + j] in corpus['bad']):
                flag_exist = -1
                if clean_text[i + j - 1] in corpus['negative']:
                    flag_bad = 1
        if (flag_exist == 1 and flag_good == 0):
            cnt += 1
        elif (flag_exist == 1 and flag_good == 1):
            cnt -= 1
        elif (flag_exist == -1 and flag_bad == 0):
            cnt -= 1
        elif (flag_exist == -1 and flag_bad == 1):
            cnt += 1
    elif (clean_text[i] in corpus[topic + "_good"]):
        if (i > 0):
            if clean_text[i - 1] in corpus['negative']:
                cnt -= 1
            else:
                cnt += 1
        else:
            cnt += 1
    elif (clean_text[i] in corpus[topic + "_bad"]):
        if (i > 0):
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
    if (cnt > 0):
        return np.array([1, 0, 0])
    elif (cnt == 0):
        return np.array([0, 1, 0])
    elif (cnt < 0):
        return np.array([0, 0, 1])


# build the restaurant class and store all the parameters
class restaurant():
    def __init__(self, service_cnt, food_cnt, cp_cnt, speed_cnt, environment_cnt, reachable_cnt):
        self.total = np.array([0, 0])
        self.service = np.array([0, 0])
        self.food = np.array([0, 0])
        self.cp = np.array([0, 0])
        self.env = np.array([0, 0])
        self.reach = np.array([0, 0])
        self.speed = np.array([0, 0])
        self.name = ' '


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
            if (term == '\ufeffgood'):
                key += 'good'
            elif (i == 0):
                key += term
            elif (term.isalpha()):
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

    #第二層會是針對該餐廳的文章
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

