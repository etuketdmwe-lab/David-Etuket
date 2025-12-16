import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

DB_NAME = "library.db"

# ================================================================
# DATABASE INITIALIZATION
# ================================================================
def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    # BOOKS TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT DEFAULT 'Available',
            due_date TEXT
        )
    """)

    # STUDENTS TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# ================================================================
# DATABASE FUNCTIONS
# ================================================================
def fetch_books():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, status, due_date FROM books")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_book_db(title, author):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

def remove_book_db(book_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

def update_status(book_id, status, due_date=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE books SET status = ?, due_date = ? WHERE id = ?", (status, due_date, book_id))
    conn.commit()
    conn.close()

def validate_student(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE username = ? AND password = ?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result is not None

def register_student(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO students (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# ================================================================
# MAIN APPLICATION
# ================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("900x650")
        self.configure(bg="#cce6ff")

        container = tk.Frame(self, bg="#cce6ff")
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (LoginPage, RegisterPage, HomePage, AboutPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page):
        self.frames[page].tkraise()

# ================================================================
# LOGIN PAGE
# ================================================================
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#003366")
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        wrapper = tk.Frame(self, bg="#003366")
        wrapper.grid(row=0, column=0, sticky="nsew")

        tk.Label(wrapper, text="STUDENT LOGIN", bg="#003366", fg="white",
                 font=("Helvetica", 30, "bold")).pack(pady=80)

        form = tk.Frame(wrapper, bg="#003366")
        form.pack()

        tk.Label(form, text="Username:", bg="#003366", fg="white",
                 font=("Helvetica", 16)).grid(row=0, column=0, pady=10)
        self.username_entry = tk.Entry(form, width=25, font=("Helvetica", 16))
        self.username_entry.grid(row=0, column=1, pady=10)

        tk.Label(form, text="Password:", bg="#003366", fg="white",
                 font=("Helvetica", 16)).grid(row=1, column=0, pady=10)
        self.password_entry = tk.Entry(form, width=25, font=("Helvetica", 16), show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        tk.Button(wrapper, text="LOGIN", font=("Helvetica", 18, "bold"),
                  width=12, bg="white",
                  command=self.login).pack(pady=20)

        tk.Button(wrapper, text="REGISTER", font=("Helvetica", 14),
                  width=12, bg="lightgray",
                  command=lambda: controller.show_frame(RegisterPage)).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if validate_student(username, password):
            self.controller.show_frame(HomePage)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# ================================================================
# REGISTRATION PAGE
# ================================================================
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#004080")
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        wrapper = tk.Frame(self, bg="#004080")
        wrapper.grid(row=0, column=0, sticky="nsew")

        tk.Label(wrapper, text="REGISTER ACCOUNT", bg="#004080", fg="white",
                 font=("Helvetica", 30, "bold")).pack(pady=60)

        form = tk.Frame(wrapper, bg="#004080")
        form.pack()

        tk.Label(form, text="Username:", bg="#004080", fg="white",
                 font=("Helvetica", 16)).grid(row=0, column=0, pady=10)
        self.username_entry = tk.Entry(form, width=25, font=("Helvetica", 16))
        self.username_entry.grid(row=0, column=1, pady=10)

        tk.Label(form, text="Password:", bg="#004080", fg="white",
                 font=("Helvetica", 16)).grid(row=1, column=0, pady=10)
        self.password_entry = tk.Entry(form, width=25, font=("Helvetica", 16), show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        tk.Label(form, text="Confirm Password:", bg="#004080", fg="white",
                 font=("Helvetica", 16)).grid(row=2, column=0, pady=10)
        self.confirm_entry = tk.Entry(form, width=25, font=("Helvetica", 16), show="*")
        self.confirm_entry.grid(row=2, column=1, pady=10)

        tk.Button(wrapper, text="REGISTER", font=("Helvetica", 18, "bold"),
                  width=12, bg="white",
                  command=self.register).pack(pady=30)

        tk.Button(wrapper, text="BACK TO LOGIN", font=("Helvetica", 14),
                  width=15, bg="lightgray",
                  command=lambda: controller.show_frame(LoginPage)).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        if register_student(username, password):
            messagebox.showinfo("Success", "Account created successfully")
            self.controller.show_frame(LoginPage)
        else:
            messagebox.showerror("Error", "Username already exists")

# ================================================================
# HEADER & FOOTER
# ================================================================
def make_header(parent, text):
    frame = tk.Frame(parent, bg="green", height=60)
    frame.pack(fill="x")
    tk.Label(frame, text=text, bg="green", fg="white",
             font=("Helvetica", 22, "bold")).pack(pady=10)

def make_footer(parent):
    frame = tk.Frame(parent, bg="green", height=40)
    frame.pack(side="bottom", fill="x")
    tk.Label(frame, text="© 2025 Library System",
             bg="green", fg="white").pack(pady=5)

# ================================================================
# HOME PAGE
# ================================================================
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#cce6ff")
        self.controller = controller

        make_header(self, "Library Management System")

        content = tk.Frame(self, bg="white", padx=20, pady=20,
                           highlightbackground="darkblue", highlightthickness=4)
        content.place(relx=0.5, rely=0.5, anchor="center")

        left = tk.Frame(content, bg="white")
        left.grid(row=0, column=0, sticky="n")

        tk.Label(left, text="Title:", bg="white").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(left, width=30)
        self.title_entry.grid(row=1, column=0, pady=5)

        tk.Label(left, text="Author:", bg="white").grid(row=2, column=0, sticky="w")
        self.author_entry = tk.Entry(left, width=30)
        self.author_entry.grid(row=3, column=0, pady=5)

        tk.Button(left, text="Add Book", width=20,
                  command=self.add_book).grid(row=4, pady=5)
        tk.Button(left, text="Remove Book", width=20,
                  command=self.remove_book).grid(row=5, pady=5)

        tk.Label(left, text="Search:", bg="white").grid(row=6, column=0, sticky="w")
        self.search_entry = tk.Entry(left, width=30)
        self.search_entry.grid(row=7, column=0, pady=5)
        tk.Button(left, text="Search", width=20,
                  command=self.search).grid(row=8, pady=5)

        middle = tk.Frame(content, bg="white")
        middle.grid(row=0, column=1, padx=20)

        self.listbox = tk.Listbox(middle, width=65, height=20, font=("Courier", 11))
        self.listbox.pack()

        right = tk.Frame(content, bg="white")
        right.grid(row=0, column=2, sticky="n")

        tk.Button(right, text="Check Out", width=18,
                  command=self.check_out).pack(pady=6)
        tk.Button(right, text="Check In", width=18,
                  command=self.check_in).pack(pady=6)
        tk.Button(right, text="About", width=18,
                  command=lambda: controller.show_frame(AboutPage)).pack(pady=6)

        make_footer(self)
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for row in fetch_books():
            self.listbox.insert(tk.END, self.format_row(row))

    def format_row(self, row):
        _, title, author, status, due = row
        return f"{title} by {author} — {status} (Due: {due or 'N/A'})"

    def get_selected_id(self):
        index = self.listbox.curselection()
        if not index:
            return None
        return fetch_books()[index[0]][0]

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        if not title or not author:
            messagebox.showwarning("Error", "Enter title and author")
            return
        add_book_db(title, author)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.refresh()

    def remove_book(self):
        book_id = self.get_selected_id()
        if not book_id:
            return
        remove_book_db(book_id)
        self.refresh()

    def check_out(self):
        book_id = self.get_selected_id()
        if not book_id:
            return
        due = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        update_status(book_id, "Checked Out", due)
        self.refresh()

    def check_in(self):
        book_id = self.get_selected_id()
        if not book_id:
            return
        update_status(book_id, "Available", None)
        self.refresh()

    def search(self):
        keyword = self.search_entry.get().lower()
        self.listbox.delete(0, tk.END)
        for row in fetch_books():
            if keyword in row[1].lower() or keyword in row[2].lower():
                self.listbox.insert(tk.END, self.format_row(row))

# ================================================================
# ABOUT PAGE
# ================================================================
class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#cce6ff")
        make_header(self, "About")

        text = (
            "This is a SQLite-powered Library Management System.\n\n"
            "It stores books permanently using a database instead of\n"
            "temporary in-memory lists.\n\n"
            "Built with Python, Tkinter, and SQLite."
        )

        box = tk.Label(self, text=text, bg="white", font=("Arial", 13),
                       justify="left", padx=40, pady=40)
        box.pack(expand=True, fill="both", padx=40, pady=40)

        tk.Button(box, text="Back",
                  command=lambda: controller.show_frame(HomePage)).pack(pady=20)

        make_footer(self)

# ================================================================
# START APP
# ================================================================
if __name__ == "__main__":
    initialize_database()
    app = App()
    app.mainloop()
