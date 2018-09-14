# from tkinter import *
import sqlite3
from tkinter import messagebox

from myBoolean import * # Дополнительные окна

# from myDialog import *
"""
Программа создает окно авторизации, где можно либо авторизоваться в программе, либо завести нового пользователя.
Нужно, чтобы использовтаь свои наработки в базе + не подтягивать собственные работы в выборку
"""
URL_JM = 'https://www.livemaster.ru/'

SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()


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
        '''
        Создает кнопку
        :param master:
        :param str text:
        :param int ver:
        :param float r_y:
        :param str fg:
        '''
        self.button_name = Button(master, text=text, command=lambda: master.check_entry(ver),
                                  width=14, height=3, fg=fg)
        self.button_name.place(relx=.87, rely=r_y, anchor="c")


class Auto_main(Tk):
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
        self.Adress = Text_Entry(self.master, 'Адрес на ЯМ:', 170, url=URL_JM)
        self.focusIni()

        Btn(self, "Авторизоваться*", 1, .35, fg='green')
        Btn(self, "Новый автор", 0, .75)
        # self.master.protocol('WM_DELETE_WINDOW', self.exitMethod)


    def focusIni(self, step = 0):
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
            elif self.Adress.get() == '':
                self.Adress.text_entry.focus_set()

        else:
            if step == 1: self.Mail.text_entry.focus_set() # Ставит курсор в указаннное пустое поле
            elif step == 2: self.Password.text_entry.focus_set()
            elif step == 3: self.FIO.text_entry.focus_set()
            elif step == 4: self.Adress.text_entry.focus_set()

    # def check_auto(self):  # ----- Если авторизация
    #     self.probe(1)
    #
    # def check_new(self):   # ----- Если новый пользователь
    #     self.probe(0)

    def check_entry(self, btn):  # ----- Смотрит, введен ли нужный текст и выдает предупреждение
        """
        Подпрограмма проверяет все возможные типы ошибок при введении текста в поля,
        :param int btn:
        """
        try: # Считываем из базы все что есть по данному е-мейлу
            cursor.execute("SELECT Mail, Pass, FIO, URL_Autor FROM Autor WHERE Mail = '{:s}'".format(self.Mail.get()))
            self.mail_sql = cursor.fetchall()

            if self.mail_sql == []:
                self.mail_sql = ''
                self.password_sql = ''
                self.name_sql = ''
                self.adress_sql = ''
            else:
                self.password_sql = str(self.mail_sql[0][1])
                self.name_sql = str(self.mail_sql[0][2])
                self.adress_sql = str(self.mail_sql[0][3])
                self.mail_sql = str(
                    self.mail_sql[0][0])  # Если такой мейл есть в базе -- запишем в переменную, иначе - ''
        except sqlite3.Error as e:
            print("GUI Python", "Ошибка при чтении из базы: '{:s}'".format(e))

        if FALSE: # Это как раз и есть проверка всех полей на корректность заполнения
            pass
        elif btn == 0 and (self.FIO.get() == '' or self.Mail.get() == ''
                           or self.Password.get() == '' or self.Adress.get() == ''):
            messagebox.showinfo("GUI Python", "Надо заполнить все поля")
            self.focusIni()
        elif btn == 1 and (self.Mail.get() == '' or self.Password.get() == ''):
            messagebox.showinfo("GUI Python", "Надо ввести е-мейл и пароль")
            self.focusIni()
        elif not re.fullmatch(r"[\w'._+-]+@[\w'._+-]+[.][\w'._+-]+", self.Mail.get()):
            messagebox.showinfo("GUI Python", "Формат е-мейла неверный.")
            self.focusIni(1)
        elif btn == 1 and self.mail_sql == '':
            messagebox.showinfo("GUI Python", "Пользователя с адресом '{:s}' нет в базе. "
                                              "Вы можете создать нового пользователя.".format(self.Mail.get()))
            self.focusIni(1)
        elif btn == 0 and re.search(r"[а-яА-ЯёЁ]", self.Adress.get()):
            messagebox.showinfo("GUI Python", "В адресе не может быть русских букв")
            self.focusIni(4)
        elif btn == 1 and self.password_sql != self.Password.get():
            messagebox.showinfo("GUI Python", "Пароль для данного адреса другой")
            self.Password.text_entry.delete('0', END)
            self.focusIni(2)
        elif btn == 0 and self.mail_sql != '' and self.password_sql == self.Password.get():
            if self.dopParam('Пользователь с е-мейлом: ' + self.mail_sql + " уже есть в базе. Хотите авторизоваться?"):
                btn = 1
                self.obnovlDan(self.name_sql, self.adress_sql, btn)
            else:
                self.master.destroy()
        elif btn == 0:
            password_new = self.openDialog(text = 'Введите пароль еще раз...')
            if password_new != self.Password.get():
                messagebox.showinfo("GUI Python", "Пароли не совпадают, введите их еще раз, пожалуйста")
                self.Password.text_entry.delete('0', END)
                self.focusIni(2)
            else:
                self.ReturnValue = {'FIO': self.FIO.get(), 'Mail': self.Mail.get(), 'Password': self.Password.get(),
                                    'Adress': self.Adress.get(), 'New': btn}
                self.destroy()

        elif btn == 1 and (self.FIO.get() != '' or self.Adress.get() != ''):
            self.obnovlDan(self.name_sql, self.adress_sql, btn)
            # if (name_sql != str(self.FIO) or adress_sql != str(self.Adress)):
            #     question = 'Хотите обновить профиль, изменив'
            #     if name_sql != str(self.FIO):
            #         question += ' Ваше имя'
            #         if adress_sql != str(self.Adress): question += ' и'
            #     if adress_sql != str(self.Adress): question += ' адрес на Ярмарке мастеров'
            #     if not self.dopParam(question + "?"):
            #         if name_sql != str(self.FIO): self.FIO.text_entry.delete('0', END)
            #         if adress_sql != str(self.Adress): self.Adress.text_entry.delete(len('https://www.livemaster.ru/'), END)
            #     else:
            #         self.ReturnValue = {'FIO': str(self.FIO), 'Mail': str(self.Mail), 'Password': str(self.Password),
            #                             'Adress': str(self.Adress), 'New': btn}
            #         self.master.destroy()
        else: # В финале возвращаем значения из корректно заполненных полей
            self.ReturnValue = {'FIO': self.FIO.get(), 'Mail': self.Mail.get(), 'Password': self.Password.get(),
                                'Adress': self.Adress.get(), 'New': btn}
            self.destroy()

    def obnovlDan(self, name_sql, adress_sql, btn):
        """
        Вместо создания нового пользователя производит авторизацию, возможно с перезаписью значений в поля
        :param str name_sql:
        :param str adress_sql:
        :param int btn:
        :return:
        """
        if (name_sql != self.FIO.get() or adress_sql != self.Adress.get()):
            question = 'Хотите обновить профиль, изменив'
            if self.FIO.get() != '' and name_sql != self.FIO.get():
                question += ' Ваше имя'
                if self.Adress.get() != '' and adress_sql != self.Adress.get(): question += ' и'
            if self.Adress.get() != '' and adress_sql != self.Adress.get(): question += ' адрес на Ярмарке мастеров'
            if not self.dopParam(question + "?"):
                if name_sql != self.FIO.get(): self.FIO.text_entry.delete('0', END)
                if adress_sql != self.Adress.get(): self.Adress.text_entry.delete(len(URL_JM), END)
            else:
                # Возврат "2" означает необходимость перезаписать данные в бвзе
                self.ReturnValue = {'FIO': self.FIO.get(), 'Mail': self.Mail.get(), 'Password': self.Password.get(),
                                    'Adress': self.Adress.get(), 'New': 2}
                # self.destroy()

    def dopParam(self, text = ''):
        """
        Используется для обратного диалога
        :param str text:
        :return:
        """
        self.text = text
        self.dialog = YesNo(self.master)
        self.returnValue = self.dialog.go('Вопрос:', self.text, width= 300, height = 120)
        if self.returnValue:
            self.destroy()
            return self.returnValue

    def exitMethod(self):
        """
        Для проверки готовности выйти
        :return:
        """
        self.dialog = YesNo(self.master)
        self.returnValue = self.dialog.go('Вопрос:', 'Вы хотите выйти?')
        if self.returnValue:
            self.destroy()

    def openDialog(self, text):
        """
        ?
        :param str text:
        :return:
        """
        self.dialog = dialog(self.master)
        self.returnValue = self.dialog.go(text)
        return self.returnValue


