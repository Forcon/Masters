# coding=utf-8
# import tkinter as tk
# from tkinter import Tk
import sqlite3

"""
Сохраняет промежуточные результаты создания коллекции в базу и извлекает из нее (незаконченную) коллекцию
"""


def url_name(img_coll, n_koll):
    """
    Ищет в базе картинки и ставит им в соответствие url работ, дополняет коллекцию до нужного размера пустыми значениями
    :param img_coll:
    :return:
    """
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    url_coll = []
    n_img = len(img_coll)
    if n_img != 0:

        next_text = ''
        f_text = """SELECT Url_Item FROM Items WHERE Name_Img = '{:}'"""
        for i in range(n_img - 1):
            next_text += (""" OR Name_Img = '{:}'""")

        cursor.execute((f_text + next_text).format(*img_coll))
        url_coll = [el[0] for el in cursor.fetchall()]

    for i in range(n_koll - n_img):
        url_coll.append('')

    print(url_coll)

    cursor.close()
    SQL_Connect.close()

    return url_coll


def save_collection(mass_url, u_name):
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    # cursor.execute("""INSERT INTO Collection (User) VALUES ('{:s}') """.format(u_name))

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

    cursor.execute(select.format(*mass_url, 1))

    SQL_Connect.commit()  # Применение изменений к базе данных

    cursor.close()
    SQL_Connect.close()


if __name__ == "__main__":
    # root = Tk()  # ---- Открываем основное окно и сразу его прячем
    # root.withdraw()

    img_coll = 16  # Количество изображений в коллекции
    # img_in_coll = []
    img_in_coll = ['img/2018-09-09 18:29:48.252179.jpg', 'img/2018-09-09 18:30:16.962517.jpg',
                   'img/2018-09-09 18:30:21.743910.jpg', 'img/2018-09-09 18:29:57.566147.jpg']

    user_name = 'forcon'
    url_coll = url_name(img_in_coll, img_coll)
    if url_coll:
        save_collection(url_coll, user_name)
    else:
        print('База не обновлена')
