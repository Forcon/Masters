# coding=utf-8
import sqlite3


def black_url(my_name=''):
    """
    Забирает из базы данных сведения об авторах, которых конкретный пользователь не хочет включать в свою коллекцию.

    :param str my_name:
    :return str:
    """
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    black_list = []
    try:
        cursor.execute("""SELECT BlackURL FROM BlackAutor WHERE (MyName = '{:s}') OR MyName IS NULL """.format(my_name))
        black_list = cursor.fetchall()
    except sqlite3.Error as e:
        print(e, '----------> ?')

    cursor.close()
    SQL_Connect.close()

    # noinspection PyShadowingBuiltins
    list = []
    for el in black_list:  # TODO: =======> Можно ли как-то избежать такого преобразования, а сразу брать из базы?
        list.extend(el[0].split(','))

    return list


# тестовая команда
if __name__ == '__main__':
    name = 'masya'
    black_name = black_url(name)
    print(black_name)
