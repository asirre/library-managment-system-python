from datetime import date as dt
import unittest
import database

class DatabaseTest(unittest.TestCase):
    """Testing some of database functions"""

    def setUp(self):
        self.books_db = database.BooksDB(':memory:')
        self.users_db = database.UsersDB(':memory:')
        self.dates_db = database.DatesDB(':memory:')
        self.books_db.insert("title", "year_of_relase", "author_name", "author_surname", "genre", 0)
        self.books_db.insert("title", "year_of_relase", "author_name", "author_surname", "genre", 1)
        self.users_db.insert("name", "surname", "city", "email", "login", "password")
        self.dates_db.insert(1, 1)

    def test_fetch_available(self):
        value = self.books_db.fetch(1)
        self.assertEqual(value[0][6], 1)

    def test_fetch_borrowed(self):
        value = self.books_db.fetch(0)
        self.assertEqual(value[0][6], 0)

    def test_find_and_delete_user(self):
        value = self.users_db.search("login", "email")
        self.users_db.remove(value[0])
        self.assertEqual(self.users_db.search("login", "email"), None)

    def test_date(self):
        value = self.dates_db.fetch(1)
        self.assertEqual(value[1], dt.today().isoformat())


if __name__ == '__main__':
    unittest.main()
