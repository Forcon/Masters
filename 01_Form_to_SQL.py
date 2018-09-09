# import requests
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# import ssl
# import re
# import sqlite3
# import urllib
# import datetime
# from tkinter import *
# from tkinter import messagebox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
from myRoot_text import *
from myOneSheet import *

"""
Программа для считывания данных с ЯМ и помещения их в SQlite
Основная программа v 2.3 (с окном ввода)
 """
URL_JM = 'https://www.livemaster.ru/'

def autor_item(url_autor):  # --- Для данных по работам автора
    item_url = []
    driver.get(URL_JM + url_autor)

    try:  # -------- Показываем по 120 картинок на странице
        Select(driver.find_element_by_name('cnt')).select_by_visible_text('120')
    except:
        pass

    iteration = True
    ver = 2
    while iteration:
        pagesours = driver.page_source
        bs = BeautifulSoup(pagesours, "html.parser")
        item_collection = bs.findAll("a", {"class": "js-stat-main-item-title"})

        for el in item_collection:  # ------ Собираем значения
            # Исключаем матариалы для творчества, винтаж и "для украшений"
            # (и другое тоже, что не может входить в коллекции)
            if not ('materialy-dlya-tvorchestva' or 'vintazh' or 'dlya-ukrashenij') in str(el):
                item_url.append(str(el).split('href="')[1].split('"')[0])

        try:  # ------- Пролистываем страницу и если это не удается -- завершаем цикл
            driver.find_element_by_link_text(str(ver)).click()
            ver += 1
        except:# =====> Как правильно задать (NoSuchElementException) ?
            iteration = False

    return item_url


def reseach_item(text_seach):  # ----- Для данных по ключевым словам
    item_url = []
    driver.get(URL_JM)
    # ---- Авторизация на сайте (если нужна) ------
    # element = driver.find_element_by_id("quicklogin").click()
    # driver.find_element_by_name("login").send_keys("art.forcon@gmail.com")
    # driver.find_element_by_name("password").send_keys("1970Fortuna")
    # driver.find_element_by_name("password").send_keys(Keys.ENTER)
    # time.sleep(1)

    elem = driver.find_element_by_name("search")  # Ввели запрос
    elem.send_keys(text_seach)
    driver.find_element_by_class_name("ui-search-btn").submit()
    time.sleep(3)

    try:  # -------- Показываем по 120 картинок на странице
        driver.find_element_by_id("perPage").click()
        select = driver.find_elements_by_class_name("js-perpage-btn")
        for option in select:
            if option.get_attribute('data-value') == '6':
                option.click()
    except:
        pass

    pagesours = driver.page_source
    bs = BeautifulSoup(pagesours, "html.parser")  # , headers = headers)
    # ---------- Надо отработать вариант с возможными ошибками (например точно делится на 120, или меньше 40 и т.д.)
    if bs.find('h1') == 'По данному запросу ничего не найдено':
        messagebox.showinfo("GUI Python", "По этому запросу ничего не найдено, попробуйте его переформулировать")
        exit()

    kol_znach = int(re.search(r'\s\d+\s', str(re.search(r'По Вашему запросу.+', bs.text)), flags=0).group())
    print(f"По Вашему запросу найдено {kol_znach} работ")

    iteration = True
    while iteration:
        pagesours = driver.page_source
        bs = BeautifulSoup(pagesours, "html.parser")

        item_collection = bs.findAll("a", {"class": "item-block__name"})
        for el in item_collection:  # ------ Собраем значения
            # Исключаем матариалы для творчества, винтаж и "для украшений"
            # (и другое тоже, что не может входить в коллекции)
            if not ('materialy-dlya-tvorchestva' or 'vintazh' or 'dlya-ukrashenij') in str(el):
                item_url.append(str(el).split('href="')[1].split('" title')[0])

        try:  # ------- Пролистываем страницу и если это не удается -- завершаем цикл
            driver.find_element_by_class_name("pagebar__arrow--right").click()
        except: # =====> Как правильно задать (NoSuchElementException) ?
            iteration = False
            pass

    return item_url


# ==================== Главная программа ===================

SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

# --------- Запуск Firefox
ssl._create_default_https_context = ssl._create_unverified_context
driver = webdriver.Firefox()

item_url_spisok = []

root = Tk()
rez_vibor = TextSearсh(root).sendValue  # Получаем текст для дальнейшего поиска на ЯМ
text_seach = rez_vibor[1] if rez_vibor[1] != '' else reseach_item(rez_vibor[0])
item_url_spisok = autor_item(text_seach) if rez_vibor[1] != '' else reseach_item(text_seach)

# ----- Проходим по каждой странице, собраем данные, записываем в базу
print(f"В базу будет внесено {len(item_url_spisok)} работ\n")
for k, el in enumerate(item_url_spisok):
    name_url = URL_JM + el
    baze = one_list(text_seach, name_url)

    try:
        cursor.execute("""INSERT INTO 'Items' (
            'Autor', 'Url_Autor', 'Url_Item', 'Favor', 'Gallery', 'Tags', 'Word_Search', 'Price', 'Name_Img', 'Material', 'Size', 'Location') 
            VALUES ('{:s}', '{:s}', '{:s}', '{:}', '{:}', '{:}', '{:s}', '{:}', '{:s}', '{:s}', '{:s}', '{:s}')
            """.format(baze[0], baze[1], baze[2], baze[3], baze[4], baze[5], baze[6], baze[7], baze[8],
                       baze[9], baze[10], baze[11]))

        SQL_Connect.commit()  # Применение изменений к базе данных
        print(f"{baze[0]}: {k + 1} из {len(item_url_spisok)} ---> {k + 1 / len(item_url_spisok):.2%}")
    except sqlite3.Error as e:
        print(e, '----------> ?', baze[0])

cursor.close()
SQL_Connect.close()

# Вы можете прочитать атрибут innerHTML, чтобы получить источник содержимого элемента или outerHTML для источника с текущим элементом.
# element.get_attribute('innerHTML')

