import tkinter as tk
import login.login as l
import logger as lu
def on_closing():
    lu.log_activity(l.current_user, "LOG-OUT")
    root.destroy()

def main():
    global root
    root = tk.Tk()
    root.state('zoomed')
    root.title("Main Window")

    main_frame = tk.Frame(root)
    main_frame.pack()
    # Call the function from the print module
    l.initloginpage(main_frame)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
