import tkinter as tk
from tkinter import ttk
import home.Homepage as Homepage
import MalkhanaTable.checkin.checkinpage as cp
import sqlite3
from datetime import datetime, date
import home.Homepage as homepage
import MalkhanaTable.MalkhanaPage as mk
import login.login as login
import logger as lu
import FSLInfo.FSLpage as f
import CourtInfo.Courtpage as cp
import Log.log as l
import printt.print as p

CL_frame = None


def update_logs(barcode, status, date, time):
    conn = sqlite3.connect('E:/Malkhana/databases/logs.db')
    cursor = conn.cursor()
    # Create the 'logs' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                        Barcode TEXT,
                        Status TEXT,
                        Date DATE,
                        Time TEXT
                    )''')
    # Assuming that the 'logs' table has columns: "Barcode", "Status", "Date", "Time"
    cursor.execute("INSERT INTO logs (Barcode, Status, Date, Time) VALUES (?, ?, ?, ?)",
                   (barcode, status, date, time))

    conn.commit()
    conn.close()


def search_logs(search_barcode):
    # Fetch logs data from the SQLite database based on the search barcode
    conn = sqlite3.connect('E:/Malkhana/databases/logs.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs WHERE barcode=?", (search_barcode,))
    logs_data = cursor.fetchall()

    conn.close()
    return logs_data


def create_logs_page(prev_homepage_frame):
    prev_homepage_frame.destroy()
    global CL_frame
    CL_destroyer()
    CL_frame = tk.Frame(prev_homepage_frame.master)
    CL_frame.master.title("Logs")
    CL_frame.pack(fill=tk.BOTH, expand=True)

    # Sidebar
    sidebar = tk.Frame(CL_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    tabs = [
        ("Malkhana Info", mkpage),
        ("FSL Info", fsl),
        ("Court Info", court),
        ("Logs", None),
        ("Print", printDetails),
        ("Log Out", logoutclicked),
    ]

    for text, command in tabs:
        if text == "Logs":
            button = tk.Button(sidebar, text=text, background="#16a085", foreground="#ecf0f1", font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        else:
            button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        button.pack(fill=tk.X, pady=5, padx=10)

    # Main content area
    main_frame = tk.Frame(CL_frame, bg="#dcdcdc")
    main_frame.pack(fill=tk.BOTH, expand=True)

    logs_tree_frame = tk.Frame(main_frame, bg="#dcdcdc")
    logs_tree_frame.pack(fill=tk.BOTH, expand=True)

    logs_tree_scroll = tk.Scrollbar(logs_tree_frame)
    logs_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    logs_tree = ttk.Treeview(
        logs_tree_frame,
        columns=("Barcode", "Status", "Date", "Time"),
        show="headings",
        yscrollcommand=logs_tree_scroll.set,
        height=30
    )
    logs_tree.pack(fill=tk.BOTH, expand=True)

    logs_tree_scroll.config(command=logs_tree.yview)

    logs_tree.heading("Barcode", text="Barcode")
    logs_tree.heading("Status", text="CheckIn/CheckOut")
    logs_tree.heading("Date", text="Date")
    logs_tree.heading("Time", text="Time")

    logs_tree.column("Barcode", width=250, anchor=tk.CENTER)
    logs_tree.column("Status", width=250, anchor=tk.CENTER)
    logs_tree.column("Date", width=200, anchor=tk.CENTER)
    logs_tree.column("Time", width=200, anchor=tk.CENTER)

    search_frame = tk.Frame(main_frame, bg="#dcdcdc")
    search_frame.pack(pady=10, anchor=tk.S)  # Align to the bottom of CL_frame

    barcode_search_label = tk.Label(
        search_frame, text="Search by Barcode: ", font=("Helvetica", 12))
    barcode_search_label.pack(side=tk.LEFT)

    barcode_search_entry = tk.Entry(
        search_frame,  background="#B9E6FF", width=20, font=("Helvetica", 12))
    barcode_search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(search_frame, background="#9a9a9a", text="Search", command=lambda: search_logs_and_display(
        barcode_search_entry.get(), logs_tree), font=("Helvetica", 12))
    search_button.pack(side=tk.LEFT)

    Home = tk.Button(CL_frame, text="Home",  background="#9a9a9a",
                     command=go_home, font=("Helvetica", 12))
    Home.pack(side=tk.LEFT, padx=10, pady=10)

    CL_frame.mainloop()


def search_logs_and_display(search_barcode, logs_tree):
    logs_data = search_logs(search_barcode)
    logs_tree.delete(*logs_tree.get_children())

    for log_entry in logs_data:
        logs_tree.insert("", tk.END, values=log_entry)


def CL_destroyer():
    if CL_frame is not None:
        CL_frame.destroy()


def go_back():
    CL_destroyer()
    homepage.open_homepage(CL_frame)


def go_home():
    CL_destroyer()
    homepage.open_homepage(CL_frame)


def logoutclicked():
    lu.log_activity(login.current_user, "LOG-OUT")
    CL_destroyer()
    login.initloginpage(CL_frame)


def mkpage():
    CL_destroyer()
    mk.mkpage(CL_frame)


def court():
    CL_destroyer()
    cp.view_court(CL_frame)


def fsl():
    CL_destroyer()
    f.viewfsl(CL_frame)


def printDetails():
    global CL_frame
    CL_destroyer()
    p.printPage(CL_frame)
