import matplotlib.pyplot as py
size = [2, 5, 10, 3]  # list
labels = 'A', 'C', 'D', 'E'  # 用逗號隔開的一串字串 'A', 'C', 'D', 'E'

py.pie(size, labels=labels, autopct='%1.1f%%')
py.axis('equal')
py.show()
