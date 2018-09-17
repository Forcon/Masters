import datetime
import re
import sqlite3
import ssl
import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup

URL_JM = 'https://www.livemaster.ru/'

def one_list(name_url, autor_name, black_autor):
    """
    Считывает данные про работу (автор, цена, материал и т.д.) с одной страницы,
    :param str autor_name:
    :param str name_url:
    """
    item = []
    html = urlopen(name_url).read()  # .decode('cp1251')
    bs = BeautifulSoup(html, "html.parser")

    name_url = bs.find("a", {"class": "master__name"})
    name_url = str(name_url).split('href="')[1].split('">')[0]
    name = bs.find("a", {"class": "master__name"}).text

    if name_url == autor_name:
        return (False, 'Ваша работа')

    if name_url in black_autor:
        return (False, 'Черный список', name_url)

    if 'Работа продана или удалена мастером' in bs.find("li", {"class": "item-info__item"}).text:
        print('Работа продана или удалена мастером')
        return (False, 'Работа удалена', name_url, name)

    else:
        img_url = bs.find("a", {"class": "photo-switcher__slide--active"}).img  # Cохраняем картинку для коллекции
        img_url = str(img_url).split('src="')[1].split('"')[0]
        now_img = 'img/' + str(datetime.datetime.now()).replace('.', '_').replace(':', '_') + '.jpg'
        urllib.request.urlretrieve(img_url, now_img) # Записали на диск

        try:
            price = bs.find("span", {"class": "price"}).text
            price = ''.join(str(re.search(r'.*', price).group(0)).split(' ')[:-1])
        except AttributeError:
            price = 0
            pass

        counter = bs.find("span", {"class": "item-social-actions__counter"}).text[1:-1]
        list_item = bs.findAll("li", {"class": "tag-list__item"})
        gallery_all = bs.findAll("span", {"class": "item-social-actions__text"})
        link = bs.find("link", {"rel": "canonical"})
        url = str(link).split('"')[1][len(URL_JM):]
        try:
            materyal = bs.find("span", {"class": "js-translate-item-materials"}).text
            materyal = "".join([i for i in materyal if i.isalnum() or i == ' ' or i == ','])
            materyal = materyal.replace(', ', ',')
            size = bs.find("span", {"class": "js-translate-item-size"}).text
        except AttributeError:
            materyal = 'не указано'
            size = 'не указано'
        location = bs.find("div", {"class": "master__location"}).text

        for el in list_item:
            item.append(el.text[1:-1])

        for el in gallery_all:
            if not el.text.find('Галерея коллекций с работой'):
                gallery = str(el.text).split('(')[1][:-1]

        return (True, name, name_url, url, counter, gallery, ','.join(item).lower(),
                price, now_img, materyal.lower(), size, location)

# тестовая команда
if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    # --------- Формирует в базе данные по запросу ключевого слова
    name_url = 'https://www.livemaster.ru/item/18831117-ukrasheniya-tryapichnaya-ptichka-s-podveskoj'

    text = 'брошь'
    autor_name = 'forcon'
    html = urlopen(name_url).read()  # .decode('cp1251')
    bs = BeautifulSoup(html, "html.parser")

    baze = one_list(name_url, autor_name, [(''),('')]) # ------- Сама программа -----------
    k = 0

    if baze[0]:
        print(baze)
        # try:
        #     cursor.execute("""INSERT INTO 'Items' (
        #     'Autor', 'Url_Autor', 'Url_Item', 'Favor', 'Gallery', 'Tags', 'Word_Search', 'Price', 'Name_Img', 'Material', 'Size', 'Location')
        #         VALUES ('{:s}', '{:s}', '{:s}', '{:}', '{:}', '{:}', '{:}', '{:}', '{:}', '{:}', '{:}', '{:}')
        #         """.format(baze[1], baze[2], baze[3], baze[4], baze[5], baze[6], baze[7], baze[8], baze[9],
        #                    baze[10], baze[11], baze[12]))
        #
        #     SQL_Connect.commit()  # Применение изменений к базе данных
        #     print(f"{baze[1]}: {k + 1} из {1} ---> {k + 1 / 1:.2%}")
        #     # print('{0:} : {1:} из {2:} ---> {3:.2%}'.format(baze[0], (0 + 1), 1, (0 + 1) / 1))
        # except sqlite3.Error as e:
        #     print(e, '----------> ?', baze[0])

    cursor.close()
    SQL_Connect.close()