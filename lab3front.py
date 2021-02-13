# Maria Gorbunova
# Lab3frontend is a GUI that opens windows with the data user requests

import tkinter as tk
import webbrowser
import tkinter.messagebox as tkmb
import sqlite3


class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('lab3back.db')
        self.cur = self.conn.cursor()

        self.geometry("350x100")
        self.title("Colleges")
        self.label = tk.Label(self, text="Two-Year College Ranking", fg="blue").grid()

        self.buttonframe = tk.Frame(self)

        # this variable is used for naming buttons and naming the new window
        self.textlist = ['By Salary Potential', 'By Early Career Pay', 'By Mid Career Pay', 'By STEM Percentage']

        '''for i, line in enumerate(self.textlist):
            tk.Button(self.buttonframe, text=line, command=lambda: self.new_window(i)).grid(row=idx[i], column=i % 2)'''

        tk.Button(self.buttonframe, text=self.textlist[0], command=lambda: self.new_window(0)).grid(row=1, column=0)
        tk.Button(self.buttonframe, text=self.textlist[1], command=lambda: self.new_window(1)).grid(row=1, column=1)
        tk.Button(self.buttonframe, text=self.textlist[2], command=lambda: self.new_window(2)).grid(row=2, column=0)
        tk.Button(self.buttonframe, text=self.textlist[3], command=lambda: self.new_window(3)).grid(row=2, column=1)
        self.buttonframe.grid()

        self.protocol("WM_DELETE_WINDOW", self.exit_fct)

    def new_window(self, idx):
        newWin = ChoiceWin(self)
        self.wait_window(newWin)
        choice = newWin.get_choice()
        print(choice)  # private public etc

        self.cur.execute("PRAGMA TABLE_INFO( CollegesDB )")
        val = self.cur.fetchall()
        row_names = [t[1] for t in val]
        
        sector = ['Public', 'Private not-for-profit', '%']  # DISTINCT
        print_options = [
            '''SELECT  ''' + row_names[0] + "," + row_names[5] + ''' FROM CollegesDB WHERE ''' + row_names[
                1] + ''' LIKE ? ORDER BY ROWID  ''',
            '''SELECT name, earlyPay, url FROM CollegesDB WHERE sector LIKE ? ORDER BY earlyPay  ''',
            '''SELECT name, midPay, url FROM CollegesDB WHERE sector LIKE ? ORDER BY midPay  ''',
            '''SELECT name, stem, url FROM CollegesDB WHERE sector LIKE ? ORDER BY stem  ''']

        self.cur.execute(print_options[idx], (sector[choice],))
        myresult = self.cur.fetchall()
        print("*" * 40)
        print(myresult)
        print("*" * 40)

        if choice != -1:
            DisplayWin(self, myresult, self.textlist[idx])

    def exit_fct(self):
        """ closes the window, closes the connection with sql, exits the program"""
        self.conn.close()
        self.destroy()
        self.quit()


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

        # for printing name for the radiobuttons
        self.rb_variables = ['Public', 'Private not-for-profit', 'Both']
        self.controlVar = tk.IntVar()

        for i, item in enumerate(self.rb_variables):
            tk.Radiobutton(self, text=item, variable=self.controlVar, value=i).grid(row=i + 1, column=0, sticky="W")
        self.buttonOk = tk.Button(self, text="OK", command=lambda: self.set_close()).grid(sticky="W")

    def get_choice(self):
        """getter for the user's choice"""
        return self.choice

    def set_close(self):
        """called when user pushes OK button, sets the choice and closes the window"""
        # if none chosen, throws an exception of ValueError
        try:
            # choice is the index of the chosen option
            self.choice = self.controlVar.get()
        except ValueError:
            self.choice = -1  # double checking for later to do nothing
        self.destroy()


class DisplayWin(tk.Toplevel):
    def __init__(self, master, data, line):
        super().__init__(master)

        self.data = data
        self.label = tk.Label(self, text="College Ranking " + line).grid()

        content_frame = tk.Frame(self)
        self.geometry("300x230")
        self.scrollbar = tk.Scrollbar(content_frame)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(content_frame, height=10, width=30)

        # TODO: print in a nice way ... and formatting
        self.listbox.insert(tk.END, *self.data)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack()
        content_frame.grid()

        self.label = tk.Label(self, text="Click on a college to go to the web").grid(sticky="N")
        self.listbox.bind('<ButtonRelease-1>', self.on_click_listbox)

    # TODO: error message if no link. Not sure if it is the best approach
    def on_click_listbox(self, event):
        try:
            college_url = self.data[self.listbox.curselection()[0]][-1]  # (23,)
            if college_url == "None":
                raise Exception("No website found!")
            webbrowser.open(college_url)
        except Exception as e:
            self.error_fct(str(e))

    def error_fct(self, errmessage):
        error_str = "[Errno 1]: " + errmessage
        if tkmb.showerror("Error", error_str, parent=self):
            self.destroy()


MainWin().mainloop()
