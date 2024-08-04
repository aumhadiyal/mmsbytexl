import tkinter as tk 
import MalkhanaTable.checkin.checkinFromFSL as f
import MalkhanaTable.checkin.checkinFromCourt as c
import MalkhanaTable.checkin.checkinFromFSL as ci
import home.Homepage as Homepage
import MalkhanaTable.MalkhanaPage as m 
from login import login

CI_frame = None


def CIpage(prev_CI_frame):
    prev_CI_frame.destroy()
    global CI_frame
    checkin_page_destroyer()
    CI_frame = tk.Frame(prev_CI_frame.master)
    CI_frame.master.title("Check Out ")
    CI_frame.pack(fill=tk.BOTH, expand=True)
    # Sidebar
    sidebar = tk.Frame(CI_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Check In From FSL", fsl),
        ("Check In From Court", court),
        ("Home", go_home),
        ("Back", go_back),
    ]

    for text, command in sidebar_buttons:
        tab_button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
            "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        tab_button.pack(fill=tk.X, pady=5, padx=10)

    # Content area
    content_frame = tk.Frame(CI_frame, bg="#bdc3c7")
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Add a welcome message in the middle
    welcome_label = tk.Label(content_frame, text="Check In Page!", font=(
        "Helvetica", 20), bg="#bdc3c7")
    welcome_label.pack(pady=20)

    welcome_label = tk.Label(
        content_frame, text="You can Check In items from Court and FSL ", font=("Helvetica", 20), bg="#bdc3c7")
    welcome_label.pack(pady=20)

    # Add some additional information or widgets
    info_label = tk.Label(content_frame, text="You are logged in as: " + login.current_user, font=(
        "Helvetica", 12), bg="#bdc3c7")
    info_label.pack(pady=10)

    CI_frame.mainloop()


def go_back():
    checkin_page_destroyer()
    m.mkpage(CI_frame)


def go_home():
    checkin_page_destroyer()
    Homepage.open_homepage(CI_frame)


def fsl():
    checkin_page_destroyer()
    f.checkinfromfsl(CI_frame)


def court():
    checkin_page_destroyer()
    c.checkinfromcourt(CI_frame)


def checkin_page_destroyer():
    if CI_frame is not None:
        CI_frame.destroy()
