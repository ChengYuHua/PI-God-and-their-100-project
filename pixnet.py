import requests
from bs4 import BeautifulSoup

url = ('http://gotwtop1.pixnet.net/blog/post/326852833-%E3%80%90%E5%8F%B0%E5%8C%97-%E4%B8%AD%E6%AD%A3%E3%80%91%E7%99%BC%E7%8F%BE%E7%BE%A9%E5%A4%A7%E5%88%A9%E9%BA%B5-%E5%85%AC%E9%A4%A8%E5%95%86%E5%9C%88-%E5%8F%B0%E5%A4%A7-')
r = requests.get(url)
r.encoding='utf-8'
soup = BeautifulSoup(r.text, 'html.parser')

p_tags = soup.find_all('p')
for tag in p_tags:
  print(tag.get_text())