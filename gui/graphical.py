from tkinter import *
import tkinter.filedialog

window = Tk()
window.title("Network Orange")
window.geometry('300x300')
window.configure(bg="orange")

userFile = ""


def getTxFile():
    userFile = tkinter.filedialog.askopenfilename()
    print(userFile)


def getRxFile():
    userFile = tkinter.filedialog.askopenfilename()
    print(userFile)


txBtn = Button(window, text="Tx: Select File", command=getTxFile)
txBtn.grid(column=0, row=0)
rxBtn = Button(window, text="Rx: List Available Files", command=getRxFile)
rxBtn.grid(column=0, row=1)

window.mainloop()
