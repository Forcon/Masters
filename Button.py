from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import PIL
import pylab

def info_window():
    windows = Toplevel()
    windows.title('открытое окно')
    windows.geometry('400x400')
    panel = Label(windows, image=img)
    panel.pack(side="bottom", fill="both", expand="no")
    button = Button(windows, text='открыть окно', font='Times 12', command = info_window)
    button.place(x=0, y=0)


mGui1 = Tk()
mGui1.geometry('250x250+500+300')
mGui1.title('Info')
img = ImageTk.PhotoImage(Image.open("img/img_1.jpg"))
# img = PIL.Image.open("img/img_1.jpg")
print(img)

#
# pixels = np.array(img)
# pixels = pixels.astype(np.float32)/256.0

# print(pixels)
# pylab.imshow(np.minimum(1.0, pixels*1.5))
# pylab.show()


panel_main = Label(mGui1, image = img)
panel_main.pack(side = "top", fill = "both", expand = "no")



button_1 = Button(mGui1, text = 'открыть окно', font = 'Times 12', command = info_window)
button_1.place(x = 0, y = 0)
mGui1.mainloop()