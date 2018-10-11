# coding=utf-8
# import tkinter as tk
# from tkinter import Tk
import sqlite3
from collections import Counter

"""
Сохраняет промежуточные результаты создания коллекции в базу и извлекает из нее (незаконченную) коллекцию
"""
def open_coll(name_coll):
    """
    Ищем в базе название коллекции, если нет -- создаем запись
    :param str name_coll: Название коллекции
    :return:
    """
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()
    cursor.execute("""SELECT id FROM Collection WHERE Name = '{:}' """.format(name_coll))
    id_znach = cursor.fetchall()

    if id_znach == []:
        cursor.execute("""INSERT INTO Collection (Name) VALUES ('{:s}') """.format(name_coll))
        SQL_Connect.commit()  # Применение изменений к базе данных
        cursor.execute("""SELECT id FROM Collection WHERE Name = '{:}' """.format(name_coll))
        id_znach = cursor.fetchall()

    cursor.close()
    SQL_Connect.close()

    return id_znach[0][0]


def url_name(img_coll, n_znach):
    """
    Ищет в базе картинки и ставит им в соответствие url работ, дополняет коллекцию до нужного размера пустыми значениями
    :param img_coll: Передаваемая коллекция (названия картинок)
    :param img n_znach: Количество картинок в коллекции (16 или 12)
    :return:
    """
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    url_coll = []
    n_img = len(img_coll)
    if n_img:
        f_text = """SELECT Url_Item FROM Items WHERE Name_Img = '{:}'"""
        next_text = (""" OR Name_Img = '{:}'""") * (n_img - 1)

        cursor.execute((f_text + next_text).format(*img_coll))
        url_coll = [el[0] for el in cursor.fetchall()]

    for i in range(n_znach - n_img):
        url_coll.append('')
    # print(url_coll)

    cursor.close()
    SQL_Connect.close()

    return url_coll


def save_collection(mass_url, u_name, id_coll):
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    f_text = """UPDATE Collection set """
    next_text = ''
    last_text = """ WHERE id = '{:}'"""

    for i, el in enumerate(mass_url, 1):
        next_text += """Url_""" + str(i) + """ = '{:s}', """

    select = f_text + next_text[:-2] + last_text
    # print(select)
    # cursor.execute("""UPDATE Collection set Url_1 = '{:s}', Url_2 = '{:s}', Url_3 = '{:s}', Url_4 = '{:s}',
    #             Url_5 = '{:s}', Url_6 = '{:s}', Url_7 = '{:s}', Url_8 = '{:s}', Url_9 = '{:s}', Url_10 = '{:s}',
    #             Url_11 = '{:s}', Url_12 = '{:s}', Url_13 = '{:s}', Url_14 = '{:s}', Url_15 = '{:s}', Url_16 = '{:s}'
    #             WHERE id = '{:}'""".format(*mass_url, 1))
    cursor.execute(select.format(*mass_url, id_coll))

    SQL_Connect.commit()  # Применение изменений к базе данных
    cursor.close()
    SQL_Connect.close()


def open_colection(id, n_znach):
    """
    Забирает из базы сохраненную ранее коллекцию
    :param str id: Значение идентифкатора, по которому ишем сохраненную коллекцию
    :return:
    """
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    f_text = """SELECT"""
    next_text = ''
    for i in range(1, n_znach+1):
        next_text += """ Url_""" + str(i) + ""","""
    last_text = """ FROM Collection WHERE id = '{:}'"""
    select = f_text + next_text[:-1] + last_text

    cursor.execute(select.format(id))
    url_coll = [el for el in cursor.fetchall()[0]]

    cursor.close()
    SQL_Connect.close()
    return url_coll


def convert_coll(coll_url, n_znach):
    """
    Делает из коллекции ссылок коллекцицию картинок
    :param coll_url:
    :return:
    """
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    yes_znach = n_znach - Counter(coll_url)[''] # Считает количество непустых значений
    f_text = """SELECT Name_Img FROM Items WHERE Url_Item = '{:}'"""
    next_text = (""" OR Url_Item = '{:}'""") * (yes_znach - 1)

    cursor.execute((f_text + next_text).format(*coll_url))
    url_coll = [el[0] for el in cursor.fetchall()]
    # print(select)

    cursor.close()
    SQL_Connect.close()
    return url_coll


if __name__ == "__main__":
    # root = Tk()  # ---- Открываем основное окно и сразу его прячем
    # root.withdraw()

    img_coll = 16  # Количество изображений в коллекции
    # img_in_coll = []
    img_in_coll = ['img/2018-09-09 18:29:48.252179.jpg', 'img/2018-09-09 18:30:16.962517.jpg',
                   'img/2018-09-09 18:30:21.743910.jpg', 'img/2018-09-09 18:29:57.566147.jpg']

    user_name = 'forcon'
    user_mail = 'forcon@mail.ru'
    name_coll = 'Выдры, птицы и ондатры'

    id_coll = open_coll(name_coll)
    # url_coll = url_name(img_in_coll, img_coll)
    # save_collection(url_coll, user_name, id_coll)
    collection_url = open_colection(id_coll, img_coll)
    print(collection_url)
    coll_img = convert_coll(collection_url, img_coll)
    print(coll_img)