import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# In-memory book storage
books = []

# ================================================================
# Main Application Class
# ================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("900x650")
        self.configure(bg="#cce6ff")  # Soft light blue

        # Main container for swapping pages
        container = tk.Frame(self, bg="#cce6ff")
        container.pack(fill="both", expand=True)

        self.frames = {}
        for Page in (LandingPage, LoginPage, RegisterPage, HomePage, AboutPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LandingPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


# ================================================================
# HEADER + FOOTER
# ================================================================
def make_header(parent, text):
    header = tk.Frame(parent, bg="green", height=60)
    header.pack(fill="x")

    tk.Label(header, text=text, fg="white", bg="green",
             font=("Helvetica", 22, "bold")).pack(pady=10)
    return header


def make_footer(parent):
    footer = tk.Frame(parent, bg="green", height=40)
    footer.pack(side="bottom", fill="x")
    tk.Label(footer, text="© 2025 Library System",
             bg="green", fg="white", font=("Arial", 11)).pack(pady=5)
    return footer


# ================================================================
# LANDING PAGE — NICE BACKGROUND (NO IMAGE)
# ================================================================
class LandingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#cce6ff")

        make_header(self, "Welcome to The Library Management System")

        # Create gradient background using canvas
        canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=20, pady=20)


        # Smooth vertical gradient
        for i in range(450):
            color = f"#cce6ff" if i < 225 else f"#b3d9ff"
            canvas.create_line(0, i, 850, i, fill=color)

        canvas.create_text(
            425, 100,
            text="Your Digital Library Space",
            fill="#003366",
            font=("Helvetica", 28, "bold")
        )

        canvas.create_text(
            425, 160,
            text="Organize books • Track loans • Manage everything",
            fill="#004080",
            font=("Helvetica", 16)
        )

        # Buttons under the canvas
        btn_frame = tk.Frame(self, bg="#cce6ff")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Login", width=20, font=("Arial", 12),
                  command=lambda: controller.show_frame(LoginPage)).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Enter Library", width=20, font=("Arial", 12),
                  command=lambda: controller.show_frame(HomePage)).grid(row=0, column=1, padx=10)

        make_footer(self)


# ================================================================
# LOGIN PAGE
# ================================================================
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#cce6ff")
        make_header(self, "Login")

        box = tk.Frame(self, bg="white", padx=25, pady=25,
                       highlightbackground="darkblue", highlightthickness=3)
        box.pack(pady=60, expand=True)


        tk.Label(box, text="Username:", bg="white", font=("Arial", 12)).grid(row=0, column=0, pady=10)
        username = tk.Entry(box, font=("Arial", 12), width=25)
        username.grid(row=0, column=1, pady=10)

        tk.Label(box, text="Password:", bg="white", font=("Arial", 12)).grid(row=1, column=0, pady=10)
        password = tk.Entry(box, show="*", font=("Arial", 12), width=25)
        password.grid(row=1, column=1, pady=10)

        tk.Button(box, text="Login", width=20, font=("Arial", 12),
                  command=lambda: controller.show_frame(HomePage)).grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(box, text="No Account? Register Here", font=("Arial", 10),
                  command=lambda: controller.show_frame(RegisterPage)).grid(row=3, column=0, columnspan=2)

        tk.Button(box, text="Back", font=("Arial", 10),
                  command=lambda: controller.show_frame(LandingPage)).grid(row=4, column=0, columnspan=2, pady=10)

        make_footer(self)


# ================================================================
# REGISTER PAGE
# ================================================================
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#cce6ff")
        make_header(self, "Register")

        box = tk.Frame(self, bg="white", padx=25, pady=25,
                       highlightbackground="darkblue", highlightthickness=3)
        box.pack(pady=60)

        tk.Label(box, text="New Username:", bg="white", font=("Arial", 12)).grid(row=0, column=0, pady=10)
        tk.Entry(box, font=("Arial", 12), width=25).grid(row=0, column=1, pady=10)

        tk.Label(box, text="New Password:", bg="white", font=("Arial", 12)).grid(row=1, column=0, pady=10)
        tk.Entry(box, font=("Arial", 12), width=25, show="*").grid(row=1, column=1, pady=10)

        tk.Button(box, text="Register", width=20, font=("Arial", 12),
                  command=lambda: messagebox.showinfo("Success", "User Registered!")
                  ).grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(box, text="Back to Login", font=("Arial", 10),
                  command=lambda: controller.show_frame(LoginPage)).grid(row=3, column=0, columnspan=2)

        make_footer(self)


