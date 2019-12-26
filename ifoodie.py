import requests
from bs4 import BeautifulSoup

url = 'https://ifoodie.tw/post/5dea600d2261390a2235125d-%E5%8F%B0%E5%8C%97%E8%90%AC%E8%8F%AF%E6%96%B0%E5%8C%97%E4%B8%89%E9%87%8D%E8%B6%85%E5%A5%BD%E5%90%83%E8%8A%B1%E7%94%9F%E6%B2%BE%E9%86%AC%E7%9F%B3%E9%A0%AD%E7%81%AB%E9%8D%8B%E6%8E%A8'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

p_tags = soup.find_all('p')
for tag in p_tags:
  print(tag.get_text())