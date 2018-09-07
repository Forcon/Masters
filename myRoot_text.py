from tkinter import *
from tkinter import messagebox
from myBoolean import *

""" 
------ Эксперименты с окнами -------
для сбора картинок и информации про работу в базу
"""

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
        self.text_entry2.insert(END, 'https://www.livemaster.ru/')
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
                self.sendValue = (self.text_entry1.get(), self.text_entry2.get()[len('https://www.livemaster.ru/'):])
                # self.text_entry1.delete('0', END)
                self.master.destroy()
            else:
                self.text_entry1.delete('0', END) # ------ Проблема: после очистки поля фокус (и возможность выбрать поле для записи) блокируется.
                # self.master.grab_set()
                # self.master.wait_window()
                # self.master.focus_set()
                self.text_entry1.focus_set()

        elif self.text_entry2.get()[len('https://www.livemaster.ru/'):] == '' and ver == 2:
            messagebox.showinfo("GUI Python", "Надо ввести текст для поиска")
            self.text_entry2.focus_set()
        elif ver == 2 and re.search(r"[а-яА-ЯёЁ]", str(self.text_entry2.get())):
            messagebox.showinfo("GUI Python", "В адресе не может быть русских букв")
            self.text_entry2.delete(len('https://www.livemaster.ru/'), END)
            self.text_entry2.focus_set()

        else:
            self.sendValue = (self.text_entry1.get(), self.text_entry2.get()[len('https://www.livemaster.ru/'):])
            # self.text_entry.delete('0', END)
            self.master.destroy()

    # def openDialog(self):
    #     # self.dialog = child(self.master)
    #     self.sendValue = self.text_entry.get()
    #     self.returnValue = self.dialog.go(self.sendValue)
    #     if self.returnValue:
    #         self.text_entry.delete('0', END)
    #         self.text_entry.insert('0', self.returnValue)

    def exitMethod(self):
        self.dialog = YesNo(self.master)
        self.returnValue = self.dialog.go('Вопрос:', 'Вы хотите выйти?')
        if self.returnValue:
            self.master.destroy()

# # класс дочернего окна
# class child:
#     def __init__(self, master):
#         self.slave = Toplevel(master)
#         self.slave.title('child')
#         # self.slave.geometry('200x150+500+375')
#         self.slave.geometry(Center_widows(200, 150))
#         self.frame = Frame(self.slave)
#         self.frame.pack(side=BOTTOM)
#         self.accept_button = Button(self.frame, text='accept', command=self.accept)
#         self.accept_button.pack(side=LEFT)
#         self.cancel_button = Button(self.frame, text='cancel', command=self.cancel)
#         self.cancel_button.pack(side=RIGHT)
#         self.text = Text(self.slave, background='white')
#         self.text.pack(side=TOP, fill=BOTH, expand=YES)
#         self.slave.protocol('WM_DELETE_WINDOW', self.cancel)
#
#     def go(self, myText=''):
#         self.text.insert('0.0', myText)
#         self.newValue = None
#         self.slave.grab_set()
#         self.slave.focus_set()
#         self.slave.wait_window()
#         return self.newValue
#
#     def accept(self):
#         self.newValue = self.text.get('0.0', END)
#         self.slave.destroy()
#
#     def cancel(self):
#         self.slave.destroy()

# # класс диалогового окна выхода
# class yesno:
#     def __init__(self, master):
#         self.slave = Toplevel(master)
#         self.slave.title('exit dialog')
#         # self.slave.geometry('200x100+300+250')
#         self.slave.geometry(Center_widows(200, 100))
#         self.frame = Frame(self.slave)
#         self.frame.pack(side=BOTTOM)
#         self.yes_button = Button(self.frame, text='yes', command=self.yes)
#         self.yes_button.pack(side=LEFT)
#         self.no_button = Button(self.frame, text='no', command=self.no)
#         self.no_button.pack(side=RIGHT)
#         self.label = Label(self.slave)
#         self.label.pack(side=TOP, fill=BOTH, expand=YES)
#         self.slave.protocol('WM_DELETE_WINDOW', self.no)
#
#     def go(self, title='', message=''):
#         self.slave.title(title)
#         self.label.configure(text=message)
#         self.booleanValue = TRUE
#         self.slave.grab_set()
#         self.slave.focus_set()
#         self.slave.wait_window()
#         return self.booleanValue
#
#     def yes(self):
#         self.booleanValue = TRUE
#         self.slave.destroy()
#
#     def no(self):
#         self.booleanValue = FALSE
#         self.slave.destroy()

# # Располагает окно по центру страницы
# class Center_widows(object): # ----- Располагает окна по центру экрана
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#
#     def __str__(self):
#         return str(self.width) + "x" + str(self.height) + "+" + str(
#             (root.winfo_screenwidth() - self.width) // 2) + "+" + str((root.winfo_screenheight() - self.height) // 2)

# создание окна

# class ItemPozition:
#     def __init__(self, message = '[имя поля]', mes_btn = '[кнопка]', lbl_y = 0, ent_y = 0, url = ''):
#         self.name_label = Label(text='message')
#         self.name_label.place(relx=.5, y = lbl_y, anchor="c")
#
#         self.text_entry = Entry(textvariable = self.message)
#         self.text_entry.place(relx=.5, y = ent_y, anchor="c", width=300)
#         self.text_entry.focus_set()
#         self.text_entry.insert(END, url)
#         self.message_button = Button(text = mes_btn, command = self.show_message)
#         self.message_button.place(x = 485, y = ent_y, anchor="w", width = 150)

# запуск окна
if __name__ == '__main__':
    try:
        root = Tk()
        text = TextSearсh(root).sendValue
        print(text)
        # root.destroy()
    except(AttributeError):
        pass


# print(sendValue)