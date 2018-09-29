# coding=utf-8
from tkinter import *

# from tkinter.tix import *
# from tkinter import Tk, Button, Toplevel
from PIL import ImageTk  # $ pip install pillow
from pr03_Form_Collection import *
from def04_Frame_Scroll import *
from probe_Skr_new import *

"""
Версия 2.0: Основная программа
Выводит картинки для выбора из них лучших + показывает уже сформированную коллекцию
(Надо отработать с реальными картинками из базы)
"""
# user_name = 'forcon'
# text_search = 'Птичка сердолик'
#
# img_url, autor_name, len_mass = creating_coll(user_name, text_search)
# img_in_coll = []
# img_coll = 16  # Количество изображений в коллекции

# len_mass = [5, 3, 4] # Количество изображений в каждом ряду
# img_url = ['img/img_1.jpg',
# 'img/img_2.jpg',
# 'img/img_3.jpg',
# 'img/img_4.jpg',
# 'img/img_5.jpg',
# 'img/img_6.jpg',
# 'img/img_7.jpg',
# 'img/img_8.jpg',
# 'img/img_9.jpg',
# 'img/img_10.jpg',
# 'img/img_11.jpg',
# 'img/img_12.jpg']

    # print(img_in_coll)



    # root = Tk()
    # root.title("Выбор картинок в коллекцию")
    # root.geometry("800x550")

class SampleApp(Tk):
    def __init__(self, img_url, *args, **kwargs):
        super().__init__()
        # root = Tk.__init__(self, *args, **kwargs)
        self.img_url = img_url

        # self.label = Label(text="Можно уменьшить окно, чтобы активировать полосу прокрутки.")
        # self.label.pack()
        self.title("Выбор картинок в коллекцию")
        self.geometry("800x550")
        # self.resizable(width=False, height=False)

        # self.vscrollbar = Scrollbar(self, orient=VERTICAL)
        # self.vscrollbar.pack(side=RIGHT, fill=Y, expand=YES)
        # self.frame=VerticalScrolledFrame(self, self.vscrollbar)
        self.frame = VerticalScrolledFrame(self)

        for i, el in enumerate(self.img_url):
            if i > 0: break
            for y in range(1, len(len_mass) + 1):
                for x in range(1, (len_mass[y - 1] + 1)):
                    if not os.path.isfile(self.img_url[i]):  # Проверка на наличие картинки в базе
                        breakpoint()
                    image = ImageTk.PhotoImage(file=self.img_url[i])  # Открываем изображение.
                    btn = Button(self.frame.interior, image=image)
                    btn.image = image
                    btn.grid(row=y, column=x)
                    btn.bind('<Button-1>', self.click_button)
                    i += 1

        self.frame.pack(anchor=NW, fill=BOTH, expand=YES)
        # self.vscrollbar = Scrollbar(self, orient=VERTICAL)
        # self.frame.vscrollbar.pack(side=RIGHT, fill=Y, expand=YES)

        self.coll = Toplevel()
        self.coll.title("Картинки, включенные в коллекцию")
        self.coll.geometry("336x336+0+700")

        self.rez_col(img_coll)  # Делает пустые кнопки
    # coll.mainloop()

    def rez_col(self, img_coll):  # Вставляет в "готовую коллекцию" пустые кнопки
        for i in range(img_coll):
            image_1 = ImageTk.PhotoImage(file='img/img_0.jpg')
            buttn = Button(self.coll, image=image_1)
            buttn.image = image_1
            y = i // 4
            buttn.grid(row=y + 1, column=i - (y * 4))
            buttn.bind('<Button-1>', self.cl_coll)

    def new_img(self):  # Заливка новых изображений
        for i in range(img_coll):
            if len(img_in_coll) > i:
                name_img = img_in_coll[i]
            else:
                name_img = 'img/img_0.jpg'
            name_button = "!button" + ('' if i == 0 else str(i + 1))
            image_1 = ImageTk.PhotoImage(file=name_img)
            self.coll.children[name_button].config(image="{:}".format(image_1))
            self.coll.children[name_button].image = image_1

    def cl_coll(self, event):  # Какая из кнопок нажата на панели коллекций
        name = event.widget._name
        try:
            number = int(name.split('!button')[1])
        except:  # TODO: Нужно указание на правильную ошибку
            number = 1

        if len(img_in_coll) >= number:  # Если коллекция не пуста
            number_img = img_url.index(img_in_coll[number - 1]) + 1
            name = '!button' + ('' if number_img == 1 else str(number_img))
            self.give_img(name, number_img)

    def row_img(self, number):  # ----- Дает номер строки в котором находится картинка
        int_znach = 0
        for i in range(0, len(len_mass)):
            if (int(len_mass[i]) + int_znach) >= number:
                return i
            else:
                int_znach += len_mass[i]

    def start_fin(self, n, int_znach):  # ----- Дает количество начала (или конца) по списку, где есть значения
        start = 0
        for i, znac in enumerate(len_mass):
            if i < int_znach + n:
                start += znac
        return start

    def give_img(self, name, number):  # Устaнавливает размер картинок
        int_znach = self.row_img(number)
        if img_url[number - 1] in img_in_coll:
            img_in_coll.remove(img_url[number - 1])
            for i, el in enumerate(self.children):
                if self.start_fin(0, int_znach) <= i < self.start_fin(1, int_znach):
                    self.children[el].config(height="{:}".format(80))
        else:
            for i, el in enumerate(self.children):
                if self.start_fin(0, int_znach) <= i < self.start_fin(1, int_znach):
                    try:
                        img_in_coll.remove(img_url[i])
                    except:  # TODO: Нужно указание на правильную ошибку
                        pass
                    if el != name:
                        self.children[el].config(height="{:}".format(40))
                    else:
                        self.children[name].config(height="{:}".format(80))
                        img_in_coll.append(img_url[number - 1])
        self.new_img()

    def click_button(self, event):  # Обработка нажатия на кнопку в выборе
        name = event.widget._name
        try:
            number = int(name.split('!button')[1])
        except:  # TODO: Нужно указание на правильную ошибку
            number = 1  # TODO: qase

        self.give_img(name, number)  # Размер картинки
        self.new_img()  # Обновление коллекции


if __name__ == "__main__":
    user_name = 'forcon'
    text_search = 'Птичка сердолик'

    img_url, autor_name, len_mass = creating_coll(user_name, text_search)
    img_in_coll = []
    img_coll = 16  # Количество изображений в коллекции

    app = SampleApp(img_url)
    app.mainloop()

# for i, el in enumerate(img_url):
#     if i > 0: break
#     for y in range(1, len(len_mass) + 1):
#         for x in range(1, (len_mass[y - 1] + 1)):
#             if not os.path.isfile(img_url[i]): # Проверка на наличие картинки в базе
#                 breakpoint()
#             image = ImageTk.PhotoImage(file=img_url[i])  # Открываем изображение.
#             btn = Button(root, image=image)
#             btn.image = image
#             btn.grid(row=y, column=x)
#             btn.bind('<Button-1>', click_button)
#             i += 1


    # root.mainloop()
