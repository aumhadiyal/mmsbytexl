import tkinter as tk 
import MalkhanaTable.additems.additems as a
import home.Homepage as Homepage
import MalkhanaTable.checkin.checkinpage as cp
import MalkhanaTable.checkin.checkinFromCourt as cic
import Log.log as log
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
import logger as lu
import login.login as login

fsl_checkin_frame = None


def update_item_status(barcode, checkin_date, checkin_time,
                       order_no, examiner, examiner_report):
    con = sqlite3.connect('databases/items_in_malkhana.db')
    cursor = con.cursor()
    cursor.execute(
        "UPDATE items SET item_status='malkhana' where barcode = ?", (barcode,))
    con.commit()
    con.close()
    conn = sqlite3.connect("databases/fsl_records.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE fsl_records SET checkin_date = ?,checkin_time=?,examiner_name=?,fsl_report = ? WHERE order_no = ?",
                   (checkin_date, checkin_time, examiner, examiner_report, order_no))
    barcode_entry.delete(0, tk.END)
    examiner_entry.delete(0, tk.END)
    checkin_date_entry.set_date(None)
    order_no_entry.delete(0, tk.END)
    examiner_report_entry.delete("1.0", tk.END)
    conn.commit()
    conn.close()
    messagebox.showinfo("Successful", "Succesfully entered into Malkhana")
    log.update_logs(barcode, "Checked In From FSL",
                    checkin_date, checkin_time)
    activity = "Item checked in from FSL barcode no: "+barcode
    lu.log_activity(login.current_user, activity)


def checkin():
    barcode = barcode_entry.get()
    checkin_time = f"{hour_var.get()}:{minute_var.get()}"
    checkin_date = checkin_date_entry.get_date()
    order_no = order_no_entry.get()
    examiner = examiner_entry.get()
    examiner_report = examiner_report_entry.get("1.0", "end-1c")

    if not barcode or not checkin_date or not checkin_time or not order_no or not examiner or not examiner_report:
        messagebox.showerror("Error", "All fields must be filled in to check in an item.")
        return
    barcode_checker(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report)


def checkinfromcourt():
    global fsl_checkin_frame
    fsL_checkin_destroyer()
    cic.checkinfromcourt(fsl_checkin_frame)


