# coding=utf-8
from tkinter import *   # from x import * is bad practice
# from ttk import *

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    """
    Чистый Tkinter прокручивать кадр, который на самом деле работает!
    * Используйте атрибут 'interior' для размещения виджетов внутри прокручиваемой рамки
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, master, width):
        super().__init__(master=master)

        # создание объекта canvas и вертикальной полосы прокрутки для прокрутки
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(side=RIGHT, fill=Y,  expand=YES)
        self.canvas = Canvas(self, yscrollcommand=vscrollbar.set, width=width)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        vscrollbar.config(command=self.canvas.yview)

        # сброс представления
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # создайте рамку внутри холста, которая будет прокручиваться вместе с ним
        self.interior = interior = Frame(self.canvas)#, bg = 'green')
        self.interior.pack(side=LEFT, fill=BOTH, expand=YES)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)

        self.interior.bind('<Configure>', lambda e: self.configure_interior(e))
        self.canvas.bind('<Configure>', lambda e: self.configure_canvas(e))



        # отслеживайте изменения ширины холста и рамки и синхронизируйте их,
        # также обновление полосы прокрутки
    def configure_interior(self, event):
    # обновите полосы прокрутки в соответствии с размером внутренней рамки
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)

        # print('>>>', self.winfo_width(), self.winfo_height())
        # print(size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # обновите ширину холста, чтобы она соответствовала внутренней рамке
            self.canvas.config(width=self.interior.winfo_width())


    def configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # обновление ширины внутренней рамки для заполнения холста
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())



if __name__ == "__main__":

    class SampleApp(Tk):
        """

        """
        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)

            self.geometry("800x550")
            self.frame = VerticalScrolledFrame(self)
            self.frame.pack()
            # self.label = Label(self.frame.interior, text="Можно уменьшить окно, чтобы активировать полосу прокрутки.", width = 1000)
            # self.label.pack()

            buttons = []
            for i in range(12):
                buttons.append(Button(self.frame.interior, text="Button " + str(i)))
                buttons[-1].pack(anchor=NW)

    app = SampleApp()
    app.mainloop()
