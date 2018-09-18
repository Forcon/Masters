
import sqlite3

SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

def creating_coll(user_name, text_search):
    cursor.execute("""SELECT Name_Img, Autor FROM Items WHERE (Word_Search = '{:s}' AND Coll_User LIKE '{:}') 
                        ORDER BY Autor ASC""".format(text_search, user_name))
    item_list = cursor.fetchall()
    # print(item_list)

    base_img = []
    base_autor = []
    for el in item_list:
        base_img.append(el[0])
        base_autor.append(el[1])
    # print(base_autor)

    koll_autor = []
    for i, el in enumerate(base_autor):
        koll_autor.append(base_autor.count(el))
        m = koll_autor[-1]
        if m > 1:
            del base_autor[i:i + koll_autor[-1] - 1]

    print(koll_autor)
    # # print(base_img)
    # print(base_autor)

    cursor.close()
    SQL_Connect.close()
    return base_img, base_autor, koll_autor[:6]

if __name__ == '__main__':
    autor_name = 'forcon'
    t_search = 'выдра'
    creating_coll(autor_name, t_search)