# coding=utf-8
# from tkinter import *
from tkinter import messagebox
from form_Boolean import *

""" 
------ Создает окно с выбором: либо для поиска по всем картинкам, лиюо для конкретного автора -------
для сбора картинок и информации про работу в базу
"""
URL_JM = 'https://www.livemaster.ru/'


class TextEntryButton:
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
        self.geometry(center_window(self, 650, 145))  # Располагает по центру страницы

        self.item = TextEntryButton(self, 'Введите текст для поиска работ по "Ярмарке Мастеров":',
                                      "Работы по запросу", 20, 45, 1)
        self.author = TextEntryButton(self, 'Либо адрес страницы мастера, чьи работы Вы хотите добавить в базу:',
                                       "Работы автора", 90, 115, 2, URL_JM)

        # self.grab_set()
        # self.wait_window()
        self.item.text_entry.focus_set()
        self.protocol('WM_DELETE_WINDOW', self.exitMethod)  # TODO: Отключено временно

    def get(self):
        return self.sendValue

    def show_message(self, ver):
        """
        # ----- Смотрит, введен ли текст и выдает предупреждение
        :param int ver:
        """
        if ver == 1:
            if self.item.get() == '':
                messagebox.showinfo("GUI Python", "Надо ввести текст для поиска")
                self.item.text_entry.focus_set()
            elif re.search(r"[a-zA-Z]", self.item.get()):
                self.dialog = YesNo()
                self.returnValue = self.dialog.go('Вопрос:', 'В запросе латинские буквы. Вы уверены?')
                if self.returnValue:
                    self.sendValue = self.item.get(), self.author.get()
                    self.destroy()
                else:
                    # self.grab_set()
                    # self.wait_window()
                    self.item.text_entry.delete('0', END)
                    #  TODO: Проблема: после очистки поля фокус (и возможность выбрать поле для записи) блокируется.
                    self.item.text_entry.focus_set()
            else:
                self.sendValue = self.item.get(), self.author.get()
                self.destroy()
        elif ver == 2:
            if self.author.get() == '':
                messagebox.showinfo("GUI Python", "Надо ввести текст для поиска")
                self.author.text_entry.focus_set()
            elif re.search(r"[а-яА-ЯёЁ]", self.author.get()):
                messagebox.showinfo("GUI Python", "В адресе не может быть русских букв")
                self.author.text_entry.delete(len(URL_JM), END)
                self.author.text_entry.focus_set()
            else:
                self.sendValue = self.item.get(), self.author.get()
                self.destroy()

    def exitMethod(self):
        self.dialog = YesNo()
        self.returnValue = self.dialog.go('Вопрос:', 'Вы хотите выйти?')
        if self.returnValue:
            self.destroy()


if __name__ == '__main__':
    root = Tk()
    root.withdraw()

    app = TextSearch()
    root.wait_window(app)
    text = app.get()
    print(text)

    try:
        pass
    except AttributeError:
        pass
