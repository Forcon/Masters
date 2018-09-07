# import requests
# from urllib.request import urlopen
# from selenium.webdriver.support.ui import Select
# from bs4 import BeautifulSoup
# import ssl
# import re
# import sqlite3
# import urllib
# import datetime
# from tkinter import *
# from tkinter import messagebox
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from myRoot_text import *
from myOneSheet import *

"""
Программа для считывания данных с ЯМ и помещения их в SQlite

Основная программа v 2.3 (с окном ввода)
 """
text_seach = 'птичка сердолик'
# text_seach = "ведьма украшение"

# root = Tk()
# text_seach = str(main(root)) # Получаем текст для дальнейшего поиска на ЯМ
# if text_seach == '':
#     sys.exit()
autor = 'set-bs'

ssl._create_default_https_context = ssl._create_unverified_context
SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

item_url = []
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

# --------- Формирует в базе данные по запросу ключевого слова
url_list = 'https://www.livemaster.ru/search.php?action=paging&searchtype=1&thw=0&from='
url_autor = 'https://www.livemaster.ru/set-bs'

# --------- Запуск Firefox
driver = webdriver.Firefox()


if autor == '':
    driver.get('https://www.livemaster.ru')
    element = driver.find_element_by_id("quicklogin").click()

    # ---- Авторизация на сайте ------
    # driver.find_element_by_name("login").send_keys("art.forcon@gmail.com")
    # driver.find_element_by_name("password").send_keys("1970Fortuna")
    # driver.find_element_by_name("password").send_keys(Keys.ENTER)
    #
    # time.sleep(1)

    elem = driver.find_element_by_name("search")
    elem.send_keys(text_seach)
    driver.find_element_by_class_name("ui-search-btn").submit()
    # elem.send_keys(Keys.ENTER)
    time.sleep(3)
else:
    driver.get(url_autor)

# -------- Показываем по 120 картинок на странице
try:
    driver.find_element_by_id("perPage").click()
    select = driver.find_elements_by_class_name("js-perpage-btn")
    for option in select:
        if option.get_attribute('data-value') == '6':
            option.click()
except:
    pass

pagesours = driver.page_source
bs = BeautifulSoup(pagesours, "html.parser")#, headers = headers) # ---------- Надо отработать вариант с возможными ошибками (например точно делится на 120, или меньше 40 и т.д.)
if bs.find('h1') == 'По данному запросу ничего не найдено':
    pass

if autor == '': # ----- Для данных по ключевым словам
    kol_znach = int(re.search(r'\s\d+\s', str(re.search(r'По Вашему запросу.+', bs.text)), flags=0).group())
    print(f"По Вашему запросу найдено {kol_znach} работ\n")

    # ------ Отсюда начинается сбор данных о работах
    item_collection = bs.findAll("a", { "class" : "item-block__name" })
    for el in item_collection: # ------ Собраем значения с первой страницы
        if not ('materialy-dlya-tvorchestva'  or 'vintazh' or 'dlya-ukrashenij') in str(el):# --------- Исключаем матариалы для творчества, винтаж и "для украшений" (и другое тоже добавляем, что не может входить в коллекцию)
            item_url.append(str(el).split('href="')[1].split('" title')[0])

    try: # ------- Пролистываем первую страницу
        driver.find_element_by_class_name("pagebar__arrow--right").click()
    except:
        pass

else: # --- Для данных по работам автора
    item_collection = bs.findAll("a", { "class" : "js-stat-main-item-title" })

    for el in item_collection: # ------ Собраем значения с первой страницы
        if not ('materialy-dlya-tvorchestva'  or 'vintazh' or 'dlya-ukrashenij') in str(el):# --------- Исключаем матариалы для творчества, винтаж и "для украшений" (и другое тоже добавляем, что не может входить в коллекцию)
            item_url.append(str(el).split('href="')[1].split('"')[0])

# --------- Собираем все значения ссылок на работы, начиная со второй страницы (пока без пролистывания по автору)
for i in range(1, int(kol_znach/120)+1):
    driver.get(url_list + str(120*i))
    pagesours = driver.page_source
    bs = BeautifulSoup(pagesours, "html.parser")
    item_collection = bs.findAll("a", {"class": "item-block__name"})

    for el in item_collection:
        if not ('materialy-dlya-tvorchestva' or 'vintazh' or 'dlya-ukrashenij') in str(el): # --------- Исключаем матариалы для творчества (можно и другие тоже добавить)
            item_url.append(str(el).split('href="')[1].split('" title')[0])

# ----- Проходим по каждой странице, собраем данные, записываем в базу
for k, el in enumerate(item_url):
    name_url = 'https://www.livemaster.ru/' + el
    baze = one_list(text_seach, name_url)

    try:
        cursor.execute("""INSERT INTO 'Items' (
        'Autor', 'Url_Autor', 'Url_Item', 'Favor', 'Gallery', 'Tags', 'Word_Search', 'Price', 'Name_Img', 'Material', 'Size', 'Location') 
            VALUES ('{:s}', '{:s}', '{:s}', '{:}', '{:}', '{:}', '{:s}', '{:}', '{:s}', '{:s}', '{:s}', '{:s}')
            """.format(baze[0], baze[1], baze[2], baze[3], baze[4], baze[5], baze[6], baze[7], baze[8],
                       baze[9], baze[10], baze[11]))

        SQL_Connect.commit()  # Применение изменений к базе данных
        print(f"{baze[0]}: {k + 1} из {len(item_url)} ---> {k + 1 / len(item_url):.2%}")
    except sqlite3.Error as e:
        print(e, '----------> ?', baze[0])

cursor.close()
SQL_Connect.close()

# Вы можете прочитать атрибут innerHTML, чтобы получить источник содержимого элемента или outerHTML для источника с текущим элементом.
# element.get_attribute('innerHTML')

