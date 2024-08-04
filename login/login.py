import tkinter as tk
from tkinter import messagebox, ttk
import login.logindb as logindb
import home.Homepage as Homepage
import logger as lu

entry_password = None
entry_username = None
login_frame = None


def check_login():
    global login_frame
    global current_user
    username = entry_username.get()
    password = entry_password.get()

    if logindb.check_credentials(username, password):
        messagebox.showinfo("Successful", "Login Successful!")
        current_user = username
        lu.log_activity(username, "LOG-IN")
        Homepage.open_homepage(login_frame)
    else:
        messagebox.showerror("Error", "Wrong Username or Password.")


def initloginpage(prev_main_frame):
    prev_main_frame.destroy()
    global entry_username, entry_password, login_frame

    login_destroyer()

    login_frame = tk.Frame(prev_main_frame.master,
                           background="#fafafa")  # Set background color to light gray
    login_frame.pack(expand=True, fill="both")

    style = ttk.Style()
    style.theme_use('clam')  # Change to a different theme

    # Configure label style for dark green text and larger font size
    style.configure('Green.TLabel', foreground='#1b4e39',
                    font=("Helvetica", 28, "bold"))

    label_heading = ttk.Label(
        login_frame, text="Malkhana Management Software", style='Green.TLabel', background="#fafafa")  # Set dark green text on light gray background
    label_heading.pack(pady=(50, 20))  # Add more top padding for spacing

    prev_main_frame.master.title("Login Page")
    logindb.initialize_db()

    label_username = ttk.Label(
        login_frame, text="Username:", background="#fafafa", foreground="#333", font=("Helvetica", 16))  # Adjust font size and set text color
    label_password = ttk.Label(
        login_frame, text="Password:", background="#fafafa", foreground="#333", font=("Helvetica", 16))  # Adjust font size and set text color
    entry_username = ttk.Entry(
        login_frame, font=("Helvetica", 16))  # Adjust font size
    entry_password = ttk.Entry(
        login_frame, show="*", font=("Helvetica", 16))  # Adjust font size
    button_login = tk.Button(login_frame, text="Login",
                             command=check_login, font=("Helvetica", 16), bg="#1b4e39", fg="white")  # Adjust font size and set background color to dark green

    label_username.pack(pady=10)
    entry_username.pack(pady=5)
    label_password.pack(pady=10)
    entry_password.pack(pady=5)
    button_login.pack(pady=(20, 50))  # Add more bottom padding for spacing


def login_destroyer():
    global login_frame
    if login_frame is not None:
        login_frame.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    initloginpage(root)
    root.mainloop()
