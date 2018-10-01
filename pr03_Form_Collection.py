# coding=utf-8
import os.path
import sqlite3

import numpy as np

SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()


def sort_all(img, autor, score, len_user):
    """
    Сортировка массивов взаимовлияющая -
    """

    # img = ('img_1', 'img_2', 'img_3', 'img_4', 'img_5', 'img_6', 'img_7')
    # autor = ('Masya', 'Forcon', 'Forcon', 'Forcon', 'Alex', 'Tupsya', 'Tupsya')
    # score = (1, 5, 2, 3, 7, 4, 6)
    # len_user = (1, 3, 3, 3, 1, 2, 2)

    ind = np.lexsort((img, autor, score, len_user))  # Сначала самый правый и т.д.

    image = list(reversed([(img[i]) for i in ind]))
    aut = list(reversed([(autor[i]) for i in ind]))
    # fav = list(reversed([(score[i]) for i in ind]))
    #
    # # print(image)
    # # print(aut)
    # print(fav)

    return image, aut


def creating_coll(user_name, text_search):
    """
    Получает данные из базы и разбирает их на отдельные массивы (а затем они сортируются)
    :param str user_name:
    :param str text_search:
    :return:
    """
    # TODO: Эксперимент со сборкой запроса из базы "из кусочков"
    cursor.execute("""SELECT Name_Img, Autor, Favor FROM Items WHERE (Word_Search = '{:s}' 
                        AND (Coll_User LIKE '{:}' or Coll_User is NULL)) 
                        ORDER BY Autor ASC""".format(text_search, user_name))
    item_list = cursor.fetchall()
    # print(item_list)

    img_base = []
    autor_base = []
    favor_base = []
    koll_base = []
    for i, el in enumerate(item_list):  # Делает отдельные массивы
        if os.path.isfile(el[0]):
            img_base.append(el[0])
            autor_base.append(el[1])
            favor_base.append(0 if el[2] == '' else el[2])
            # koll_base.append(item_list[1].count(el[1]))
        else:
            item_list.pop(i)  # Удаляет из списка и из базы записи, если нет файла на диске.
            cursor.execute("DELETE FROM Items WHERE (Name_Img = ?)", (el[0],))
            SQL_Connect.commit()  # Применение изменений к базе данных
            print(f'{i} ---> {el[0]}')

    for el in autor_base:
        koll_base.append(autor_base.count(el))

    # print(img_base)
    # print(autor_base)
    # print(favor_base)
    # print(koll_base)
    # print(koll_autor) # Сколько картинок у автора

    cursor.close()
    SQL_Connect.close()

    img_base, autor_base = sort_all(img_base, autor_base, favor_base, koll_base)

    koll_autor = []
    autor_base_copy = autor_base[:]
    for i, el in enumerate(autor_base_copy):
        koll_autor.append(autor_base_copy.count(el))
        if koll_autor[-1] > 1:
            del autor_base_copy[i:i + koll_autor[-1] - 1]

    # print('\n')
    # # print(img_base)
    # print(autor_base_copy)
    # print(koll_autor)

    return img_base, autor_base_copy, koll_autor


if __name__ == '__main__':
    autor_name = 'forcon'
    t_search = 'Птичка сердолик'
    creating_coll(autor_name, t_search)
