import tkinter as tk
import home.Homepage as Homepage
import MalkhanaTable.checkout.checkoutCourt as c
import MalkhanaTable.checkout.checkoutFSL as f
import MalkhanaTable.MalkhanaPage as m

from login import login

CO_frame = None


def COpage(prev_CO_frame):
    prev_CO_frame.destroy()
    global CO_frame
    checkout_page_destroyer()
    CO_frame = tk.Frame(prev_CO_frame.master)
    CO_frame.master.title("Check Out ")
    CO_frame.pack(fill=tk.BOTH, expand=True)

    # Get screen width and height
    screen_width = CO_frame.winfo_screenwidth()
    screen_height = CO_frame.winfo_screenheight()

    # Sidebar
    sidebar = tk.Frame(CO_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Checkout to FSL", fsl),
        ("Checkout to Court", court),
        ("Home", go_home),
        ("Back", go_back),
    ]

    for text, command in sidebar_buttons:
        tab_button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
            "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        tab_button.pack(fill=tk.X, pady=5, padx=10)

    # Content area
    content_frame = tk.Frame(CO_frame, bg="#bdc3c7")
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Add a welcome message in the middle
    welcome_label = tk.Label(content_frame, text="Welcome to the Check Out!", font=(
        "Helvetica", 20), bg="#bdc3c7")
    welcome_label.pack(pady=20)

    welcome_label = tk.Label(
        content_frame, text="You can Check Out items to FSL or Court ", font=("Helvetica", 20), bg="#bdc3c7")
    welcome_label.pack(pady=20)

    # Add some additional information or widgets
    info_label = tk.Label(content_frame, text="You are logged in as: " + login.current_user, font=(
        "Helvetica", 12), bg="#bdc3c7")
    info_label.pack(pady=10)

    CO_frame.mainloop()


def go_back():
    checkout_page_destroyer()
    m.mkpage(CO_frame)


def go_home():
    checkout_page_destroyer()
    Homepage.open_homepage(CO_frame)


def fsl():
    checkout_page_destroyer()
    f.checkouttoFSL_page(CO_frame)


def court():
    checkout_page_destroyer()
    c.checkouttocourt_page(CO_frame)


def checkout_page_destroyer():
    if CO_frame is not None:
        CO_frame.destroy()
