import tkinter as tk
import unittest
import main

class RegistrationTest(unittest.TestCase):
    """Testing registration panel """

    def setUp(self):
        master = tk.Tk()
        self.app = main.Register(master)
        self.app.register_screen()

    def test_registration_enties(self):

        self.app.username_entry.insert(tk.END, "username")
        self.app.password_entry.insert(tk.END, "password")
        self.app.firstname_entry.insert(tk.END, "fname")
        self.app.surname_entry.insert(tk.END, "surname")
        self.app.city_entry.insert(tk.END, "city")
        self.app.email_entry.insert(tk.END, "email")

        self.app.clear_entries()

        self.assertFalse(self.app.username_entry.get())
        self.assertFalse(self.app.password_entry.get())
        self.assertFalse(self.app.firstname_entry.get())
        self.assertFalse(self.app.surname_entry.get())
        self.assertFalse(self.app.city_entry.get())
        self.assertFalse(self.app.email_entry.get())


if __name__ == '__main__':
    unittest.main()
