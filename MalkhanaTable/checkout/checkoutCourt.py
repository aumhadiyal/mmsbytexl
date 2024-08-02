import datetime
import tkinter as tk
import home.Homepage as Homepage
import MalkhanaTable.checkout.checkoutFSL as cof
import MalkhanaTable.MalkhanaPage as m
import Log.log as log
from tkinter import ttk
import sqlite3
import MalkhanaTable.checkout.checkoutpage as co
from tkcalendar import DateEntry
from tkinter import messagebox
import login.login as login
import logger as lu

checkout_frame = None

def checkout_destroyer():
    if checkout_frame is not None:
        checkout_frame.destroy()

def autofill_details():
    barcode = barcode_entry.get()
    if not barcode:
        messagebox.showwarning("Warning", "Barcode cannot be empty.")
        return

    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()

    if result:
        fir_no_entry.delete(0, tk.END)
        seized_items_entry.delete(0, tk.END)
        court_name_entry.delete(0, tk.END)
        cnr_number_entry.delete(0, tk.END)
        fir_no_entry.insert(0, result[1])
        seized_items_entry.insert(0, result[2])
    else:
        messagebox.showerror("Error", "Barcode not found in the database.")

def update_item_status(barcode, checkout_date, checkout_time, taken_by_whom, seized_items, fir_no, court_name, cnr_number):
    con = sqlite3.connect('databases/items_in_malkhana.db')
    cursor = con.cursor()
    cursor.execute(
        "UPDATE items SET item_status='court' WHERE barcode = ?", (barcode,))
    con.commit()
    con.close()
    
    conn = sqlite3.connect("databases/court_records.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS court_records (
        barcode TEXT ,
        fir_no TEXT,
        seized_items TEXT,
        checkout_date TEXT,
        checkout_time TEXT,
        taken_by_whom TEXT,
        court_name TEXT,
        cnr_number TEXT ,
        checkin_date TEXT,
        checkin_time TEXT,
        order_details TEXT,
        entry_time TEXT
    );''')
    
    entry_time = datetime.datetime.now()
    cursor.execute("INSERT INTO court_records (barcode, fir_no, seized_items, checkout_date, checkout_time, taken_by_whom, court_name, cnr_number, entry_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (barcode, fir_no, seized_items, checkout_date, checkout_time, taken_by_whom, court_name, cnr_number, entry_time))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Successful", "Successfully checked out from Malkhana")
    log.update_logs(barcode, "Checked Out To Court", checkout_date, checkout_time)
    activity = "Item checked out to Court barcode no: "+barcode
    lu.log_activity(login.current_user, activity)

def checkouttocourt():
    barcode = barcode_entry.get()
    fir_no = fir_no_entry.get()
    seized_items = seized_items_entry.get()
    taken_by_whom = taken_by_whom_entry.get()
    checkout_date = checkout_date_entry.get_date()
    checkout_time = f"{hour_var.get()}:{minute_var.get()}"
    court_name = court_name_entry.get()
    cnr_number = cnr_number_entry.get()

    if not barcode or not fir_no or not seized_items or not taken_by_whom or not checkout_date or not checkout_time or not court_name or not cnr_number:
                    messagebox.showerror("Error", "All fields must be filled out to check out an item.")
                    return
    barcode_checker(barcode, checkout_date, checkout_time,
                    taken_by_whom, seized_items, fir_no, court_name, cnr_number)

    # Clear the input fields after checkout
    barcode_entry.delete(0, tk.END)
    fir_no_entry.delete(0, tk.END)
    seized_items_entry.delete(0, tk.END)
    taken_by_whom_entry.delete(0, tk.END)
    checkout_date_entry.set_date(None)  # Clear the date entry
    court_name_entry.delete(0, tk.END)
    cnr_number_entry.delete(0, tk.END)

def checkouttofsl_page():
    global checkout_frame
    checkout_destroyer()
    cof.checkouttoFSL_page(checkout_frame)

def checkouttocourt_page(root):
    global checkout_frame, barcode_entry, fir_no_entry, seized_items_entry, taken_by_whom_entry, checkout_date_entry, hour_var, minute_var, court_name_entry, cnr_number_entry
    checkout_destroyer()
    checkout_frame = tk.Frame(root.master)
    checkout_frame.master.title("Checkout to Court")
    checkout_frame.pack(fill=tk.BOTH, expand=True)

    screen_width = checkout_frame.winfo_screenwidth()
    screen_height = checkout_frame.winfo_screenheight()

    # Sidebar
    sidebar = tk.Frame(checkout_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Checkout to FSL", checkouttofsl_page),
        ("Checkout to Court", None),
        ("Home", go_home),
        ("Back", go_back),
    ]

    for text, command in sidebar_buttons:
        if text == "Checkout to Court":
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

    # Labels
    tk.Label(checkout_frame, text="Barcode Number:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    barcode_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    barcode_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="FIR Number:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    fir_no_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    fir_no_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Seized Items:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    seized_items_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    seized_items_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Undertaking Inspector:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    taken_by_whom_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    taken_by_whom_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Court Name:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    court_name_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    court_name_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="CNR Number:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    cnr_number_entry = tk.Entry(
        checkout_frame, background="#FFFFFF", font=textbox_font)
    cnr_number_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Check Out Date:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    checkout_date_entry = DateEntry(checkout_frame, font=textbox_font,
                                    width=12, background='darkblue', foreground='white', borderwidth=2)
    checkout_date_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Check Out Time:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")

    time_frame = tk.Frame(checkout_frame, bg="#f6f4f2")
    time_frame.pack(padx=10, pady=5, anchor="w")

    hour_var = tk.StringVar(time_frame, value='00')
    hour_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=hour_var, values=[
        str(i).zfill(2) for i in range(24)], state='readonly', width=5)

    minute_var = tk.StringVar(time_frame, value='00')
    minute_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=minute_var, values=[
        str(i).zfill(2) for i in range(60)], state='readonly', width=5)

    hour_menu.pack(side=tk.LEFT, pady=5)
    minute_menu.pack(side=tk.LEFT, padx=10, pady=5)

    button_font = ('Helvetica', 12)
    # Adjusted button sizes
    button_width = 20
    button_height = 2

    checkout_button = tk.Button(checkout_frame, text="Checkout Item",
                                background="#f6f4f2", command=checkouttocourt, font=button_font, width=button_width, height=button_height)
    checkout_button.pack(padx=10, side=tk.LEFT)

    autofill_button = tk.Button(checkout_frame, text="Autofill Details",
                                background="#f6f4f2", command=autofill_details, font=button_font, width=button_width, height=button_height)
    autofill_button.pack(padx=10, pady=5, side=tk.LEFT)

    # Back Button
    back_button = tk.Button(checkout_frame, text="Back",
                            background="#f6f4f2", command=go_back, font=button_font, width=button_width, height=button_height)
    back_button.pack(padx=10, pady=5, side=tk.LEFT)

    # Home Button
    home_button = tk.Button(checkout_frame, text="Home",
                            background="#f6f4f2", command=go_home, font=button_font, width=button_width, height=button_height)
    home_button.pack(padx=10, pady=5, side=tk.LEFT)

def go_back():
    checkout_destroyer()
    co.COpage(checkout_frame)

def go_home():
    checkout_destroyer()
    Homepage.open_homepage(checkout_frame)

def barcode_checker(barcode, checkout_date, checkout_time, taken_by_whom, seized_items, fir_no, court_name, cnr_number):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchall()
    conn.close()

    if not result:
        messagebox.showerror("Barcode not Found",
                             "Barcode doesn't exist in the database.")
        # Clear the input fields after showing the error
        barcode_entry.delete(0, tk.END)
        fir_no_entry.delete(0, tk.END)
        seized_items_entry.delete(0, tk.END)
        taken_by_whom_entry.delete(0, tk.END)
        checkout_date_entry.set_date(None)  # Clear the date entry
        court_name_entry.delete(0, tk.END)
        cnr_number_entry.delete(0, tk.END)
        return
    already_outornot(barcode, checkout_date, checkout_time,
                     taken_by_whom, seized_items, fir_no, court_name, cnr_number)
    # Clear the input fields after successful checkout
    barcode_entry.delete(0, tk.END)
    fir_no_entry.delete(0, tk.END)
    seized_items_entry.delete(0, tk.END)
    taken_by_whom_entry.delete(0, tk.END)
    checkout_date_entry.set_date(None)  # Clear the date entry
    court_name_entry.delete(0, tk.END)
    cnr_number_entry.delete(0, tk.END)

def already_outornot(barcode, checkout_date, checkout_time, taken_by_whom, seized_items, fir_no, court_name, cnr_number):
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_status FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] in ("malkhana", "Malkhana"):
        update_item_status(barcode, checkout_date, checkout_time,
                           taken_by_whom, seized_items, fir_no, court_name, cnr_number)
    else:
        messagebox.showerror("Item not found",
                             "Item is not present in Malkhana.")
        barcode_entry.delete(0, tk.END)
        fir_no_entry.delete(0, tk.END)
        seized_items_entry.delete(0, tk.END)
        taken_by_whom_entry.delete(0, tk.END)
        checkout_date_entry.set_date(None)
        court_name_entry.delete(0, tk.END)
        cnr_number_entry.delete(0, tk.END)
