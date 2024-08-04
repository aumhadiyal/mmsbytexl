import math
import tkinter as tk
import sqlite3
from tkinter import messagebox
import main
from tkinter import ttk
import home.Homepage as homepage
import MalkhanaTable.MalkhanaPage as mk
import login.login as login
import logger as lu
import CourtInfo.Courtpage as cp
import Log.log as l
import printt.print as p
from FSLInfo import FSLpage as f
import Log.log as l
import printt.print as p

court_frame = None


def view_court(prev_malkhana_frame):
    prev_malkhana_frame.destroy()
    global court_frame, tree
    court_destroyer()
    court_frame = tk.Frame(prev_malkhana_frame.master)
    court_frame.master.title("Court Info")
    court_frame.pack(fill=tk.BOTH, expand=True)

    # Get screen width and height
    screen_width = court_frame.winfo_screenwidth()
    screen_height = court_frame.winfo_screenheight()

    # Create a sidebar
    sidebar = tk.Frame(court_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Malkhana Info", mkpage),
        ("FSL Info", fsl),
        ("Court Info", None),
        ("Logs", log),
        ("Print", printDetails),
        ("Log Out", logoutclicked),
    ]

    for text, command in sidebar_buttons:
        if text == "Court Info":
            button = tk.Button(sidebar, text=text, background="#16a085", foreground="#ecf0f1", font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        else:
            button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        button.pack(fill=tk.X, pady=5, padx=10)

    # Create a Treeview widget to display the data in a tabular format
    tree = ttk.Treeview(court_frame)
    x_scrollbar = ttk.Scrollbar(tree, orient=tk.HORIZONTAL, command=tree.xview)

    # Configure the treeview to use the scrollbars
    tree.configure(xscrollcommand=x_scrollbar.set)

    # Define columns
    tree["columns"] = (
        "Barcode",
        "FIR Number",
        "Seized Items",
        "Checkout Date",
        "Checkout Time",
        "Undertaking Officer",
        "Court Name",
        "CNR Number",
        "Checkin Date",
        "Checkin Time",
        "Order Details"
    )

    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)  # Hidden first column
    tree.column("Barcode", anchor=tk.W, width=100,
                stretch=tk.YES, minwidth=100)
    tree.column("FIR Number", anchor=tk.W, width=100, stretch=tk.YES)
    tree.column("Seized Items", anchor=tk.W, width=150, stretch=tk.YES)
    tree.column("Checkout Date", anchor=tk.W, width=100, stretch=tk.YES)
    tree.column("Checkout Time", anchor=tk.W, width=100, stretch=tk.YES)
    tree.column("Undertaking Officer", anchor=tk.W, width=150, stretch=tk.YES)
    tree.column("Court Name", anchor=tk.W, width=100, stretch=tk.YES)
    tree.column("CNR Number", anchor=tk.W, width=100, stretch=tk.YES)
    tree.column("Checkin Date", anchor=tk.W, width=100, stretch=tk.YES)
    tree.column("Checkin Time", anchor=tk.W, width=100, stretch=tk.YES)
    tree.column("Order Details", anchor=tk.W, width=100, stretch=tk.YES)

    # Create headings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Barcode", text="Barcode", anchor=tk.W)
    tree.heading("FIR Number", text="FIR Number", anchor=tk.W)
    tree.heading("Seized Items", text="Seized Items", anchor=tk.W)
    tree.heading("Checkout Date", text="Checkout Date", anchor=tk.W)
    tree.heading("Checkout Time", text="Checkout Time", anchor=tk.W)
    tree.heading("Undertaking Officer",
                 text="Undertaking Officer", anchor=tk.W)
    tree.heading("Court Name",  text="Court Name", anchor=tk.W)
    tree.heading("CNR Number",  text="CNR Number", anchor=tk.W)    
    tree.heading("Checkin Date", text="Checkin Date", anchor=tk.W)
    tree.heading("Checkin Time", text="Checkin Time", anchor=tk.W)
    tree.heading("Order Details", text="Order Details", anchor=tk.W)

    # Add data to the treeview from the database
    try:
        # Connect to the database (or create if it doesn't exist)
        conn = sqlite3.connect('E:/Malkhana/databases/court_records.db')

        # Create a cursor to execute SQL commands
        cursor = conn.cursor()

        # Execute the SQL command to select all rows from the table
        cursor.execute(
            '''SELECT * FROM court_records ORDER BY entry_time DESC''')

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

    current_page_label = tk.Label(court_frame, text="Page: 1")
    current_page_label.pack(side=tk.BOTTOM)

    total_pages_label = tk.Label(court_frame, text="")
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
            conn = sqlite3.connect("E:/Malkhana/databases/court_records.db")
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT * FROM court_records ORDER BY entry_time DESC''')
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
# --------------------------------------------------------------------------------------------------------------------------------------------

    # Function to apply the selected filters

    def apply_filters():
        selected_columns = []
        for column, var in checkbox_vars.items():
            if var.get() == 1:
                selected_columns.append(column)
        # Reconfigure treeview columns
        tree["displaycolumns"] = selected_columns

    # Function to create filter window
    def create_filter_window():
        filter_window = tk.Toplevel(court_frame)
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
    search_frame = tk.Frame(court_frame)
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
        conn = sqlite3.connect('E:/Malkhana/databases/court_records.db')
        cursor = conn.cursor()

        cursor.execute(f'''
            SELECT * FROM court_records
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
    columnname = {
        "Barcode": "barcode",
        "FIR Number": "fir_no",
        "Seized Items": "seized_items",
        "Checkout Date": "checkout_date",
        "Checkout Time": "checkout_time",
        "Undertaking Officer": "taken_by_whom",
        "Court Name" : "court_name",
        "CNR Number":"cnr_number",
        "Checkin Date": "checkin_date",
        "Checkin Time": "checkin_time",
        "Order Details": "order_details",
    }

    return columnname.get(field_name, field_name)


