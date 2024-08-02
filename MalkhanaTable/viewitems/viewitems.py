import math
import tkinter as tk
import sqlite3
from tkinter import messagebox
import main
from tkinter import ttk
import home.Homepage as homepage
import MalkhanaTable.MalkhanaPage as m
from PIL import Image, ImageTk
import login.login as login
import os
import MalkhanaTable.additems.additems as ai
import MalkhanaTable.checkout.checkoutpage as co
import MalkhanaTable.checkin.checkinpage as ci
import io
import logger as lu
import printt.print as p


viewitems_frame = None


def viewitems(prev_malkhana_frame):
    prev_malkhana_frame.destroy()
    global viewitems_frame, tree
    viewitems_frame = tk.Frame(prev_malkhana_frame.master)
    viewitems_frame.master.title("View Items")
    viewitems_frame.pack(fill=tk.BOTH, expand=True)

    sidebar = tk.Frame(viewitems_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Add Items", additemsclicked),
        ("View Items", None),
        ("Checkout Items", checkoutclicked),
        ("Checkin Items", checkinclicked),
        ("Back", go_back),
        ("Log Out", logoutclicked)
    ]

    for text, command in sidebar_buttons:
        if text == "View Items":
            button = tk.Button(sidebar, text=text, background="#16a085", foreground="#ecf0f1", font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        else:
            button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        button.pack(fill=tk.X, pady=5, padx=10)

    # Create a Treeview widget to display the data in a tabular format
    tree = ttk.Treeview(viewitems_frame)
    x_scrollbar = ttk.Scrollbar(tree, orient=tk.HORIZONTAL, command=tree.xview)

    # Configure the treeview to use the scrollbars
    tree.configure(xscrollcommand=x_scrollbar.set)

    # Define columns
    tree["columns"] = (
        "Barcode",
        "FIR Number",
        "Seized Items",
        "IPC Section",
        "Crime Location",
        "Crime Date",
        "Crime Time",
        "Crime Witness",
        "Crime Inspector",
        "Item Status",
        "Where Kept",
        "Item Description"
        # "attachments"
    )

    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)  # Hidden first column
    tree.column("Barcode", anchor=tk.W, width=80, stretch=tk.NO, minwidth=80)
    tree.column("FIR Number", anchor=tk.W,
                stretch=tk.NO, width=100)
    tree.column("Seized Items", anchor=tk.W,
                stretch=tk.NO, width=200)
    tree.column("IPC Section", anchor=tk.W,
                stretch=tk.NO, width=150)
    tree.column("Crime Location", anchor=tk.W,
                stretch=tk.NO, width=200)
    tree.column("Crime Date", anchor=tk.W,
                stretch=tk.NO, width=120)
    tree.column("Crime Time", anchor=tk.W,
                stretch=tk.NO, width=120)
    tree.column("Crime Witness", anchor=tk.W,
                stretch=tk.NO, width=200)
    tree.column("Crime Inspector", anchor=tk.W,
                stretch=tk.NO, width=150)
    tree.column("Item Status", anchor=tk.W,
                stretch=tk.NO, width=100)
    tree.column("Where Kept", anchor=tk.W,
                stretch=tk.NO, width=150)
    tree.column("Item Description", anchor=tk.W,
                stretch=tk.NO, width=700)

    # Create headings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Barcode", text="Barcode", anchor=tk.W)
    tree.heading("FIR Number", text="FIR Number", anchor=tk.W)
    tree.heading("Seized Items", text="Seized Items", anchor=tk.W)
    tree.heading("IPC Section", text="IPC Section", anchor=tk.W)
    tree.heading("Crime Location", text="Crime Location", anchor=tk.W)
    tree.heading("Crime Date", text="Crime Date", anchor=tk.W)
    tree.heading("Crime Time", text="Crime Time", anchor=tk.W)
    tree.heading("Crime Witness", text="Crime Witness", anchor=tk.W)
    tree.heading("Crime Inspector", text="Crime Inspector", anchor=tk.W)
    tree.heading("Item Status", text="Item Status", anchor=tk.W)
    tree.heading("Where Kept", text="Where Kept", anchor=tk.W)
    tree.heading("Item Description", text="Item Description", anchor=tk.W)

    # Add data to the treeview from the database
    try:
        # Connect to the database (or create if it doesn't exist)
        conn = sqlite3.connect('databases/items_in_malkhana.db')

        # Create a cursor to execute SQL commands
        cursor = conn.cursor()

        # Execute the SQL command to select all rows from the table
        cursor.execute('''SELECT barcode, fir_no, seized_items, ipc_section, crime_location, crime_date, crime_time, crime_witness, crime_inspector, item_status, where_kept,description_of_items
 FROM items ORDER BY entry_time DESC''')

        # Fetch all the rows and insert them into the treeview
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        # Commit the changes
        conn.commit()
        conn.close()

    except Exception as e:
        # Display error message if there's an issue with the database
        tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")

    # Get the height of the screen
    screen_height = prev_malkhana_frame.master.winfo_screenheight()

    # Set the height of the treeview to half of the screen height
    treeview_height = screen_height // 90

    # Pack the treeview with the specified height and other configurations
    tree.pack(fill=tk.BOTH, expand=True,
              side=tk.TOP, pady=(0, treeview_height))

    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)


