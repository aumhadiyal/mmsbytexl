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
viewfsl_frame = None


def viewfsl(prev_malkhana_frame):
    prev_malkhana_frame.destroy()
    global viewfsl_frame, tree
    fsl_destroyer()
    viewfsl_frame = tk.Frame(prev_malkhana_frame.master)
    viewfsl_frame.master.title("FSL Info")
    viewfsl_frame.pack(fill=tk.BOTH, expand=True)  # To occupy the whole screen

    # Get screen width and height
    screen_height = viewfsl_frame.winfo_screenheight()

    # Create a sidebar
    sidebar = tk.Frame(viewfsl_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Sidebar buttons
    sidebar_buttons = [
        ("Malkhana Info", mkpage),
        ("FSL Info", None),
        ("Court Info", court),
        ("Logs", log),
        ("Print", printDetails),
        ("Log Out", logoutclicked),
    ]

    for text, command in sidebar_buttons:
        if text == "FSL Info":
            button = tk.Button(sidebar, text=text, background="#16a085", foreground="#ecf0f1", font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        else:
            button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        button.pack(fill=tk.X, pady=5, padx=10)

    # Create a Treeview widget to display the data in a tabular format
    tree = ttk.Treeview(viewfsl_frame)
    x_scrollbar = ttk.Scrollbar(tree, orient=tk.HORIZONTAL, command=tree.xview)

    # Configure the treeview to use the scrollbars
    tree.configure(xscrollcommand=x_scrollbar.set)

    # Define columns
    tree["columns"] = (
        "Barcode",
        "FIR Number",
        "Seized Items",
        "FSL Order Number",
        "Checkout Date",
        "Checkout Time",
        "Undertaking Officer",
        "Checkin Date",
        "Checkin Time",
        "Examiner",
        "FSL Report")

    # Format columns
    tree.column("#0", width=0, stretch=tk.NO)  # Hidden first column
    tree.column("Barcode", anchor=tk.W, width=80, stretch=tk.NO, minwidth=80)
    tree.column("FIR Number", anchor=tk.W, stretch=tk.NO, width=100)
    tree.column("Seized Items", anchor=tk.W, stretch=tk.NO, width=200)
    tree.column("FSL Order Number", anchor=tk.W, stretch=tk.NO, width=150)
    tree.column("Checkout Date", anchor=tk.W, stretch=tk.NO, width=120)
    tree.column("Checkout Time", anchor=tk.W, stretch=tk.NO, width=120)
    tree.column("Undertaking Officer", anchor=tk.W, stretch=tk.NO, width=200)
    tree.column("Checkin Date", anchor=tk.W, stretch=tk.NO, width=120)
    tree.column("Checkin Time", anchor=tk.W, stretch=tk.NO, width=120)
    tree.column("Examiner", anchor=tk.W, stretch=tk.NO, width=100)
    tree.column("FSL Report", anchor=tk.W, stretch=tk.NO, width=650)

    # Create headings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Barcode", text="Barcode", anchor=tk.W)
    tree.heading("FIR Number", text="FIR Number", anchor=tk.W)
    tree.heading("Seized Items", text="Seized Items", anchor=tk.W)
    tree.heading("FSL Order Number", text="FSL Order Number", anchor=tk.W)
    tree.heading("Checkout Date", text="Checkout Date", anchor=tk.W)
    tree.heading("Checkout Time", text="Checkout Time", anchor=tk.W)
    tree.heading("Undertaking Officer",
                 text="Undertaking Officer", anchor=tk.W)
    tree.heading("Checkin Date", text="Checkin Date", anchor=tk.W)
    tree.heading("Checkin Time", text="Checkin Time", anchor=tk.W)
    tree.heading("Examiner", text="Examiner", anchor=tk.W)
    tree.heading("FSL Report", text="FSL Report", anchor=tk.W)
    # Add data to the treeview from the database
    try:
        # Connect to the database (or create if it doesn't exist)
        conn = sqlite3.connect('databases/fsl_records.db')

        # Create a cursor to execute SQL commands
        cursor = conn.cursor()

        # Execute the SQL command to select all rows from the table
        cursor.execute('''SELECT barcode, fir_no, seized_items, order_no, checkout_date,checkout_time,taken_by_whom,checkin_date,checkin_time,examiner_name,fsl_report
 FROM fsl_records ORDER BY entry_time DESC''')

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

    current_page_label = tk.Label(viewfsl_frame, text="Page: 1")
    current_page_label.pack(side=tk.BOTTOM)

    total_pages_label = tk.Label(viewfsl_frame, text="")
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
            conn = sqlite3.connect("databases/fsl_records.db")
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT * FROM fsl_records ORDER BY entry_time DESC''')
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
        filter_window = tk.Toplevel(viewfsl_frame)
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
    search_frame = tk.Frame(viewfsl_frame)
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
        conn = sqlite3.connect('databases/fsl_records.db')
        cursor = conn.cursor()

        cursor.execute(f'''
            SELECT * FROM fsl_records
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
        "FIR Number": "fir_number",
        "Seized Items": "seized_items",
        "FSL Order Number": "order_no",
        "Checkout Date": "checkout_date",
        "Checkout Time": "checkout_time",
        "Undertaking Officer": "taken_by_whom",
        "Checkin Date": "checkin_date",
        "Checkin Tiame": "checkin_time",
        "Examiner": "examiner_name",
        "FSL Report": "fsl_report"
    }

    return columnname.get(field_name, field_name)


def fsl_destroyer():
    if viewfsl_frame is not None:
        viewfsl_frame.destroy()


def go_back():
    fsl_destroyer()
    homepage.open_homepage(viewfsl_frame)


def go_home():
    fsl_destroyer()
    homepage.open_homepage(viewfsl_frame)


def logoutclicked():
    lu.log_activity(login.current_user, "LOG-OUT")
    fsl_destroyer()
    login.initloginpage(viewfsl_frame)


def mkpage():
    fsl_destroyer()
    mk.mkpage(viewfsl_frame)


def court():
    fsl_destroyer()
    cp.view_court(viewfsl_frame)


def log():
    fsl_destroyer()
    l.create_logs_page(viewfsl_frame)


def print_item():
    selected_item = tree.focus()
    # Assuming the barcode is the first value in the row
    barcode = tree.item(selected_item, 'values')[0]

    p.print_details(barcode)


def printDetails():
    global viewfsl_frame
    fsl_destroyer()
    p.printPage(viewfsl_frame)
