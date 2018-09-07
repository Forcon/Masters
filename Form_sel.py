import unittest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import sqlite3
from myRoot_text import *

"""
Предварительная версия программы для записи данных в коллекцию на моей странице(?)
"""

ssl._create_default_https_context = ssl._create_unverified_context # Использование ssl

url_collect = 'https://www.livemaster.ru/gallery/876453/edit&wf=general&pos=2'

# --------- Запуск Firefox без того, чтобы отборажать его на экране
# opts = Options()
# opts.set_headless()
# assert opts.headless  # без графического интерфейса.
#
# driver = Firefox(options=opts)


text_seach = 'кот серебряная подвеска'


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

try:
    driver.find_element_by_id("more-items-button-show").click()
except:
    pass
bs = BeautifulSoup(driver.find_element_by_id("caption").get_attribute('outerHTML'), "html.parser")
name_coll = str(bs).split('value="')[1].split('"')[0]

SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

# ----- Берем из базы 30 лучших
cursor.execute("""SELECT Autor, Url_Item, Tags, Favor, id FROM Items
            WHERE (Word_Search = '{:s}') AND (Use_in_Coll <> '{:s}' OR Use_in_Coll IS NULL) 
            ORDER BY Favor DESC LIMIT 30""".format (text_seach, name_coll)) # Извлечение при сортировке
adress_list = cursor.fetchall()

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

for el in id_list:
    cursor.execute("UPDATE Items SET Use_in_Coll = ('{:s}') WHERE id = ('{:}')".format(name_coll, el))

SQL_Connect.commit()  # Применение изменений к базе данных
cursor.close()
SQL_Connect.close()

tag_summ = {}
for el in srt_item:
    if el not in tag_summ: tag_summ[el] = 1
    else: tag_summ[el] += 1

srt_tag = [] # -------- Самые популярные тэги
for i, el in enumerate(sorted(tag_summ.items(), key=lambda x: x[1], reverse=True)):
    if i < 20: srt_tag.append(el[0])

# print(srt_tag)

# ------- Ищет только пустые поля, чтобы внести туда данные
for i, el in enumerate(driver.find_elements_by_class_name('uriInput')):
    el.send_keys(url_list[i])
    el.send_keys(Keys.ENTER)
#
# for el in srt_tag:# ---- Теги - в поле с ними
#     driver.find_element_by_id("tags-selectized").send_keys(el)
#     driver.find_element_by_id("tags-selectized").send_keys(Keys.ENTER)

driver.find_element_by_id("savebtn").click()

# <button class="btn btn--large" id="savebtn" onclick="DoAction('save'); return false;">Сохранить</button>
# print(elem)<input autocomplete="off" tabindex="" id="tags-selectized" style="width: 4px; opacity: 1; position: relative; left: 0px;" type="text">



# for i, el in enumerate(driver.find_elements_by_class_name('list-no-item')):
    # print(BeautifulSoup(el.get_attribute('outerHTML'), "html.parser"))
    # # if el.text == '  OK':
    #     # elem = driver.find_element_by_name("itemUrl_" + str(i + 1))

#<input class="itemMasterId" value="48062" type="hidden">

