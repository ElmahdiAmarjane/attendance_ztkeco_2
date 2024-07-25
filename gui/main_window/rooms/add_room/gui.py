# from pathlib import Path
# from tkinter import (
#     Frame,
#     Canvas,
#     Entry,
#     StringVar,
#     Button,
#     PhotoImage,
#     Toplevel,
#     Tk,
#     messagebox,
#     DISABLED,
#     NORMAL,
# )
# import controller as db_controller

# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path("./assets")

# def relative_to_assets(path: str) -> Path:
#     return ASSETS_PATH / Path(path)

# def add_rooms():
#     AddRooms()

# class AddRooms(Frame):
#     def __init__(self, parent, controller=None, *args, **kwargs):
#         Frame.__init__(self, parent, *args, **kwargs)
#         self.parent = parent
#         self.controller = controller
#         self.data = {"username": StringVar(), "telephone": StringVar()}
#         self.message = None  # Initialize the message attribute
#         self.configure(bg="#FFFFFF")

#         self.canvas = Canvas(
#             self,
#             bg="#FFFFFF",
#             height=432,
#             width=797,
#             bd=0,
#             highlightthickness=0,
#             relief="ridge",
#         )
#         self.canvas.place(x=0, y=0)

#         self.process_image = PhotoImage(file=relative_to_assets("process_image.png"))
#         self.success_image = PhotoImage(file=relative_to_assets("success_image.png"))

#         self.process_image_id = None
#         self.success_image_id = None

#         self.image_image_1 = PhotoImage(file=relative_to_assets("image_2.png"))
#         image_1 = self.canvas.create_image(258.0, 153.0, image=self.image_image_1)

#         self.canvas.create_text(
#             52.0,
#             128.0,
#             anchor="nw",
#             text="Username",
#             fill="#5E95FF",
#             font=("Montserrat Bold", 14 * -1),
#         )

#         self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_2.png"))
#         entry_1 = Entry(
#             self,
#             textvariable=self.data["username"],
#             bd=0,
#             bg="#EFEFEF",
#             highlightthickness=0,
#             font=("Montserrat Bold", 18 * -1),
#             foreground="#777777",
#         )
#         entry_1.place(x=52.0, y=153.0, width=179.0, height=22.0)

#         self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
#         image_2 = self.canvas.create_image(258.0, 259.0, image=self.image_image_2)

#         self.canvas.create_text(
#             52.0,
#             234.0,
#             anchor="nw",
#             text="Telephone",
#             fill="#5E95FF",
#             font=("Montserrat Bold", 14 * -1),
#         )

#         self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
#         entry_2 = Entry(
#             self,
#             textvariable=self.data["telephone"],
#             bd=0,
#             bg="#EFEFEF",
#             highlightthickness=0,
#             font=("Montserrat Bold", 18 * -1),
#             foreground="#777777",
#         )
#         entry_2.place(x=52.0, y=259.0, width=411.0, height=22.0)

#         self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
#         button_1 = Button(
#             self,
#             image=self.button_image_1,
#             borderwidth=0,
#             highlightthickness=0,
#             command=self.save,
#             relief="flat",
#         )
#         button_1.place(x=164.0, y=322.0, width=190.0, height=48.0)

#         self.message_text_id = self.canvas.create_text(
#             181.0,
#             58.0,
#             anchor="nw",
#             text="",  # Initialize with empty text
#             fill="#5E95FF",
#             font=("Montserrat Bold", 26 * -1),
#         )

#         self.canvas.create_rectangle(
#             515.0, 59.0, 517.0, 370.0, fill="#EFEFEF", outline=""
#         )

#     def save(self):
#         # Disable all widgets in the main window
#         self.disable_widgets(self.parent)

#         # Show process image
#         self.show_process_image()
#         self.update()  # Ensure the canvas updates immediately

#         # Simulate saving operation
#         success = db_controller.create_new_employee(self.data["username"].get(), self.data["telephone"].get())

#         # Remove process image and show success image
#         self.canvas.after(500, lambda: self.show_success_image() if success else self.hide_process_image())

#         # Re-enable the window after operation completes
#         self.after(2500, self.enable_widgets)  # Adjust timing as needed

#     def show_process_image(self):
#         if self.process_image_id:
#             self.canvas.delete(self.process_image_id)
#         self.process_image_id = self.canvas.create_image(397, 216, image=self.process_image)

#     def show_success_image(self):
#         if self.process_image_id:
#             self.canvas.delete(self.process_image_id)
#         self.success_image_id = self.canvas.create_image(397, 216, image=self.success_image)
#         self.after(2000, self.hide_success_image)  # Hide success image after 2 seconds

#     def hide_success_image(self):
#         if self.success_image_id:
#             self.canvas.delete(self.success_image_id)

