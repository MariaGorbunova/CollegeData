# Maria Gorbunova
# Lab3frontend is a GUI that opens windows with the colleges of the sector that user requested

# Reviewed my code with Ben Lublin. Reviewed his code

import tkinter as tk
import webbrowser
import tkinter.messagebox as tkmb
import sqlite3


class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('lab3back.db')
        self.cur = self.conn.cursor()

        # fetch the db header and save it in row_names
        self.cur.execute("PRAGMA TABLE_INFO( CollegesDB )")
        val = self.cur.fetchall()
        self.row_names = [t[1] for t in val]
        # row_names: ['name', 'sector_id', 'earlyPay', 'midPay', 'stem', 'url']
        self.cur.execute("PRAGMA TABLE_INFO( SectorsDB )")
        val = self.cur.fetchall()
        self.sectors_ = [t[1] for t in val]
        self.cur.execute('SELECT DISTINCT {} FROM SectorsDB'.format(self.sectors_[1]))
        val = self.cur.fetchall()
        self.types_sectors = [t[0] for t in val[::-1]]
        # ['Public', 'Private not-for-profit']

        self.geometry("350x100")
        self.title("Colleges")
        self.label = tk.Label(self, text="Two-Year College Ranking", fg="blue").grid()
        self.buttonframe = tk.Frame(self)
        # this variable is used for naming buttons and naming the new window later in the displayWin
        self.textlist = ['By Salary Potential', 'By Early Career Pay',
                         'By Mid Career Pay', 'By STEM Percentage']
        # could not use for loop. It sends the last i to the buttons so they print the same thing if its a loop
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
        newWin = ChoiceWin(self, self.types_sectors.copy())
        self.wait_window(newWin)
        # gets users choice in a idx format so can use it later
        choice = newWin.get_choice()
        if choice != -1:
            self.valid_choice(idx, choice)

    def valid_choice(self, idx, choice):
        """if the user choice is valid start the work with databases"""
        sectors = self.types_sectors.copy()
        sectors.append('%')
        print_options = [
            '''SELECT  {},{} FROM CollegesDB JOIN SectorsDB ON
            CollegesDB.{sid} = SectorsDB.{} AND
            SectorsDB.{} LIKE ? ORDER BY CollegesDB.ROWID'''.format(self.row_names[0], self.row_names[5],
                                                                    self.sectors_[0], self.sectors_[1], sid=self.row_names[1]),
            self.build_q(2), self.build_q(3), self.build_q(4)]
        # execute the sql command with the sector choice
        self.cur.execute(print_options[idx], (sectors[choice],))
        myresult = self.cur.fetchall()
        # if user made a choice open display window
        DisplayWin(self, myresult, self.textlist[idx], idx)

    def build_q(self, column):
        """ build the query depending on the button option"""
        return '''SELECT {}, {}, {} FROM CollegesDB JOIN SectorsDB ON
            CollegesDB.{sid} = SectorsDB.{} AND
            SectorsDB.{} LIKE ?  ORDER BY {} DESC'''.format(self.row_names[0], self.row_names[column],
                                                            self.row_names[5], self.sectors_[0], self.sectors_[1],
                                                            self.row_names[column], sid=self.row_names[1])

    def exit_fct(self):
        """ closes the window, closes the connection with sql, exits the program"""
        self.conn.close()
        self.destroy()
        self.quit()


class ChoiceWin(tk.Toplevel):
    """Toplevel window to prompt the user to pick type of college"""

    def __init__(self, master, sectors):
        """constructor creates the window of certain size, has label, radiobuttons and Ok button"""
        super().__init__(master)
        self.geometry("200x125")
        self.grab_set()
        self.focus_set()
        self.choice = -1
        self.label = tk.Label(self, text="Choose type of college", fg="black").grid(sticky="W")

        # for printing name of the radiobuttons
        self.rb_variables = sectors
        self.rb_variables.append('Both')

        self.controlVar = tk.IntVar()
        for i, item in enumerate(self.rb_variables):
            tk.Radiobutton(self, text=item, variable=self.controlVar, value=i).grid(sticky="W")
        self.buttonOk = tk.Button(self, text="OK", command=self.set_close).grid(sticky="W")

    def get_choice(self):
        """getter for the user's choice"""
        return self.choice

    def set_close(self):
        """called when user pushes OK button, sets the choice and closes the window"""
        # changes the value of choice only if the ok button is pressed
        self.choice = self.controlVar.get()
        self.destroy()


class DisplayWin(tk.Toplevel):
    """Toplevel window to list the colleges with their websites' links"""

    def __init__(self, master, data, line, formatting_idx):
        """passed in all needed data, line - for the window text label, formatting_idx - for formatting the 3d column"""
        super().__init__(master)
        self.geometry("300x230")
        self.format = formatting_idx
        self.data = data
        self.label = tk.Label(self, text="College Ranking " + line).grid()
        self.content_frame = tk.Frame(self)
        self.scrollbar = tk.Scrollbar(self.content_frame)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(self.content_frame, height=10, width=30)
        # prepare data for printing
        view = [self.formatting(i, college) for i, college in enumerate(self.data, 1)]
        self.listbox.insert(tk.END, *view)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack()
        self.content_frame.grid()
        self.label = tk.Label(self, text="Click on a college to go to the web").grid(sticky="N")
        self.listbox.bind('<<ListboxSelect>>', self.on_click_listbox)

    def formatting(self, idx, data):
        """format the values for gui output in listbox"""
        val = ''
        if self.format == 3:
            val = str(data[1]) + '%'
        elif self.format == 1 or self.format == 2:
            val = '$' + f'{data[1]:,d}'
        return f'{str(idx)}. {data[0]} {val}'

    def on_click_listbox(self, event):
        """in event when user clicks on the college in listbox it opens a corresponding website"""
        try:
            college_url = self.data[self.listbox.curselection()[0]][-1]
            # this works because in the backend if there is any exception caught it'll replace the link with "None"str
            if college_url == "None":
                raise Exception(f"No website for {self.data[self.listbox.curselection()[0]][0]} found!")
            webbrowser.open(college_url)
        except Exception as e:
            tkmb.showerror("Error", str(e), parent=self)


MainWin().mainloop()
