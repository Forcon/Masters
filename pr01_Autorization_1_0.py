# coding=utf-8
# from tkinter import *
# import sqlite3
# from tkinter import messagebox
# from myBoolean import *  # Дополнительные окна

from pr02_Form_to_SQL import *

# from myDialog import *
"""
Программа создает окно авторизации, где можно либо авторизоваться в программе, либо завести нового пользователя.
Нужно, чтобы использовтаь свои наработки в базе + не подтягивать собственные работы в выборку
"""
URL_JM = 'https://www.livemaster.ru/'


class Text_Entry:
    """
    Создает пару: подпись и поле для заполнения
    """
    def __init__(self, master, message='[имя поля]', pi_y=10, show='', url=''):
        """
        :param str message:
        :param int pi_y:
        :param str show:
        :param str url:
        """
        self.name_label = Label(master, text=message)
        self.name_label.place(relx=.05, y=pi_y, anchor="w")
        self.x = StringVar()
        self.text_entry = Entry(master, textvariable=self.x, show=show)
        self.url = url
        self.text_entry.insert(END, self.url)
        self.text_entry.place(relx=.5, y=pi_y, anchor="c", width=300)

    def get(self):
        return self.x.get()[len(self.url):]


class Btn:
    """
    Создает кнопку
    """
    def __init__(self, master, text='[надпись]', ver=0, r_y=0, fg='black'):
        """
        Создает кнопку
        :param master:
        :param str text:
        :param str ver:
        :param float r_y:
        :param str fg:
        """
        self.button_name = Button(master, text=text, command=lambda: master.check_entry(ver),
                                  width=14, height=3, fg=fg)
        self.button_name.place(relx=.87, rely=r_y, anchor="c")


