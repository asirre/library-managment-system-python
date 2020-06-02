import tkinter as tk
from tkinter import messagebox
import database as db
import variables

"""Defines class responsible for logging  """
class Login:

    def __init__(self, master):
        self.user_app = master
        self.user_app.title('Library')
        self.user_app.geometry('650x350')

        self.udb = db.UsersDB('library.db')

        self.username_entry = None
        self.password_entry = None

        self.username_text = tk.StringVar()
        self.password_text = tk.StringVar()

    def register_panel(self):
        """Goes to registration panel"""
        self.user_app.destroy()
        self.user_app=tk.Tk()
        tmp = Register(self.user_app)
        tmp.register_screen()
        self.user_app.mainloop()

    def check_fields(self):
        """Checks if all fields are filled"""
        if self.username_text.get() == "" or self.password_text.get() == "":
            messagebox.showerror('Required Fields', 'Please include all fields')
            return
        self.login_user()

    def login_user(self):
        """Checks if user with provided details exists"""

        exists = self.udb.login_data(self.username_text.get(), self.password_text.get())
        if exists:
            variables.logged_userid = exists[0]
            self.user_app.destroy()
            self.user_app = tk.Tk()
            main=Main_Page(self.user_app)
            main.menu_screen()

        else:
            tk.messagebox.showerror('Error', 'User does not exists!')
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


    def welcome_screen(self):
        """Prepares Labels, entries, buttons"""
        tk.Label(self.user_app, text="Please enter details below  ").pack()
        tk.Label(self.user_app, text="").pack()
        tk.Label(self.user_app, text="Username * ").pack()
        self.username_entry = tk.Entry(self.user_app, textvariable=self.username_text)
        self.username_entry.pack()
        tk.Label(self.user_app, text="Password * ").pack()
        self.password_entry = tk.Entry(self.user_app, textvariable=self.password_text)
        self.password_entry.pack()

        tk.Label(self.user_app, text="").pack()

        tk.Button(self.user_app, text="Login", width=10, height=1, command=self.check_fields).pack()
        tk.Label(self.user_app, text="").pack()
        tk.Button(self.user_app, text="Create account", width=10, height=1, command=self.register_panel).pack()
        tk.Label(self.user_app, text="").pack()
        tk.Button(self.user_app, text="Exit", width=10, height=1, command=exit).pack()


class Register:

    def __init__(self,user_app):

        self.user_app = user_app
        self.user_app.title('Registration Panel')
        self.user_app.geometry('650x350')

        self.udb = db.UsersDB('library.db')

        self.username_entry = None
        self.password_entry = None
        self.firstname_entry = None
        self.surname_entry = None
        self.email_entry = None
        self.city_entry = None

        self.username_text = tk.StringVar()
        self.password_text = tk.StringVar()
        self.firstname_text = tk.StringVar()
        self.surname_text = tk.StringVar()
        self.email_text = tk.StringVar()
        self.city_text = tk.StringVar()

    def back_to_login(self):
            """Turns back to loginpanel"""
            self.user_app.destroy()
            self.user_app = tk.Tk()
            login_window = Login(self.user_app)
            login_window.welcome_screen()
            self.user_app.mainloop()

    def checks_fields(self):
        """Checks if all fields are filed"""
        if self.username_text.get() == "" or self.password_text.get() == "" or self.firstname_text.get() == "" or self.surname_text.get() == "" or self.email_text.get() == "" or self.city_text.get() == "":
            messagebox.showerror('Required Fields', 'Please include all fields')
        elif len(self.password_text.get()) < 4:
                messagebox.showerror('Password fail','Password must be at least 4 characters long')
        else:
            self.register_user()

    def register_user(self):
        """Checks if user with provided details exists"""
        if_exists = self.udb.search(self.username_text.get(), self.email_text.get())
        if if_exists is not None:
            messagebox.showerror('Error', 'User with this username or email exists')
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.firstname_entry.delete(0, tk.END)
            self.surname_entry.delete(0, tk.END)
            self.city_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        else:
            self.udb.insert(self.firstname_text.get(), self.surname_text.get(), self.city_text.get(), self.email_text.get(),
                                          self.username_text.get(), self.password_text.get())
            messagebox.showinfo('Succes', 'Registered succesfull')
            self.back_to_login()


    def register_screen(self):

        tk.Label(self.user_app, text="Please enter details below  ").pack()
        tk.Label(self.user_app, text="").pack()
        tk.Label(self.user_app, text="Username * ").pack()
        self.username_entry = tk.Entry(self.user_app, textvariable=self.username_text)
        self.username_entry.pack()
        tk.Label(self.user_app, text="Password * ").pack()
        self.password_entry = tk.Entry(self.user_app, textvariable=self.password_text)
        self.password_entry.pack()
        tk.Label(self.user_app, text="Name * ").pack()
        self.firstname_entry = tk.Entry(self.user_app, textvariable=self.firstname_text)
        self.firstname_entry.pack()
        tk.Label(self.user_app, text="Surname * ").pack()
        self.surname_entry = tk.Entry(self.user_app, textvariable=self.surname_text)
        self.surname_entry.pack()
        tk.Label(self.user_app, text="Email * ").pack()
        self.email_entry = tk.Entry(self.user_app, textvariable=self.email_text)
        self.email_entry.pack()
        tk.Label(self.user_app, text="City * ").pack()
        self.city_entry = tk.Entry(self.user_app, textvariable=self.city_text)
        self.city_entry.pack()
        tk.Label(self.user_app, text="").pack()

        tk.Button(self.user_app, text="Register", width=10, height=1, command=self.checks_fields).pack()


