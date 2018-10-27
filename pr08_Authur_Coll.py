# coding=utf-8
# import unittest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver import Firefox
# from selenium.common.exceptions import NoSuchElementException
import time
# from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import sqlite3

# from tkinter import *
# from my_02_TextSeach import *

"""
Авторизуется на сайте и заполняет коллекцию работами из базы + добавляет список тегов
(Доработки: надо будет увязать с собранными коллекциями)
"""

ssl._create_default_https_context = ssl._create_unverified_context  # Использование ssl
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

url_collect = 'https://www.livemaster.ru/gallery/2661313/edit&wf=my'
# text_seach = 'елочная игрушка дерево'

# root = Tk()
# text_seach = main(root)
# print(text_seach)
# print(text_seach.sendValue == '')
#
# if text_seach.sendValue == '':
#     sys.exit()

# --------- Запуск Firefox
driver = webdriver.Firefox()
driver.get('https://www.livemaster.ru')
element = driver.find_element_by_id("quicklogin").click()

# ---- Авторизация на сайте ------
driver.find_element_by_name("login").send_keys("art.forcon@gmail.com")
driver.find_element_by_name("password").send_keys("1970Fortuna")
driver.find_element_by_name("password").send_keys(Keys.ENTER)

time.sleep(1)
driver.get(url_collect)

# try:
driver.find_element_by_id("more-items-button-show").click()
# except:  # TODO: Нужно указание на правильную ошибку
#     pass
bs = BeautifulSoup(driver.find_element_by_id("caption").get_attribute('outerHTML'), "html.parser", headers=headers)
name_coll = str(bs).split('value="')[1].split('"')[0]

SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

autor_list = []
for i, el in enumerate(driver.find_elements_by_class_name('author')):  # ---- Вытащили имена авторов
    bs = BeautifulSoup(el.get_attribute('outerHTML'), "html.parser").text
    autor_list.append(bs)

# ----- Берем из базы 30 лучших
cursor.execute("""SELECT Autor, Url_Item, Tags, Favor FROM Items
            WHERE (Word_Search = '{:s}') AND (Use_in_Coll <> '{:s}' OR Use_in_Coll IS NULL) 
            ORDER BY Favor DESC LIMIT 100""".format(text_seach, name_coll))  # Извлечение при сортировке
adress_list = cursor.fetchall()

url_list = []
srt_item = []
for el in adress_list:
    if el[0] not in autor_list:
        autor_list.extend(el[0].split(','))
        url_list.extend(el[1].split(','))
        srt_item.extend(el[2].split(','))

tag_summ = {}
for el in srt_item:
    if el not in tag_summ:
        tag_summ[el] = 1
    else:
        tag_summ[el] += 1

srt_tag = []  # -------- Самые популярны тэги
for i, el in enumerate(sorted(tag_summ.items(), key=lambda x: x[1], reverse=True)):
    if i < 20:
        srt_tag.append(el[0])

# print(srt_tag)

# ------- Ищет только пустые поля, чтобы внести туда данные
for i, el in enumerate(driver.find_elements_by_class_name('uriInput')):
    el.send_keys(url_list[i])
    el.send_keys(Keys.ENTER)
    cursor.execute("UPDATE Items SET Use_in_Coll = ('{:s}') WHERE Url_Item = ('{:}')".format(name_coll, url_list[i]))

SQL_Connect.commit()  # Применение изменений к базе данных
cursor.close()
SQL_Connect.close()

# ---- Теги не подгружаются, если уже есть 20 штук...

for el in srt_tag:  # ---- Теги - в поле с ними
    if len(driver.find_elements_by_class_name('item')) < 20:
        driver.find_element_by_id("tags-selectized").send_keys(el)
        driver.find_element_by_id("tags-selectized").send_keys(Keys.ENTER)
    else:
        break

time.sleep(1)
driver.find_element_by_id("savebtn").click()
