from PIL import Image, ImageGrab, ImageDraw
from PIL import ImageTk  # $ pip install pillow
import sqlite3
from probe_sort import *
import os.path


SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

def creating_coll(user_name, text_search):
    cursor.execute("""SELECT Name_Img, Autor FROM Items WHERE (Word_Search = '{:s}' AND Coll_User LIKE '{:}') 
                        ORDER BY Autor ASC""".format(text_search, user_name))
    item_list = cursor.fetchall()
    # print(item_list)

    base_img = []
    base_autor = []
    dict_img_autor = {}
    for i, el in enumerate(item_list):
        if os.path.isfile(el[0]):
            dict_img_autor[el[0]] = el[1]
            # base_img.append(el[0])
            base_autor.append(el[1])
        else:
            # item_list.pop(i)
            # cursor.execute("DELETE FROM Items WHERE (Name_Img = ?)", (el[0],))
            # SQL_Connect.commit()  # Применение изменений к базе данных
            print(f'{i} ---> {el[0]}')
    # print(len(item_list))
    # print('\n')
    print(item_list)
    print(base_autor)
    # print('\n')


    koll_autor = []
    dict_kol_autor = {}
    for i, el in enumerate(base_autor):
        koll_autor.append(base_autor.count(el))
        if koll_autor[-1] > 1:
            del base_autor[i:i + koll_autor[-1] - 1]
        dict_kol_autor[el] = koll_autor[i]

    # print(dict_img_autor)
    # print(dict_kol_autor)
    # # print(base_img)
    # print(base_autor)

    cursor.close()
    SQL_Connect.close()

    base_img, base_autor, koll_autor = sort_massiv(dict_img_autor, dict_kol_autor)

    print(base_img)
    print(base_autor)
    print(koll_autor)

    return base_img, base_autor, koll_autor

if __name__ == '__main__':
    autor_name = 'forcon'
    t_search = 'выдра'
    creating_coll(autor_name, t_search)