# -*- coding:utf-8 -*-

import tkinter
import tkinter.simpledialog
import tkinter.filedialog


def Instr():
    r = tkinter.simpledialog.askstring('python tkinter', 	# 创建字符串输入对话框
                                       'input string',		# 指定提示字符
                                       initialvalue='tkinter')		# 指定初始化文本
    print(r)


def Inint():
    r = tkinter.simpledialog.askinteger('python tkinter', 'input integer')
    print(r)


def InFlo():
    r = tkinter.simpledialog.askfloat('python tkinter', 'input float')
    print(r)


# 打开文件
def FileOpen():
    r = tkinter.filedialog.askopenfilename(title='python tkinter',
                                           filetypes=[('Python', '*.py *.pyw'), ('All files', '*')])  # 指定文件类型为Python
    print(r)


# 保存文件
def FileSave():
    r = tkinter.filedialog.asksaveasfilename(title='python tkinter',
                                             initialdir=r'E:\Code\py\test',
                                             initialfile='test.py')
    print(r)

root = tkinter.Tk()
button1 = tkinter.Button(root, text='input string',
                         command=Instr)		# 指定按钮事件处理函数
button1.pack(side='left')

button2 = tkinter.Button(root, text='input integer',
                         command=Inint)		# 指定按钮事件处理函数
button2.pack(side='left')

button3 = tkinter.Button(root, text='input float',
                         command=InFlo)		# 指定按钮事件处理函数
button3.pack(side='left')

button4 = tkinter.Button(root, text='file open',
                         command=FileOpen)  # 指定按钮事件处理函数
button4.pack()

button5 = tkinter.Button(root, text='file save',
                         command=FileSave)  # 指定按钮事件处理函数
button5.pack()

root.mainloop()