def printDetails():
    global court_frame
    # Function to print details
    court_destroyer()
    p.print_details(court_frame)


def convert_to_column(field_name):
    # Function to convert field name to column name
    columnname = {
        "Barcode": "barcode",
        "FIR Number": "fir_no",
        "Seized Items": "seized_items",
        "Checkout Date": "checkout_date",
        "Checkout Time": "checkout_time",
        "Undertaking Officer": "taken_by_whom",
        "Court Name" : "court_name",
        "CNR Number":"cnr_number",        
        "Checkin Date": "checkin_date",
        "Checkin Time": "checkin_time",
        "Order Details": "order_details"
    }

    return columnname.get(field_name, field_name)


def court_destroyer():
    # Function to destroy the court frame
    if court_frame is not None:
        court_frame.destroy()


def go_back():
    # Function to go back to the homepage
    court_destroyer()
    homepage.open_homepage(court_frame)


def logoutclicked():
    # Function to handle logout
    lu.log_activity(login.current_user, "LOG-OUT")
    court_destroyer()
    login.initloginpage(court_frame)


def logoutclicked():
    lu.log_activity(login.current_user, "LOG-OUT")
    court_destroyer()
    login.initloginpage(court_frame)


def mkpage():
    court_destroyer()
    mk.mkpage(court_frame)


def fsl():
    court_destroyer()
    f.viewfsl(court_frame)


def log():
    court_destroyer()
    l.create_logs_page(court_frame)


def print_item():
    selected_item = tree.focus()
    # Assuming the barcode is the first value in the row
    barcode = tree.item(selected_item, 'values')[0]

    p.print_details(barcode)


def printDetails():
    global court_frame
    court_destroyer()
    p.printPage(court_frame)


import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import fitz  # PyMuPDF

def view_attachment():
    selected_item = tree.focus()
    cnr_number = tree.item(selected_item, 'values')[7]

    conn = sqlite3.connect('E:/Malkhana/databases/court_records.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT court_report_path FROM court_records WHERE cnr_number = ?", (cnr_number,))
    attachment_data = cursor.fetchone()

    conn.close()
    if not attachment_data:
        messagebox.showerror("Error", "No File Uploaded Yet.")
        return
    if attachment_data:
        file_path = attachment_data[0]

        # Create a new window to display the PDF
        pdf_window = tk.Toplevel(court_frame)
        pdf_window.title("View PDF")
        pdf_window.state('zoomed')

        pdf_document = None
        current_page = [0]  # Use a list to allow updates inside nested functions

        def open_pdf():
            nonlocal pdf_document
            try:
                pdf_document = fitz.open(file_path)
                if len(pdf_document) > 0:
                    update_page(current_page[0])
                else:
                    messagebox.showerror("Error", "No pages found in PDF.")
                    pdf_document.close()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open PDF file: {e}")

        def update_page(page_number):
            if not pdf_document:
                open_pdf()
            if pdf_document:
                try:
                    # Check if the page number is valid
                    if page_number < 0 or page_number >= len(pdf_document):
                        messagebox.showerror("Error", "Page number out of range.")
                        return
                    
                    page = pdf_document.load_page(page_number)
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    photo = ImageTk.PhotoImage(img)

                    page_label.config(image=photo)
                    page_label.photo = photo  # Keep a reference to the PhotoImage object

                    # Update the label text
                    index_label.config(text=f"Page {page_number + 1} of {len(pdf_document)}")

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open PDF page: {e}")

        def prev_page():
            if current_page[0] > 0:
                current_page[0] -= 1
                update_page(current_page[0])

        def next_page():
            if current_page[0] < len(pdf_document) - 1:
                current_page[0] += 1
                update_page(current_page[0])

        # Create a Frame to hold the PDF and buttons
        frame = tk.Frame(pdf_window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a Page Label
        page_label = tk.Label(frame)
        page_label.pack()

        # Create navigation buttons
        nav_frame = tk.Frame(frame)
        nav_frame.pack(pady=10)

        prev_button = tk.Button(nav_frame, text="Previous", command=prev_page)
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = tk.Button(nav_frame, text="Next", command=next_page)
        next_button.pack(side=tk.LEFT, padx=5)

        # Create an Index Label
        index_label = tk.Label(frame, text="")
        index_label.pack(pady=5)

        # Open the PDF and show the first page
        open_pdf()

    else:
        messagebox.showinfo("Attachment Not Available!")
