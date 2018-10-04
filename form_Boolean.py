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
    def __init__(self, master, title='Сообщение', message='', fg='black', width=250, height=80):
        super().__init__()
        self.title(title)

        if (7 * len(message)) > width: width = 7 * len(message)
        self.geometry(Center_widows(self, width, height))
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


"""
Диалоговое окно типа да/нет
"""
class YesNo(Toplevel): # класс диалогового окна выхода
    def __init__(self, master):
        super().__init__()
        self.master = master
        # self.slave = Toplevel(master)
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
        self.geometry(Center_widows(self.master, width, height))
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


# Располагает окно по центру страницы
class Center_widows(object):  #
    """
    # ----- Располагает окна по центру экрана
    """
    def __init__(self, master, width, height):
        self.screen = str(width) + "x" + str(height) + "+" + str(
            (master.winfo_screenwidth() - width) // 2) + "+" + str((master.winfo_screenheight() - height) // 2)

    def __str__(self):
        return self.screen


# тестовая команда

if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    InformWin(root, message='Вы успешно авторизовались', fg='green')

    # Выводит значок программы в нижнюю панель
    img = tk.PhotoImage(file='img/Logo_JM.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)

    myTest = YesNo(root)
    if myTest.go(message='Is it working?'):
        print('Yes')
    else:
        print('No')
