from tkinter import *
from tkinter import messagebox
from myBoolean import *


""" 
------ Эксперименты с окнами -------
для сбора картинок и информации про работу в базу
"""

# класс главного окна
class main:
    def __init__(self, master):  # ----- Создает плашку для ввода текста для поиска
        self.master = master
        self.sendValue = ''
        # self.master.title('parent')
        # self.master.geometry('400x300+200+150')
        # def text_search():
        # global text_entry
        # global root
        # width = 600
        # height = 100
        # center = Center_widows(width, height)
        # width_sc = (root.winfo_screenwidth() - width) // 2
        # height_sc = (root.winfo_screenheight() - height) // 2
        #
        self.master.title("Отбор картинок в базу")
        self.master.geometry(Center_widows(600, 130))  # Располагает по центру страницы

        self.message = StringVar()
        self.name_label = Label(text='Введите текст для поиска работ по "Ярмарке Мастеров":')
        self.name_label.place(relx=.5, rely=.2, anchor="c")

        self.text_entry = Entry(self.master, textvariable = self.message)
        self.text_entry.place(relx=.5, rely=.5, anchor="c", width=300)
        self.text_entry.focus_set()
        self.message_button = Button(self.master, text = "Найти картинки", command = self.show_message)
        self.message_button.place(relx=.85, rely=.5, anchor="c")

        self.master.protocol('WM_DELETE_WINDOW', self.exitMethod)
        self.master.mainloop()

    def __str__(self):
        return self.sendValue

    def show_message(self):  # ----- Смотрит, введен ли текст и
        if self.text_entry.get() == '':
            messagebox.showinfo("GUI Python", "Надо ввести текст для поиска")
        elif re.search(r"[a-zA-Z]", str(self.text_entry.get())):
            self.dialog = yesno(self.master)
            self.returnValue = self.dialog.go('Вопрос:', 'В запросе латинские буквы. Вы уверены?')
            if self.returnValue:
                self.sendValue = self.text_entry.get()
                self.text_entry.delete('0', END)
                self.master.destroy()
            else:
                self.text_entry.delete('0', END)
                self.text_entry.focus_set()
        else:
            self.sendValue = self.text_entry.get()
            self.text_entry.delete('0', END)
            self.master.destroy()

    # def openDialog(self):
    #     # self.dialog = child(self.master)
    #     self.sendValue = self.text_entry.get()
    #     self.returnValue = self.dialog.go(self.sendValue)
    #     if self.returnValue:
    #         self.text_entry.delete('0', END)
    #         self.text_entry.insert('0', self.returnValue)

    def exitMethod(self):
        self.dialog = yesno(self.master)
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


# запуск окна
if __name__ == '__main__':
    try:
        root = Tk()
        text = main(root)
        print(text)
        # root.destroy()
    except(AttributeError):
        pass


# print(sendValue)