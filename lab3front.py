# Maria Gorbunova
# Lab3frontend is a GUI that opens windows with the data user requests

import tkinter as tk
import webbrowser
import tkinter.messagebox as tkmb
import sqlite3


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
            print(choice)
            DisplayWin(self, idx, choice)


class ChoiceWin(tk.Toplevel):
    """Toplevel window to prompt the user to pick type of college"""

    def __init__(self, master):
        """constructor creates the window of certain size, has label, radiobuttons and Ok button"""
        super().__init__(master)
        self.geometry("200x150")
        self.grab_set()
        self.focus_set()
        self.choice = -1

        self.label = tk.Label(self, text="Choose type of college", fg="black").grid(sticky="W")
        self.rb_variables = ["Public", "Private", "Both"]
        self.controlVar = tk.StringVar()
        for i, item in enumerate(self.rb_variables):
            tk.Radiobutton(self, text=item, variable=self.controlVar, value=item,
                           ).grid(row=i + 1, column=0, sticky="W")
        self.buttonOk = tk.Button(self, text="OK", command=lambda: self.setAndClose()).grid(sticky="W")

    def getChoice(self):
        """getter for the user's choice"""
        return self.choice

    def setAndClose(self):
        """called when user pushes OK button, sets the choice and closes the window"""
        # if none chosen, throws an exception of ValueError
        try:
            self.choice = self.rb_variables.index(self.controlVar.get())
        except ValueError:
            self.choice = -1  # double checking for later to do nothing
        self.destroy()


class DisplayWin(tk.Toplevel):
    def __init__(self, master, idx, sectorChoice):
        super().__init__(master)
        # TODO: add sector choice to the sql query
        print_options = ['''SELECT name FROM CollegesDB ORDER BY ROWID''',
                         '''SELECT name, earlyPay FROM CollegesDB ORDER BY ROWID''',
                         '''SELECT name, midPay FROM CollegesDB ORDER BY ROWID''',
                         '''SELECT name, stem FROM CollegesDB ORDER BY ROWID''']

        self.conn = sqlite3.connect('lab3back.db')
        self.cur = self.conn.cursor()
        self.cur.execute(print_options[idx])
        # self.myresult = self.cur.fetchall()
        print("*" * 40)
        self.myresult = [item[0] for item in self.cur.fetchall()]
        print(self.myresult)
        print("*" * 40)

        self.geometry("300x200")
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(self, height=10, width=30)
        self.listbox.insert(tk.END, *self.myresult)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack()

        self.listbox.bind('<ButtonRelease-1>', self.on_click_listbox)

    # TODO: error message if no link. Not sure if it is the best approach
    def on_click_listbox(self, event):
        try:
            print(self.listbox.curselection())
            college_name = self.myresult[self.listbox.curselection()[0]]
            self.cur.execute('''SELECT url FROM CollegesDB WHERE name = (?)''', (college_name,))
            myurl = self.cur.fetchone()[0]
            if myurl == "None":
                raise Exception("No website found!")
            webbrowser.open(myurl)
        except Exception as e:
            self.error_fct(str(e))

    def error_fct(self, errmessage):
        error_str = "[Errno 1]: " + errmessage
        if tkmb.showerror("Error", error_str, parent=self):
            self.destroy()


MainWin().mainloop()
