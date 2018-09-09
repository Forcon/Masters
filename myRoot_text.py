from tkinter import *
from tkinter import messagebox
from myBoolean import *

""" 
------ Эксперименты с окнами -------
для сбора картинок и информации про работу в базу
"""
URL_JM = 'https://www.livemaster.ru/'

# класс главного окна
class TextSearсh:
    def __init__(self, master):  # ----- Создает плашку для ввода текста для поиска
        self.master = master
        self.sendValue = ''
        self.master.title("Отбор картинок в базу")
        self.master.geometry(Center_widows(650, 145))  # Располагает по центру страницы

        self.message1 = StringVar()
        self.message2 = StringVar()

        self.name_label1 = Label(text='Введите текст для поиска работ по "Ярмарке Мастеров":')
        self.name_label1.place(relx=.5, y = 20, anchor="c")
        self.name_label2 = Label(text='Либо адрес страницы мастера, чьи работы Вы хотите добавить в базу:')
        self.name_label2.place(relx=.5, y = 90, anchor="c")

        self.text_entry1 = Entry(self.master, textvariable = self.message1)
        self.text_entry1.place(relx=.5, y = 45, anchor="c", width=300)
        # self.text_entry1.insert(END, '')
        self.text_entry1.focus_set()
        self.message_button1 = Button(self.master, text = "Работы по запросу", command = self.text_item)
        self.message_button1.place(x = 485, y = 45, anchor="w", width = 150)

        self.text_entry2 = Entry(self.master, textvariable = self.message2)
        self.text_entry2.place(relx=.5, y = 115, anchor="c", width=300)
        self.text_entry2.insert(END, URL_JM)
        self.message_button2 = Button(self.master, text = "Работы автора", command = self.text_autor)
        self.message_button2.place(x = 485, y = 115, anchor="w", width = 150)

        self.master.protocol('WM_DELETE_WINDOW', self.exitMethod)
        self.master.mainloop()


    def __str__(self):
        return self.sendValue


    def text_item(self):
        self.show_message(1)


    def text_autor(self):
        self.show_message(2)


    def show_message(self, ver):  # ----- Смотрит, введен ли текст и выдает предупреждение
        if self.text_entry1.get() == '' and ver == 1:
            messagebox.showinfo("GUI Python", "Надо ввести текст для поиска")
            self.text_entry1.focus_set()
        elif re.search(r"[a-zA-Z]", str(self.text_entry1.get())) and ver == 1:
            self.dialog = YesNo(self.master)
            self.returnValue = self.dialog.go('Вопрос:', 'В запросе латинские буквы. Вы уверены?')
            if self.returnValue:
                self.sendValue = (self.text_entry1.get(), self.text_entry2.get()[len(URL_JM):])
                # self.text_entry1.delete('0', END)
                self.master.destroy()
            else:
                self.text_entry1.delete('0', END) # ------ Проблема: после очистки поля фокус (и возможность выбрать поле для записи) блокируется.
                # self.master.grab_set()
                # self.master.wait_window()
                # self.master.focus_set()
                self.text_entry1.focus_set()

        elif self.text_entry2.get()[len(URL_JM):] == '' and ver == 2:
            messagebox.showinfo("GUI Python", "Надо ввести текст для поиска")
            self.text_entry2.focus_set()
        elif ver == 2 and re.search(r"[а-яА-ЯёЁ]", str(self.text_entry2.get())):
            messagebox.showinfo("GUI Python", "В адресе не может быть русских букв")
            self.text_entry2.delete(len(URL_JM), END)
            self.text_entry2.focus_set()

        else:
            self.sendValue = (self.text_entry1.get(), self.text_entry2.get()[len(URL_JM):])
            # self.text_entry.delete('0', END)
            self.master.destroy()


    def exitMethod(self):
        self.dialog = YesNo(self.master)
        self.returnValue = self.dialog.go('Вопрос:', 'Вы хотите выйти?')
        if self.returnValue:
            self.master.destroy()


if __name__ == '__main__':
    try:
        root = Tk()
        text = TextSearсh(root).sendValue
        print(text)
    except (AttributeError):
        pass
