# coding=utf-8
from tkinter import *
# from tkinter.tix import *
# from tkinter import Tk, Button, Toplevel
import tkinter as tk
from PIL import ImageTk  # $ pip install pillow
from pr03_Form_Collection import *
from def_04_Frame_Scroll import *

"""
Версия 2.5: Основная программа
Выводит картинки для выбора из них лучших + показывает уже сформированную коллекцию
"""

class SampleApp(Toplevel):
    def __init__(self, img_url, len_mass, img_coll, *args, **kwargs):
        super().__init__()
        self.img_url = img_url
        self.len_mass = len_mass
        self.img_coll = img_coll  # Количество изображений в коллекции
        self.img_in_coll = []

        # self = Toplevel()
        self.title("Выбор картинок в коллекцию")
        self.geometry("800x550")
        self.frame = VerticalScrolledFrame(self, 800)

        for i, el in enumerate(self.img_url):
            if i > 0: break
            for y in range(1, len(self.len_mass) + 1):
                for x in range(1, (self.len_mass[y - 1] + 1)):
                    if not os.path.isfile(self.img_url[i]):  # Проверка на наличие картинки в базе
                        breakpoint()
                    image = ImageTk.PhotoImage(file=self.img_url[i])  # Открываем изображение.
                    btn = Button(self.frame.interior, image=image)
                    btn.image = image
                    btn.grid(row=y, column=x)
                    btn.bind('<Button-1>', self.click_button)
                    i += 1

        self.frame.pack(anchor=NW, fill=BOTH, expand=YES)

        self.coll = Toplevel()
        self.coll.title("Картинки, включенные в коллекцию")
        self.coll.geometry("336x336+0+700")

        self.rez_col()  # Делает пустые кнопки

        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.coll.protocol('WM_DELETE_WINDOW', self.cancel)

    def cancel(self):
        self._root().destroy()

    def rez_col(self):  # Вставляет в "готовую коллекцию" пустые кнопки (ок!)
        for i in range(self.img_coll):
            image_1 = ImageTk.PhotoImage(file='img/img_0.jpg')
            buttn = Button(self.coll, image=image_1)
            buttn.image = image_1
            y = i // 4
            buttn.grid(row=y + 1, column=i - (y * 4))
            buttn.bind('<Button-1>', self.cl_coll)


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


    def cl_coll(self, event):  # Какая из кнопок нажата на панели коллекций
        name = event.widget._name
        number = 1 if name == '!button' else int(name.split('!button')[1])

        if len(self.img_in_coll) >= number:  # Если коллекция не пуста
            number_img = img_url.index(self.img_in_coll[number - 1]) + 1
            name = '!button' + ('' if number_img == 1 else str(number_img))
            self.give_img(name, number_img)


    def row_img(self, number):  # ----- Дает номер строки в котором находится картинка
        int_zn = 0
        for i in range(0, len(self.len_mass)):
            if (int(self.len_mass[i]) + int_zn) >= number:
                return i
            else:
                int_zn += self.len_mass[i]

    def start_fin(self, row):  # ----- Дает значения с которых начинается (и заканчивается) очередной ряд
        return sum(self.len_mass[:row]) + 1, sum(self.len_mass[:row]) + self.len_mass[row]


    def give_img(self, name, number):  # ------ Устaнавливает размер картинок
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
        self.new_img()


    def click_button(self, event):  # Обработка нажатия на кнопку в выборе картинок
        name = event.widget._name
        number = 1 if name == '!button' else int(name.split('!button')[1])

        self.give_img(name, number)  # Размер картинки
        self.new_img()  # Обновление коллекции


if __name__ == "__main__":
    root = Tk()  # ---- Открываем основное окно и сразу его прячем
    root.overrideredirect(1)
    root.withdraw()

    # Выводит значок программы в нижнюю панель
    img = tk.PhotoImage(file='img/Logo_JM.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)

    user_name = 'forcon'
    text_search = 'Птичка сердолик'

    img_url, autor_name, len_mass = creating_coll(user_name, text_search)
    img_coll = 16  # Количество изображений в коллекции

    app = SampleApp(img_url, len_mass, img_coll)
    app.mainloop()

    # root.destroy()
