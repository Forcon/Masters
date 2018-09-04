import sqlite3
import time

rez = []

SQL_Connect = sqlite3.connect('Probe.db')
cursor = SQL_Connect.cursor()

#
# id_1 = "SELECT * FROM New WHERE id = ('{:}')"
# url_1 = "SELECT * FROM New ORDER BY URL"

    # m = int(input())
    # if  == 0:
    # cursor.execute(id_1.format(m))
    # else:
    #     cursor.execute(url_1)

# cursor.execute("SELECT id FROM New ORDER BY id") # ----- Вытаскиваем год для сортировки
# i_id = cursor.fetchall()
#
# for el in i_id:
#     cursor.execute("SELECT Date_1 FROM New WHERE id = ('{:}')".format(el[0]))
#     date_1 = cursor.fetchall()
#     date_1 = date_1[0][0][-4:]
#     # print(date_1)
#     cursor.execute("UPDATE New SET Yar = ('{:s}') WHERE id = ('{:}')".format(date_1, el[0]))
# SQL_Connect.commit()  # Применение изменений к базе данных
#
# breakpoint()

cursor.execute("SELECT id FROM New ORDER BY id")
i_id = cursor.fetchall()

rez = []
for i, el in enumerate(i_id, 1):
    if i > 100:
        # print(el[0])
        cursor.execute("SELECT URL, Date_1, Znach_1, Date_2, Znach_2, Date_3, Znach_3, Date_4, Znach_4, Date_5, Znach_5 FROM New WHERE id = ('{:}')".format(el[0]))

        # print(cursor.fetchall())
        # rez.extend(cursor.fetchall())
        rez = cursor.fetchall()
        # print(rez[0])

        # breakpoint()
        for el in rez[0]:
            # print(el[k])
            if el == None:
                break
            else:
                # pass
            # print(el)
                print(el)

        # del_baze = int(input())
        #
        # if del_baze == 0:
        #     try:
        #         cursor.execute("DELETE FROM New WHERE id = ('{:}')".format(i))
        #         SQL_Connect.commit()  # Применение изменений к базе данных
        #         print("------ Удалил! -------")
        #     except sqlite3.Error as e:
        #         print(e, '----------> ?', el)

cursor.close()