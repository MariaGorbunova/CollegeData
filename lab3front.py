# Maria Gorbunova
# Lab3frontend is a GUI that opens windows with the data user requests

import tkinter as tk
import webbrowser
import tkinter.messagebox as tkmb


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
        choice = newWin.getChoice()
        if choice != -1:
            DisplayWin(self, idx, choice)


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


class DisplayWin(tk.Toplevel):
    def __init__(self, master, idx, sectorChoice):
        super().__init__(master)
        self.geometry("300x200")
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(self, height=10, width=30)
        # TODO: insert data from DB
        # TODO: depending on the idx print it in a certain order
        # TODO: and pic only colleges of a chosen sector
        self.listbox.insert(tk.END, *[1, 2, 3, 4])
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack()

        self.listbox.bind('<ButtonRelease-1>', self.on_click_listbox)

    #TODO: error message if no link
    def on_click_listbox(self, event):
        try:
            webbrowser.open('URL')
        except Exception as e:
            self.error_fct(str(e))

    def error_fct(self, errmessage):
        error_str = "[Errno 1]: " + errmessage
        if tkmb.showerror("Error", error_str, parent=self):
            self.destroy()


MainWin().mainloop()
