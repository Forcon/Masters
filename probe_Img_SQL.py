# coding=utf-8
# import sqlite3
import sqlite3 as lite
import sys
import io
# from PIL import Image, ImageGrab, ImageDraw
from PIL import ImageTk  # $ pip install pillow

# filename = 'img/img_1.jpg'

"""
Функция открытия изображения в бинарном режиме (эксперименты)
"""


def readImage(filename):
    try:
        fin = open(filename, "rb")
        img = fin.read()
        return img

    except IOError as e:
        # В случае ошибки, выводим ее текст
        print("Error readImage %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:
        if fin:
            # Закрываем подключение с файлом
            fin.close()


def writeImage(data):
    try:
        fout = open('img/woman2.jpg', 'wb')
        fout.write(data)


    except IOError as e:
        # В случае ошибки, выводим ее текст
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

    finally:
        if fout:
            fout.close()


if __name__ == '__main__':

    # imag = Image.open('img/img_1.jpg')
    # imag.show()

    try:
        # Открываем базу данных
        con = lite.connect('Masters.db')
        cur = con.cursor()
        # Получаем бинарные данные нашего файла
        data = readImage('img/img_1.jpg')
        # # Конвертируем данные
        binary = lite.Binary(data)
        # Готовим запрос в базу
        # cur.execute("INSERT INTO Items(Image) VALUES (?) WHERE id = 1", (binary,))
        # print('{}'.format(binary))
        cur.execute("""UPDATE Items set Image = (?) WHERE id = 1""", (binary,))

        cur.execute("SELECT Image FROM Items WHERE id = 1")
        data = cur.fetchone()[0]

        # Самый простой
        # способ
        # создать
        # двоичный
        # поток - с
        # open()
        # с
        # 'b'
        # в
        # строке
        # режима:
        #
        # f = open("myfile.jpg", "rb")
        #
        # Бинарные потоки в памяти также доступны как объекты BytesIO:

        f = io.BytesIO(data)
        photo = ImageTk.PhotoImage(f.read())
        photo.show

        print(type(data))
        writeImage(bytes(data))
        # Выполняем запрос
        con.commit()

    # В случае ошибки выводим ее текст.
    except lite.Error as e:
        if con:
            con.rollback()

        print("Error %s:" % e.args[0])
        sys.exit(1)

    finally:
        if con:
            # Закрываем подключение с базой данных
            con.close()

#
# def sql_item():
#     SQL_Connect = sqlite3.connect('Masters.db')
#     cursor = SQL_Connect.cursor()
#
#
#
#
#     SQL_Connect.commit()  # Применение изменений к базе данных
#
#     cursor.close()
#     SQL_Connect.close()
#


# readImage(filename)

# sql_item()