class Auto_Main(Toplevel):
    """
    Класс главного окна, создает окно авторизации
    """
    def __init__(self):  # ----- Создает плашку для ввода текста для поиска
        super().__init__()
        # self.master = master
        self.sendValue = ''
        self.title("Авторизация в программе")
        self.geometry(Center_widows(600, 200))  # Располагает по центру страницы
        # self.message = StringVar()
        self.name_label = Label(text='Введите необходимые данные ниже:')
        self.name_label.place(relx=.5, y=20, anchor="c")

        self.Mail = Text_Entry(self.master, 'E-mail:*', 50)
        self.Password = Text_Entry(self.master, 'Пароль:*', 90, '*')
        self.FIO = Text_Entry(self.master, 'Имя:', 130)
        self.Address = Text_Entry(self.master, 'Адрес на ЯМ:', 170, url=URL_JM)
        self.focus_ini()

        Btn(self, "Авторизоваться*", 'auto', .35, fg='green')
        Btn(self, "Новый автор", 'new', .75)
        self.protocol('WM_DELETE_WINDOW', self.exit_method)


    def focus_ini(self, step=0):
        """
        Устанавливает фокус либо на первом пустом поле, либо на поле, для которого указан порядковый номер
        :param int step:
        """
        if step == 0:
            if self.Mail.get() == '':
                self.Mail.text_entry.focus_set()  # Ставит курсор в первое пустое поле
            elif self.Password.get() == '':
                self.Password.text_entry.focus_set()
            elif self.FIO.get() == '':
                self.FIO.text_entry.focus_set()
            elif self.Address.get() == '':
                self.Address.text_entry.focus_set()

        else:
            if step == 1:
                self.Mail.text_entry.focus_set()  # Ставит курсор в указаннное пустое поле
            elif step == 2:
                self.Password.text_entry.focus_set()
            elif step == 3:
                self.FIO.text_entry.focus_set()
            elif step == 4:
                self.Address.text_entry.focus_set()


    @staticmethod
    def base_read(mail):
        """
        Считывает из базы данные пользователя при авторизации
        :param str mail:
        :return:
        """
        try:  # Считываем из базы все что есть по данному е-мейлу
            cursor.execute("SELECT Mail, Pass, FIO, URL_User FROM Autor WHERE Mail = '{:s}'".format(mail))
            mail_sql = cursor.fetchall()
            # Если такой мейл есть в базе -- запишем в переменные, иначе - ''
            if mail_sql == []:
                return '', '', '', ''
            else:
                return mail_sql[0][0], mail_sql[0][1], mail_sql[0][2], mail_sql[0][3]
        except sqlite3.Error as e:
            print(f"Ошибка при чтении из базы: {e}")


    def return_disc(self, action='auto'):
        """
        Программа возвращает словарь со значениями
        :param str action:
        """
        self.ReturnValue = {'FIO': self.FIO.get(), 'Mail': self.Mail.get(), 'Password': self.Password.get(),
                            'Adress': self.Address.get(), 'User': self.adress_sql, 'Name': self.name_sql,
                            'Action': action}
        self.destroy()


    def check_entry(self, btn):  # ----- Смотрит, введен ли нужный текст и выдает предупреждение
        """
        Подпрограмма проверяет все возможные типы ошибок при введении текста в поля,
        :param str btn:
        """
        # Плучаем данные пользователя из базы
        self.mail_sql, self.password_sql, self.name_sql, self.adress_sql = self.base_read(self.Mail.get())

        if FALSE:  # Это как раз и есть проверка всех полей на корректность заполнения
            pass
        elif btn == 'new' and (self.FIO.get() == '' or self.Mail.get() == ''
                               or self.Password.get() == '' or self.Address.get() == ''):
            # InformWin("Подсказка:", "Надо заполнить все поля")
            messagebox.showinfo("Подсказка:", "Надо заполнить все поля")
            self.focus_ini()
        elif btn == 'auto' and (self.Mail.get() == '' or self.Password.get() == ''):
            messagebox.showinfo("Подсказка:", "Надо ввести е-мейл и пароль")
            self.focus_ini()
        elif not re.fullmatch(r"[\w'._+-]+@[\w'._+-]+[.][\w'._+-]+", self.Mail.get()):
            messagebox.showinfo("Подсказка:", "Формат е-мейла неверный.")
            self.focus_ini(1)
        elif btn == 'auto' and self.mail_sql == '':
            messagebox.showinfo("Подсказка:", "Пользователя с адресом '{:s}' нет в базе. "
                                              "Вы можете создать нового пользователя.".format(self.Mail.get()))
            self.focus_ini(1)
        elif btn == 'new' and re.search(r"[а-яА-ЯёЁ]", self.Address.get()):
            messagebox.showinfo("Подсказка:", "В адресе не может быть русских букв")
            self.focus_ini(4)
        elif btn == 'auto' and self.password_sql != self.Password.get():
            messagebox.showinfo("Подсказка:", "Пароль для данного адреса другой")
            self.Password.text_entry.delete('0', END)
            self.focus_ini(2)
        elif btn == 'new' and self.mail_sql != '' and self.password_sql == self.Password.get():
            if self.dop_param('Пользователь с е-мейлом: ' + self.mail_sql + " уже есть в базе. Хотите авторизоваться?"):
                # btn = 'auto'
                self.refresh_dan(self.name_sql, self.adress_sql)
            else:
                self.destroy()
        elif btn == 'new':
            password_new = self.open_dialog(text='Введите пароль еще раз...')
            if password_new != self.Password.get():
                messagebox.showinfo("Подсказка:", "Пароли не совпадают, введите их еще раз, пожалуйста")
                self.Password.text_entry.delete('0', END)
                self.focus_ini(2)
            else:
                self.return_disc(btn)
                # self.destroy()

        elif btn == 'auto' and (self.FIO.get() != '' or self.Address.get() != ''):
            self.refresh_dan(self.name_sql, self.adress_sql)

        else:  # В финале возвращаем значения из корректно заполненных полей
            self.return_disc(btn)
            # self.destroy()


    def refresh_dan(self, name_sql, address_sql):
        """
        Вместо создания нового пользователя производит авторизацию, возможно с перезаписью значений в поля
        :param str name_sql:
        :param str address_sql:
        :return:
        """
        if (self.FIO.get() == '' or name_sql == self.FIO.get()) and (
                self.Address.get() == '' or address_sql == self.Address.get()):
            self.return_disc()
        else:
            # elif (name_sql != self.FIO.get() or adress_sql != self.Adress.get()):
            question = 'Хотите обновить профиль, изменив'
            if self.FIO.get() != '' and name_sql != self.FIO.get():
                question += ' Ваше имя'
                if self.Address.get() != '' and address_sql != self.Address.get(): question += ' и'
            if self.Address.get() != '' and address_sql != self.Address.get(): question += ' адрес на Ярмарке мастеров'
            if not self.dop_param(question + "?"):
                if name_sql != self.FIO.get(): self.FIO.text_entry.delete('0', END)
                if address_sql != self.Address.get(): self.Address.text_entry.delete(len(URL_JM), END)
                self.return_disc()
            else:  # Необходимо перезаписать данные в бвзе
                self.return_disc('refr')
        # else:
        #     self.ReturnDisc('auto')
        #         # self.destroy()


    def dop_param(self, text=''):
        """
        Используется для обратного диалога
        :param str text:
        :return:
        """
        self.text = text
        self.dialog = YesNo(self.master)
        self.returnValue = self.dialog.go('Вопрос:', self.text, width=300, height=120)
        if self.returnValue:
            self.destroy()
            return self.returnValue


    def exit_method(self):
        """
        Для проверки готовности выйти
        :return:
        """
        self.dialog = YesNo(self.master)
        self.returnValue = self.dialog.go('Вопрос:', 'Вы хотите выйти?')
        if self.returnValue:
            self.destroy()


    def open_dialog(self, text):
        """
        ?
        :param str text:
        :return:
        """
        self.dialog = Passv_Verify(self.master)
        self.returnValue = self.dialog.go(text)
        return self.returnValue