#     def update_message_text(self):
#         if self.message is not None:
#             self.canvas.itemconfig(self.message_text_id, text=self.message)
#         else:
#             self.canvas.itemconfig(self.message_text_id, text="")

#     def disable_widgets(self, widget):
#         # Disable all child widgets
#         for child in widget.winfo_children():
#             if isinstance(child, (Button, Entry, Canvas)):
#                 child.config(state=DISABLED)
#             self.disable_widgets(child)  # Recursively disable child widgets

#     def enable_widgets(self):
#         # Enable all child widgets in the main window
#         self.enable_widgets_recursive(self.parent)

#     def enable_widgets_recursive(self, widget):
#         for child in widget.winfo_children():
#             if isinstance(child, (Button, Entry, Canvas)):
#                 child.config(state=NORMAL)
#             self.enable_widgets_recursive(child)  # Recursively enable child widgets
from pathlib import Path
from tkinter import (
    Frame,
    Canvas,
    Entry,
    StringVar,
    Button,
    PhotoImage,
    messagebox,
    DISABLED,
    NORMAL,
)
import controller as db_controller
from zk import ZK, const

from pyzk.example.set_user import setup_new_employee

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def add_rooms():
    AddRooms()

class AddRooms(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.data = {"username": StringVar(), "telephone": StringVar()}
        self.message = None  # Initialize the message attribute
        self.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=432,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        self.process_image = PhotoImage(file=relative_to_assets("process_image.png"))
        self.success_image = PhotoImage(file=relative_to_assets("success_image.png"))

        self.process_image_id = None
        self.success_image_id = None

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_2.png"))
        image_1 = self.canvas.create_image(258.0, 153.0, image=self.image_image_1)

        self.canvas.create_text(
            52.0,
            128.0,
            anchor="nw",
            text="Username",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_1 = Entry(
            self,
            textvariable=self.data["username"],
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 18 * -1),
            foreground="#777777",
        )
        entry_1.place(x=52.0, y=153.0, width=179.0, height=22.0)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(258.0, 259.0, image=self.image_image_2)

        self.canvas.create_text(
            52.0,
            234.0,
            anchor="nw",
            text="Telephone",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_2 = Entry(
            self,
            textvariable=self.data["telephone"],
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 18 * -1),
            foreground="#777777",
        )
        entry_2.place(x=52.0, y=259.0, width=411.0, height=22.0)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.save,
            relief="flat",
        )
        button_1.place(x=164.0, y=322.0, width=190.0, height=48.0)

        self.message_text_id = self.canvas.create_text(
            181.0,
            58.0,
            anchor="nw",
            text="",  # Initialize with empty text
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_rectangle(
            515.0, 59.0, 517.0, 370.0, fill="#EFEFEF", outline=""
        )

    def save(self):
        # Disable the main window by disabling widgets
        self.set_widgets_state(DISABLED)

        # Show process image
        self.show_process_image()
        self.update()  # Ensure the canvas updates immediately

        # Simulate saving operation
        result = setup_new_employee(self.data["username"].get(), self.data["telephone"].get())

        # Handle the result
        self.handle_result(result)

    def show_process_image(self):
        if self.process_image_id:
            self.canvas.delete(self.process_image_id)
        self.process_image_id = self.canvas.create_image(397, 216, image=self.process_image)

    def show_success_image(self):
        if self.process_image_id:
            self.canvas.delete(self.process_image_id)
        self.success_image_id = self.canvas.create_image(397, 216, image=self.success_image)

    def hide_success_image(self):
        if self.success_image_id:
            self.canvas.delete(self.success_image_id)
    
    def update_message_text(self):
        if self.message is not None:
            self.canvas.itemconfig(self.message_text_id, text=self.message)
        else:
            self.canvas.itemconfig(self.message_text_id, text="")

    def set_widgets_state(self, state):
        for child in self.winfo_children():
            try:
                child.configure(state=state)
            except:
                pass

    def hide_process_image(self):
        if self.process_image_id:
            self.canvas.delete(self.process_image_id)
    def handle_result(self, result):
        if result == "success":
            self.show_success_image()
            self.after(1000, self.hide_success_image)  # Hide success image after 1 second
            self.after(1000, lambda: self.set_widgets_state(NORMAL))
        elif result == "errorCreateEmployee":
            self.hide_process_image()
            messagebox.showerror("Error", "Error creating employee.")
            self.set_widgets_state(NORMAL)
            
            
        elif result == "errorSavingFingerPrint":
            self.hide_process_image()
            messagebox.showerror("Error", "Error saving fingerprint.")
            self.set_widgets_state(NORMAL)
            
        elif result == "errorConnection":
            self.hide_process_image()
            messagebox.showerror("Error", "Error connecting to the device.")
            self.set_widgets_state(NORMAL)
            
        else:
            self.hide_process_image()
            messagebox.showerror("Error", "Unknown error.")
            self.set_widgets_state(NORMAL)
            

   