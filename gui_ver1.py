import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
import matplotlib.pyplot as py
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math


class window(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        f1 = tkFont.Font(size=48, family='Courier New')
        f2 = tkFont.Font(size=32, family='Courier New')
        self.lbltitle = tk.Label(self, text='好吃指南')
        self.entmeal = tk.Entry(self)
        self.entlocation = tk.Entry(self)
        self.btnsearch = tk.Button(self, text='搜尋', height=1, width=7,command=self.clicksearch)

        #self.canvas1=tk.Canvas(self, width=600,height=300,bg='blue')

        self.lbltitle.grid(row=0, column=3, columnspan=4, sticky=tk.NE + tk.SW)
        self.entmeal.grid(row=1, column=1,columnspan=4,sticky=tk.NE + tk.SW)
        self.entlocation.grid(row=1, column=6,columnspan=4, sticky=tk.NE + tk.SW)
        self.btnsearch.grid(row=2, column=5,columnspan=2, sticky=tk.NE + tk.SW)
        #self.canvas1.grid(row=5)
        #self.canvas1.create_text(20,40,text='最好吃')

    def clicksearch(self):
        #將使用者輸入的值傳入爬蟲
        #global meal
        #global location
        #meal =self.entmeal.get()
        #location=self.location.get()

        self.comboitem = ttk.Combobox(self, value=['總評', '服務', '餐點', 'CP值', '環境', '交通', '速度'])
        self.comboitem.bind("<<ComboboxSelected>>", self.callbackFunc)

        #self.comboitem.current(0)
        self.comboitem.grid(row=3, column=3,columnspan=6)
        #顯示餐廳名稱
        self.lbl1st=tk.Label(self,text='1st') #text之後要get餐廳名稱
        self.lbl1st.grid(row=5,column=2,columnspan=3)
        #下面是畫圓餅圖的模組
        self.pieSizes = [1, 2, 3]
        self.labels = 'a', 'b', 'c'
        self.figure1 = Figure(figsize=(1, 1), dpi=100)
        self.subplot1 = self.figure1.add_subplot(111)
        self.explode1 = (0, 0, 0)
        self.subplot1.pie(self.pieSizes, explode=self.explode1, labels=self.labels, shadow=True, startangle=90)
        self.subplot1.axis('equal')
        self.pie2 = FigureCanvasTkAgg(self.figure1, self)
        self.pie2.get_tk_widget().grid(row=4,column=7,rowspan=3,columnspan=3)

    def callbackFunc(self,event):
        self.lbl1st['text']=self.comboitem.get()

window = window()
window.master.title('餐應推薦')
window.mainloop()
