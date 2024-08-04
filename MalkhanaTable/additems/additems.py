import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
import datetime
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import io
import logger as lu
import MalkhanaTable.viewitems.viewitems as vi
import home.Homepage as Homepage
import MalkhanaTable.MalkhanaPage as m
import random
import string
import login.login as login
import MalkhanaTable.checkout.checkoutpage as co
import MalkhanaTable.checkin.checkinpage as ci

additems_frame = None
file_path = None
barcode_image_label = None  # For displaying the barcode image

def generate_unique_barcode(fir_no):
    if not fir_no:
        return None

    # Connect to the database
    conn = sqlite3.connect('E:/Malkhana/databases/items_in_malkhana.db')
    cursor = conn.cursor()

    while True:
        random_suffix = random.randint(100000, 999999)
        barcode = f"{fir_no}-{random_suffix}"
        cursor.execute("SELECT COUNT(*) FROM items WHERE barcode = ?", (barcode,))
        count = cursor.fetchone()[0]

        if count == 0:
            break

    conn.close()
    return barcode

def generate_barcode_image(barcode_number):
    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(barcode_number, writer=ImageWriter())
    barcode_image = barcode_instance.render()
    
    with io.BytesIO() as buf:
        barcode_image.save(buf, format='PNG')
        img_data = buf.getvalue()
    
    img = Image.open(io.BytesIO(img_data))
    img = ImageTk.PhotoImage(img)
    
    return img

def generate_barcode():
    fir_no = fir_no_entry.get()
    if not fir_no:
        messagebox.showerror("Error", "FIR Number must be entered to generate a barcode.")
        return
    
    barcode_number = generate_unique_barcode(fir_no)
    barcode_entry.config(state=tk.NORMAL)
    barcode_entry.delete(0, tk.END)
    barcode_entry.insert(0, barcode_number)
    barcode_entry.config(state=tk.DISABLED)
    
    barcode_img = generate_barcode_image(barcode_number)
    if barcode_image_label:
        barcode_image_label.config(image=barcode_img)
        barcode_image_label.image = barcode_img

