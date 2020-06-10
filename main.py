import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
import database as db

LIBRARY_COLUMNS = ('Id', 'Title', 'Year', 'Author\'s name', 'Author\'s surname', 'Genre')
LIBRARY_COLUMNS_SIZE = (25, 150, 35, 70, 70, 70)

BORROWINGS_COLUMNS = ('Id', 'Title', 'Day of borrowing', 'Due to return')
BORROWINGS_COLUMNS_SIZE = (25, 120, 100, 90)


class Login:
    """Defines class responsible for logging  """

    def __init__(self, master):
        self.user_app = master
        self.user_app.title('Library')
        self.user_app.geometry('650x350')

        self.udb = db.UsersDB('library.db')

        self.logged_userid = 0

        self.username_entry = None
        self.password_entry = None

        self.username_text = tk.StringVar()
        self.password_text = tk.StringVar()

    def register_panel(self):
        """Goes to registration panel"""
        self.user_app.destroy()
        self.user_app = tk.Tk()
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
            self.logged_userid = exists[0]
            self.user_app.destroy()
            self.user_app = tk.Tk()
            main = Main_Page(self.user_app, self.logged_userid)
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

    def __init__(self, user_app):

        self.user_app = user_app
        self.user_app.title('Registration Panel')
        self.user_app.geometry('1250x850')

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
        if (self.username_text.get() == "" or self.password_text.get() == "" or self.firstname_text.get() == ""
                or self.surname_text.get() == "" or self.email_text.get() == "" or self.city_text.get() == ""):
            messagebox.showerror('Required Fields', 'Please include all fields')
        elif len(self.password_text.get()) < 4:
            messagebox.showerror('Password fail', 'Password must be at least 4 characters long')
        else:
            self.register_user()

    def clear_entries(self):
        """Clearing registration entries """
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.firstname_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.city_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def register_user(self):
        """Checks if user with provided details exists"""
        if_exists = self.udb.search(self.username_text.get(), self.email_text.get())
        if if_exists is not None:
            messagebox.showerror('Error', 'User with this username or email exists')
            self.clear_entries()
        else:
            self.udb.insert(self.firstname_text.get(), self.surname_text.get(), self.city_text.get(),
                            self.email_text.get(), self.username_text.get(), self.password_text.get())
            messagebox.showinfo('Succes', 'Registered succesfull')
            self.back_to_login()

    def register_screen(self):
        """Displaying entries for registration"""
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

    def __init__(self, master, logged_userid):

        self.user_app = master
        self.user_app.title('Library')
        self.user_app.geometry('850x350')
        self.users_list = Treeview(self.user_app, columns=BORROWINGS_COLUMNS, show='headings', height=10)
        self.books_list = Treeview(self.user_app, columns=LIBRARY_COLUMNS, show='headings', height=10)

        self.logged_userid = logged_userid
        self.borrowed_books_counter = 0

        self.dbd = db.DatesDB('library.db')
        self.udb = db.UsersDB('library.db')
        self.bdb = db.BooksDB('library.db')

        self.search_text = tk.StringVar()
        self.search_entry = None

    def logout(self):
        """Log out"""
        if messagebox.askyesno("Logging out", "Do you want to log out?"):
            self.user_app.destroy()
            self.user_app = tk.Tk()
            login_window = Login(self.user_app)
            login_window.welcome_screen()
            self.user_app.mainloop()

    def populate_list(self):
        """Displays books available to borrow"""
        self.books_list.delete(*self.books_list.get_children())
        for row in self.bdb.fetch(1):
            self.books_list.insert('', tk.END, values=row[0:6])

    def user_list(self):
        """Daysplays books borrowed by user"""
        self.users_list.delete(*self.users_list.get_children())
        for row in self.dbd.fetch_users(self.logged_userid):
            self.borrowed_books_counter += 1
            self.users_list.insert('', tk.END, values=row[0:4])

    def borrow_book(self):
        """Borrowing selected book"""
        if self.books_list.selection():
            if self.borrowed_books_counter < 3:
                selected_book = self.books_list.set(self.books_list.selection())
                id = selected_book.get('Id')
                self.dbd.insert(self.logged_userid, id)
                self.bdb.status_update(id, 0)
                self.user_list()
                self.populate_list()
                self.borrowed_books_counter += 1
            else:
                messagebox.showerror('Limit', 'You can have up to 3 books borrowed!')
                return

    def return_book(self):
        """Returning seleted book"""
        if self.users_list.selection():
            selected_book = self.users_list.set(self.users_list.selection())
            id = selected_book.get('Id')
            self.bdb.status_update(id, 1)
            self.dbd.remove(id)
            self.populate_list()
            self.user_list()
            self.borrowed_books_counter -= 1

    def menu_screen(self):
        """Prepares labels, listboxes, buttons"""

        # Available book treeview
        self.books_list.grid(row=1, column=0, padx=8)

        for column_name, width in zip(LIBRARY_COLUMNS, LIBRARY_COLUMNS_SIZE):
            self.books_list.column(column_name, width=width, anchor=tk.CENTER)
            self.books_list.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.user_app, orient=tk.VERTICAL)
        scrollbar.configure(command=self.books_list.set)
        self.books_list.configure(yscrollcommand=scrollbar)

        # User's borrowed books treeview
        self.users_list.grid(row=1, column=1, padx=8)

        for column_name, width in zip(BORROWINGS_COLUMNS, BORROWINGS_COLUMNS_SIZE):
            self.users_list.column(column_name, width=width, anchor=tk.CENTER)
            self.users_list.heading(column_name, text=column_name)

        scrollbar = tk.Scrollbar(self.user_app, orient=tk.VERTICAL)
        scrollbar.configure(command=self.users_list.set)
        self.users_list.configure(yscrollcommand=scrollbar)

        borrow_btn = tk.Button(self.user_app, text='Borrow book', width=12, command=self.borrow_book)
        borrow_btn.grid(row=9, column=0, pady=10)

        return_btn = tk.Button(self.user_app, text='Return book', width=12, command=self.return_book)
        return_btn.grid(row=9, column=1, pady=10)

        logout_btn = tk.Button(self.user_app, text='Logout', width=12, command=self.logout)
        logout_btn.grid(row=0, column=1, pady=10)

        self.populate_list()
        self.user_list()


if __name__ == "__main__":
    library_app = tk.Tk()
    Login(library_app).welcome_screen()
    library_app.mainloop()
