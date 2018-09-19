import sqlite3

SQL_Connect = sqlite3.connect('Samizdat.db')
cursor = SQL_Connect.cursor()


cursor.execute("SELECT * FROM 'Samizdat'") # Извлечь все из таблицы Самиздат
for el in cursor:
    # print(el)
    pass
cursor.execute("SELECT * FROM Samizdat WHERE Aдpeс LIKE '%@%'") # Все строки, где есть сивол @ в столбце Адрес
# print(cursor.fetchall())
cursor.execute("SELECT ФИО, Название FROM Samizdat WHERE Aдpeс LIKE '%@%'") # Только из столбца Адрес все мейлы
print(cursor.fetchall())

cursor.execute("SELECT MAX(id), ФИО FROM Samizdat") # Максимальное заначение id
print(cursor.fetchall())

cursor.execute("DELETE FROM Адреса_страниц WHERE (Адреса = ?)", (k,))
SQL_Connect.commit()  # Применение изменений к базе данных

cursor.execute("""SELECT Name_Img, Autor FROM Items WHERE (Word_Search = '{:s}' 
                    AND (Coll_User LIKE '{:}' or Coll_User is NULL)) 
                    ORDER BY Autor ASC""".format(text_search, user_name))

cursor.close()
SQL_Connect.close()