def additems(prev_malkhana_frame):
    prev_malkhana_frame.destroy()

    global additems_frame, barcode_entry, fir_no_entry, seized_items_entry, ipc_section_entry, crime_location_entry, crime_date_entry, hour_var, minute_var, crime_witness_entry, crime_inspector_entry, where_kept_entry, description_of_items_entry, barcode_image_label
    additems_frame = tk.Frame(prev_malkhana_frame.master)
    additems_frame.master.title("Add Items")
    additems_frame.pack(fill=tk.BOTH, expand=True)

    # Sidebar
    sidebar = tk.Frame(additems_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons 
    sidebar_buttons = [
        ("Add Items", None),  # None as a placeholder for the command
        ("View Items", viewitemsclicked),
        ("Checkout Items", checkoutclicked),
        ("Checkin Items", checkinclicked),
        ("Back", go_back),
        ("Log Out", logoutclicked)
    ]

    for text, command in sidebar_buttons:
        button = tk.Button(sidebar, text=text, background="#34495e" if command else "#16a085", 
                           foreground="#ecf0f1", command=command, font=("Helvetica", 12), 
                           width=20, height=2, relief=tk.FLAT)
        button.pack(fill=tk.X, pady=5, padx=10)

    # Create a Canvas widget for scrolling
    canvas = tk.Canvas(additems_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a vertical scrollbar
    y_scrollbar = ttk.Scrollbar(additems_frame, orient=tk.VERTICAL, command=canvas.yview)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a frame inside the canvas for content
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=y_scrollbar.set)

    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", update_scrollregion)

    # Define fonts
    textbox_font = ('Helvetica', 12)
    font_style = ('Helvetica', 12)

    # Container for barcode number and image
    barcode_frame = tk.Frame(content_frame)
    barcode_frame.pack(padx=10, pady=5, anchor="w", fill=tk.X)

    tk.Label(barcode_frame, text="Barcode Number:", font=font_style).pack(
        padx=10, pady=5, anchor="w")

    # Container for barcode entry and button
    barcode_container = tk.Frame(barcode_frame, bg="#f6f4f2")
    barcode_container.pack(padx=10, pady=5, anchor="w")

    barcode_entry = tk.Entry(barcode_container, background="#FFFFFF", font=textbox_font, state=tk.DISABLED, width=20)
    barcode_entry.pack(side=tk.LEFT, padx=5)

    generate_barcode_button = tk.Button(barcode_container, text="Generate Barcode", background="#f6f4f2", 
                                        command=generate_barcode, font=font_style, width=20)
    generate_barcode_button.pack(side=tk.LEFT, padx=5)

    barcode_image_label = tk.Label(barcode_frame, bg="#f6f4f2")
    barcode_image_label.pack(side=tk.LEFT, padx=10)

    # Labels and Entry Fields
    labels_and_entries = [
        ("FIR Number:", "fir_no_entry"),
        ("Seized Items:", "seized_items_entry"),
        ("IPC Section:", "ipc_section_entry"),
        ("Crime Location:", "crime_location_entry"),
        ("Crime Witnesses:", "crime_witness_entry"),
        ("Crime Inspector:", "crime_inspector_entry"),
        ("Where Kept:", "where_kept_entry"),
        ("Description of Item:", "description_of_items_entry")
    ]

    for label_text, entry_var in labels_and_entries:
        tk.Label(content_frame, text=label_text, background="#f6f4f2", font=font_style).pack(
            padx=10, pady=5, anchor="w")
        entry = tk.Entry(content_frame, background="#FFFFFF", font=textbox_font)
        entry.pack(padx=10, pady=5, anchor="w")
        globals()[entry_var] = entry

    # Crime Date and Time
    tk.Label(content_frame, text="Crime Date:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")
    crime_date_entry = DateEntry(content_frame, font=textbox_font,
                                 width=12, background='darkblue', foreground='white', borderwidth=2)
    crime_date_entry.pack(padx=10, pady=5, anchor="w")

    tk.Label(content_frame, text="Crime Time:", background="#f6f4f2", font=font_style).pack(
        padx=10, pady=5, anchor="w")

    time_frame = tk.Frame(content_frame, bg="#f6f4f2")
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
    button_width = 20
    button_height = 2

    # Add Attachment Button
    add_attachment_button = tk.Button(content_frame, text="Add Attachment", background="#f6f4f2", 
                                      command=browse_file, font=button_font, width=button_width, height=button_height)
    add_attachment_button.pack(padx=10, pady=5, anchor="w")

    # Add Item Button
    add_item_button = tk.Button(content_frame, text="Add Item", background="#f6f4f2", 
                                command=insert_data, font=button_font, width=button_width, height=button_height)
    add_item_button.pack(padx=10, pady=5, side=tk.LEFT)

    # Back Button
    back_button = tk.Button(content_frame, text="Back", background="#f6f4f2", 
                            command=go_back, font=button_font, width=button_width, height=button_height)
    back_button.pack(padx=10, pady=5, side=tk.LEFT)

    # Home Button
    home_button = tk.Button(content_frame, text="Home", background="#f6f4f2", 
                            command=go_home, font=button_font, width=button_width, height=button_height)
    home_button.pack(padx=10, pady=5, side=tk.LEFT)

    # Logout Button
    logout = tk.Button(content_frame, text="Log Out", background="#f6f4f2", 
                       command=logoutclicked, font=button_font, width=button_width, height=button_height)
    logout.pack(padx=10, pady=5, side=tk.LEFT)

def insert_data():
    global barcodee, fir_no_entry, seized_items_entry, ipc_section_entry, crime_location_entry, crime_date_entry, hour_var, minute_var, crime_witness_entry, crime_inspector_entry, where_kept_entry, description_of_items_entry
    fir_no = fir_no_entry.get()
    seized_items = seized_items_entry.get()
    ipc_section = ipc_section_entry.get()
    crime_location = crime_location_entry.get()
    crime_date = crime_date_entry.get()
    crime_witness = crime_witness_entry.get()
    crime_inspector = crime_inspector_entry.get()
    where_kept = where_kept_entry.get()
    description_of_items = description_of_items_entry.get()

    crime_hour = int(hour_var.get())
    crime_minute = int(minute_var.get())
    crime_time = f"{crime_hour:02d}:{crime_minute:02d}"

    if not fir_no or not seized_items or not ipc_section or not crime_location or not crime_date or not crime_witness or not crime_inspector or not where_kept or not description_of_items:
        messagebox.showerror("Error", "All fields must be filled out to add an item.")
        return
    
    if not barcodee:
        messagebox.showerror("Error", "A barcode must be generated to add an item.")
        return

    try:
        conn = sqlite3.connect('E:/Malkhana/databases/items_in_malkhana.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                            barcode INTEGER PRIMARY KEY,
                            fir_no TEXT,
                            seized_items TEXT,
                            ipc_section TEXT,
                            crime_location TEXT,
                            crime_date TEXT,
                            crime_time TEXT,
                            crime_witness TEXT,
                            crime_inspector TEXT,
                            item_status TEXT,
                            where_kept TEXT,
                            description_of_items TEXT,
                            entry_time TEXT,
                            attachments TEXT
                        );''')

        entry_time = datetime.datetime.now()
        item_status = "MALKHANA"

        cursor.execute('''INSERT INTO items (barcode, fir_no, seized_items, ipc_section, 
                          crime_location, crime_date, crime_time, crime_witness, 
                          crime_inspector, item_status, where_kept, description_of_items, entry_time, attachments) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (barcodee, fir_no, seized_items, ipc_section, crime_location, crime_date,
                        crime_time, crime_witness, crime_inspector, item_status, where_kept, description_of_items, entry_time, file_entry))

        conn.commit()
        conn.close()
        activity = "\nAdded item barcode no: " + str(barcodee)
        lu.log_activity(login.current_user, activity)

        # Clear the entry fields
        barcode_entry.config(state=tk.NORMAL)
        barcode_entry.delete(0, tk.END)
        barcode_entry.config(state=tk.DISABLED)
        fir_no_entry.delete(0, tk.END)
        seized_items_entry.delete(0, tk.END)
        ipc_section_entry.delete(0, tk.END)
        crime_location_entry.delete(0, tk.END)
        crime_date_entry.delete(0, tk.END)
        crime_witness_entry.delete(0, tk.END)
        crime_inspector_entry.delete(0, tk.END)
        where_kept_entry.delete(0, tk.END)
        description_of_items_entry.delete(0, tk.END)

        messagebox.showinfo("Successful", "Item Stored Successfully!" + activity)

    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {str(e)}")

