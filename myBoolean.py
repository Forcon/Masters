#!/usr/bin/python
# -*- coding: utf-8 -*-

# импортирование модулей python
from tkinter import *
import tkinter as tk

"""
Диалоговре окно выхода
"""

# класс диалогового окна выхода
class yesno:
    def __init__(self, master):
        self.slave = Toplevel(master)
        self.frame = Frame(self.slave)

        self.frame.pack(side = BOTTOM)
        self.yes_button = Button(self.frame, text='Да', command = self.yes, width=5, height=2)
        self.yes_button.pack(side = LEFT, padx = 5, pady = 5)
        self.no_button = Button(self.frame, text='Нет', command = self.no, width=5, height=2)
        self.no_button.pack(side = RIGHT, pady = 5)

        self.message = Message(self.slave, bg = 'LightGray')
        self.message.pack(side = TOP, fill = BOTH, expand = TRUE)
        self.slave.protocol('WM_DELETE_WINDOW', self.no)

    def go(self, title='Question', message = '[question goes here]', width = 200, height = 80):#, geometry='200x70+300+265'):
        self.slave.title(title)
        self.slave.geometry(Center_widows(width, height))
        # self.slave.geometry(geometry)
        self.message.configure(text = message)
        self.booleanValue = TRUE
        self.slave.grab_set()
        self.slave.focus_set()
        self.slave.wait_window()
        return self.booleanValue

    def yes(self):
        self.booleanValue = TRUE
        self.slave.destroy()

    def no(self):
        self.booleanValue = FALSE
        self.slave.destroy()

# Располагает окно по центру страницы
class Center_widows(object):  # ----- Располагает окна по центру экрана
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        root = Tk() # ---- Можно ли без открытия окна?
        root.overrideredirect(1)
        root.withdraw()
        screen = str(self.width) + "x" + str(self.height) + "+" + str(
            (root.winfo_screenwidth() - self.width) // 2) + "+" + str((root.winfo_screenheight() - self.height) // 2)
        root.destroy()
        return screen

# тестовая команда
if __name__ == '__main__':
    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    myTest = yesno(root)
    if myTest.go(message = 'Is it working?'):
      print('Yes')
    else:
      print('No')
