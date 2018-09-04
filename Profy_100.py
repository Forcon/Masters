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

import time
start = time.time()


SQL_Connect = sqlite3.connect('Adress_Profy.db')
cursor = SQL_Connect.cursor()

SQL_Connect_1 = sqlite3.connect('Probe.db')
cursor_new = SQL_Connect_1.cursor()

ssl._create_default_https_context = ssl._create_unverified_context # Использование ssl
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

# URL = 'https://profi.ru/repetitor/maths/s-foto/?seamless=1&tabName=PROFILES&profileId=MokeevMV' #

url_avt = []
# --------- Запуск Firefox
# opts = Options()
# opts.set_headless()
# assert opts.headless  # без графического интерфейса.
#
# driver = Firefox(options=opts)

driver = webdriver.Firefox()

for i_id in range (2002, 3994):
    cursor.execute("""SELECT URL FROM Rep WHERE (id = '{:}')""".format(i_id)) # Извлечение
    url_zn = str(cursor.fetchall()[0][0])
    print(str(i_id))

    driver.get(url_zn)
    time.sleep(0.5)
    driver.find_elements_by_class_name("profile-tab-link_desktop")[0].click()
    time.sleep(0.25)

    click_list = []
    lost = 9
    for k in range(2000):
        click_list = driver.find_elements_by_class_name("ui-link")
        l_d = len(click_list)
        # print(l_d, '-------')
        # for i, el in enumerate(driver.find_elements_by_class_name("ui-link")): #[1].click()
        for m in range(lost, l_d):
            el = click_list[m]
            if el.text == 'Показать ещё':
                el.click()
                time.sleep(0.25)
                lost = m
                break
        if m + 1 == l_d:# and not ('Показать ещё' in click_list):
            break

    k =- 1
    kol = 0
    for i, el in enumerate(driver.find_elements_by_class_name("ui-text_inline")):
        bs = BeautifulSoup(el.get_attribute('outerHTML'), "html.parser").text
        if str(bs).find(' 100 ба') != -1:
            text_o = str(bs)
            k = i + 2
        if k == i:
            bs_1 = BeautifulSoup(el.get_attribute('outerHTML'), "html.parser").text
            k = -1
            # print(bs_1, '------->',  text_o)
            try:
                kol +=1
                if kol == 1:
                    print(url_zn)
                    cursor_new.execute("""INSERT INTO 'New' (URL) VALUES('{:}')""".format(url_zn))
                    SQL_Connect_1.commit()  # Применение изменений к базе данных
                    cursor_new.execute("""UPDATE New SET  Znach_1 = ('{:s}'), Date_1 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))
                elif kol == 2:
                    cursor_new.execute("""UPDATE New SET  Znach_2 = ('{:s}'), Date_2 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))
                elif kol == 3:
                    cursor_new.execute("""UPDATE New SET  Znach_3 = ('{:s}'), Date_3 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))
                elif kol == 4:
                    cursor_new.execute("""UPDATE New SET  Znach_4 = ('{:s}'), Date_4 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))
                elif kol == 5:
                    cursor_new.execute("""UPDATE New SET  Znach_5 = ('{:s}'), Date_5 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))
                elif kol == 6:
                    cursor_new.execute("""UPDATE New SET  Znach_6 = ('{:s}'), Date_6 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))
                elif kol == 7:
                    cursor_new.execute("""UPDATE New SET  Znach_7 = ('{:s}'), Date_7 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))
                elif kol == 8:
                    cursor_new.execute("""UPDATE New SET  Znach_8 = ('{:s}'), Date_8 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))
                elif kol == 9:
                    cursor_new.execute("""UPDATE New SET  Znach_9 = ('{:s}'), Date_9 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))
                elif kol == 10:
                    cursor_new.execute("""UPDATE New SET  Znach_10 = ('{:s}'), Date_10 = ('{:s}') WHERE URL = ('{:}')""".format(text_o, str(bs_1), url_zn))

                SQL_Connect_1.commit()  # Применение изменений к базе данных
                # print(i)
                # print('{0:} из {1:} ---> {2:.2%}'.format((k + 1), len(item_url), (k + 1) / len(item_url)))
            except sqlite3.Error as e:
                print(e, '----------> ?', el)
        if kol > 10: break

cursor.close()
cursor_new.close()
SQL_Connect.close()
SQL_Connect_1.close()

print("\nTime: %.03f s" % (time.time() - start))

driver.close()
quit()