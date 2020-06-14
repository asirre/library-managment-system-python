from datetime import timedelta, date as dt
import random
import sqlite3




class BooksDB:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,"
                         "title text NOT NULL, "
                         "year_of_relase integer NOT NULL,"
                         "author_name text NOT NULL,"
                         "author_surname text NOT NULL,"
                         "isbn integer NOT NULL, "
                         "genre text NOT NULL,"
                         "availbility integer NOT NULL DEFAULT 1)")
        self.conn.commit()

    def fetch(self, availbility):
        self.cur.execute("SELECT id,title,year_of_relase, author_name, author_surname, genre, availbility "
                         "FROM books WHERE availbility = ?", (availbility,))
        return self.cur.fetchall()

    def fetch_borrowed(self):
        self.cur.execute("SELECT book_id, user_id, borrowed, due_to_return "
                         "FROM borrowings JOIN books ON borrowings.book_id = books.id"
                         "WHERE books.availbility = 0")
        return self.cur.fetchall()

    def insert(self, title, year_of_release, author_name, author_surname, genre, availbility):
        isbn = random.randint(100000, 999999)
        self.cur.execute("INSERT INTO books (title,year_of_relase,author_name, author_surname, isbn,genre,availbility)"
                         " VALUES(?,?,?,?,?,?,?)",
                         (title, year_of_release, author_name, author_surname, isbn, genre, availbility))
        self.conn.commit()

    def status_update(self, id, availability):
        self.cur.execute("UPDATE books SET availbility = ? WHERE id =?", (availability, id))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM books WHERE book_id=?", (id,))
        self.conn.commit()

    def search(self, author_name='', author_surname='', genre='', title=''):
        self.cur.execute("SELECT id,title,year_of_relase, author_name, author_surname, genre"
                         " FROM books WHERE (title=? OR author_name = ? OR author_surname = ? OR genre = ?) AND availbility = 1",
                         (author_name, author_surname, genre, title,))
        return self.cur.fetchall()


class UsersDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,"
                         "name text NOT NULL,"
                         "surname text NOT NULL, "
                         "city text NOT NULL, "
                         "email text NOT NULL,"
                         "permission integer DEFAULT (1) NOT NULL,"
                         "login text NOT NULL ,"
                         "password text NOT NULL )")
        self.conn.commit()

    def fetch(self, id):
        self.cur.execute("SELECT name from users WHERE id =?", (id,))
        return self.cur.fetchone()

    def insert(self, name, surname, city, email, login, password):
        self.cur.execute("INSERT INTO users (name,surname,city,email,login,password)"
                         " VALUES(?,?,?,?,?,?)", (name, surname, city, email, login, password))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM users WHERE id=?", (id,))
        self.conn.commit()

    def search(self, login='', email=''):
        self.cur.execute("SELECT id FROM users WHERE login=? OR email=?", (login, email))
        return self.cur.fetchone()

    def login_data(self, login='', password=''):
        self.cur.execute("SELECT id,permission FROM users WHERE login=? AND password= ?", (login, password))
        return self.cur.fetchone()


class DatesDB:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS borrowings (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                         "borrowed text NOT NULL,"
                         "due_to_return text NOT NULL,"
                         "user_id integer NOT NULL ,"
                         "book_id integer NOT NULL ,"
                         "FOREIGN KEY(user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                         "FOREIGN KEY(book_id) REFERENCES books(id) ON UPDATE CASCADE ON DELETE CASCADE)")
        self.conn.commit()

    def fetch_users(self, userid):
        self.cur.execute("SELECT book_id, books.title, borrowed, due_to_return"
                         " FROM borrowings JOIN books ON borrowings.book_id = books.id"
                         " WHERE borrowings.user_id = ?", (userid,))
        return self.cur.fetchall()

    def fetch(self, id):
        self.cur.execute("SELECT book_id, borrowed, due_to_return FROM borrowings"
                         " WHERE id = ?", (id,))
        return self.cur.fetchone()

    def insert(self, user_id, book_id):
        borrowed = dt.today()
        due_to_return = borrowed + timedelta(days=20)

        self.cur.execute("INSERT INTO borrowings (borrowed, due_to_return, user_id, book_id)"
                         " VALUES(?,?,?,?)", (borrowed, due_to_return, user_id, book_id))
        self.conn.commit()

    def update_to_returned(self, user_id, book_id):
        self.cur.execute("UPDATE borrowings SET date_of_returning = ? WHERE user_id = ? OR book_id = ?,"
                         "(date.today())")

    def remove(self, book_id):
        self.cur.execute("DELETE FROM borrowings WHERE book_id=?", (book_id,))
        self.conn.commit()
