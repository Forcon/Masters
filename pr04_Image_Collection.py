# coding=utf-8
# from tkinter import *
# from tkinter.tix import *
from tkinter import Tk, Button, Toplevel
from functools import partial
import tkinter as tk
from PIL import ImageTk  # $ pip install pillow
from pr03_Form_Collection import *
from def_04_Frame_Scroll import *
from def_05_Save_Collection import *

"""
Версия 2.6: Основная программа
Выводит картинки для выбора из них лучших + показывает уже сформированную коллекцию, с сохранением промежуточных результатов
"""

class SampleApp(Toplevel):
    def __init__(self, img_url, len_mass, img_coll, name_coll):
        super().__init__()
        self.img_url = img_url
        self.len_mass = len_mass
        self.img_coll = img_coll  # Количество изображений в коллекции
        self.img_in_coll = []
        self.name_coll = name_coll

        self.title("Выбор картинок в коллекцию")
        self.geometry("800x550")
        self.frame = VerticalScrolledFrame(self, 800)

        for i, el in enumerate(self.img_url):
            if i > 0:
                break
            for y in range(1, len(self.len_mass) + 1):
                for x in range(1, (self.len_mass[y - 1] + 1)):
                    if not os.path.isfile(self.img_url[i]):  # Проверка на наличие картинки в базе
                        breakpoint()
                    image = ImageTk.PhotoImage(file=self.img_url[i])  # Открываем изображение.
                    btn = Button(self.frame.interior, image=image)
                    btn.image = image
                    btn.grid(row=y, column=x)
                    btn.bind('<Button-1>',
                             partial(self.click_button, i + 1))  # Через функцию partial мы передаем номер кнопки
                    i += 1

        self.frame.pack(anchor=NW, fill=BOTH, expand=YES)

        self.coll = Toplevel()
        self.coll.title("Картинки, включенные в коллекцию")
        self.coll.geometry("336x360+0+650")
        self.coll.minsize(336, 360)

        self.rez_col()  # Делает пустые кнопки

        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.coll.protocol('WM_DELETE_WINDOW', self.cancel)


    def cancel(self):
        self._root().destroy()
        SQL_Connect = sqlite3.connect('Masters.db')
        cursor = SQL_Connect.cursor()

        id_coll = open_coll(self.name_coll, cursor, SQL_Connect)  # Сохранение коллекции в базу
        url_coll = url_name(self.img_in_coll, img_coll, cursor)
        save_collection(url_coll, user_name, id_coll, cursor, SQL_Connect)

        cursor.close()
        SQL_Connect.close()


    def insert_coll(self):
        """Считывает данные из базы и помещает в массив"""
        SQL_Connect = sqlite3.connect('Masters.db')
        cursor = SQL_Connect.cursor()

        id_coll = open_coll(name_coll, cursor, SQL_Connect)  # Получение коллекции из базы
        collection_url = open_colection(id_coll, img_coll, cursor)
        self.in_coll = convert_coll(collection_url, img_coll, cursor)

        cursor.close()
        SQL_Connect.close()


    def rez_col(self):  # Вставляет в "готовую коллекцию" пустые кнопки
        self.label = Label(self.coll)
        self.label.grid(column=0, columnspan=4, pady=1, sticky='s')
        self.label.configure(text='Коллекция: "' +self.name_coll + '"', relief=GROOVE, fg='blue')#, bg='lightgrey')
        self.insert_coll()

        for i in range(self.img_coll):
            image = ImageTk.PhotoImage(file='img/img_0.jpg')
            buttn = Button(self.coll, image=image)
            buttn.image = image
            y = i // 4
            buttn.grid(row = y + 2, column = i - (y * 4))
            buttn.bind('<Button-1>', partial(self.cl_coll, i + 1))  # Через функцию partial мы передаем номер кнопки
        self.start_collection()


    def start_collection(self):
        for i in range(len(self.in_coll)):
            number = self.img_url.index(self.in_coll[i]) + 1
            self.give_img(number)  # Размер картинки

        self.new_img()


    def new_img(self):  # Заливка новых изображений
        for i in range(self.img_coll):
            if len(self.img_in_coll) > i:
                name_img = self.img_in_coll[i]
            else:
                name_img = 'img/img_0.jpg'
            name_button = "!button" + ('' if i == 0 else str(i + 1))
            image_1 = ImageTk.PhotoImage(file=name_img)
            self.coll.children[name_button].config(image="{:}".format(image_1))
            self.coll.children[name_button].image = image_1

    def cl_coll(self, number, event):  # Какая из кнопок нажата на панели коллекций
        if len(self.img_in_coll) >= number:  # Если коллекция не пуста
            number_img = img_url.index(self.img_in_coll[number - 1]) + 1

            self.give_img(number_img)
            self.new_img()


    def row_img(self, number):  # ----- Дает номер строки в котором находится картинка
        int_zn = 0
        for i in range(0, len(self.len_mass)):
            if (int(self.len_mass[i]) + int_zn) >= number:
                return i
            else:
                int_zn += self.len_mass[i]


    def start_fin(self, row):  # ----- Дает значения с которых начинается (и заканчивается) очередной ряд
        return sum(self.len_mass[:row]) + 1, sum(self.len_mass[:row]) + self.len_mass[row]

    def give_img(self, number):
        """
        Устaнавливает размер картинок, для того чтобы обозначить, какая из картинок изпользуется в коллекции
        :param str name:
        :param int number:
        :return:
        """
        name = '!button' + ('' if number == 1 else str(number))
        st, fin = self.start_fin(self.row_img(number))
        row_btn = list(self.frame.interior.children)[st - 1:fin]

        if img_url[number - 1] in self.img_in_coll:
            self.img_in_coll.remove(img_url[number - 1])
            for i, el in enumerate(row_btn, st - 1):
                self.frame.interior.children[el].config(height="{:}".format(80))
        else:
            for i, el in enumerate(row_btn, st - 1):
                if img_url[i] in self.img_in_coll:  #
                    self.img_in_coll.remove(img_url[i])
                if el != name:  # Уменьшает картинки которые не совпадают с номером кнопки
                    self.frame.interior.children[el].config(height="{:}".format(40))
                else:
                    self.frame.interior.children[name].config(height="{:}".format(80))
                    self.img_in_coll.append(img_url[number - 1])

    def click_button(self, number, event):  # Обработка нажатия на кнопку в выборе картинок
        self.give_img(number)  # Размер картинки в
        self.new_img()  # Обновление коллекции


if __name__ == "__main__":
    root = Tk()  # ---- Открываем основное окно и сразу его прячем
    root.withdraw()

    # Выводит значок программы в нижнюю панель
    img = tk.PhotoImage(file='img/Logo_JM.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)

    user_name = 'forcon'
    user_mail = 'forcon@mail.ru'
    text_search = 'Птичка сердолик'
    name_coll = 'Выдры, птицы и ондатры'

    img_url, autor_name, len_mass = creating_coll(user_name, text_search)
    img_coll = 16  # Количество изображений в коллекции

    app = SampleApp(img_url, len_mass, img_coll, name_coll)
    app.mainloop()

    # root.destroy()
