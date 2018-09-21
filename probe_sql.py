# coding=utf-8
import sqlite3


SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

def probe_sql(user_name, text_search):
    """
    Это эксперимент по сбору SQL запроса "из кусочков", чтобы получать именно тот результат выдачи, который нужен
    :param str user_name:
    :param str text_search:
    :return:
    """
    # TODO: Эксперимент со сборкой запроса из базы "из кусочков"
    order_row_coll = ['Favor', 'Gallery', 'Price']

    sql_t_first = """SELECT Name_Img, Autor, """
    sql_t_last = """ FROM Items WHERE (Word_Search = '{:s}' 
                            AND (Coll_User LIKE '{:}' or Coll_User is NULL)) 
                            ORDER BY Autor ASC"""

    sql_text = sql_t_first + order_row_coll[2] + sql_t_last
    print(sql_text)

    sql_format = []
    sql_format.append(text_search)
    sql_format.append(user_name)

    cursor.execute(sql_text.format(*sql_format))
    # cursor.execute("""SELECT Name_Img, Autor, Favor FROM Items WHERE (Word_Search = '{:s}'
    #                     AND (Coll_User LIKE '{:}' or Coll_User is NULL))
    #                     ORDER BY Autor ASC""".format(text_search, user_name))
    item_list = cursor.fetchall()

    print(item_list)


    cursor.close()
    SQL_Connect.close()


if __name__ == '__main__':
    autor_name = 'forcon'
    t_search = 'Птичка сердолик'
    probe_sql(autor_name, t_search)