def browse_file():
    global file_paths, file_entry

    file_paths = filedialog.askopenfilenames()
    if file_paths:
        file_entry = ';'.join(file_paths)
        messagebox.showinfo("Files Selected", "Selected files: \n" + "\n".join(file_paths))

def go_back():
    # Logic to go back to the previous page
    pass

def go_home():
    # Logic to go to the home page
    pass

def logoutclicked():
    # Logic to handle logout
    pass

def viewitemsclicked():
    # Logic to handle view items
    pass

def checkoutclicked():
    # Logic to handle checkout items
    pass

def checkinclicked():
    # Logic to handle checkin items
    pass

    additems_destroyer()
    m.mkpage(additems_frame)


def go_home():
    additems_destroyer()
    Homepage.open_homepage(additems_frame)


def viewitemsclicked():
    additems_destroyer()
    vi.viewitems(additems_frame)


def checkoutclicked():
    additems_destroyer()
    co.COpage(additems_frame)


def checkinclicked():
    additems_destroyer()
    ci.CIpage(additems_frame)


def logoutclicked():
    activity = "LOG-OUT"
    lu.log_activity(login.current_user, activity)
    additems_destroyer()
    login.initloginpage(additems_frame)


def additems_destroyer():
    if additems_frame is not None:
        additems_frame.destroy()
