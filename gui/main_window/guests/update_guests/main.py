from pathlib import Path
from tkinter import (
    Frame,
    Canvas,
    Entry,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
    IntVar,
)
import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def update_guests():
    UpdateGuests()

class UpdateGuests(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.selected_r_id = self.parent.selected_rid

        self.configure(bg="#FFFFFF")

        self.data = {
            "id": StringVar(),
            "name": StringVar(),
            "telephone": StringVar(),
            "created_at": IntVar(),
        }

        self.initialize()

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
        self.canvas.create_rectangle(
            40.0, 14.0, 742.0, 16.0, fill="#EFEFEF", outline=""
        )

        self.canvas.create_text(
            116.0,
            33.0,
            anchor="nw",
            text="Update Employee",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.canvas.create_text(
            116.0,
            65.0,
            anchor="nw",
            text="Change Details",
            fill="#808080",
            font=("Montserrat SemiBold", 16 * -1),
        )

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("view"),
            relief="flat",
        )
        button_1.place(x=40.0, y=33.0, width=53.0, height=53.0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(206.0, 170.0, image=self.image_image_1)

        self.canvas.create_text(
            71.56398010253906,
            145.0,
            anchor="nw",
            text="Employee ID",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.id_text = self.canvas.create_text(
            72.0,
            172.0,
            anchor="nw",
            text=self.parent.selected_rid,
            fill="#777777",
            font=("Montserrat SemiBold", 17 * -1),
        )

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(206.0, 276.0, image=self.image_image_2)

        self.canvas.create_text(
            71.56398010253906,
            251.0,
            anchor="nw",
            text="Employee Phone",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            212.8127899169922, 288.0, image=self.entry_image_1
        )
        entry_1 = Entry(
            self,
            font=("Montserrat Bold", 18 * -1),
            textvariable=self.data["telephone"],
            foreground="#777777",
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
        )
        entry_1.place(
            x=71.56398010253906, y=276.0, width=282.49761962890625, height=22.0
        )

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        image_3 = self.canvas.create_image(583.0, 170.0, image=self.image_image_3)

        self.canvas.create_text(
            455.0473937988281,
            145.0,
            anchor="nw",
            text="Employee Name",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(589.5, 182.0, image=self.entry_image_2)
        entry_2 = Entry(
            self,
            font=("Montserrat Bold", 18 * -1),
            textvariable=self.data["name"],
            foreground="#777777",
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
        )
        entry_2.place(x=455.0, y=170.0, width=269.0, height=22.0)

        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        image_4 = self.canvas.create_image(583.0, 278.0, image=self.image_image_4)

        self.canvas.create_text(
            455.0473937988281,
            253.0,
            anchor="nw",
            text="Created At",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )

        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        entry_bg_3 = self.canvas.create_image(
            589.5094757080078, 290.0, image=self.entry_image_3
        )
        entry_3 = Entry(
            self,
            font=("Montserrat Bold", 18 * -1),
            textvariable=self.data["created_at"],
            foreground="#777777",
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            state="readonly"
        )
        entry_3.place(
            x=455.0473937988281, y=278.0, width=268.9241638183594, height=22.0
        )

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_update,
            relief="flat",
        )
        button_2.place(x=326.0, y=339.0, width=144.0, height=48.0)

    def initialize(self):
        self.selected_r_id = self.parent.selected_rid
        
        # Fetch the employee details
        employee_details = db_controller.get_employee_by_id(self.selected_r_id)
        
        # Update the StringVar and IntVar with the fetched details
        if employee_details:
            self.data["id"].set(employee_details['id'])
            self.data["name"].set(employee_details['name'])
            self.data["telephone"].set(employee_details['telephone'])
            self.data["created_at"].set(employee_details['created_at'])

    def handle_update(self):
        data = [
            x
            for x in [self.data[label].get() for label in ("name", "telephone")]
        ]

        result = db_controller.update_employee(
            name=data[0], telephone=data[1], id=self.selected_r_id
        )
        if result:
            messagebox.showinfo("Success", "Employee Updated")
            self.parent.navigate("view")
            self.parent.windows['view'].handle_refresh()
        else:
            messagebox.showerror("Error", "Failed to update employee. Please verify that all details are correct.")
