import tkinter as tk
import MalkhanaTable.checkout.checkoutCourt as coc
import home.Homepage as Homepage
import MalkhanaTable.checkout.checkoutpage as cof
import MalkhanaTable.MalkhanaPage as m
import Log.log as log
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry
import datetime
import logger as lu
import login.login as login

checkout_frame = None

def autofill_details():
    """Autofill FIR and Seized Items based on the barcode."""
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
        order_no_entry.delete(0, tk.END)
        fir_no_entry.insert(0, result[1])
        seized_items_entry.insert(0, result[2])
    else:
        messagebox.showerror("Error", "Barcode not found in the database.")

def update_item_status(barcode, fir_no, seized_items, taken_by_whom, checkout_date, checkout_time, order_no):
    """Update item status in the database and log the checkout activity."""
    try:
        # Update items table
        conn = sqlite3.connect('databases/items_in_malkhana.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET item_status='FSL' WHERE barcode = ?", (barcode,))
        conn.commit()
        conn.close()

        # Insert into fsl_records table
        conn = sqlite3.connect("databases/fsl_records.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS fsl_records (
            barcode TEXT,
            fir_no TEXT,
            seized_items TEXT,
            order_no INTEGER UNIQUE,
            checkout_date TEXT,
            checkout_time TEXT,
            taken_by_whom TEXT,
            checkin_date TEXT,
            checkin_time TEXT,
            examiner_name TEXT,
            fsl_report TEXT,
            entry_time TEXT
        );''')
        entry_time = datetime.datetime.now()
        cursor.execute("INSERT INTO fsl_records (barcode, fir_no, seized_items, order_no, checkout_date, checkout_time, taken_by_whom, entry_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (barcode, fir_no, seized_items, order_no, checkout_date, checkout_time, taken_by_whom, entry_time))
        conn.commit()
        conn.close()

        messagebox.showinfo("Successful", "Successfully checked out from Malkhana")
        log.update_logs(barcode, "Checked Out To FSL", checkout_date, checkout_time)
        activity = f"Item checked out to FSL barcode no: {barcode}"
        lu.log_activity(login.current_user, activity)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def checkout_destroyer():
    """Destroy the checkout frame if it exists."""
    global checkout_frame
    if checkout_frame is not None:
        checkout_frame.destroy()

def checkouttoFSL():
    """Handle the checkout to FSL process."""
    barcode = barcode_entry.get()
    fir_no = fir_no_entry.get()
    seized_items = seized_items_entry.get()
    taken_by_whom = taken_by_whom_entry.get()
    checkout_date = checkout_date_entry.get()
    checkout_time = f"{hour_var.get()}:{minute_var.get()}"
    order_no = order_no_entry.get()

    if not barcode or not fir_no or not seized_items or not taken_by_whom or not checkout_date or not checkout_time or not order_no:
        messagebox.showerror("Error", "All fields must be filled out to check out an item.")
        return

    barcode_checker(barcode, fir_no, seized_items, taken_by_whom, checkout_date, checkout_time, order_no)

def checkouttocourt_page():
    """Navigate to the Checkout to Court page."""
    global checkout_frame
    checkout_destroyer()
    coc.checkouttocourt_page(checkout_frame)

def checkouttoFSL_page(root):
    """Navigate to the Checkout to FSL page."""
    root.destroy()
    global checkout_frame, barcode_entry, fir_no_entry, seized_items_entry, taken_by_whom_entry, checkout_date_entry, hour_var, minute_var, order_no_entry
    checkout_destroyer()
    checkout_frame = tk.Frame(root.master)
    checkout_frame.master.title("Check Out to FSL")
    checkout_frame.pack(fill=tk.BOTH, expand=True)

    # Sidebar
    sidebar = tk.Frame(checkout_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Checkout to FSL", checkouttoFSL_page),
        ("Checkout to Court", checkouttocourt_page),
        ("Home", go_home),
        ("Back", go_back),
    ]

    for text, command in sidebar_buttons:
        if text == "Checkout to FSL":
            button = tk.Button(sidebar, text=text, background="#16a085", foreground="#ecf0f1", font=("Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        else:
            button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=("Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        button.pack(fill=tk.X, pady=5, padx=10)

    # Define fonts
    textbox_font = ('Helvetica', 12)
    font_style = ('Helvetica', 12)

    # Labels and Entry Fields
    tk.Label(checkout_frame, text="Barcode Number:", background="#f6f4f2", font=font_style).pack(padx=10, pady=5, anchor="w")
    barcode_entry = tk.Entry(checkout_frame, background="#FFFFFF", font=textbox_font)
    barcode_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="FIR Number:", background="#f6f4f2", font=font_style).pack(padx=10, pady=5, anchor="w")
    fir_no_entry = tk.Entry(checkout_frame, background="#FFFFFF", font=textbox_font)
    fir_no_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Seized Items:", background="#f6f4f2", font=font_style).pack(padx=10, pady=5, anchor="w")
    seized_items_entry = tk.Entry(checkout_frame, background="#FFFFFF", font=textbox_font)
    seized_items_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Undertaking Inspector:", background="#f6f4f2", font=font_style).pack(padx=10, pady=5, anchor="w")
    taken_by_whom_entry = tk.Entry(checkout_frame, background="#FFFFFF", font=textbox_font)
    taken_by_whom_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Check Out Date:", background="#f6f4f2", font=font_style).pack(padx=10, pady=5, anchor="w")
    checkout_date_entry = DateEntry(checkout_frame, font=textbox_font, width=12, background='darkblue', foreground='white', borderwidth=2)
    checkout_date_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(checkout_frame, text="Check Out Time:", background="#f6f4f2", font=font_style).pack(padx=10, pady=5, anchor="w")

    time_frame = tk.Frame(checkout_frame, bg="#f6f4f2")
    time_frame.pack(padx=10, pady=5, anchor="w")

    hour_var = tk.StringVar(time_frame, value='00')
    hour_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=hour_var, values=[str(i).zfill(2) for i in range(24)], state='readonly', width=5)
    minute_var = tk.StringVar(time_frame, value='00')
    minute_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=minute_var, values=[str(i).zfill(2) for i in range(60)], state='readonly', width=5)

    hour_menu.pack(side=tk.LEFT, pady=5)
    minute_menu.pack(side=tk.LEFT, padx=10, pady=5)

    tk.Label(checkout_frame, text="Order Number:", background="#f6f4f2", font=font_style).pack(padx=10, pady=5, anchor="w")
    order_no_entry = tk.Entry(checkout_frame, background="#FFFFFF", font=textbox_font)
    order_no_entry.pack(padx=10, pady=5, anchor="w")

    button_font = ('Helvetica', 12)
    button_width = 20
    button_height = 2

    # Checkout button
    checkout_button = tk.Button(checkout_frame, text="Checkout Item", background="#f6f4f2", command=checkouttoFSL, font=button_font, width=button_width, height=button_height)
    checkout_button.pack(padx=10, side=tk.LEFT)

    # Autofill button
    autofill_button = tk.Button(checkout_frame, text="Autofill Details", background="#f6f4f2", command=autofill_details, font=button_font, width=button_width, height=button_height)
    autofill_button.pack(padx=10, pady=5, side=tk.LEFT)

    # Back button
    back_button = tk.Button(checkout_frame, text="Back", background="#f6f4f2", command=go_back, font=button_font, width=button_width, height=button_height)
    back_button.pack(padx=10, pady=5, side=tk.LEFT)

    # Home button
    home_button = tk.Button(checkout_frame, text="Home", background="#f6f4f2", command=go_home, font=button_font, width=button_width, height=button_height)
    home_button.pack(padx=10, pady=5, side=tk.LEFT)

def go_back():
    """Navigate to the Checkout page."""
    checkout_destroyer()
    cof.COpage(checkout_frame)

def go_home():
    """Navigate to the Home page."""
    checkout_destroyer()
    Homepage.open_homepage(checkout_frame)

def barcode_checker(barcode, fir_no, seized_items, taken_by_whom, checkout_date, checkout_time, order_no):
    """Check if the barcode exists in the database and proceed with the checkout."""
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchall()
    conn.close()

    if not result:
        messagebox.showerror("Barcode Not Found!", "Barcode doesn't exist in the database.")
        clear_input_fields()
        return

    already_outornot(barcode, fir_no, seized_items, taken_by_whom, checkout_date, checkout_time, order_no)
    clear_input_fields()

def already_outornot(barcode, fir_no, seized_items, taken_by_whom, checkout_date, checkout_time, order_no):
    """Check if the item is already checked out and update its status if it's not."""
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT item_status FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0].lower() == "malkhana":
        update_item_status(barcode, fir_no, seized_items, taken_by_whom, checkout_date, checkout_time, order_no)
    else:
        messagebox.showerror("Item not found", "Item is not present in Malkhana.")
        clear_input_fields()

def clear_input_fields():
    """Clear all input fields."""
    barcode_entry.delete(0, tk.END)
    fir_no_entry.delete(0, tk.END)
    seized_items_entry.delete(0, tk.END)
    taken_by_whom_entry.delete(0, tk.END)
    checkout_date_entry.set_date(None)
    order_no_entry.delete(0, tk.END)