def checkinfromfsl(prev_checkin_page):
    prev_checkin_page.destroy()
    global fsl_checkin_frame, barcode_entry, order_no_entry, checkin_date_entry, hour_var, minute_var, examiner_report_entry, examiner_entry
    fsL_checkin_destroyer()
    fsl_checkin_frame = tk.Frame(prev_checkin_page.master)
    fsl_checkin_frame.master.title("Checkin From FSL")
    fsl_checkin_frame.pack(fill=tk.BOTH, expand=True)

    # Get screen width and height
    screen_width = fsl_checkin_frame.winfo_screenwidth()
    screen_height = fsl_checkin_frame.winfo_screenheight()

    # Use pack for the fsl_checkin_frame
    fsl_checkin_frame.pack(fill=tk.BOTH, expand=True)

    # Sidebar
    sidebar = tk.Frame(fsl_checkin_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Checkin From FSL", None),
        ("Checkin From Court", checkinfromcourt),
        ("Home", go_home),
        ("Back", go_back),
    ]

    for text, command in sidebar_buttons:
        if text == "Checkin From FSL":
            button = tk.Button(sidebar, text=text, background="#16a085", foreground="#ecf0f1", font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        else:
            button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        button.pack(fill=tk.X, pady=5, padx=10)

    # Define fonts
    textbox_font = ('Helvetica', 12)
    font_style = ('Helvetica', 12)

    # Labels and Entry Fields
    font_style = ('Helvetica', 12)

    tk.Label(fsl_checkin_frame, text="Barcode Number:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    barcode_entry = tk.Entry(
        fsl_checkin_frame, background="#FFFFFF", font=textbox_font)
    barcode_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(fsl_checkin_frame, text="Order Number:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    order_no_entry = tk.Entry(
        fsl_checkin_frame, background="#FFFFFF", font=textbox_font)
    order_no_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(fsl_checkin_frame, text="Check In Date:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    checkin_date_entry = DateEntry(fsl_checkin_frame, font=textbox_font,
                                   width=12, background='darkblue', foreground='white', borderwidth=2)
    checkin_date_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(fsl_checkin_frame, text="Check In Time:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")

    time_frame = tk.Frame(fsl_checkin_frame, bg="#f6f4f2")
    time_frame.pack(padx=10, pady=5, anchor="w")

    hour_var = tk.StringVar(time_frame, value='00')
    hour_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=hour_var, values=[
        str(i).zfill(2) for i in range(24)], state='readonly', width=5)

    minute_var = tk.StringVar(time_frame, value='00')
    minute_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=minute_var, values=[
        str(i).zfill(2) for i in range(60)], state='readonly', width=5)

    hour_menu.pack(side=tk.LEFT, pady=5)
    minute_menu.pack(side=tk.LEFT, padx=10, pady=5)

    tk.Label(fsl_checkin_frame, text="Examiner Name:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    examiner_entry = tk.Entry(
        fsl_checkin_frame, background="#FFFFFF", font=textbox_font)
    examiner_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(fsl_checkin_frame, text="FSL Report:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    examiner_report_entry = tk.Text(
        fsl_checkin_frame, height=5, background="#FFFFFF", font=textbox_font)
    examiner_report_entry.pack(padx=10, pady=5, anchor="w")

    button_font = ('Helvetica', 12)
    # Adjusted button sizes
    button_width = 20
    button_height = 2

    checkin_button = tk.Button(
        fsl_checkin_frame, text="Check In", background="#f6f4f2", command=checkin, font=button_font, width=button_width, height=button_height)
    checkin_button.pack(
        padx=10, pady=5, anchor="w")

    back_button = tk.Button(
        fsl_checkin_frame, text="Back", background="#f6f4f2", command=go_back, font=button_font, width=button_width, height=button_height)
    back_button.pack(
        padx=10, pady=5, anchor="w")

    home_button = tk.Button(
        fsl_checkin_frame, text="Home", background="#f6f4f2", command=go_home, font=button_font, width=button_width, height=button_height)
    home_button.pack(
        padx=10, pady=5, anchor="w")


def go_home():
    fsL_checkin_destroyer()
    Homepage.open_homepage(fsl_checkin_frame)


def go_back():
    fsL_checkin_destroyer()
    cp.CIpage(fsl_checkin_frame)


def fsL_checkin_destroyer():
    if fsl_checkin_frame is not None:
        fsl_checkin_frame.destroy()


def barcode_checker(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchall()
    conn.close()

    if not result:
        messagebox.showerror("Barcode Not Found",
                             "Entered Barcode Not Found In Database.")
        # Clear the input fields after showing the error
        barcode_entry.delete(0, tk.END)
        examiner_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)
        examiner_report_entry.delete("1.0", tk.END)
        return

    already_inornot(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report)
    # Clear the input fields after successful checkout
    barcode_entry.delete(0, tk.END)
    examiner_entry.delete(0, tk.END)
    checkin_date_entry.set_date(None)
    examiner_report_entry.delete("1.0", tk.END)


def already_inornot(barcode, checkin_date, checkin_time,
                    order_no, examiner, examiner_report):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_status FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] in ("fsl", "FSL"):
        update_item_status(barcode, checkin_date, checkin_time,
                           order_no, examiner, examiner_report)

    else:
        messagebox.showerror("Item Exists In Malkhana/Court",
                             "Item Already Exists In Malkhana/Court.")
        barcode_entry.delete(0, tk.END)
        examiner_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)
        examiner_report_entry.delete("1.0", tk.END)
