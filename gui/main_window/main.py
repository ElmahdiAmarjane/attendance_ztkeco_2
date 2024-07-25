from pathlib import Path
from tkinter import (
    Toplevel,
    Frame,
    Canvas,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
from tkinter.font import Font
from controller import *
# from gui.main_window.dashboard.gui import Dashboard
from gui.main_window.Dashboard_.main import Dashboard
from gui.main_window.about.main import About
from gui.main_window.rooms.main import Rooms
from gui.main_window.guests.main import Guests
from .. import login
from pyzk.example.get_attendence import get_attendence
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def mainWindow():
    MainWindow()


class MainWindow(Toplevel):
    global user

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.title("Devsol - Attandance System managemant")

        self.geometry("1012x506")
        self.configure(bg="#173c5c")

        self.current_window = None
        #self.current_window_label = StringVar()

        self.canvas = Canvas(
            self,
            bg="#173c5c",
            height=506,
            width=1012,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(
            215, 0.0, 1012.0, 506.0, fill="#FFFFFF", outline=""
        )

        # Add a frame rectangle
        self.sidebar_indicator = Frame(self, background="#FFFFFF")

        self.sidebar_indicator.place(x=0, y=133, height=47, width=7)
 #########################################
    

        self.create_rounded_button(
            x=35.0, y=60.0, width=120.0, height=35.0, radius=10, text="Update Data", command=get_attendence
        )
    def create_rounded_button(self, x, y, width, height, radius, text, command):
        self.canvas.create_oval(x, y, x + radius, y + radius, fill="#8c8d8f", outline="")
        self.canvas.create_oval(x + width - radius, y, x + width, y + radius, fill="#8c8d8f", outline="")
        self.canvas.create_oval(x, y + height - radius, x + radius, y + height, fill="#8c8d8f", outline="")
        self.canvas.create_oval(x + width - radius, y + height - radius, x + width, y + height, fill="#8c8d8f", outline="")
        self.canvas.create_rectangle(x + radius / 2, y, x + width - radius / 2, y + height, fill="#8c8d8f", outline="")
        self.canvas.create_rectangle(x, y + radius / 2, x + width, y + height - radius / 2, fill="#8c8d8f", outline="")
        button = Button(
            self.canvas,
            text=text,
            borderwidth=0,
            highlightthickness=0,
            cursor='hand2',
            activebackground="#1a73e8",
            activeforeground="#ffffff",
            background="#8c8d8f",
            foreground="#ffffff",
            font=("Helvetica", 12, "bold"),
            command=command,
            relief="flat",
        )
        button.place(x=x + radius / 4, y=y + radius / 4, width=width - radius / 2, height=height - radius / 2)

 #########################################
        bold_font = Font(family="Helvetica", size=12, weight="bold")
        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.dashboard_btn = Button(
            self.canvas,
            text="Dashboard",
            borderwidth=1,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.dashboard_btn, "res"),
            cursor='hand2', activebackground="#173c5c",background="#173c5c",
            fg="white",
            relief="flat",
            font=bold_font,  # Set the font to the bold font
            anchor="w",  # Left justify the text
            padx=10  # Add padding to the left side of the text

        )
        self.dashboard_btn.place(x=7.0, y=133.0, width=208.0, height=47.0)

        button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.rooms_btn = Button(
            self.canvas,
            text="Add employee",
            borderwidth=1,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.rooms_btn, "roo"),
            cursor='hand2', activebackground="#173c5c",background="#173c5c",
            fg="white",
            relief="flat",
            font=bold_font,  # Set the font to the bold font
            anchor="w",  # Left justify the text
            padx=10  # Add padding to the left side of the text
        )
        self.rooms_btn.place(x=7.0, y=183.0, width=208.0, height=47.0)

        button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.guests_btn = Button(
            self.canvas,
            text="Employees",
            borderwidth=1,
            highlightthickness=0,
            command=lambda: self.handle_btn_press(self.guests_btn, "gue"),
            cursor='hand2', activebackground="#173c5c",background="#173c5c",
             fg="white",
            relief="flat",
            font=bold_font,  # Set the font to the bold font
            anchor="w",  # Left justify the text
            padx=10  # Add padding to the left side of the text
        )
        self.guests_btn.place(x=7.0, y=233.0, width=208.0, height=47.0)

        button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        # self.about_btn = Button(
        #     self.canvas,
        #     text="Employees",
        #     borderwidth=1,
        #     highlightthickness=0,
        #     command=lambda: self.handle_btn_press(self.about_btn, "abt"),
        #     cursor='hand2', activebackground="#173c5c",background="#173c5c",
        #      fg="white",
        #     relief="flat",
        #     font=bold_font , # Set the font to the bold font
        #     anchor="w",  # Left justify the text
        #     padx=10  # Add padding to the left side of the text
        # )
        # self.about_btn.place(x=7.0, y=233.0, width=208.0, height=47.0)

        button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        self.logout_btn = Button(
            self.canvas,
            image=button_image_5,
            borderwidth=1,
            highlightthickness=0,
            command=self.logout,
             fg="white",
            relief="flat",
            font=bold_font , # Set the font to the bold font
            anchor="w",  # Left justify the text
            padx=10  # Add padding to the left side of the text
        )
        self.logout_btn.place(x=0.0, y=441.0, width=215.0, height=47.0)

        # button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
        # self.reservations_btn = Button(
        #     self.canvas,
        #     text="Dashboard",
        #     borderwidth=1,
        #     highlightthickness=0,
        #     command=lambda: self.handle_btn_press(self.reservations_btn, "res"),
        #     cursor='hand2', activebackground="#173c5c", background="#173c5c",
        #      fg="white",
        #     relief="flat",
        #     font=bold_font , # Set the font to the bold font
        #     anchor="w",  # Left justify the text
        #     padx=10  # Add padding to the left side of the text
        # )
        # self.reservations_btn.place(x=7.0, y=233.0, width=208.0, height=47.0)

        self.heading = self.canvas.create_text(
            255.0,
            33.0,
            anchor="nw",
            text="Hello",
            fill="#173c5c",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_text(
            28.0,
            21.0,
            anchor="nw",
            text="Devsol",
            fill="#FFFFFF",
            font=("Montserrat Bold", 22 * -1),
        )

        self.canvas.create_text(
            844.0,
            43.0,
            anchor="nw",
            text="",
            fill="#808080",
            font=("Montserrat Bold", 16 * -1),
        )

        self.canvas.create_text(
            341.0,
            213.0,
            anchor="nw",
            text="(The screens below",
            fill="#5E95FF",
            font=("Montserrat Bold", 48 * -1),
        )

        self.canvas.create_text(
            420.0,
            272.0,
            anchor="nw",
            text="will come here)",
            fill="#5E95FF",
            font=("Montserrat Bold", 48 * -1),
        )

        # Loop through windows and place them
        self.windows = {
            # "dash": Dashboard(self),
            "roo": Rooms(self),
            "gue": Guests(self),
            "abt": About(self),
            "res": Dashboard(self),
        }

        self.handle_btn_press(self.dashboard_btn, "res")
        self.sidebar_indicator.place(x=0, y=133)

        self.current_window.place(x=215, y=72, width=1013.0, height=506.0)

        self.current_window.tkraise()
        self.resizable(False, False)
        self.mainloop()

    def place_sidebar_indicator(self):
        pass

    def logout(self):
        confirm = messagebox.askyesno(
            "Confirm log-out", "Do you really want to log out?"
        )
        if confirm == True:
            user = None
            self.destroy()
            login.gui.loginWindow()

    def handle_btn_press(self, caller, name):
        # Place the sidebar on respective button
        self.sidebar_indicator.place(x=0, y=caller.winfo_y())

        # Hide all screens
        for window in self.windows.values():
            window.place_forget()

        # Set ucrrent Window
        self.current_window = self.windows.get(name)

        # Show the screen of the button pressed
        self.windows[name].place(x=215, y=72, width=1013.0, height=506.0)

        # Handle label change
        current_name = self.windows.get(name)._name.split("!")[-1].capitalize()
        if current_name == 'Rooms':
            current_name = "Add New Employee"
        if current_name == 'Guests':
            current_name = "Employees"
        
        self.canvas.itemconfigure(self.heading, text=current_name)

    def handle_dashboard_refresh(self):
        # Recreate the dash window
        # self.windows["dash"] = Dashboard(self)
        None
    
