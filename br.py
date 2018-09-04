import tkinter


def func():
        label_visible_false.grid()
        button_visible_false.grid()
        label_visible_true.grid_remove()
        button_visible_true.grid_remove()


def visible_true():
        label_visible_false.grid_remove()
        button_visible_false.grid_remove()
        label_visible_true.grid()
        button_visible_true.grid()


root = tkinter.Tk()
root.geometry("400x400")
label_visible_true = tkinter.Label(root, text='Не скрытый текст')
label_visible_true.grid()

button_visible_true = tkinter.Button(root, text='Не скрытая кнопка', command=func)
button_visible_true.grid()

label_visible_false = tkinter.Label(root, text='Скрытый текст')

button_visible_false = tkinter.Button(root, text='Скрытая кнопка', command=visible_true)

root.mainloop()

