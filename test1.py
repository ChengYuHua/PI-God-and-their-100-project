"""
from selenium import webdriver
from django.utils.encoding import smart_str

url = 'http://www.w3.org/1999/xhtml'
driver = webdriver.PhantomJS("./phantomjs")

print(driver)
"""


import requests

headers = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

r = requests.get('https://ecshweb.pchome.com.tw/search/v3.3/?q=%E7%B1%B3&scope=all&sortParm=sale&sortOrder=dc&cateId=DBBY', headers=headers)
r.encoding = 'utf-8'

print(r.request.headers)    # 看requests送出的header
print(r.text)
