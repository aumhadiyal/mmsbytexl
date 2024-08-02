import tkinter as tk
import home.Homepage as Homepage  # Importing homepage module
import MalkhanaTable.additems.additems as a
import MalkhanaTable.checkout.checkoutpage as co
import MalkhanaTable.checkin.checkinpage as ci
import MalkhanaTable.viewitems.viewitems as v
import login.login as login

malkhanapage_frame = None
sidebar_buttons = []


def mkpage(prev_homepage_frame):
    prev_homepage_frame.destroy()

    global malkhanapage_frame
    malkhanapage_frame = tk.Frame(prev_homepage_frame.master)
    malkhanapage_frame.master.title("Malkhana page")
    malkhanapage_frame.pack(fill=tk.BOTH, expand=True)

    # Sidebar with buttons
    sidebar = tk.Frame(malkhanapage_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    tabs = [
        ("Add Items", additemsclicked),
        ("View Items", viewitemsclicked),
        ("Checkout Items", checkoutclicked),
        ("Checkin Items", checkinclicked),
        ("Back", go_back),
        ("Log Out", logoutclicked),
    ]

    for text, command in tabs:
        tab_button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
            "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        tab_button.pack(fill=tk.X, pady=5, padx=10)
        sidebar_buttons.append(tab_button)

    # Content area
    content_frame = tk.Frame(malkhanapage_frame, bg="#bdc3c7")
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Add a welcome message in the middle
    welcome_label = tk.Label(
        content_frame, text="Malkhana Page ", font=("Helvetica", 20), bg="#bdc3c7")
    welcome_label.pack(pady=20)
    welcome_label = tk.Label(
        content_frame, text="You can Add,View,Checkin,Checkout items ", font=("Helvetica", 20), bg="#bdc3c7")
    welcome_label.pack(pady=20)

    malkhanapage_frame.mainloop()


def switch_tab(command, tab):
    for button in sidebar_buttons:
        if button.cget("text") == tab:
            button.config(bg="#2c3e50", fg="#ecf0f1")
        else:
            button.config(bg="#34495e", fg="#ecf0f1")
    command()


def go_back():
    malkhana_destroyer()
    Homepage.open_homepage(malkhanapage_frame)


def logoutclicked():
    malkhana_destroyer()
    login.initloginpage(malkhanapage_frame)


def additemsclicked():
    malkhana_destroyer()
    a.additems(malkhanapage_frame)


def checkinclicked():
    malkhana_destroyer()
    ci.CIpage(malkhanapage_frame)


def checkoutclicked():
    malkhana_destroyer()
    co.COpage(malkhanapage_frame)


def viewitemsclicked():
    malkhana_destroyer()
    v.viewitems(malkhanapage_frame)


def malkhana_destroyer():
    if malkhanapage_frame is not None:
        malkhanapage_frame.destroy()
