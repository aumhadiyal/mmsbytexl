import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime

import MalkhanaTable.additems.additems as a
import home.Homepage as Homepage
import Log.log as log
import MalkhanaTable.checkin.checkinpage as cp
import MalkhanaTable.checkin.checkinFromFSL as cif
import login.login as login
import logger as lu

court_checkin_frame = None

def update_item_status(barcode, checkin_date, checkin_time, order_details):
    if not order_details:
        messagebox.showerror("Fill up the Order Details.")
        
    """Update item status in the database."""
    try:
        # Update items table
        conn = sqlite3.connect('databases/items_in_malkhana.db')
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE items SET item_status='malkhana' WHERE barcode = ?", (barcode,))
        conn.commit()
        conn.close()

        # Update court_records table
        conn = sqlite3.connect("databases/court_records.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE court_records SET checkin_date = ?, checkin_time = ?, order_details = ? WHERE barcode = ?",
                       (checkin_date, checkin_time, order_details, barcode))
        conn.commit()
        conn.close()

        # Log the activity
        log.update_logs(barcode, "Checked In From Court", checkin_date, checkin_time)
        activity = f"Item checked in from Court barcode no: {barcode}"
        lu.log_activity(login.current_user, activity)

        messagebox.showinfo("Successful", "Successfully entered into Malkhana")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def checkin():
    """Handle the check-in process."""
    barcode = barcode_entry.get()
    checkin_time = f"{hour_var.get()}:{minute_var.get()}"
    checkin_date = checkin_date_entry.get_date()
    order_details = order_details_entry.get("1.0", "end-1c")
    
    if not barcode or not checkin_time or not checkin_date or not order_details:
                messagebox.showerror("Error", "All fields must be filled out to check in an item.")
                return
    barcode_checker(barcode, checkin_date, checkin_time, order_details)

    # Clear the input fields after check-in
    barcode_entry.delete(0, tk.END)
    checkin_date_entry.set_date(None)  # Clear the date entry
    order_details_entry.delete("1.0", tk.END)

def checkinfromfsl():
    """Navigate to Checkin from FSL page."""
    global court_checkin_frame
    court_checkin_destroyer()
    cif.checkinfromfsl(court_checkin_frame)

def checkinfromcourt(root):
    """Navigate to Checkin from Court page."""
    root.destroy()
    global court_checkin_frame, barcode_entry, checkin_date_entry, hour_var, minute_var, order_details_entry

    court_checkin_destroyer()
    court_checkin_frame = tk.Frame(root.master)
    court_checkin_frame.master.title("Checkin From Court")
    court_checkin_frame.pack(fill=tk.BOTH, expand=True)

    # Sidebar
    sidebar = tk.Frame(court_checkin_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Checkin From FSL", checkinfromfsl),
        ("Checkin From Court", None),
        ("Home", go_home),
        ("Back", go_back),
    ]

    for text, command in sidebar_buttons:
        if text == "Checkin From Court":
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
    tk.Label(court_checkin_frame, text="Barcode Number:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    barcode_entry = tk.Entry(court_checkin_frame, background="#FFFFFF", font=textbox_font)
    barcode_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(court_checkin_frame, text="Check In Date:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    date_frame = tk.Frame(court_checkin_frame, bg="#f6f4f2")
    date_frame.pack(padx=10, pady=5, anchor="w")
    checkin_date_entry = DateEntry(date_frame, font=textbox_font, width=12, background='darkblue', foreground='white', borderwidth=2)
    checkin_date_entry.pack(side=tk.LEFT, padx=5, pady=5)

    tk.Label(court_checkin_frame, text="Check In Time:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    time_frame = tk.Frame(court_checkin_frame, bg="#f6f4f2")
    time_frame.pack(padx=10, pady=5, anchor="w")
    hour_var = tk.StringVar(time_frame, value='00')
    hour_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=hour_var, values=[str(i).zfill(2) for i in range(24)], state='readonly', width=5)
    minute_var = tk.StringVar(time_frame, value='00')
    minute_menu = ttk.Combobox(time_frame, font=textbox_font, textvariable=minute_var, values=[str(i).zfill(2) for i in range(60)], state='readonly', width=5)
    hour_menu.pack(side=tk.LEFT, pady=5)
    minute_menu.pack(side=tk.LEFT, padx=10, pady=5)

    tk.Label(court_checkin_frame, text="Order Details:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    order_details_entry = tk.Text(court_checkin_frame, height=5, background="#FFFFFF", font=textbox_font)
    order_details_entry.pack(padx=10, pady=5, anchor="w")

    # Check-in button
    button_font = ('Helvetica', 12)
    button_width = 20
    button_height = 2
    checkin_button = tk.Button(court_checkin_frame, text="Check In", background="#f6f4f2", command=checkin, font=button_font, width=button_width, height=button_height)
    checkin_button.pack(padx=10, pady=5, anchor="w")

    # Back and Home buttons
    back_button = tk.Button(court_checkin_frame, text="Back", background="#f6f4f2", command=go_back, font=button_font, width=button_width, height=button_height)
    back_button.pack(padx=10, pady=5, anchor="w")
    home_button = tk.Button(court_checkin_frame, text="Home", background="#f6f4f2", command=go_home, font=button_font, width=button_width, height=button_height)
    home_button.pack(padx=10, pady=5, anchor="w")

def go_home():
    """Navigate to the home page."""
    court_checkin_destroyer()
    Homepage.open_homepage(court_checkin_frame)

def go_back():
    """Navigate to the previous page."""
    court_checkin_destroyer()
    cp.CIpage(court_checkin_frame)

def court_checkin_destroyer():
    """Destroy the court check-in frame if it exists."""
    if court_checkin_frame is not None:
        court_checkin_frame.destroy()

def barcode_checker(barcode, checkin_date, checkin_time, order_details):
    """Check if the barcode exists in the database."""
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchall()
    conn.close()

    if not result:
        messagebox.showerror("Barcode Not Found", "Barcode Entered Is Not Found In The Database.")
        barcode_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)  # Clear the date entry
        order_details_entry.delete("1.0", tk.END)
    else:
        already_in_or_not(barcode, checkin_date, checkin_time, order_details)

def already_in_or_not(barcode, checkin_date, checkin_time, order_details):
    """Check if the item is already in Malkhana/FSL."""
    conn = sqlite3.connect("databases/items_in_malkhana.db")
    cursor = conn.cursor()
    cursor.execute("SELECT item_status FROM items WHERE barcode = ?", (barcode,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] in ("court", "Court"):
        update_item_status(barcode, checkin_date, checkin_time, order_details)
    else:
        messagebox.showerror("Item Exists In Malkhana/FSL", "Item Already Exists In Malkhana/FSL.")
        barcode_entry.delete(0, tk.END)
        checkin_date_entry.set_date(None)  # Clear the date entry
        order_details_entry.delete("1.0", tk.END)
