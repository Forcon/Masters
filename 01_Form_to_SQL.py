import requests
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from bs4 import BeautifulSoup
import ssl
import re
import time
import sqlite3
import urllib
import datetime
from tkinter import *
from tkinter import messagebox
from Root_text import *

"""
Программа для считывания данных с ЯМ и помещения их в SQlite

Основная программа v 2.2 (с окном ввода)
 """

# def clear_text(): # ----- Очищает поле от введенного текста
#     text_entry.delete(0, END)
#
# def show_message(): # ----- Смотрит, введен ли текст и
#     if text_entry.get() == '':
#         messagebox.showinfo("GUI Python", "Надо ввести текст для поиска")
#     else:
#         # messagebox.showinfo("Начинаем поиск картинок по словосочетанию...", text_entry.get())
#         text = text_entry.get()
#         clear_text()
#         root.destroy()
#
# def text_search(): # ----- Создает плашку для ввода текста для поиска
#     global text_entry
#     global root
#     width = 600
#     height = 100
#     root = Tk()
#     width_sc = (root.winfo_screenwidth() - width) // 2
#     height_sc = (root.winfo_screenheight() - height) // 2
#
#     root.title("Отбор картинок в базу")
#     root.geometry(str(width) + "x" + str(height) + "+" + str(width_sc) + "+" + str(height_sc))
#
#
#     message = StringVar()
#     name_label = Label(text = 'Введите текст для поиска по "Ярмарке Мастеров":')
#     name_label.place(relx=.5, rely=.2, anchor="c")
#
#     text_entry = Entry(textvariable = message)
#     text_entry.place(relx=.5, rely=.5, anchor="c", width = 300)
#
#     message_button = Button(text="Найти картинки", command = show_message)
#     message_button.place(relx=.85, rely=.5, anchor="c")
#     root.mainloop()
#
#     return message.get()

def one_list(bs, i):
    """
    Считывает данные про работу (автор, цена, материал и т.д.) с одной страницы

    (надо сделать в виде отдельного файла для простоты отладки)
    """
    if 'Работа продана или удалена мастером' in bs.find("li", {"class": "item-info__item"}).text:
        print('Работа продана или удалена мастером')

    else:
        img_url = bs.find("a", {"class": "photo-switcher__slide--active"}).img  # Cохраняем картинку для коллекции
        img_url = str(img_url).split('src="')[1].split('"')[0]
        now_img = 'img/' + str(datetime.datetime.now()) + '.jpg'
        urllib.request.urlretrieve(img_url, now_img)

        try:
            price = bs.find("span", {"class": "price"}).text
            price = ''.join(str(re.search(r'.*', price).group(0)).split(' ')[:-1])
        except AttributeError:
            price = 0
            pass

        name = bs.find("a", {"class": "master__name"}).text
        name_url = bs.find("a", {"class": "master__name"})
        counter = bs.find("span", {"class": "item-social-actions__counter"}).text[1:-1]
        list_item = bs.findAll("li", {"class": "tag-list__item"})
        gallery_all = bs.findAll("span", {"class": "item-social-actions__text"})
        link = bs.find("link", {"rel": "canonical"})
        materyal = bs.find("span", {"class": "js-translate-item-materials"}).text
        materyal = "".join([i for i in materyal if i.isalnum() or i == ' ' or i == ','])
        materyal = materyal.replace(', ', ',')
        size = bs.find("span", {"class": "js-translate-item-size"}).text
        location = bs.find("div", {"class": "master__location"}).text

        for el in list_item:
            item.append(el.text[1:-1])
        name_url = 'https://www.livemaster.ru/' + str(name_url).split('href="')[1].split('">')[0]
        url = str(link).split('"')[1]

        for el in gallery_all:
            if not el.text.find('Галерея коллекций с работой'):
                gallery = str(el.text).split('(')[1][:-1]

        try:
            cursor.execute("""INSERT INTO 'Items' (
            'Autor', 'Url_Autor', 'Url_Item', 'Favor', 'Gallery', 'Tags', 'Word_Search', 'Price', 'Name_Img', 'Material', 'Size', 'Location') 
                VALUES ('{:s}', '{:s}', '{:s}', '{:}', '{:}', '{:}', '{:s}', '{:}', '{:s}', '{:s}', '{:s}', '{:s}')
                """.format(name, name_url, url, counter, gallery, ','.join(item).lower(), text, price, now_img,
                           materyal.lower(), size, location))

            SQL_Connect.commit()  # Применение изменений к базе данных
            print('{0:} из {1:} ---> {2:.2%}'.format((k + 1), len(item_url), (k + 1) / len(item_url)))
        except sqlite3.Error as e:
            print(e, '----------> ?', name)

