#!/usr/bin/python
# -*- coding: utf-8 -*-

# импортирование модулей python
from tkinter import *
import tkinter as tk


"""
Информационное окно
"""


class InformWin(Toplevel):
    """
    Создание окна с сообщением
    """
    def __init__(self, title='Сообщение', message='', fg='black', width=250, height=80):
        super().__init__()
        self.title(title)

        if (7 * len(message)) > width: width = 7 * len(message)
        self.geometry(center_window(self, width, height))
        # self.wm_iconbitmap(bitmap = 'img/Logo_JM.ico')
        # bk_image = tk.PhotoImage('img/Logo_LJ.jpg')
        # frame = Frame(self, image=bk_image)
        # frame.place()

        self.message = Message(self, aspect=800)
        self.message.place(relx=.5, y=20, anchor="c")
        self.message.configure(text=message, fg=fg)

        self.button = Button(self, text='Закрыть', command=self.close)
        position = width - 80 - 12
        self.button.place(x=position, y=40, anchor="nw", width=80, height=28)

        self.grab_set()
        self.button.focus_set()
        self.wait_window()

    def close(self):
        self.destroy()


class YesNo(Tk):  # класс диалогового окна выхода
    """
    Диалоговое окно типа да/нет
    """
    def __init__(self):
        super().__init__()
        self.frame = Frame(self)  # , bg = 'LightGray')

        self.frame.pack(side=BOTTOM)
        self.yes_button = Button(self.frame, text='Да', command=self.yes, width=5, height=2)
        self.yes_button.pack(side=LEFT, padx=5, pady=5)
        self.no_button = Button(self.frame, text='Нет', command=self.no, width=5, height=2)
        self.no_button.pack(side=RIGHT, pady=5)

        self.message = Message(self, aspect=400)
        self.message.pack(side=TOP, fill=BOTH, expand=YES)
        self.protocol('WM_DELETE_WINDOW', self.no)

    def go(self, title='Question', message='[question goes here]', width=200, height=80):
        self.title(title)
        # from form_02_TextSeach import center_window # Передавать мастер
        self.geometry(center_window(self, width, height))
        self.message.configure(text=message)
        self.booleanValue = TRUE
        self.grab_set()
        self.focus_set()
        self.wait_window()
        return self.booleanValue

    def yes(self):
        self.booleanValue = TRUE
        self.destroy()

    def no(self):
        self.booleanValue = FALSE
        self.destroy()


def center_window(master, width=0, height=0):
    scr_w = master.winfo_screenwidth()
    scr_h = master.winfo_screenheight()
    screen = str(width) + "x" + str(height) + "+" + str((scr_w - width) // 2) + "+" + str((scr_h - height) // 2)
    return screen

# тестовая команда
if __name__ == '__main__':
    root = Tk()  # Создаем одно коневое окно Tk, остальные от него TopLevel
    root.withdraw()
    # rrr = Toplevel()
    # print(center_window(rrr))

    InformWin(message='Вы успешно авторизовались', fg='green')
    # root.wait_window(app)
    # Выводит значок программы в нижнюю панель
    img = tk.PhotoImage(file='img/Logo_JM.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)

    myTest = YesNo()
    if myTest.go(message='Is it working?'):
        print('Yes')
    else:
        print('No')
