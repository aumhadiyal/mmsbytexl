import tkinter as tk
 
import login.login as login
import MalkhanaTable.MalkhanaPage as mk
import FSLInfo.FSLpage as fp
import CourtInfo.Courtpage as cp
import Log.log as l
import logger
import printt.print as p

homepage_frame = None
sidebar_buttons = []


def open_homepage(prev_login_frame):
    prev_login_frame.destroy()
    global homepage_frame
    homepage_destroyer()

    homepage_frame = tk.Frame(prev_login_frame.master)
    homepage_frame.pack(fill=tk.BOTH, expand=True)

    # Get screen width and height
    screen_width = homepage_frame.winfo_screenwidth()
    screen_height = homepage_frame.winfo_screenheight()
    homepage_frame.master.title("HomePage")

    # Create a sidebar with vertical tabs
    sidebar = tk.Frame(homepage_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    tabs = [
        ("Malkhana Info", mkpage),
        ("FSL Info", fsl),
        ("Court Info", court),
        ("Logs", log),
        ("Print", printDetails),
        ("Log Out", logoutclicked),
    ]

    for text, command in tabs:
        tab_button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
            "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        tab_button.pack(fill=tk.X, pady=5, padx=10)
        sidebar_buttons.append(tab_button)

    # Content area
    content_frame = tk.Frame(homepage_frame, bg="#bdc3c7")
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Add a welcome message in the middle
    welcome_label = tk.Label(content_frame, text="Welcome to the Malkhana Management Software!", font=(
        "Helvetica", 20), bg="#bdc3c7")
    welcome_label.pack(pady=20)

    # Add some additional information or widgets
    info_label = tk.Label(content_frame, text="You are logged in as: " + login.current_user, font=(
        "Helvetica", 12), bg="#bdc3c7")
    info_label.pack(pady=10)

    homepage_frame.mainloop()


def homepage_destroyer():
    global homepage_frame
    if homepage_frame is not None:
        homepage_frame.destroy()


def logoutclicked():
    logger.log_activity(login.current_user, "LOG-OUT")
    homepage_destroyer()
    login.initloginpage(homepage_frame)


def mkpage():
    homepage_destroyer()
    mk.mkpage(homepage_frame)


def fsl():
    homepage_destroyer()
    fp.viewfsl(homepage_frame)


def court():
    homepage_destroyer()
    cp.view_court(homepage_frame)


def log():
    homepage_destroyer()
    l.create_logs_page(homepage_frame)


def printDetails():
    homepage_destroyer()
    p.printPage(homepage_frame)
