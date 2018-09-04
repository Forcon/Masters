import sqlite3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import sqlite3 as lite
import sys
from PIL import Image, ImageDraw #Подключим необходимые библиотеки.
import urllib
import urllib.request, urllib.error, urllib.parse
import datetime

SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()

ssl._create_default_https_context = ssl._create_unverified_context

text = 'птичка сердолик'
item = []
item_url = [''] # для возможности беспроблемного переноса
k = 1
# --------- Извлекает со страницы ключевые слова и количество лайков
#URL = 'https://www.livemaster.ru/item/22734923-kukly-i-igrushki-pichuga-sedrik'
URL = 'https://www.livemaster.ru/item/13695699-ukrasheniya-podveska-osennij-list'

html = urlopen(URL).read()#.decode('cp1251')
bs = BeautifulSoup(html, "html.parser")

if 'Работа продана или удалена мастером' in bs.find("li", { "class" : "item-info__item" }).text:
    print('Работа продана или удалена мастером')

else:
    img_url = bs.find("a", { "class" : "photo-switcher__slide--active" }).img # Cохраняем картинку для коллекции
    img_url = str(img_url).split('src="')[1].split('"')[0]
    now_img = 'img/' + str(datetime.datetime.now()) + '.jpg'
    urllib.request.urlretrieve(img_url, now_img)

    try:
        price = bs.find("span", {"class": "price"}).text
        price = ''.join(str(re.search(r'.*', price).group(0)).split(' ')[:-1])
    except AttributeError:
        price = 0
        pass

    name = bs.find("a", { "class" : "master__name" }).text
    name_url = bs.find("a", { "class" : "master__name" })
    counter = bs.find("span", { "class" : "item-social-actions__counter" }).text[1:-1]
    list_item = bs.findAll("li", { "class" : "tag-list__item" })
    gallery_all = bs.findAll("span", { "class" : "item-social-actions__text" })
    link = bs.find("link", { "rel" : "canonical" })
    materyal = bs.find("span", { "class" : "js-translate-item-materials" }).text
    materyal = "".join([i for i in materyal if i.isalnum() or i ==' ' or i == ','])
    materyal = materyal.replace(', ', ',')
    size = bs.find("span", { "class" : "js-translate-item-size" }).text
    location = bs.find("div", { "class" : "master__location" }).text

    for el in list_item:
        item.append(el.text[1:-1])
    name_url = 'https://www.livemaster.ru/' + str(name_url).split('href="')[1].split('">')[0]
    url = str(link).split('"')[1]

    for el in gallery_all:
        if not el.text.find('Галерея коллекций с работой'):
            gallery = str(el.text).split('(')[1][:-1]

    print(url)
    print(name)
    print(name_url)
    print(item)
    print(materyal)
    print(price)
    print(size)
    print(location)
    print('В избранное - ' + counter)
    print('Галлерей с работой - ' + gallery)

    try:
        cursor.execute("""INSERT INTO 'Items' (
        'Autor', 'Url_Autor', 'Url_Item', 'Favor', 'Gallery', 'Tags', 'Word_Search', 'Price', 'Name_Img', 'Material', 'Size', 'Location') 
            VALUES ('{:s}', '{:s}', '{:s}', '{:}', '{:}', '{:}', '{:s}', '{:}', '{:s}', '{:s}', '{:s}', '{:s}')
            """.format(name, name_url, url, counter, gallery, ','.join(item).lower(), text, price, now_img, materyal.lower(), size, location))

        SQL_Connect.commit()  # Применение изменений к базе данных
        print('{0:} из {1:} ---> {2:.2%}'.format((k + 1), len(item_url), (k + 1) / len(item_url)))
    except sqlite3.Error as e:
        print(e, '----------> ?', name)

cursor.close()
SQL_Connect.close()

# <a class="master__name" href="surr">"Артефакториум"</a>
# <span class="item-social-actions__text">Галерея коллекций с работой (78)</span>