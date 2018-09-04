from tkinter import*

root = Tk()
frame2 = Frame(root,bg='red',bd=5)
tex = Text(frame2,
          width=20, height=5,
          font="Verdana 12",
          wrap=WORD)

scr = Scrollbar(frame2,command=tex.yview,)

tex.configure(yscrollcommand=scr.set)

scr.pack(side='right', fill='y') # "Прилепить" к правому краю фрейма, заполнять по высоте (ось y)
tex.pack(fill='both') # Упаковать в оставшуюся часть фрейма, заполнять по высоте и

frame2.configure(yscrollcommand=scr.set)

root.mainloop()