# --------------------------------------------------------------------------------------------------------------------------------------

    current_page = 1
    entries_per_page = 40
    total_entries = 0
    data = []

    current_page_label = tk.Label(viewitems_frame, text="Page: 1")
    current_page_label.pack(side=tk.BOTTOM)

    total_pages_label = tk.Label(viewitems_frame, text="")
    total_pages_label.pack(side=tk.BOTTOM)

    def update_treeview(page_num):
        nonlocal current_page
        current_page = page_num

        total_pages = math.ceil(total_entries / entries_per_page)
        current_page_label.config(text=f"Page: {current_page}/{total_pages}")
        tree.delete(*tree.get_children())
        start_idx = (current_page - 1) * entries_per_page
        end_idx = start_idx + entries_per_page
        for row in data[start_idx:end_idx]:
            tree.insert("", tk.END, values=row)

    def show_all():
        nonlocal total_entries, data
        tree.delete(*tree.get_children())
        try:
            conn = sqlite3.connect("databases/items_in_malkhana.db")
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM items ORDER BY entry_time DESC''')
            data = cursor.fetchall()
            total_entries = len(data)
            update_treeview(current_page)
            conn.commit()
            conn.close()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")

    show_all()

    def go_to_previous_page():
        if current_page > 1:
            update_treeview(current_page - 1)

    def go_to_next_page():
        total_pages = math.ceil(total_entries / entries_per_page)
        if current_page < total_pages:
            update_treeview(current_page + 1)
            
    def apply_filters():
        selected_columns = []
        for column, var in checkbox_vars.items():
            if var.get() == 1:
                selected_columns.append(column)
        # Reconfigure treeview columns
        tree["displaycolumns"] = selected_columns

    # Function to create filter window
    def create_filter_window():
        filter_window = tk.Toplevel(viewitems_frame)
        filter_window.title("Select Filters")

        global checkbox_vars
        checkbox_vars = {}

        for idx, column in enumerate(tree["columns"]):
            var = tk.IntVar(value=1)
            checkbox_vars[column] = var
            cb = tk.Checkbutton(filter_window, text=column, variable=var)
            cb.grid(row=idx, column=0, sticky="w")

        apply_button = tk.Button(
            filter_window, text="Apply Filters", command=apply_filters)
        apply_button.grid(row=len(tree["columns"]), column=0, pady=5)

    # Search and filter row
    search_frame = tk.Frame(viewitems_frame)
    search_frame.pack(side=tk.BOTTOM, fill=tk.X)
    # Labels
    search_label = tk.Label(search_frame, text="Search Field:",
                            background="#FFFFFF", font=("Helvetica", 13))
    search_label.grid(row=1, column=0, padx=5, pady=5)

    # Combobox for selecting search field
    search_field_var = tk.StringVar(value="Barcode")
    search_field_menu = ttk.Combobox(search_frame, textvariable=search_field_var,
                                     values=tree["columns"], background="#FFFFFF", state='readonly', font=("Helvetica", 13))
    search_field_menu.grid(row=1, column=1, padx=5, pady=5)

    # Entry for search input
    search_entry = tk.Entry(search_frame, background="#D3D3D3",
                            textvariable=tk.StringVar(), font=("Helvetica", 13))
    search_entry.grid(row=1, column=2, padx=5, pady=5)

    # Buttons for actions
    search_button = tk.Button(search_frame, text="Search", background="#9a9a9a", command=lambda: search_items(
        tree, search_field_var.get(), search_entry.get()), font=("Helvetica", 13))
    search_button.grid(row=1, column=3, padx=15, pady=5)

    select_filter_button = tk.Button(search_frame, text="Select Filter",
                                     command=create_filter_window, background="#9a9a9a", font=("Helvetica", 13))
    select_filter_button.grid(row=2, column=2, padx=(0, 100), pady=5)

    show_all_btn = tk.Button(search_frame, text="Show All",
                             background="#9a9a9a", command=show_all, font=("Helvetica", 13))
    show_all_btn.grid(row=2, column=2, padx=(100, 0), pady=5)

    view_attachment_button = tk.Button(search_frame, background="#9a9a9a",
                                       text="View Attachment", command=view_attachment, font=("Helvetica", 13))
    view_attachment_button.grid(row=1, column=6, padx=15, pady=5)

    print_details_button = tk.Button(search_frame, background="#9a9a9a",
                                     text="Print Item Details", command=print_item, font=("Helvetica", 13))
    print_details_button.grid(row=1, column=7, padx=15, pady=5)

    # Previous Button
    previous_button = tk.Button(search_frame, text="Previous", command=go_to_previous_page,
                                background="#9a9a9a", font=("Helvetica", 13), width=12)
    previous_button.grid(row=1, column=8, padx=(180, 0), pady=5)

    # Next Button
    next_button = tk.Button(search_frame, text="Next", command=go_to_next_page,
                            background="#9a9a9a", font=("Helvetica", 13), width=12)
    next_button.grid(row=1, column=9, padx=10, pady=5)

    # Go Back Button
    go_back_button = tk.Button(search_frame, background="#9a9a9a",
                               text="Go Back", command=go_back, font=("Helvetica", 13), width=12)
    go_back_button.grid(row=1, column=10, pady=5)


def search_items(tree, search_field, search_text):
    # Clear previous search results
    for item in tree.get_children():
        tree.delete(item)

    # Convert the search_field back to the original column name (in English)

    search_field = convert_to_column(search_field)

    # Add data to the treeview from the database based on the search criteria
    try:
        conn = sqlite3.connect('databases/items_in_malkhana.db')
        cursor = conn.cursor()

        cursor.execute(f'''
            SELECT * FROM items
            WHERE {search_field} LIKE ?
        ''', ('%' + search_text + '%',))

        # Fetch the rows and insert them into the treeview
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        # Commit the changes
        conn.commit()
        conn.close()
    except Exception as e:
        # Display error message if there's an issue with the database
        tk.messagebox.showerror("Error", f"Error occurred: {str(e)}")


def convert_to_column(field_name):
    # Replace this with the appropriate mapping from Gujarati to English column names
    columnname = {
        "Barcode": "barcode",
        "FIR Number": "fir_no",
        "Seized Items": "seized_items",
        "IPC Section": "ipc_section",
        "Crime Location": "crime_location",
        "Crime Date": "crime_date",
        "Crime Time": "crime_time",
        "Crime Witness": "crime_witness",
        "Crime Inspector": "crime_inspector",
        "Item Status": "item_status",
        "Where Kept": "where_kept",
        "Item Description": "description_of_items"

    }

    return columnname.get(field_name, field_name)


def additemsclicked():
    viewitems_destroyer()
    ai.additems(viewitems_frame)


def checkoutclicked():
    viewitems_destroyer()
    co.COpage(viewitems_frame)


def checkinclicked():
    viewitems_destroyer()
    ci.CIpage(viewitems_frame)


def logoutclicked():
    activity = "LOG-OUT"
    lu.log_activity(login.current_user, activity)
    viewitems_destroyer()
    login.initloginpage(viewitems_frame)


def go_home():
    viewitems_destroyer()
    homepage.open_homepage(viewitems_frame)


def go_back():
    viewitems_destroyer()
    m.mkpage(viewitems_frame)


def viewitems_destroyer():
    if viewitems_frame is not None:
        viewitems_frame.destroy()


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

def view_attachment():
    selected_item = tree.focus()
    barcode = tree.item(selected_item, 'values')[0]

    conn = sqlite3.connect('databases/items_in_malkhana.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT attachments FROM items WHERE barcode = ?", (barcode,))
    attachment_data = cursor.fetchone()

    conn.close()

    if attachment_data:
        attachments = attachment_data[0]
        file_paths = attachments.split(';')

        # Create a new window to display the images
        image_window = tk.Toplevel(viewitems_frame)
        image_window.title("View Attachments")

        current_index = [0]  # Use a list to allow updates inside nested functions

        def update_image(index):
            try:
                image = Image.open(file_paths[index])
                photo = ImageTk.PhotoImage(image)

                image_label.config(image=photo)
                image_label.photo = photo  # Keep a reference to the PhotoImage object

                # Update the label text
                index_label.config(text=f"Image {index + 1} of {len(file_paths)}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")

        def prev_image():
            if current_index[0] > 0:
                current_index[0] -= 1
                update_image(current_index[0])

        def next_image():
            if current_index[0] < len(file_paths) - 1:
                current_index[0] += 1
                update_image(current_index[0])

        # Create a Frame to hold the image and buttons
        frame = tk.Frame(image_window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create an Image Label
        image_label = tk.Label(frame)
        image_label.pack()

        # Create navigation buttons
        nav_frame = tk.Frame(frame)
        nav_frame.pack(pady=10)

        prev_button = tk.Button(nav_frame, text="Previous", command=prev_image)
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = tk.Button(nav_frame, text="Next", command=next_image)
        next_button.pack(side=tk.LEFT, padx=5)

        # Create an Index Label
        index_label = tk.Label(frame, text="")
        index_label.pack(pady=5)

        # Show the first image
        update_image(current_index[0])

    else:
        messagebox.showinfo("Attachment Not Available!")



def print_item():
    selected_item = tree.focus()
    # Assuming the barcode is the first value in the row
    barcode = tree.item(selected_item, 'values')[0]

    p.print_details(barcode)
