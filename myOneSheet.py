from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import datetime
import re
import ssl
import sqlite3

def one_list(text, name_url):
    """
    Считывает данные про работу (автор, цена, материал и т.д.) с одной страницы,
    :param str text:
    :param str name_url:
    """
    item = []
    html = urlopen(name_url).read()  # .decode('cp1251')
    bs = BeautifulSoup(html, "html.parser")

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

        return (name, name_url, url, counter, gallery, ','.join(item).lower(), text, price, now_img, materyal.lower(), size, location)

# тестовая команда
if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    # --------- Формирует в базе данные по запросу ключевого слова
    name_url = 'https://www.livemaster.ru/item/26258031-ukrasheniya-kulon-s-nastoyaschimi-golubymi-tsvetami-iz-yuveli'

    text = 'брошь'
    html = urlopen(name_url).read()  # .decode('cp1251')
    bs = BeautifulSoup(html, "html.parser")

    baze = one_list(text, name_url) # ------- Сама программа -----------
    k = 0

    try:
        cursor.execute("""INSERT INTO 'Items' (
        'Autor', 'Url_Autor', 'Url_Item', 'Favor', 'Gallery', 'Tags', 'Word_Search', 'Price', 'Name_Img', 'Material', 'Size', 'Location') 
            VALUES ('{:s}', '{:s}', '{:s}', '{:}', '{:}', '{:}', '{:s}', '{:}', '{:s}', '{:s}', '{:s}', '{:s}')
            """.format(baze[0], baze[1], baze[2], baze[3], baze[4], baze[5], baze[6], baze[7], baze[8],
                       baze[9], baze[10], baze[11]))

        SQL_Connect.commit()  # Применение изменений к базе данных
        print(f"{baze[0]}: {k + 1} из {1} ---> {k + 1 / 1:.2%}")
        # print('{0:} : {1:} из {2:} ---> {3:.2%}'.format(baze[0], (0 + 1), 1, (0 + 1) / 1))
    except sqlite3.Error as e:
        print(e, '----------> ?', baze[0])

    cursor.close()
    SQL_Connect.close()