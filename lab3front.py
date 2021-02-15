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
        # this variable is used for naming buttons and naming the new window later in the displayWin
        self.textlist = ['By Salary Potential', 'By Early Career Pay',
                         'By Mid Career Pay', 'By STEM Percentage']

        # could not use for loop. It sends the last i to the buttons so they print the same thing if its a loop
        '''for i, line in enumerate(self.textlist):
            tk.Button(self.buttonframe, text=line, command=lambda: self.new_window(i)).grid(row=idx[i], column=i % 2)'''

        tk.Button(self.buttonframe, text=self.textlist[0],
                  command=lambda: self.new_window(0)).grid(row=1, column=0)
        tk.Button(self.buttonframe, text=self.textlist[1],
                  command=lambda: self.new_window(1)).grid(row=1, column=1)
        tk.Button(self.buttonframe, text=self.textlist[2],
                  command=lambda: self.new_window(2)).grid(row=2, column=0)
        tk.Button(self.buttonframe, text=self.textlist[3],
                  command=lambda: self.new_window(3)).grid(row=2, column=1)
        self.buttonframe.grid()
        self.protocol("WM_DELETE_WINDOW", self.exit_fct)

    def new_window(self, idx):
        """this method is called by event when user pushes a button.
        It opens the sector choice window and then the display window"""

        # fetch the db header and save it in row_names
        self.cur.execute("PRAGMA TABLE_INFO( CollegesDB )")
        val = self.cur.fetchall()
        row_names = [t[1] for t in val]
        # row_names is: ['name', 'sector', 'earlyPay', 'midPay', 'stem', 'url']

        print_options = [
            '''SELECT  {},{} FROM CollegesDB WHERE {} LIKE ? ORDER BY ROWID'''.format(row_names[0],
                                                                                      row_names[5],
                                                                                      row_names[1]),
            '''SELECT {}, {}, {} FROM CollegesDB WHERE {} LIKE ? ORDER BY {}'''.format(row_names[0],
                                                                                       row_names[2],
                                                                                       row_names[5],
                                                                                       row_names[1],
                                                                                       row_names[2]),
            '''SELECT {}, {}, {} FROM CollegesDB WHERE {} LIKE ? ORDER BY {}'''.format(row_names[0],
                                                                                       row_names[3],
                                                                                       row_names[5],
                                                                                       row_names[1],
                                                                                       row_names[3]),
            '''SELECT {}, {}, {} FROM CollegesDB WHERE {} LIKE ? ORDER BY {}'''.format(row_names[0],
                                                                                       row_names[4],
                                                                                       row_names[5],
                                                                                       row_names[1],
                                                                                       row_names[4])]

        sector = ['Public', 'Private not-for-profit', '%']

        # decided to not do this cause in any case a different size of a tuple will break it
        # self.cur.execute('SELECT DISTINCT {} FROM CollegesDB'.format(row_names[1]))

        newWin = ChoiceWin(self)
        self.wait_window(newWin)
        # gets users choice in a idx format so can use it later
        choice = newWin.get_choice()

        # execute the sql command with the sector choice
        self.cur.execute(print_options[idx], (sector[choice],))
        # get all the needed data
        myresult = self.cur.fetchall()
        # if user made a choice open display window
        if choice != -1:
            DisplayWin(self, myresult, self.textlist[idx], idx)

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
        self.geometry("200x125")
        self.grab_set()
        self.focus_set()
        self.choice = -1

        self.label = tk.Label(self, text="Choose type of college", fg="black").grid(sticky="W")

        # for printing name of the radiobuttons
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
        # TODO: with changes... do I still need try catch?
        try:
            # choice is the index of the chosen option
            self.choice = self.controlVar.get()
        except ValueError:
            self.choice = -1  # double checking for later to do nothing if no choice was made
        self.destroy()


class DisplayWin(tk.Toplevel):
    """Toplevel window to list the colleges with their websites' links"""

    def __init__(self, master, data, line, formatting_idx):
        super().__init__(master)
        self.format = formatting_idx

        self.data = data
        self.label = tk.Label(self, text="College Ranking " + line).grid()

        content_frame = tk.Frame(self)
        self.geometry("300x230")
        self.scrollbar = tk.Scrollbar(content_frame)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(content_frame, height=10, width=30)

        view = [self.formatting(i + 1, line) for i, line in enumerate(self.data)]

        # TODO: print in a nice way ... and formatting

        self.listbox.insert(tk.END, *view)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack()
        content_frame.grid()

        self.label = tk.Label(self, text="Click on a college to go to the web").grid(sticky="N")
        self.listbox.bind('<ButtonRelease-1>', self.on_click_listbox)

    def formatting(self, idx, data):
        val = ''
        if self.format == 3:
            val = str(data[1]) + '%'
        elif self.format == 1 or self.format == 2:
            val = '$' + f'{data[1]:,d}'
        mystr = str(idx) + '. ' + data[0] + ' ' + val
        return mystr

    # TODO: error message if no link. Not sure if it is the best approach
    def on_click_listbox(self, event):
        """in event when user clicks on the college in listbox it opens a corresponding website"""
        try:
            college_url = self.data[self.listbox.curselection()[0]][-1]
            if college_url == "None":
                raise Exception("No website found!")
            webbrowser.open(college_url)
        except Exception as e:
            self.error_fct(str(e))

    def error_fct(self, errmessage):
        """open the error message window"""
        if tkmb.showerror("Error", errmessage, parent=self):
            self.destroy()


MainWin().mainloop()
