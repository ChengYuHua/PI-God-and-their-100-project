import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

aalist =[5,5,2]
class window(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        f1 = tkFont.Font(size=24, family='黑體')
        f2 = tkFont.Font(size=32, family='Courier New')


        self.lbltitle = tk.Label(self, text='食神',font=f1,bg='green')
        self.lblmeal = tk.Label(self, text='餐點',font=f1)
        self.entmeal = tk.Entry(self)
        self.lbllocation = tk.Label(self, text='地點',font=f1)
        self.entlocation = tk.Entry(self)
        self.btnsearch = tk.Button(self, text='搜尋', font=f2,bg='blue',command=self.clicksearch)

        #self.canvas1=tk.Canvas(self, width=600,height=300,bg='blue')

        self.lbltitle.grid(row=0, column=2, columnspan=4, sticky=tk.NE + tk.SW)
        self.lblmeal.grid(row=1, column=0,columnspan=1,sticky=tk.W)
        self.entmeal.grid(row=1, column=1,columnspan=3,sticky=tk.NE + tk.SW)
        self.lbllocation.grid(row=1, column=4,columnspan=1,sticky=tk.W)
        self.entlocation.grid(row=1, column=5,columnspan=3, sticky=tk.NE + tk.SW)
        self.btnsearch.grid(row=2, column=3,columnspan=2, sticky=tk.NE + tk.SW)
        #self.canvas1.grid(row=5)
        #self.canvas1.create_text(20,40,text='最好吃')

    def clicksearch(self):
        f3 = tkFont.Font(size=28, family='楷體')
        #將使用者輸入的值傳入爬蟲
        #global meal
        #global location
        #meal =self.entmeal.get()
        #location=self.location.get()

        self.comboitem = ttk.Combobox(self, value=['總評', '服務', '餐點', 'CP值', '環境', '交通', '速度'])
        self.comboitem.bind("<<ComboboxSelected>>", self.callbackFunc)

        #self.comboitem.current(0)
        self.comboitem.grid(row=3, column=1,columnspan=6)
        #顯示餐廳名稱
        self.lbl1st=tk.Label(self,text='窩巷弄', font=f3) #text之後要get餐廳名稱
        self.lbl1st.grid(row=5,column=0,columnspan=3)
        #下面是畫圓餅圖的模組
        self.pieSizes1 = aalist
        self.labels = 'Good', 'Bad', 'Neutral'
        self.figure1 = Figure(figsize=(2.5,1.5), dpi=100)
        self.subplot1 = self.figure1.add_subplot(111)
        self.explode1 = (0, 0, 0)
        self.subplot1.pie(self.pieSizes1, explode=self.explode1, labels=self.labels, shadow=True, startangle=90)
        self.subplot1.axis('equal')
        self.pie1 = FigureCanvasTkAgg(self.figure1, self)
        self.pie1.get_tk_widget().grid(row=4,column=3,rowspan=3,columnspan=5)

        # 顯示餐廳名稱
        self.lbl2st = tk.Label(self, text='麵工坊義大利麵', font=f3)  # text之後要get餐廳名稱
        self.lbl2st.grid(row=8, column=0, columnspan=3)
        # 下面是畫圓餅圖的模組
        self.pieSizes2 = [8, 1, 1]
        self.figure2 = Figure(figsize=(2.5,1.5), dpi=100)
        self.subplot2 = self.figure2.add_subplot(111)
        self.subplot2.pie(self.pieSizes2, explode=self.explode1, labels=self.labels, shadow=True, startangle=90)
        self.subplot2.axis('equal')
        self.pie2 = FigureCanvasTkAgg(self.figure2, self)
        self.pie2.get_tk_widget().grid(row=7, column=3,rowspan=3,columnspan=5)

        # 顯示餐廳名稱
        self.lbl3st = tk.Label(self, text='蘇活義大利麵坊', font=f3)  # text之後要get餐廳名稱
        self.lbl3st.grid(row=11, column=0, columnspan=3)
        # 下面是畫圓餅圖的模組
        self.pieSizes3 = [6, 2, 2]
        self.figure3 = Figure(figsize=(2.5,1.5), dpi=100)
        self.subplot3 = self.figure3.add_subplot(111)
        self.subplot3.pie(self.pieSizes3, explode=self.explode1, labels=self.labels, shadow=True, startangle=90)
        self.subplot3.axis('equal')
        self.pie3 = FigureCanvasTkAgg(self.figure3, self)
        self.pie3.get_tk_widget().grid(row=10, column=3, rowspan=3, columnspan=5)

    def callbackFunc(self,event):
        if self.comboitem.get() == '餐點':
            self.lbl2st['text']= '夢駝鈴'
            self.lbl3st['text']= 'Go Go Pasta'


            #self.comboitem.get()


window = window()
window.master.geometry('512x900+200+100')
window.master.title('餐應推薦')
window.master.configure(background='#EE82EE')
window.mainloop()


