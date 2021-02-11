# Maria Gorbunova
# Lab3frontend is a GUI that opens windows with the data user requests

import tkinter as tk
import tkinter.messagebox as tkmb  # open error message if no link


class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("350x100")
        self.title("Colleges")
        # TODO: put label in the middle
        self.label = tk.Label(self, text="Two-Year College Ranking", fg="blue").grid()

        self.button = tk.Button(self, text='By Salary Potential', command=lambda: self.new_window(0)).grid(row=1,
                                                                                                           column=0)
        self.button1 = tk.Button(self, text='By Early Career Pay', command=lambda: self.new_window(1)).grid(row=1,
                                                                                                            column=1)
        self.button2 = tk.Button(self, text='By Mid Career Pay', command=lambda: self.new_window(2)).grid(row=2,
                                                                                                          column=0)
        self.button3 = tk.Button(self, text='By STEM Percentage', command=lambda: self.new_window(3)).grid(row=2,
                                                                                                           column=1)

    def new_window(self, idx):
        newWin = ChoiceWin(self)
        self.wait_window(newWin)
        # TODO: open another class window with proper sort depending on idx
        if newWin.getChoice != -1:
            print("Hello")


class ChoiceWin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("300x200")
        self.grab_set()
        self.focus_set()
        self.choice = -1
        # TODO:add radio buttons

        self.buttonOk = tk.Button(self, text="OK", command=lambda: self.destroy()).pack()

    def getChoice(self):
        return self.choice


MainWin().mainloop()
