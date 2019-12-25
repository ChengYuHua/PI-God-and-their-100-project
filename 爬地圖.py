import requests
from bs4 import BeautifulSoup

user_agents = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'

keywords = input()  # 查詢的關鍵字
map_url = 'https://www.google.com.tw/maps/search/'
results = requests.get(map_url+keywords, user_agents)

soup = BeautifulSoup(results.text, 'html.parser')

items = soup.find_all("span", attrs={"jstcache": "125"})
print(items)
titles = []
for item in items:
    try:
        title = item.get_text().strip()
        titles.append(title)
    except:
        pass

for i in titles:
    print(i)
