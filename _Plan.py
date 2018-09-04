"""Питон - управление коллекциями ЯМ
"Программа для автоматической генерации коллекций на Ярмарке Мастеров."

Как создается коллекция:
-------
Три части:
- Наполнение базы картинками;
- Отбор картинок из базы;
- Размещение картинок в коллекцию.

------
Размещение картинок (только для моего магазина):
- Берет файл, подготовленный программой
- Открывает ЯМ и авторизуется там (м.б. в фоновом режиме)
- Записывает данные
- Сохраняет как черновик
? Нужно ли тут какое-то облегчение выбора коллекции из всех файлов, заранее подготовленных (скорее всего да, кстати, этим функционалом можно будет дополнить коммерческую программу):
- Считывание с моего эккаунта всех картинок, актуальных для продажи работ, и выведение их на управляющую панель
- Выбор из картинок ту, которая войдет в коллекцию
- Управляющая панель, на которой можно "прокручивать" заранее подготовленные коллекции (с добавлением на пустое место целевой картинки)
? Возможность здесь же "двигать" картинки с места на место, с сохранением потом результата в файле / коллекции.
- Поля под название, описание (с возможностью оставить их пустыми)
- Возможность исключить из коллекции-черновика картинку, а также пометить / сохранить коллекцию-черновик на доработку, вместо того, чтобы сохранять на сайт.
------

Отбор картинок:
- В управляющем окне вводится запрос для поиска (+)
- Открывает браузер
- По заданным ключевым словам - генерится поиск картинок
- Данные по картинкам сохраняются в базу (отсеиваются материалы для творчества и винтаж (м.б. что-то еще, что не может войти в коллекцию))
- В конце выводится: сколько уникальных картинок полпало в базу
Для каждой такой картинки сохраняются в базе:
- Сама картинка (пока на диск компьютера)
- Ссылка на эту картинку
- Автор + ссылка на страницу
- Ключевые слова
- Кол-во добавления в избранное
- Адрес страницы
- Количество галлерей коллекций с работой
- Стоимость
- Материалы работы
- Дата создания страницы с работой (? - похоже что ее на странице с работой нет (см. Арлекин созданый 08-08-2018))
- ?
-------

Картинки - в коллекцию.
- По управляющей панели отбирает из базы картинки
- Выводит картинки в удобном виде (по авторам)
- При щелчке по картинке она помещается в "виртуальную коллекцию" (и показывает на демо-панели), остальные картинки того же автора помечаются как "не активные"
- Повторный щелчок по картинке разблокирует все картинки этого автора (и убирает из демо-пенели)
- После того, как нужное количество картинок отобрано, все сохраняется как файл с "коллекцией-черновиком"
- Не полностью сформированная коллекция должна помечаться "на доработку", так же такую отметку должна быть возможность поставить и специально

----
Нужна контрольная панель, которая позволяет задавать логику отбора картинок из базы:
- сами картинки: по слову поиска, по тегам, использованные или не использованные ранее в коллекциях...
- в горизонталях, например: самые популярные, самые помещаемые в коллекции, самые дорогие, дешевые, в диапазоне и т.д
- в вертикалях, например: авторы, получившие "лайк"
- работа производится с новыми коллекциями или коллекциями "на доработку"  (тогда авторы, попавшие в коллекцию, должны ультимативно подтягиваться из базы)

Нужна возможность (при формировании коллекции) ставить лайки автору, удалять авторов из базы, удалять картинки из базы (удаленные авторы и картинки не должны больше попадать в базу / отдельный вопрос про это при сохранении, либо отдельное движение: например двойной щелчок)
- При постановке автору "лайка", должны все его записи в базе получать эту отметку, включая те, которые добавляются после



Доработки:
1. Научиться генерить запросы к базе из контрольной панели (собирать "запрос на извлечение из кусочков") (+ понял как!)
2. Подтягивать реальные работы из базы
3. Генерить файл с адресами и тегами для вставки в коллекцию
4. Не уменьшать картинки, а, например, затенять их или делать полупрозрачными
5. Рисовать поверх картинок, например зачеркивания, чтобы обозначить, что картинка пойдет на удаление
5. Сделать возможность пополнить базу не только из поиска, но и работами конкретного автора  (в том числе по имени / ссылке на него)
8. Сделать "черную базу авторов", например в нее должны попадать авторы при удалении их из базы (еще одна база?), эти авторы не должны потом попадать в отбор. Должен быть режим просмотра этой базы + подтягивания работ этих авторов, с возможностью автора из базы исключить.
8.1 Сделать "черную базу работ", попавшие туда - потом в коллекцию не подтягиваются и не выводятся при поиске. Сделать режим на управляющей панели, когда это игнорируется, но работы получают отметку, что они в "черном списке". Отметку должна быть возможность снять и убрать работу из базы.
9. Нужны полосы прокрутки на панели вывода результатов и ограничение на размер панели от разрешения экрана + управление клавишами
10. Возможность наполнять уже ранее сгенеренные коллекции "на доработку"
11. Показывать на результатах отбора что та или иная картинку уже использовалась мной в коллекции
12. Сделать в базе поле "е-мейл" и "пароль", чтобы отбирать только сбор определенного пользователя.
13. Сделать возможность посмотреть картинку в размере, которую она будет иметь в готовой коллекции (увидеть всю коллекцию в таком размере?)
14. Работы самого автора не должны записываться в базу!
15. Сделать чтобы поле для записи разблокировалось сразу после отказа от закрытия окна.

--------
Не пролучается:
7. Найти на страничке работы дату создания и добавлять в базу - через создания своей странички, когда дата создания известна.
Похоже что на странице с работой даты нет (см. Арлекин созданый 08-08-2018))

--------

Сделано:
Дополнить базу всем, что можно взять со странички: например материал, размер и т.д. (4 ч.)
Нужна панель с выводом на нее результатов отбора в коллекцию (4 ч.)
Сделать, чтобы из отобраные работы можно было возвращать назад в отбор (6 ч.)
"""