# coding=utf-8
# import tkinter as tk
# from tkinter import Tk
import sqlite3

"""
Сохраняет промежуточные результаты создания коллекции в базу
"""

def url_name(img_coll):
    """
    Ищет в базе картинки и ставит им в соответствие url работ
    :param img_coll:
    :return:
    """

    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    url_coll = []
    for i, el in enumerate(img_coll):
        cursor.execute("""SELECT Url_Item FROM Items WHERE Name_Img = '{:s}'""".format(el))
        url_coll.append(cursor.fetchall()[0][0])
    # print(url_coll)

    cursor.close()
    SQL_Connect.close()

    return url_coll


def save_collection(mass_url, u_name):

    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    cursor.execute("""INSERT INTO Collection (User) VALUES ('{:s}') """.format(u_name))

    for i, el in enumerate(mass_url, 1):
        select = """UPDATE Collection set Url_""" + str(i) + """ = '{:s}'  WHERE id = '{:}' """
        cursor.execute(select.format(el, 1))

    SQL_Connect.commit()  # Применение изменений к базе данных

    cursor.close()
    SQL_Connect.close()


if __name__ == "__main__":
    # root = Tk()  # ---- Открываем основное окно и сразу его прячем
    # root.withdraw()
    img_in_coll = ['img/2018-09-09 18:29:48.252179.jpg', 'img/2018-09-09 18:30:16.962517.jpg',
                   'img/2018-09-09 18:30:21.743910.jpg', 'img/2018-09-09 18:29:57.566147.jpg']


    user_name = 'forcon'
    url_coll = url_name(img_in_coll)
    save_collection(url_coll, user_name)