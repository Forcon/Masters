import sqlite3

def sql_item():
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    autor_name = 'forcon'
    url_item = 'item/4527905-ukrasheniya-serebryanaya-podveska-ili-brosh-spyaschij-kot'


     # ---- Из этих данных забираем данные про то, какие пользователи эту картинку уже использовали
    cursor.execute("""SELECT Coll_Autor FROM Items WHERE Url_Item = '{:s}'""".format(url_item))
    autor_list = cursor.fetchall()

    if not autor_name in autor_list:
        autor_list.append(autor_name)
          # ---- Записываем обновленные данные о том, что и этот пользователь ее отобрал
        cursor.execute("""UPDATE 'Items' set Coll_Autor = '{:s}' 
                        WHERE (Url_Item = '{:s}')""".format(autor_list, autor_name))
        SQL_Connect.commit()  # Применение изменений к базе данных

    cursor.close()
    SQL_Connect.close()

if __name__ == '__main__':
    sql_item()