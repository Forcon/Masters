# coding=utf-8
# import tkinter as tk
# from tkinter import Tk
import sqlite3
from collections import Counter

"""
Сохраняет промежуточные результаты создания коллекции в базу и извлекает из нее (незаконченную) коллекцию
"""


def open_coll(name_coll, cursor, sql_connect):
    """
    Ищем в базе название коллекции, если нет -- создаем запись
    :param sql_connect:
    :param cursor:
    :param str name_coll: Название коллекции
    :return:
    """
    cursor.execute("""SELECT id FROM Collection WHERE Name = '{:}' """.format(name_coll))
    id_znach = cursor.fetchall()

    if id_znach:  # Если массив пустой - создаем такую запись и возвращаем id
        cursor.execute("""INSERT INTO Collection (Name) VALUES ('{:s}') """.format(name_coll))
        sql_connect.commit()  # Применение изменений к базе данных
        cursor.execute("""SELECT id FROM Collection WHERE Name = '{:}' """.format(name_coll))
        id_znach = cursor.fetchall()

    return id_znach[0][0]


def url_name(img_coll, n_znach, cursor):
    """
    Ищет в базе картинки и ставит им в соответствие url работ, дополняет коллекцию до нужного размера пустыми значениями
    :param cursor:
    :param img_coll: Передаваемая коллекция (названия картинок)
    :param img n_znach: Количество картинок в коллекции (16 или 12)
    :return:
    """
    url_coll = []
    n_img = len(img_coll)
    if n_img:
        f_text = """SELECT Url_Item FROM Items WHERE Name_Img = '{:}'"""
        next_text = """ OR Name_Img = '{:}'""" * (n_img - 1)

        cursor.execute((f_text + next_text).format(*img_coll))
        url_coll = [el[0] for el in cursor.fetchall()]

    for i in range(n_znach - n_img):
        url_coll.append('')

    return url_coll


def save_collection(mass_url, u_name, id_coll, cursor, sql_connect):
    """

    :param mass_url:
    :param u_name:
    :param id_coll:
    :param cursor:
    :param sql_connect:
    """
    f_text = """UPDATE Collection set """
    next_text = ''
    last_text = """ WHERE id = '{:}'"""
    for i, el in enumerate(mass_url, 1):
        next_text += """Url_""" + str(i) + """ = '{:s}', """
    select = f_text + next_text[:-2] + last_text

    cursor.execute(select.format(*mass_url, id_coll))
    sql_connect.commit()  # Применение изменений к базе данных


def open_colection(id_el, n_znach, cursor):
    """
    Забирает из базы сохраненную ранее коллекцию
    :param n_znach: 
    :param cursor: 
    :param str id_el: Значение идентифкатора, по которому ишем сохраненную коллекцию
    :return:
    """
    f_text = """SELECT"""
    next_text = ''
    for i in range(1, n_znach+1):
        next_text += """ Url_""" + str(i) + ""","""
    last_text = """ FROM Collection WHERE id = '{:}'"""
    select = f_text + next_text[:-1] + last_text

    cursor.execute(select.format(id_el))
    url_coll = [el for el in cursor.fetchall()[0]]

    return url_coll


def convert_coll(coll_url, n_znach, cursor):
    """
    Делает из коллекции ссылок коллекцию картинок
    :param n_znach:
    :param cursor:
    :param coll_url:
    :return:
    """
    yes_znach = n_znach - Counter(coll_url)[''] # Считает количество непустых значений
    f_text = """SELECT Name_Img FROM Items WHERE Url_Item = '{:}'"""
    next_text = """ OR Url_Item = '{:}'""" * (yes_znach - 1)

    cursor.execute((f_text + next_text).format(*coll_url))
    url_coll = [el[0] for el in cursor.fetchall()]
    #
    # for i in range(Counter(coll_url)['']):
    #     url_coll.append('')

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

    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    id_coll = open_coll(name_coll, cursor, SQL_Connect)
    u_coll = url_name(img_in_coll, img_coll, cursor)
    save_collection(u_coll, user_name, id_coll, cursor, SQL_Connect)
    # collection_url = open_colection(id_coll, img_coll, cursor)
    # print(collection_url)
    # coll_img = convert_coll(collection_url, img_coll, cursor)
    # print(coll_img)

    cursor.close()
    SQL_Connect.close()