# coding=utf-8
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
import os
import time

from selenium import webdriver, common
from selenium.webdriver.support.ui import Select

from def_02_BlackAutor import *
from def_02_OneSheet import *
from form_02_TextSeach import *
from form_Boolean import *

"""
Программа для считывания данных с ЯМ и помещения их в SQlite
Основная программа v 2.3 (с окном ввода)
 """
URL_JM = 'https://www.livemaster.ru/'


def autor_item(url_autor):
    """
    # --- Для данных по работам автора
    :param driver:
    :param url_autor:
    :return:
    """
    item_url = []
    driver = webdriver.Firefox()
    driver.get(URL_JM + url_autor)

    # try:  # -------- Показываем по 120 картинок на странице
    Select(driver.find_element_by_name('cnt')).select_by_visible_text('120')
    # except:  # TODO: Нужно указание на правильную ошибку
    #     pass

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
        except common.exceptions.NoSuchElementException:
            iteration = False

    return item_url


def reseach_item(text_seach):
    """
    # ----- Для данных по ключевым словам
    :param driver:
    :param text_seach:
    :return:
    """
    item_url = []
    driver = webdriver.Firefox()
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

    # try:  # -------- Показываем по 120 картинок на странице
    driver.find_element_by_id("perPage").click()
    select = driver.find_elements_by_class_name("js-perpage-btn")
    for option in select:
        if option.get_attribute('data-value') == '6':
            option.click()
    # except:  # TODO: Нужно указание на правильную ошибку
    #     pass

    pagesours = driver.page_source
    bs = BeautifulSoup(pagesours, "html.parser")  # , headers = headers)
    # ---------- Надо отработать вариант с возможными ошибками (например точно делится на 120, или меньше 40 и т.д.)
    if bs.find('h1') == 'По данному запросу ничего не найдено':
        messagebox.showinfo("GUI Python", "По этому запросу ничего не найдено, попробуйте его переформулировать")
        exit()

    # kol_znach = int(re.search(r'\s\d+\s', str(re.search(r'По Вашему запросу.+', bs.text)), flags=0).group())
    # print(f"По Вашему запросу найдено работ: {kol_znach}")

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
        except common.exceptions.NoSuchElementException:  #
            iteration = False

    return item_url


# ==================== Главная программа ===================
def read_JM(autor_name):
    """

    :param str autor_name:
    :return:
    """
    sql_connect = sqlite3.connect('Masters.db')
    cursor = sql_connect.cursor()

    # --------- Запуск Firefox
    ssl._create_default_https_context = ssl._create_unverified_context

    # autor_name = 'forcon'
    #

    app = TextSearch()
    root.wait_window(app)
    rez_vibor = app.get()  # Получаем текст для дальнейшего поиска на ЯМ

    # rez_vibor = TextSearсh(root).sendValue  # Получаем текст для дальнейшего поиска на ЯМ
    text_seach = rez_vibor[1] if rez_vibor[1] != '' else rez_vibor[0]
    # driver = webdriver.Firefox()
    # item_url_spisok = []
    # item_url_spisok = autor_item(driver, text_seach) if rez_vibor[1] != '' else reseach_item(driver, text_seach)
    item_url_spisok = autor_item(text_seach) if rez_vibor[1] != '' else reseach_item(text_seach)
    # text_seach = 'Птичка сердолик'
    # item_url_spisok = reseach_item(text_seach)

    # ----- Проходим по каждой странице, собраем данные, записываем в базу
    kol_rab = len(item_url_spisok)
    rab_autor = 0
    print(f"Обрабатываются работы для внесения в базу: {kol_rab}\n")

    autor_black = black_url(autor_name)  # TODO: найти ошибку

    for k, el in enumerate(item_url_spisok):
        name_url = URL_JM + el
        base_one_list = one_list(name_url, autor_name, autor_black)  # Сбор данных со страницы с работой

        if base_one_list[0]:
            try:  # Проверяем наличие этой работы у нас в базе и удаляем старую картинку
                cursor.execute("""SELECT Name_Img FROM Items WHERE Url_Item = '{:s}'""".format(base_one_list[3]))
                img_name = cursor.fetchall()
                if not img_name:
                    pass
                else:
                    # try:
                    os.remove(str(os.getcwd() + '/' + img_name[0][0]))
                    # except:  # TODO: Нужно указание на правильную ошибку
                    #     pass
            except sqlite3.Error as e:
                print(e, '----------> ?', base_one_list[0])

            try:  # ---- Записываем данные со страницы
                cursor.execute("""INSERT INTO 'Items' ('Autor', 'Url_Autor', 'Url_Item', 'Favor', 'Gallery', 
                    'Tags', 'Price', 'Name_Img', 'Material', 'Size', 'Location', 'Word_Search') 
                    VALUES ('{:s}', '{:s}', '{:s}', '{:}', '{:}', '{:}', '{:}', '{:}', '{:}', '{:}', '{:s}', '{:s}')
                    """.format(base_one_list[1], base_one_list[2], base_one_list[3], base_one_list[4], base_one_list[5],
                               base_one_list[6], base_one_list[7], base_one_list[8], base_one_list[9],
                               base_one_list[10], base_one_list[11], text_seach))
                sql_connect.commit()  # Применение изменений к базе данных

                print(f"{base_one_list[1]}: {k + 1} из {kol_rab} ---> {(k + 1) / kol_rab:.2%}")
            except sqlite3.Error as e:
                print(e, '----------> ?', base_one_list[0])

            try:  # ---- Для этой вещи получаем данные про то, какие пользователи эту картинку уже использовали
                cursor.execute("""SELECT Coll_User FROM Items WHERE Url_Item = '{:s}'""".format(base_one_list[3]))
                autor_list = str(cursor.fetchall()[0][0])
            except sqlite3.Error as e:
                print(e, '----------> ?')

            if not autor_name in autor_list:
                # ---- Записываем обновленные данные о том, что и этот пользователь отобрал вещь в коллекцию
                new_list = ('' if (autor_list == '' or autor_list == 'None') else autor_list + ',') + autor_name
                try:
                    cursor.execute("""UPDATE Items set Coll_User = '{:s}' 
                                   WHERE (Url_Item = '{:s}')""".format(new_list, base_one_list[3]))
                    sql_connect.commit()  # Применение изменений к базе данных
                except sqlite3.Error as e:
                    print(e, '----------> ?')

        elif base_one_list[1] == 'Ваша работа':
            rab_autor += 1
            print(f"===> Вашу работу не записываем, будет сохранено работ: {kol_rab - rab_autor}")
        elif base_one_list[1] == 'Черный список':
            rab_autor += 1
            print(f"===> Автор {base_one_list[2]} в исключениях, будет сохранено работ: {kol_rab - rab_autor}")
        elif base_one_list[1] == 'Работа удалена':
            rab_autor += 1
            print(f"===> Работа {base_one_list[3]} удалена автором, будет сохранено работ: {kol_rab - rab_autor}")
            # надо добавить проверку наличия такой работы у нас в базе и ее удаление, если есть

    print(f"Всего в базу внесено работ: {kol_rab - rab_autor}")
    cursor.close()
    sql_connect.close()


if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    # center_window = ScreenSize(root)

    autor_name = 'forcon'
    read_JM(autor_name)

# Вы можете прочитать атрибут innerHTML, чтобы получить источник содержимого элемента или outerHTML 
# для источника с текущим элементом.
# element.get_attribute('innerHTML')

#