# ================================================================
# ABOUT PAGE
# ================================================================
class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#cce6ff")

        # FULL-WIDTH HEADER
        make_header(self, "About This System")

        # Main content area (expands to fill screen)
        content = tk.Frame(
            self,
            bg="white",
            padx=40,
            pady=40,
            highlightbackground="darkblue",
            highlightthickness=4
        )
        content.pack(fill="both", expand=True, padx=40, pady=40)

        about_text = (
            "This project is a Python Tkinter–based desktop Library Management System designed\n"
            "for small academic or organizational libraries. It provides essential features such as\n"
            "adding, removing, searching, checking in, and checking out books, along with automatic\n"
            "due-date calculation.\n\n"
            
            "The system offers a simple offline solution that replaces error-prone manual logs and\n"
            "uses an in-memory list to store book data. While effective for small-scale use, it lacks\n"
            "persistent storage, user authentication, and borrower tracking.\n\n"

            "Future improvements include integrating a database, adding user accounts, tracking\n"
            "borrowers, issuing overdue alerts, and enhancing the interface with widgets such as\n"
            "Treeview for better data visualization."
        )

        label = tk.Label(
            content,
            text=about_text,
            bg="white",
            font=("Arial", 13),
            justify="left",
            anchor="nw"
        )
        label.pack(fill="both", expand=True)

        tk.Button(
            content,
            text="Back to Home",
            font=("Arial", 12),
            width=20,
            command=lambda: controller.show_frame(HomePage)
        ).pack(pady=20)

        make_footer(self)



# ================================================================
# HOME PAGE (YOUR ACTUAL LIBRARY SYSTEM)
# ================================================================
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#cce6ff")

        make_header(self, "Library System")

        content = tk.Frame(self, bg="white", padx=20, pady=20,
                           highlightbackground="darkblue", highlightthickness=4)
        content.pack(pady=20, padx=20, fill="both", expand=True)

        # LEFT COLUMN — book entry & search
        left = tk.Frame(content, bg="white")
        left.grid(row=0, column=0, sticky="n")

        tk.Label(left, text="Book Title:", bg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.entry_title = tk.Entry(left, width=30, font=("Arial", 12))
        self.entry_title.grid(row=1, column=0, pady=5)

        tk.Label(left, text="Author:", bg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.entry_author = tk.Entry(left, width=30, font=("Arial", 12))
        self.entry_author.grid(row=3, column=0, pady=5)

        tk.Button(left, text="Add Book", width=20, font=("Arial", 12),
                  command=self.add_book).grid(row=4, pady=5)
        tk.Button(left, text="Remove Book", width=20, font=("Arial", 12),
                  command=self.remove_book).grid(row=5, pady=5)

        tk.Label(left, text="Search:", bg="white", font=("Arial", 12)).grid(row=6, column=0, sticky="w", pady=5)
        self.entry_search = tk.Entry(left, width=30, font=("Arial", 12))
        self.entry_search.grid(row=7, column=0, pady=5)
        tk.Button(left, text="Search", width=20, font=("Arial", 12),
                  command=self.search_book).grid(row=8, pady=5)

        # MIDDLE COLUMN — listbox
        middle = tk.Frame(content, bg="white")
        middle.grid(row=0, column=1, padx=20)

        self.listbox = tk.Listbox(middle, width=60, height=20, font=("Courier", 11))
        self.listbox.pack()

        # RIGHT COLUMN — actions & navigation
        right = tk.Frame(content, bg="white")
        right.grid(row=0, column=2, sticky="n")

        tk.Button(right, text="Check Out", width=18, font=("Arial", 12),
                  command=self.check_out).pack(pady=8)
        tk.Button(right, text="Check In", width=18, font=("Arial", 12),
                  command=self.check_in).pack(pady=8)
        tk.Button(right, text="About", width=18, font=("Arial", 12),
                  command=lambda: controller.show_frame(AboutPage)).pack(pady=8)
        tk.Button(right, text="Logout", width=18, font=("Arial", 12),
                  command=lambda: controller.show_frame(LoginPage)).pack(pady=8)

        self.update_listbox()
        make_footer(self)

    # ---------- Library Functions ----------
    def add_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()

        if not title or not author:
            messagebox.showwarning("Missing Info", "Enter both title and author.")
            return

        books.append({"title": title, "author": author,
                      "status": "Available", "due": ""})
        self.update_listbox()
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)

    def remove_book(self):
        sel = self.listbox.curselection()
        if sel:
            books.pop(sel[0])
            self.update_listbox()
        else:
            messagebox.showinfo("Info", "Select a book first.")

    def search_book(self):
        keyword = self.entry_search.get().lower()
        self.listbox.delete(0, tk.END)
        for book in books:
            if keyword in book["title"].lower() or keyword in book["author"].lower():
                self.listbox.insert(tk.END, self.format_book(book))

    def check_out(self):
        sel = self.listbox.curselection()
        if not sel: 
            messagebox.showinfo("Info", "Select a book first.")
            return

        index = sel[0]
        if books[index]["status"] == "Checked Out":
            messagebox.showinfo("Info", "Already checked out.")
            return

        due = datetime.now() + timedelta(days=14)
        books[index]["status"] = "Checked Out"
        books[index]["due"] = due.strftime("%Y-%m-%d")
        self.update_listbox()

    def check_in(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a book first.")
            return

        index = sel[0]
        books[index]["status"] = "Available"
        books[index]["due"] = ""
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for b in books:
            self.listbox.insert(tk.END, self.format_book(b))

    def format_book(self, book):
        return f"{book['title']} by {book['author']} — {book['status']} (Due: {book['due']})"


# ================================================================
# START APPLICATION
# ================================================================
if __name__ == "__main__":
    app = App()
    app.mainloop()
