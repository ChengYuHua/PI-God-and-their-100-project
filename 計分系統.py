# import csv
#
# filename = "______.csv "
# with open filename as f
#     reader csv reader f
#     header_row=next(reader)
#     print(header_row)


class Restaurant:
    service = [0, 0, 0]
    food = [0, 0, 0]
    cp = [0, 0, 0]
    environment = [0, 0, 0]
    reachable = [0, 0, 0]
    speed = [0, 0, 0]
    total = [0, 0]  # 中立就跳過不要計
    articles = 0


    def total_service(self):
        # 名詞
        if ["服務", "態度", "老闆", "員工", "笑容" ] in string :
            # 正向模糊詞
            if ["不賴", "完美", "好", "讚", "佳", "高級", "滿意", "優良", "優秀", "棒","不錯", "厲害",
                "專業", "有", "用心", "享受", "精湛", "精緻", "實在", "特別", "可愛", "豐富", "喜歡",
                "幸福", "推薦", "首選", "美", "用心", "優質", "高", "爆表", "多", "足", "夠", "驚豔",
                "愉快", "愛", "推"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.service[2] += 1
                else:
                    self.service[0] += 1
            # 負向模糊詞
            elif ["差", "糟", "爛", "失望", "待加強", "錯", "噁心"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.service[0] += 1
                else:
                    self.service[2] += 1
        # 正向精準詞
        elif ["周詳", "細心", "周到", "親切", "貼心", "友善", "熱情", "禮貌", "認真", "健談",
              "和氣", "有禮", "熱心", "溫柔", "客氣", "和善", "親民", "熱忱", "體貼"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.service[2] += 1
            else:
                self.service[0] += 1
        # 負向精準詞
        elif ["不耐煩", "自以為是", "不屑", "馬虎"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.service[0] += 1
            else:
                self.service[2] += 1
        # 找不到任何詞
        else:
            self.service[1] += 1

        return (self.service[0] / self.articles), (self.service[1] / self.articles), (self.service[2] / self.articles)


    def total_food(self):
        # 名詞
        if ["餐點", "口感", "口味", "食材", "料理", "菜色", "食物",
            "品項", "品質", "風味", "手藝", "廚藝", "滋味", "味道", "水準", "創意"] in string:
            # 正向模糊詞
            if ["不賴", "完美", "好", "讚", "佳", "高級", "滿意", "優良", "優秀", "棒","不錯", "厲害",
                "專業", "有", "用心", "享受", "精湛", "精緻", "實在", "特別", "可愛", "豐富", "喜歡",
                "幸福", "推薦", "首選", "美", "用心", "優質", "高", "爆表", "多", "足", "夠", "驚豔",
                "愉快", "愛", "推"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.food[2] += 1
                else:
                    self.food[0] += 1
            # 負向模糊詞
            elif ["差", "糟", "爛", "失望", "待加強", "錯", "噁心"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.food[0] += 1
                else:
                    self.food[2] += 1
        # 正向精準詞
        elif ["好吃", "新鮮", "鮮美", "好滋味", "美味", "好喝", "水準高", "有特色", "回味無窮", "讓人回味", "可口", "驚艷",
                "爽口", "正宗", "正統", "色香味俱全", "香氣四溢", "道地", "健康", "營養", "清爽", "多樣", "多元",
                "經典", "真材實料", "順口"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.food[2] += 1
            else:
                self.food[0] += 1
        # 負向精準詞
        elif ["膩口", "難吃", "難喝", "奇怪", "沒熟", "油膩"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.food[0] += 1
            else:
                self.food[2] += 1
        # 找不到任何詞
        else:
            self.food[1] += 1

        return (self.food[0] / self.articles), (self.food[1] / self.articles), (self.food[2] / self.articles)


    def total_cp(self):
        # 名詞
        if ["速度", "出菜", "上菜", "等", "排隊"] in string:
            # 正向模糊詞
            if ["不賴", "完美", "好", "讚", "佳", "高級", "滿意", "優良", "優秀", "棒", "不錯", "厲害",
                "專業", "有", "用心", "享受", "精湛", "精緻", "實在", "特別", "可愛", "豐富", "喜歡",
                "幸福", "推薦", "首選", "美", "用心", "優質", "高", "爆表", "多", "足", "夠", "驚豔",
                "愉快", "愛", "推"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.cp[2] += 1
                else:
                    self.cp[0] += 1
            # 負向模糊詞
            elif ["差", "糟", "爛", "失望", "待加強", "錯", "噁心"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.cp[0] += 1
                else:
                    self.cp[2] += 1
        # 正向精準詞
        elif ["迅速", "快速", "快"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.cp[2] += 1
            else:
                self.cp[0] += 1
        # 負向精準詞
        elif ["久", "慢"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.cp[0] += 1
            else:
                self.cp[2] += 1
        # 找不到任何詞
        else:
            self.cp[1] += 1

        return (self.cp[0] / self.articles), (self.cp[1] / self.articles), (self.cp[2] / self.articles)


    def total_environment(self):
        # 名詞
        if ["裝潢", "氣氛", "環境", "空間", "氛圍", "採光", "格調", "衛生", "場地", "空間", "樓梯"] in string:
            # 正向模糊詞
            if ["不賴", "完美", "好", "讚", "佳", "高級", "滿意", "優良", "優秀", "棒", "不錯", "厲害",
                "專業", "有", "用心", "享受", "精湛", "精緻", "實在", "特別", "可愛", "豐富", "喜歡",
                "幸福", "推薦", "首選", "美", "用心", "優質", "高", "爆表", "多", "足", "夠", "驚豔",
                "愉快", "愛", "推"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.environment[2] += 1
                else:
                    self.environment[0] += 1
            # 負向模糊詞
            elif ["差", "糟", "爛", "失望", "待加強", "錯", "噁心"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.environment[0] += 1
                else:
                    self.environment[2] += 1
        # 正向精準詞
        elif ["划算", "物有所值", "物超所值", "平價", "佛心", "實惠", "超值", "公道", "料多", "豐盛", "澎湃"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.environment[2] += 1
            else:
                self.environment[0] += 1
        # 負向精準詞
        elif ["乾淨", "舒適", "明亮", "涼爽", "燈光美", "輕鬆", "簡潔", "自在", "舒服", "悠閒", "寬敞",
              "衛生", "寧靜", "溫馨", "光亮", "整潔", "整齊"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.environment[0] += 1
            else:
                self.environment[2] += 1
        # 找不到任何詞
        else:
            self.environment[1] += 1

        return (self.environment[0] / self.articles), (self.environment[1] / self.articles), (self.environment[2] / self.articles)


    def total_reachable(self):
        # 名詞
        if ["裝潢", "氣氛", "環境", "空間", "氛圍", "採光", "格調", "衛生", "場地", "空間", "樓梯"] in string:
            # 正向模糊詞
            if ["不賴", "完美", "好", "讚", "佳", "高級", "滿意", "優良", "優秀", "棒", "不錯", "厲害",
                "專業", "有", "用心", "享受", "精湛", "精緻", "實在", "特別", "可愛", "豐富", "喜歡",
                "幸福", "推薦", "首選", "美", "用心", "優質", "高", "爆表", "多", "足", "夠", "驚豔",
                "愉快", "愛", "推"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.reachable[2] += 1
                else:
                    self.reachable[0] += 1
            # 負向模糊詞
            elif ["差", "糟", "爛", "失望", "待加強", "錯", "噁心"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.reachable[0] += 1
                else:
                    self.reachable[2] += 1
        # 正向精準詞
        elif ["乾淨", "舒適", "明亮", "涼爽", "燈光美", "輕鬆", "簡潔", "自在", "舒服", "悠閒", "寬敞",
              "衛生", "寧靜", "溫馨", "光亮", "整潔", "整齊"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.reachable[2] += 1
            else:
                self.reachable[0] += 1
        # 負向精準詞
        elif ["狹小", "窄", "擁擠", "擠", "簡陋"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.reachable[0] += 1
            else:
                self.reachable[2] += 1
        # 找不到任何詞
        else:
            self.reachable[1] += 1

        return (self.reachable[0] / self.articles), (self.reachable[1] / self.articles), (self.reachable[2] / self.articles)


    def total_speed(self):
        # 名詞
        if ["裝潢", "氣氛", "環境", "空間", "氛圍", "採光", "格調", "衛生", "場地", "空間", "樓梯"] in string:
            # 正向模糊詞
            if ["不賴", "完美", "好", "讚", "佳", "高級", "滿意", "優良", "優秀", "棒", "不錯", "厲害",
                "專業", "有", "用心", "享受", "精湛", "精緻", "實在", "特別", "可愛", "豐富", "喜歡",
                "幸福", "推薦", "首選", "美", "用心", "優質", "高", "爆表", "多", "足", "夠", "驚豔",
                "愉快", "愛", "推"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.speed[2] += 1
                else:
                    self.speed[0] += 1
            # 負向模糊詞
            elif ["差", "糟", "爛", "失望", "待加強", "錯", "噁心"] in 名詞的後3位內的詞:
                # 否定詞判斷
                if ["不", "沒有"] in 模糊詞的前面:
                    self.speed[0] += 1
                else:
                    self.speed[2] += 1
        # 正向精準詞
        elif ["乾淨", "舒適", "明亮", "涼爽", "燈光美", "輕鬆", "簡潔", "自在", "舒服", "悠閒", "寬敞",
              "衛生", "寧靜", "溫馨", "光亮", "整潔", "整齊"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.speed[2] += 1
            else:
                self.speed[0] += 1
        # 負向精準詞
        elif ["狹小", "窄", "擁擠", "擠", "簡陋"] in string:
            # 否定詞判斷
            if ["不", "沒有"] in 模糊詞的前面:
                self.speed[0] += 1
            else:
                self.speed[2] += 1
        # 找不到任何詞
        else:
            self.speed[1] += 1
        return (self.speed[0] / self.articles), (self.speed[1] / self.articles), (self.speed[2] / self.articles)






string = input()
string = Restaurant()
print(string.service)

string.service[0] += 1
string.articles += 1
print(string.service, string.articles)
print(string.total_service())