# класс дочернего окна
class dialog:
    """
    Создает дополнительное окно с обратной связью
    """

    def __init__(self, master, text=''):
        self.top = Toplevel(master)
        self.top.title('Проверка пароля')
        self.top.geometry(Center_widows(390, 100))  # Располагает по центру страницы

        self.label = Label(self.top, text=text)
        self.label.place(relx=.5, y=20, anchor="c")

        self.yes_button = Button(self.top, text='Подтвердить', command = self.cancel)
        self.yes_button.place(x=275, y = 50, anchor="w", width=100, height=30)

        self.x = StringVar()
        self.text_entry = Entry(self.top, textvariable = self.x, show='*')
        self.text_entry.place(x=15, y=50, anchor="w", width=250)

        self.top.protocol('WM_DELETE_WINDOW', self.cancel)


    def go(self, myText=''):
        """
        :param str myText:
        :return: str
        """
        self.label['text'] = myText
        self.top.grab_set()
        self.top.focus_set()
        self.text_entry.focus_set()
        self.top.wait_window()
        return self.newValue

    def cancel(self):
        self.newValue = self.text_entry.get()
        self.top.destroy()

if __name__ == '__main__':
    # try:
    # root = Tk()
    # baze_to_sql = Auto_main(root).ReturnValue

    app = Auto_main()
    app.mainloop()
    baze_to_sql = app.ReturnValue

    print(baze_to_sql)
        # root.destroy()
    # except(AttributeError):
    #     pass

    # try:
    #     cursor.execute("""INSERT INTO 'Autor' ('FIO', 'URL_Autor', 'Mail', 'Pass')
    #         VALUES ('{:s}', '{:s}', '{:s}', '{:s}')
    #         """.format(baze_to_sql['FIO'], baze_to_sql['Adress'], baze_to_sql['Mail'], baze_to_sql['Password']))
    #
    #     SQL_Connect.commit()  # Применение изменений к базе данных
    # except sqlite3.Error as e:
    #     print(e, '----------> ?', baze_to_sql['FIO'])

cursor.close()
SQL_Connect.close()