"""
Основная программа для сбора картинок и информации про работу в базу
"""

# text = "ведьма украшение"

root = Tk()
text = str(main(root)) # Получаем текст для дальнейшего поиска на ЯМ
if text == '':
    sys.exit()

ssl._create_default_https_context = ssl._create_unverified_context
SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

item_url = []
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

# --------- Формирует в базе данные по запросу ключевого слова
url_list = 'https://www.livemaster.ru/search.php?action=paging&searchtype=1&thw=0&from='
# text = 'птичка сердолик'

# --------- Запуск Firefox
driver = webdriver.Firefox()
driver.get('https://www.livemaster.ru')
element = driver.find_element_by_id("quicklogin").click()

# ---- Авторизация на сайте ------
driver.find_element_by_name("login").send_keys("art.forcon@gmail.com")
driver.find_element_by_name("password").send_keys("1970Fortuna")
driver.find_element_by_name("password").send_keys(Keys.ENTER)

time.sleep(1)

elem = driver.find_element_by_name("search")
elem.send_keys(text)
driver.find_element_by_class_name("ui-search-btn").submit()
# elem.send_keys(Keys.ENTER)
time.sleep(3)

# -------- Показываем по 120 на странице
try:
    Select(driver.find_element_by_name('cnt')).select_by_visible_text('120')
except:
    pass

pagesours = driver.page_source
bs = BeautifulSoup(pagesours, "html.parser")#, headers = headers) # ---------- Надо отработать вариант с возможными ошибками (например точно делится на 120, или меньше 40 и т.д.)
if bs.find('h1') == 'По данному запросу ничего не найдено':
    pass

kol_znach = int(re.search(r'\s\d+\s', str(re.search(r'По Вашему запросу.+', bs.text)), flags=0).group())
print(kol_znach)

item_collection = bs.findAll("a", { "class" : "js-stat-main-item-title" })
for el in item_collection:
    if not ('materialy-dlya-tvorchestva'  or 'vintazh' or 'dlya-ukrashenij') in str(el):# --------- Исключаем матариалы для творчества, винтаж и "для украшений" (и другое тоже добавляем, что не может входить в коллекцию)
        item_url.append(str(el).split('href="')[1].split('" itemprop=')[0])

try:
    driver.find_element_by_class_name("pagebar__page").send_keys(Keys.ENTER)
except:
    pass

# --------- Собираем все значения ссылок на работы
for i in range(1, int(kol_znach/120)+1):
    driver.get(url_list + str(120*i))
    pagesours = driver.page_source
    bs = BeautifulSoup(pagesours, "html.parser")
    item_collection = bs.findAll("a", { "class" : "js-stat-main-item-title" })

    for el in item_collection:
        if not ('materialy-dlya-tvorchestva' or 'vintazh' or 'dlya-ukrashenij') in str(el): # --------- Исключаем матариалы для творчества (можно и другие тоже добавить)
            item_url.append(str(el).split('href="')[1].split('" itemprop=')[0])
"""
Выше -- какой-то повтор кода, надо пом с ним разобраться...
"""

for k, el in enumerate(item_url):
    item = []
    name_url = 'https://www.livemaster.ru/' + el
    html = urlopen(name_url).read()  # .decode('cp1251')
    bs = BeautifulSoup(html, "html.parser")
    one_list(bs, k)

cursor.close()
SQL_Connect.close()

# Вы можете прочитать атрибут innerHTML, чтобы получить источник содержимого элемента или outerHTML для источника с текущим элементом.
# element.get_attribute('innerHTML')
