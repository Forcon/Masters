# coding=utf-8
# from tkinter import *
from tkinter import messagebox
from form_Boolean import *

""" 
------ Создает окно с выбором: либо для поиска по всем картинкам, лиюо для конкретного автора -------
для сбора картинок и информации про работу в базу
"""
URL_JM = 'https://www.livemaster.ru/'


class Text_Entry_Button:
    """
    Создает: надпись, поле для заполнения и кнопку
    """
    def __init__(self, master, message='[имя поля]', text='[надпись]', pi_l_y=0, pi_y=0, var=0, url=''):
        self.url = url
        self.name_label = Label(master, text=message)
        self.name_label.place(relx=.5, y=pi_l_y, anchor="c")

        self.x = StringVar()
        self.text_entry = Entry(master, textvariable=self.x)
        self.text_entry.place(relx=.5, y=pi_y, anchor="c", width=300)
        self.text_entry.insert(END, self.url)

        self.message_button = Button(master, text=text, command=lambda: master.show_message(var))
        self.message_button.place(x=485, y=pi_y, anchor="w", width=150)

    def get(self):
        return self.x.get()[len(self.url):]


# класс главного окна
class TextSearch(Toplevel):
    """
    # ----- Создает плашку для ввода текста для поиска
    """
    def __init__(self):
        super().__init__()
        self.sendValue = ''
        self.title("Отбор картинок в базу")
        self.geometry(Screen_Size(650, 145))  # Располагает по центру страницы

        self.Item = Text_Entry_Button(self, 'Введите текст для поиска работ по "Ярмарке Мастеров":',
                                      "Работы по запросу", 20, 45, 1)
        self.Autor = Text_Entry_Button(self, 'Либо адрес страницы мастера, чьи работы Вы хотите добавить в базу:',
                                       "Работы автора", 90, 115, 2, URL_JM)
        # self.Item.text_entry.focus_set()
        self.protocol('WM_DELETE_WINDOW', self.exitMethod)

    def get(self):
        return self.sendValue

    def show_message(self, ver):
        """
        # ----- Смотрит, введен ли текст и выдает предупреждение
        :param int ver:
        """
        if ver == 1:
            if self.Item.get() == '':
                messagebox.showinfo("GUI Python", "Надо ввести текст для поиска")
                self.Item.text_entry.focus_set()
            elif re.search(r"[a-zA-Z]", self.Item.get()):
                self.dialog = YesNo(self)
                self.returnValue = self.dialog.go('Вопрос:', 'В запросе латинские буквы. Вы уверены?')
                if self.returnValue:
                    self.sendValue = (self.Item.get(), self.Autor.get())
                    self.destroy()
                else:
                    self.Item.text_entry.delete('0', END)
                    #  ------ Проблема: после очистки поля фокус (и возможность выбрать поле для записи) блокируется.
                    # self.destroy()  # Временное решение проблемы с блокировкой
                    # self.__init__()
                    self.Item.text_entry.focus_set()
            else:
                self.sendValue = (self.Item.get(), self.Autor.get())
                self.destroy()
        elif ver == 2:
            if self.Autor.get() == '':
                messagebox.showinfo("GUI Python", "Надо ввести текст для поиска")
                self.Autor.text_entry.focus_set()
            elif re.search(r"[а-яА-ЯёЁ]", self.Autor.get()):
                messagebox.showinfo("GUI Python", "В адресе не может быть русских букв")
                self.Autor.text_entry.delete(len(URL_JM), END)
                # self.destroy()  # Временное решение проблемы с блокировкой
                # self.__init__()
                self.Autor.text_entry.focus_set()
            else:
                self.sendValue = (self.Item.get(), self.Autor.get())
                self.destroy()

    def exitMethod(self):
        self.dialog = YesNo(self)
        self.returnValue = self.dialog.go('Вопрос:', 'Вы хотите выйти?')
        if self.returnValue:
            self.destroy()


if __name__ == '__main__':
    root = Tk()  # ---- Открываем основное окно и сразу его прячем
    root.overrideredirect(1)
    root.withdraw()

    try:
        app = TextSearch()
        app.mainloop()
        text = app.sendValue
        # root = Tk
        # text = TextSearсh(root).sendValue

        print(text)
    except AttributeError:
        pass
