# from tkinter import *
import sqlite3
from tkinter import messagebox

from myBoolean import *

# from myDialog import *

SQL_Connect = sqlite3.connect('Masters.db')
cursor = SQL_Connect.cursor()


class Auto_main:
    """
    класс главного окна
    """
    def __init__(self, master):  # ----- Создает плашку для ввода текста для поиска
        self.master = master
        self.sendValue = ''
        self.master.title("Авторизация в программе")
        self.master.geometry(Center_widows(600, 200))  # Располагает по центру страницы
        self.message = StringVar()
        self.name_label = Label(text='Введите необходимые данные ниже:')
        self.name_label.place(relx=.5, y=20, anchor="c")

        self.Mail = self.Text_Entry('E-mail:*', 50)
        self.focusIni()
        self.Password = self.Text_Entry('Пароль:*', 90, '*')
        self.FIO = self.Text_Entry('Имя:', 130)
        self.Adress = self.Text_Entry('Адрес на ЯМ:', 170, url = 'https://www.livemaster.ru/')

        self.button_name = Button(self.master, text = "Авторизоваться*", command = self.check_auto,  width = 14, height = 3, fg='green')
        self.button_name.place(relx=.87, rely=.35, anchor="c")
        self.button_avto = Button(self.master, text = "Новый автор", command = self.check_new, width = 14, height = 3, fg='black')
        self.button_avto.place(relx=.87, rely=.75, anchor="c")

        # self.master.protocol('WM_DELETE_WINDOW', self.exitMethod)
        self.master.mainloop()

    def focusIni(self, step = 0):
        """

        :param int step:
        :return:
        """
        if step == 0:
            if str(self.Mail) == '': self.Mail.text_entry.focus_set() # Ставит курсор в первое пустое поле
            elif str(self.Password) == '': self.Password.text_entry.focus_set()
            elif str(self.FIO) == '': self.FIO.text_entry.focus_set()
            elif str(self.Adress) == '': self.Adress.text_entry.focus_set()
        else:
            if step == 1: self.Mail.text_entry.focus_set() # Ставит курсор в указаннное пустое поле
            elif step == 2: self.Password.text_entry.focus_set()
            elif step == 3: self.FIO.text_entry.focus_set()
            elif step == 4: self.Adress.text_entry.focus_set()

    def check_auto(self):  # ----- Авторизация
        self.probe(1)
        # self.master.destroy()

    def check_new(self):   # ----- Новый пользователь
        self.probe(0)

    def probe(self, btn): # ----- Смотрит, введен ли нужный текст и выдает предупреждение
        """Подпрограмма проверяет все возможные типы ошибок при введении в поля"""
        try:
            cursor.execute("SELECT Mail, Pass, FIO, URL_Autor FROM Autor WHERE Mail = '{:s}'".format(str(self.Mail)))  # Пароль по е-мейл
            mail_sql = cursor.fetchall()

            if mail_sql == []:
                mail_sql = ''
                password_sql = ''
                name_sql = ''
                adress_sql = ''
            else:
                password_sql = str(mail_sql[0][1])
                name_sql = str(mail_sql[0][2])
                adress_sql = str(mail_sql[0][3])
                mail_sql = str(mail_sql[0][0]) # Если такой мейл есть в базе -- запишем в переменную, иначе - ''
        except sqlite3.Error as e:
            messagebox.showinfo("GUI Python", "Ошибка при чтении из базы: '{:s}'".format(e))

        if FALSE:
            pass

        elif btn == 0 and (str(self.FIO) == '' or str(self.Mail) == '' or str(self.Password) == '' or str(
                self.Adress) == ''):
            messagebox.showinfo("GUI Python", "Надо заполнить все поля")
            self.focusIni()

        elif btn == 1 and (str(self.Mail) == '' or str(self.Password) == ''):
            messagebox.showinfo("GUI Python", "Надо ввести е-мейл и пароль")
            self.focusIni()

        elif not re.fullmatch(r"[\w'._+-]+@[\w'._+-]+[.][\w'._+-]+", str(self.Mail)):
            messagebox.showinfo("GUI Python", "Формат е-мейла неверный.")
            self.focusIni(1)

        elif btn == 1 and mail_sql == '':
            messagebox.showinfo("GUI Python", "Пользователя с адресом '{:s}' нет в базе. Вы можете создать нового пользователя.".format(str(self.Mail)))
            self.focusIni(1)

        elif btn == 0 and re.search(r"[а-яА-ЯёЁ]", str(self.Adress)):
            messagebox.showinfo("GUI Python", "В адресе не может быть русских букв")
            self.focusIni(4)

        elif btn == 1 and password_sql != str(self.Password):
            messagebox.showinfo("GUI Python", "Пароль для данного адреса другой")
            self.Password.text_entry.delete('0', END)
            self.focusIni(2)

        elif btn == 0 and mail_sql != '' and password_sql == str(self.Password):
            if self.dopParam('Пользователь с е-мейлом: ' + mail_sql + " уже есть в базе. Хотите авторизоваться?"):
                btn = 1
                self.obnovlDan(name_sql, adress_sql, btn)
            else:
                self.master.destroy()

        elif btn == 0:
            password_new = self.openDialog(text = 'Введите пароль еще раз...')
            if password_new != str(self.Password):
                messagebox.showinfo("GUI Python", "Пароли не совпадают, введите их еще раз, пожалуйста")
                self.Password.text_entry.delete('0', END)
                self.focusIni(2)
            else:
                self.ReturnValue = {'FIO': str(self.FIO), 'Mail': str(self.Mail), 'Password': str(self.Password),
                                    'Adress': str(self.Adress), 'New': btn}
                self.master.destroy()

        elif btn == 1 and (str(self.FIO) != '' or str(self.Adress) != ''):
            self.obnovlDan(name_sql, adress_sql, btn)

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
        else:
            self.ReturnValue = {'FIO': str(self.FIO), 'Mail': str(self.Mail), 'Password': str(self.Password),
                                'Adress': str(self.Adress), 'New': btn}
            self.master.destroy()

    def obnovlDan(self, name_sql, adress_sql, btn):
        if (name_sql != str(self.FIO) or adress_sql != str(self.Adress)):
            question = 'Хотите обновить профиль, изменив'
            if name_sql != str(self.FIO):
                question += ' Ваше имя'
                if adress_sql != str(self.Adress): question += ' и'
            if adress_sql != str(self.Adress): question += ' адрес на Ярмарке мастеров'
            if not self.dopParam(question + "?"):
                if name_sql != str(self.FIO): self.FIO.text_entry.delete('0', END)
                if adress_sql != str(self.Adress): self.Adress.text_entry.delete(len('https://www.livemaster.ru/'), END)
            else:
                self.ReturnValue = {'FIO': str(self.FIO), 'Mail': str(self.Mail), 'Password': str(self.Password),
                                    'Adress': str(self.Adress), 'New': btn}
                self.master.destroy()

    def dopParam(self, text = ''):
        self.text = text
        self.dialog = yesno(self.master)
        self.returnValue = self.dialog.go('Вопрос:', self.text, width= 300, height = 120)
        if self.returnValue:
            self.master.destroy()
            return self.returnValue

    def exitMethod(self):
        self.dialog = yesno(self.master)
        self.returnValue = self.dialog.go('Вопрос:', 'Вы хотите выйти?')
        if self.returnValue:
            self.master.destroy()

    def openDialog(self, text):
        self.dialog = dialog(self.master)
        self.returnValue = self.dialog.go(text)
        return self.returnValue
        # self.sendValue = self.Password

        # if self.returnValue:
        #     # self.text.delete('0.0', END)
        #     self.text_entry.insert('0', self.returnValue)


    class Text_Entry:
        def __init__(self, message='[имя поля]', pi_y=10, show = '', url = ''):
            self.name_label = Label(text = message)
            self.name_label.place(relx=.05, y = pi_y, anchor="w")

            self.x = StringVar()
            self.text_entry = Entry(textvariable = self.x , show = show)
            self.url = url
            self.text_entry.insert(END, self.url)
            self.text_entry.place(relx=.5, y = pi_y, anchor="c", width=300)

        def __str__(self):
            return self.x.get()[len(self.url):]

# класс дочернего окна
class dialog:
    def __init__(self, master, text = ''):
        self.top = Toplevel(master)
        self.top.title('Проверка пароля')
        self.top.geometry(Center_widows(390, 100))  # Располагает по центру страницы
        # self.frame = Frame(self.top)
        # self.frame.pack(side=BOTTOM)
        self.label = Label(self.top, text = text)
        self.label.place(relx=.5, y=20, anchor="c")

        self.yes_button = Button(self.top, text='Подтвердить', command = self.cancel)
        self.yes_button.place(x=275, y = 50, anchor="w", width=100, height=30)

        self.x = StringVar()
        self.text_entry = Entry(self.top, textvariable = self.x, show='*')
        self.text_entry.place(x = 15, y = 50, anchor="w", width=250)

        self.top.protocol('WM_DELETE_WINDOW', self.cancel)

        # def __str__(self):
        #     return self.x.get()

    def go(self, myText=''):
        self.label['text']  = myText
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
    root = Tk()
    baze_to_sql = Auto_main(root).ReturnValue

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