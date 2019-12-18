import requests
from bs4 import BeautifulSoup

user_agents = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'

keywords = input()  # 查詢的關鍵字
google_url = 'https://www.google.com.tw/search?q='
results = requests.get(google_url+keywords, user_agents)

soup = BeautifulSoup(results.text, 'html.parser')

items = soup.find_all("div", attrs={"class": "kCrYT"})
urls = []
for item in items:
    try:
        temp = item.find("a")["href"]
        urls.append(temp[temp.find("h"):temp.find("&s")])
    except:
        pass

print(urls)
