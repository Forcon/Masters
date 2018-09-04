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

SQL_Connect = sqlite3.connect('Adress_Profy.db')
cursor = SQL_Connect.cursor()

ssl._create_default_https_context = ssl._create_unverified_context # Использование ssl
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

# URL = 'https://profi.ru/repetitor/maths/s-foto/?seamless=1&tabName=PROFILES' # Только математики
URL = 'https://profi.ru/repetitor/obshestvoznanie/s-foto/?seamless=1&tabName=PROFILES'

url_avt = []
err_i = 0
# --------- Запуск Firefox
opts = Options()
opts.set_headless()
assert opts.headless  # без графического интерфейса.

driver = Firefox(options=opts)

#  driver = webdriver.Firefox()
driver.get(URL)
# for i in range (1):
i = 0
try:
    while driver.find_element_by_class_name("pagination_desktop__show-more") != None:
        driver.find_element_by_class_name("pagination_desktop__show-more").click()
        i += 1
        print(i, ' - страниц')
        time.sleep(0.25)
except:
    pass

# breakpoint()
for i, el in enumerate(driver.find_elements_by_class_name("desktop-profile__name")):
    bs = BeautifulSoup(el.get_attribute('outerHTML'), "html.parser")
    url_rep = str(bs).split('href="')[1].split('" target="')[0]
    u = url_rep.replace('amp;tabName', 'tabName')
    u1 = u.replace('amp;profileTabName=reviews&amp;profileId', 'profileId')
    # url_avt.append('https://profi.ru' + u1)

# for el in url_avt:
    try:
        cursor.execute("""INSERT INTO 'Rep' ('URL') VALUES ('{:s}')""".format('https://profi.ru' + u1))
        SQL_Connect.commit()  # Применение изменений к базе данных
        print(i)
        # print('{0:} из {1:} ---> {2:.2%}'.format((k + 1), len(item_url), (k + 1) / len(item_url)))
    except sqlite3.Error as e:
        print(e, '----------> ?', el)
        err_i += 1

print('Записано: ', i)
print('Ошибок: ', err_i)

cursor.close()
SQL_Connect.close()

breakpoint()

print('--- ок ---')
driver.get(url_avt[0])
time.sleep(1)
driver.find_elements_by_class_name("profile-tab-link_desktop")[0].click()
time.sleep(0.25)

click_list = []
lost = 9
for k in range(100):
    click_list = driver.find_elements_by_class_name("ui-link")
    l_d = len(click_list)
    # print(l_d, '-------')
    # for i, el in enumerate(driver.find_elements_by_class_name("ui-link")): #[1].click()
    for i in range(lost, l_d):
        el = click_list[i]
        # print(i)
        if el.text == 'Показать ещё':
            el.click()
            time.sleep(0.25)
            # print(i)
            lost = i
            break
    if i + 1 == l_d:# and not ('Показать ещё' in click_list):
        break
    # print(k)
    # print('')
# for el in driver.find_elements_by_class_name("ui-text_italic"):
# for i, el in enumerate(driver.find_elements_by_class_name("ui-text_italic")):
#     bs = BeautifulSoup(el.get_attribute('outerHTML'), "html.parser").text
#     if str(bs).find('балл') != -1:
#         print(bs)
k =- 1
for i, el in enumerate(driver.find_elements_by_class_name("ui-text_inline")):
    bs = BeautifulSoup(el.get_attribute('outerHTML'), "html.parser").text
    if str(bs).find('100') != -1:
        text_o = str(bs)
        k = i + 2
    if k == i:
        bs_1 = BeautifulSoup(el.get_attribute('outerHTML'), "html.parser").text
        k = -1
        print(bs_1, text_o)