# класс дочернего окна
class Passv_Verify(Toplevel):
    """
    Создает дополнительное окно с обратной связью
    """

    def __init__(self, master, text=''):
        super().__init__()
        # self = Toplevel(master)
        self.title('Проверка пароля')
        self.geometry(Center_widows(390, 100))  # Располагает по центру страницы

        self.label = Label(self, text=text)
        self.label.place(relx=.5, y=20, anchor="c")

        self.yes_button = Button(self, text='Подтвердить', command=self.cancel)
        self.yes_button.place(x=275, y=50, anchor="w", width=100, height=30)

        self.x = StringVar()
        self.text_entry = Entry(self, textvariable=self.x, show='*')
        self.text_entry.place(x=15, y=50, anchor="w", width=250)

        self.protocol('WM_DELETE_WINDOW', self.cancel)


    def go(self, myText=''):
        """
        :param str myText:
        :return: str
        """
        self.label['text'] = myText
        self.grab_set()
        self.focus_set()
        self.text_entry.focus_set()
        self.wait_window()
        return self.newValue


    def cancel(self):
        self.newValue = self.text_entry.get()
        self.destroy()


if __name__ == '__main__':
    root = Tk()  # ---- Открываем основное окно и сразу его прячем
    root.overrideredirect(1)
    root.withdraw()

    SQL_Connect = sqlite3.connect('Masters.db')
    cursor = SQL_Connect.cursor()

    app = Auto_Main()
    app.mainloop()
    base_to_sql = app.ReturnValue

    print(base_to_sql)

    if base_to_sql['Action'] == 'new':
        try:
            cursor.execute("""INSERT INTO 'Autor' ('FIO', 'URL_User', 'Mail', 'Pass')
                VALUES ('{:s}', '{:s}', '{:s}', '{:s}')
                """.format(base_to_sql['FIO'], base_to_sql['Adress'], base_to_sql['Mail'], base_to_sql['Password']))

            SQL_Connect.commit()  # Применение изменений к базе данных
            InformWin(message=base_to_sql['Name'] + ' Вы успешно создали нового пользователя',
                      fg='green')
        except sqlite3.Error as e:
            print(e, '----------> ?', base_to_sql['FIO'], ' --> Попытка записать нового пользователя')

    elif base_to_sql['Action'] == 'refr':
        try:
            if base_to_sql['FIO'] != '':
                cursor.execute("""UPDATE Autor set FIO = '{:s}' 
                               WHERE (Mail = '{:s}')""".format(base_to_sql['FIO'], base_to_sql['Mail']))
            if base_to_sql['Adress'] != '':
                cursor.execute("""UPDATE Autor set URL_User = '{:s}' 
                               WHERE (Mail = '{:s}')""".format(base_to_sql['Adress'], base_to_sql['Mail']))
            SQL_Connect.commit()  # Применение изменений к базе данных
            InformWin(message=base_to_sql['Name'] + ', Вы успешно авторизовались и обновили свои данные', fg='green')
        except sqlite3.Error as e:
            print(e, '----------> ? Перезапись данных в базу')
    else:
        InformWin(message=base_to_sql['Name'] + ', Вы успешно авторизовались', fg='green')
        pass

    cursor.close()
    SQL_Connect.close()

    user_name = base_to_sql['User']  # В дальнейшем это значение должно передаваться в следующую программу
    print(user_name)
    read_JM(user_name)
