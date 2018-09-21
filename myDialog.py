#!/usr/bin/python
# -*- coding: utf-8 -*-

# импортирование модулей python
# from tkinter import *
from myBoolean import *

"""
Диалоговое окно проверки пароля - импортируемый модуль
"""


# класс дочернего окна
class dialog:
    def __init__(self, master):
        self.top = Toplevel(master)
        self.top.title('Проверка пароля')
        self.top.geometry(Center_widows(390, 100))  # Располагает по центру страницы
        # self.frame = Frame(self.top)
        # self.frame.pack(side=BOTTOM)
        self.label = Label(self.top, text='Введите пароль еще раз...')
        self.label.place(relx=.5, y=20, anchor="c")

        self.yes_button = Button(self.top, text='Подтвердить', command=self.cancel)
        self.yes_button.place(x=275, y=50, anchor="w", width=100, height=30)

        self.x = StringVar()
        self.text_entry = Entry(self.top, textvariable=self.x, show='*')
        self.text_entry.place(x=15, y=50, anchor="w", width=250)

        self.top.protocol('WM_DELETE_WINDOW', self.cancel)

    def __str__(self):
        return self.x.get()

    def go(self, myText='', ):
        self.text_entry.insert('0', myText)
        self.newValue = None
        self.top.grab_set()
        self.top.focus_set()
        self.top.wait_window()
        return self.newValue

    def accept(self):
        self.newValue = self.text_entry.get()
        self.top.destroy()
        pass

    def cancel(self):
        self.top.destroy()


# тестовая команда
if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    myTest = dialog(root)
    print(myTest.go('Hello World!'))
