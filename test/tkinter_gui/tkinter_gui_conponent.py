# -*- coding:utf-8 -*-

import tkinter

# 显示主界面
root = tkinter.Tk()

# 多行文本居中对齐
label = tkinter.Label(root, text="你好\nPython", justify=tkinter.CENTER)
# 添加标签
label.pack()

# anchor对齐方式 height两行字符高度
button1 = tkinter.Button(root, text="按钮1", anchor=tkinter.E, width=10, height=2)
#添加到主界面左侧
button1.pack(side=tkinter.LEFT)

# 背景色，前景色
button2 = tkinter.Button(root, text="按钮2", bg='blue', fg='red')
button2.pack(side=tkinter.RIGHT)

# 单行文本框，文本框中显示的字符
entry1 = tkinter.Entry(root, show='*', width=50)
entry1.pack()

# 文本框背景色，前景色
entry2 = tkinter.Entry(root, bg='red', fg='blue')
entry2.pack()

# 多行文本框，选中的文本背景色，前景色
edit = tkinter.Text(root, selectbackground='green', selectforeground='gray')
edit.pack()


# 生成菜单
menu = tkinter.Menu(root)
# 生成下拉菜单
submenu = tkinter.Menu(menu, tearoff=0)
submenu.add_command(label="open")
submenu.add_command(label="save")
# 下拉菜单中添加分隔符
submenu.add_separator()
submenu.add_command(label="close")
# 将下拉菜单添加到菜单中
menu.add_cascade(label="File", menu=submenu)
root.config(menu=menu)


# 弹出式菜单
menu2 = tkinter.Menu(root, tearoff=0)
menu2.add_command(label="copy")
menu2.add_command(label="save")
# 下拉菜单中添加分隔符
menu2.add_separator()
menu2.add_command(label="close")
# 定义右键事件处理函数


def popupmenu(event):
    # 显示函数
    menu2.post(event.x_root, event.y_root)
# 绑定右键事件
root.bind("<Button-3>", popupmenu)
# 区分大小写
# root.bind("<KeyPress-A>", popupmenu)


# 单选框 复选框
# 生成字符串变量用于单选框组件
r = tkinter.StringVar()
# 初始化变量值
r.set('1')
# variable设置单选框关联变量，value选中单选框时其所关联的变量的值
radio = tkinter.Radiobutton(root, variable=r, value=1, text='radio1')
radio.pack()
# 当选中该单选框时，r的值为2
radio = tkinter.Radiobutton(root, variable=r, value=2, text='radio2')
radio.pack()
# 生成整型变量用于复选框
c = tkinter.IntVar()
c.set('1')
# variable复选框关联的变量，onvalue选中复选框时c值为1，未选中时值为2
check = tkinter.Checkbutton(root, text='Checkbutton', variable=c, onvalue=1, offvalue=2)
check.pack()
print('r', r.get())
print(c.get())


# 画布
canvas = tkinter.Canvas(root, width=600, height=480, bg='white')
# im = tkinter.PhotoImage(file='E:\photos\工作获奖.jpg')
# canvas.create_image(100, 300, image=im)
canvas.create_line(250, 130, 350, 130)
canvas.pack()


root.mainloop()
