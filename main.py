import tkinter as tk
import login.login as l


def main():
    root = tk.Tk()
    root.state('zoomed')
    root.title("Main Window")

    main_frame = tk.Frame(root)
    main_frame.pack()
    # Call the function from the print module
    l.initloginpage(main_frame)

    root.mainloop()


if __name__ == "__main__":
    main()
