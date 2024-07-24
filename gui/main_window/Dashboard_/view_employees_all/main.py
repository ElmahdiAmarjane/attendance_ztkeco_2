from logging import disable
from pathlib import Path
import controller as db_controller

from tkinter import (
    Frame,
    Canvas,
    Entry,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
)
from tkinter.ttk import Treeview

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def view_employees_all():
    ViewEmployeesAll()


class ViewEmployeesAll(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.search_query = StringVar()
        self.reservation_data = None

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
        self.canvas.create_rectangle(
            40.0, 14.0, 742.0, 16.0, fill="#EFEFEF", outline=""
        )

        self.canvas.create_rectangle(
            40.0, 342.0, 742.0, 344.0, fill="#EFEFEF", outline=""
        )

        self.canvas.create_text(
            116.0,
            33.0,
            anchor="nw",
            text="View Employees All",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )



        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(680.5, 60.0, image=self.entry_image_1)
        entry_1 = Entry(
            self,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            foreground="#777777",
            font=("Montserrat Bold", 18 * -1),
            textvariable=self.search_query,
        )
        # Bind text change to function
        entry_1.bind(
            "<KeyRelease>",
            lambda event: self.filter_treeview_records(self.search_query.get()),
        )

        entry_1.place(x=637.0, y=48.0, width=87.0, height=22.0)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.refresh_btn = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_refresh,
            relief="flat",
        )
        self.refresh_btn.place(x=525.0, y=33.0, width=53.0, height=53.0)

        # Add treeview here
        self.columns = {
            "id": "Employee ID",
            "name": "Name",
            "telephone": "Telephone",
            "created_at": "Created At",
        }

        self.treeview = Treeview(
            self,
            columns=list(self.columns.keys()),
            show="headings",
            height=200,
            selectmode="browse",
        )

        # Show the headings
        for col_key, col_name in self.columns.items():
            self.treeview.heading(col_key, text=col_name)
            self.treeview.column(col_key, width=100)

        self.treeview.place(x=40.0, y=101.0, width=700.0, height=229.0)

        # Insert data
        self.handle_refresh()

        # Add selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.navigate_back_btn = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_navigate_back,
            relief="flat",
        )
        self.navigate_back_btn.place(x=40.0, y=33.0, width=53.0, height=53.0)

    def filter_treeview_records(self, query):
        self.treeview.delete(*self.treeview.get_children())
        # Run for loop from original data
        for row in self.reservation_data:
            # Check if query exists in any value from data
            if query.lower() in str(row).lower():
                # Insert the data into the treeview
                self.treeview.insert("", "end", values=row)
        self.on_treeview_select()

    def on_treeview_select(self, event=None):
        try:
            self.treeview.selection()[0]
        except:
            self.parent.selected_rid = None
            return
        # Get the selected item
        item = self.treeview.selection()[0]
        # Get the reservation id
        self.parent.selected_rid = self.treeview.item(item, "values")[0]

    def handle_refresh(self):
        self.treeview.delete(*self.treeview.get_children())
        self.reservation_data = db_controller.get_all_employees()
        for row in self.reservation_data:
            self.treeview.insert("", "end", values=row)

        # Refresh the dashboard if applicable
        try:
            self.parent.parent.handle_dashboard_refresh()
        except:
            pass

    def handle_navigate_back(self):
        self.parent.navigate("add")
