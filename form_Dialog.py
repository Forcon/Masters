#!/usr/bin/python
# -*- coding: utf-8 -*-

# импортирование модулей python
# from tkinter import *
from form_Boolean import *

"""
Диалоговое окно проверки пароля - импортируемый модуль
"""

# класс дочернего окна
class Dialog(Toplevel):
    def __init__(self):
        super().__init__()

        self.title('Проверка пароля')
        self.geometry(center_window(390, 100))  # Располагает по центру страницы
        # self.frame = Frame(self)
        # self.frame.pack(side=BOTTOM)
        self.label = Label(self, text='Введите пароль еще раз...')
        self.label.place(relx=.5, y=20, anchor="c")

        self.yes_button = Button(self, text='Подтвердить', command=self.cancel)
        self.yes_button.place(x=275, y=50, anchor="w", width=100, height=30)

        self.x = StringVar()
        self.text_entry = Entry(self, textvariable=self.x, show='*')
        self.text_entry.place(x=15, y=50, anchor="w", width=250)

        self.protocol('WM_DELETE_WINDOW', self.cancel)

    def __str__(self):
        return self.x.get()

    def go(self, myText='', ):
        self.text_entry.insert('0', myText)
        self.newValue = None
        self.grab_set()
        self.focus_set()
        self.wait_window()
        return self.newValue

    def accept(self):
        self.newValue = self.text_entry.get()
        self.destroy()
        pass

    def cancel(self):
        self.destroy()


# тестовая команда
if __name__ == '__main__':
    # root = Tk()
    # root.withdraw()
    myTest = Dialog()
    print(myTest.go('Hello World!'))
