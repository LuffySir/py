# -*- coding:utf-8 -*-

import tkinter

# 事件响应
# bind(seq，func，add)
# bind_class(class，seq，func，add) 类绑定
# bind_all(seq，func，add) 所有组件事件绑定到事件响应函数
# seq为绑定的事件，以<>包围的字符串，如<Button-1>左键按下，<KeyPress-A>按下A键等


class MyButton:

    def __init__(self, root, canvas, label, type):
        self.root = root
        self.canvas = canvas
        self.label = label
        # 根据类型创建按钮
        if type == 0:
            button = tkinter.Button(root, text='DrawLine', command=self.DrawLine)
        elif type == 1:
            button = tkinter.Button(root, text='DrawArc', command=self.DrawArc)
        elif type == 2:
            button = tkinter.Button(root, text='DrawRec', command=self.DrawRec)
        else:
            button = tkinter.Button(root, text='DrawOval', command=self.DrawOval)
        button.pack(side='left')

    def DrawLine(self):
        self.label.text.set('Draw Line')
        self.canvas.SetStatus(0)

    def DrawArc(self):
        self.label.text.set('Draw Arc')
        self.canvas.SetStatus(1)

    def DrawRec(self):
        self.label.text.set('Draw Rec')
        self.canvas.SetStatus(2)

    def DrawOval(self):
        self.label.text.set('Draw Oval')
        self.canvas.SetStatus(3)


class MyCanvas:

    def __init__(self, root):
        self.status = 0
        self.draw = 0
        self.root = root
        self.canvas = tkinter.Canvas(root, bg='white', width=600, height=480)
        self.canvas.pack()
        # 绑定事件到左键
        self.canvas.bind('<ButtonRelease-1>', self.Draw)
        # 绑定事件到中键
        self.canvas.bind('<Button-2>', self.Exit)
        # 绑定事件到右键
        self.canvas.bind('<Button-3>', self.Del)
        # 绑定事件到delete键
        self.canvas.bind_all('<Delete>', self.Del)
        self.canvas.bind_all('<KeyPress-d>', self.Del)
        self.canvas.bind_all('<KeyPress-e>', self.Exit)

    def Draw(self, event):
        if self.draw == 0:
            self.x = event.x
            self.y = event.y
            self.draw = 1
        else:
            if self.status == 0:
                self.canvas.create_line(self.x, self.y, event.x, event.y)
                self.draw = 0
            elif self.status == 1:
                self.canvas.create_arc(self.x, self.y, event.x, event.y)
                self.draw = 0
            elif self.status == 2:
                self.canvas.create_rectangle(self.x, self.y, event.x, event.y)
                self.draw = 0
            else:
                self.canvas.create_oval(self.x, self.y, event.x, event.y)
                self.draw = 0

    # 按下右键或d键删除图形
    def Del(self, event):
        items = self.canvas.find_all()
        # for item in items:
        #     self.canvas.delete(item)
        i = len(items)
        while i > 0:
            self.canvas.delete(items[i - 1])
            i -= 1

    # 按下中键或e键退出
    def Exit(self, event):
        self.root.quit()

    # 设置绘制的图形
    def SetStatus(self, status):
        self.status = status


class MyLabel:

    def __init__(self, root):
        self.root = root
        self.canvas = canvas
        self.text = tkinter.StringVar()
        self.text.set('Draw Line')
        self.label = tkinter.Label(root, textvariable=self.text, fg='red', width=50)
        self.label.pack(side='left')

root = tkinter.Tk()
canvas = MyCanvas(root)
label = MyLabel(root)
MyButton(root, canvas, label, 0)
MyButton(root, canvas, label, 1)
MyButton(root, canvas, label, 2)
MyButton(root, canvas, label, 3)


root.mainloop()
