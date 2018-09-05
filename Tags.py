import sqlite3
import re
import numpy as np
"""
Программа для вытаскивания списка тегов из базы и отбора самых популярныхйф
"""

SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

text_seach = 'кот серебряная подвеска'
name_coll = 'Все в зеленом'

cursor.execute("""SELECT Autor, Url_Item, Tags, Favor, id FROM Items
            WHERE (Word_Search = '{:s}') AND (Use_in_Coll <> '{:s}' OR Use_in_Coll IS NULL) ORDER BY Favor DESC LIMIT 30""".format (text_seach, name_coll)) # Извлечение при сортировке
# cursor.execute("""SELECT Autor, Url_Item, Tags, Favor, id FROM Items
#                     WHERE Use_in_Coll IS NULL ORDER BY Favor DESC LIMIT 30""" .format(name_coll)) # Извлечение при сортировке

adress_list = cursor.fetchall()
# print(adress_list)

url_list = []
autor_list = []
srt_item = []
id_list = []
for el in adress_list:
    if el[0] not in autor_list:
        autor_list.extend(el[0].split(','))
        url_list.extend(el[1].split(','))
        srt_item.extend(el[2].split(','))
        id_list.append(el[4])

# for el in id_list:
#     cursor.execute("UPDATE Items SET Use_in_Coll = ('{:s}') WHERE id = ('{:}')".format(name_coll, el))

SQL_Connect.commit()  # Применение изменений к базе данных
cursor.close()
SQL_Connect.close()

# print(autor_list)
# print(url_list)
# print(id_list)

tag_summ = {}
for el in srt_item:
    if el not in tag_summ: tag_summ[el] = 1
    else: tag_summ[el] += 1

srt_tag = [] # -------- Самые популярны тэги
for i, el in enumerate(sorted(tag_summ.items(), key=lambda x: x[1], reverse=True)):
    if i < 20: srt_tag.append(el[0])

print(srt_tag)

print(url_list[0])