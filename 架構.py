"""
1.前置作業
import 需要的 library
建置六面向和總評的正、負評語料庫，皆以 list 儲存（杰、楊）
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
    ptt_url = []
    dcard_url = []
    ifoodie_url = []
    pixnet_url = []
	
    # 函數呼叫時，依序回傳該細項正評總分、中立總分和負評總分

    def total_service(self):
	return (self.service[0] / articles), (self.service[1] / articles) , (self.service[2] / articles)
    # 這邊只列一個，其他略過

class Article:
    # 這邊放計算單篇文章的分數和細項的函數

讓使用者依序輸入地點和食物種類
location = input()
category = input()
建一個 all_restaraunt 的 list，之後會拿來存所有餐廳的評分和資訊

2.程式動起來
使用爬蟲找出所有符合條件的餐廳，放入一個 list(restaraunts_list)
使用 for 迴圈從 restaraunts_list 裡，一家一家餐廳抓出來
把餐廳變成 Restaurant class
i = Restaurant()
i.service

# 依序為好評文章、負評文章
"""