class Main_Page:
    """Displaying available books and user's borrowed books"""
    def __init__(self,master):
        self.user_app = master
        self.user_app.title('Library')
        self.user_app.geometry('850x350')

        self.dbd = db.DatesDB('library.db')
        self.udb = db.UsersDB('library.db')
        self.bdb = db.BooksDB('library.db')



    def logout(self):
        """Log out"""
        if messagebox.askyesno("Logging out","Do you want to log out?"):
            variables.logged_userid=0
            self.user_app.destroy()
            self.user_app = tk.Tk()
            login_window = Login(self.user_app)
            login_window.welcome_screen()
            self.user_app.mainloop()


    def populate_list(self):
        """Displays books available to borrow"""
        try:
            self.books_list.delete(0, tk.END)
            for row in self.bdb.fetch_available():
                values = [row[0],row[1], row[2], row[3], row[4]]
                self.books_list.insert(tk.END, values)
        except IndexError:
            pass

    def user_list(self):
        """Daysplays books borrowed by user"""
        try:
            self.users_list.delete(0, tk.END)
            for row in self.dbd.fetch_users(variables.logged_userid):
                values = [row[0],row[1], row[2], row[3]]
                self.users_list.insert(tk.END, values)
        except IndexError:
            pass

    def borrow_book(self):
        index = self.books_list.curselection()[0]
        selected_book = self.books_list.get(index)
        self.dbd.insert(variables.logged_userid, selected_book[0])
        self.bdb.status_update(selected_book[0],0)
        self.populate_list()
        self.user_list()

    def return_book(self):
        index = self.users_list.curselection()[0]
        selected_book = self.users_list.get(index)
        self.bdb.status_update(selected_book[0],1)
        self.dbd.remove(selected_book[0])
        self.populate_list()
        self.user_list()




    def menu_screen(self):
        """Prepares labels, listboxes, buttons"""

        search_text = tk.StringVar()
        search_label = tk.Label(self.user_app, text='Search book', font=('bold', 10), pady=20)
        search_label.grid(row=0, column=0, sticky=tk.E)
        search_entry = tk.Entry(self.user_app, textvariable=search_text)
        search_entry.grid(row=0, column=1)


        # Available book list listbox
        books_label = tk.Label(self.user_app, text='Available books', font=('bold', 10), pady=20)
        books_label.grid(row=2, column=0)
        self.books_list = tk.Listbox(self.user_app, height=8, width=50, border=0)
        self.books_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

        # scrollbar
        scrollbar = tk.Scrollbar(self.user_app)
        scrollbar.grid(row=3, column=3)
        # set scroll to listbox
        self.books_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.books_list.yview)
        # bind select
        self.books_list.bind('<<ListboxSelect>>')

        # Users books list listbox
        mybooks_label = tk.Label(self.user_app, text='My books', font=('bold', 10), pady=20)
        mybooks_label.grid(row=2, column=4)
        self.users_list = tk.Listbox(self.user_app, height=8, width=50, border=0)
        self.users_list.grid(row=3, column=4, columnspan=3, rowspan=6, pady=20, padx=20)

        # scrollbar
        scrollbar = tk.Scrollbar(self.user_app)
        scrollbar.grid(row=3, column=7)
        # set scroll to listbox
        self.users_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.users_list.yview)
        # bind select
        self.users_list.bind('<<ListboxSelect>>')

        borrow_btn = tk.Button(self.user_app, text='Borrow book', width=12, command = self.borrow_book)
        borrow_btn.grid(row=9, column=1, pady=20)

        return_btn = tk.Button(self.user_app, text='Return book', width=12, command = self.return_book)
        return_btn.grid(row=9, column=5, pady=20)

        logout_btn = tk.Button(self.user_app, text='Logout', width=12,command =self.logout)
        logout_btn.grid(row=9, column=7, pady=20)


        self.populate_list()
        self.user_list()


if __name__ == "__main__":
    library_app = tk.Tk()
    Login(library_app).welcome_screen()
    library_app.mainloop()