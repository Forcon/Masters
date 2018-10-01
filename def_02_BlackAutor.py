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

    try:
        cursor.execute("""SELECT BlackURL FROM BlackAutor WHERE (MyName = '{:s}') OR MyName IS NULL """.format(my_name))
        return [el[0] for el in cursor.fetchall()]
    except sqlite3.Error as e:
        print(e, '----------> ?')

    cursor.close()
    SQL_Connect.close()


# тестовая команда
if __name__ == '__main__':
    name = 'masya'
    black_name = black_url(name)
    print(black_name)
