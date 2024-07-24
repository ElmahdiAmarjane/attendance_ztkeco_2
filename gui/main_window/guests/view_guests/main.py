from logging import disable
from pathlib import Path
from tkinter import ttk
import controller as db_controller

from tkinter import (
    Frame,
    Canvas,
    Entry,
    Text,
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


def view_guests():
    ViewGuests()


class ViewGuests(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.search_query = StringVar()

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
            text="All Employees",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )


        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(666.0, 59.0, image=self.image_image_1)

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

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(617.0, 60.0, image=self.image_image_2)

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

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.delete_btn = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_delete,
            relief="flat",
            state="disabled",
        )

        self.delete_btn.place(x=596.0, y=359.0, width=146.0, height=48.0)

        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        self.edit_btn = Button(
            self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_edit,
            relief="flat",
            state="disabled",
        )
        self.edit_btn.place(x=463.0, y=359.0, width=116.0, height=48.0)

        # self.canvas.create_rectangle(
        #     40.0,
        #     101.0,
        #     742.0,
        #     329.0,
        #     fill="#EFEFEF",
        #     outline="")
        # Add treeview here

        self.columns = {
            "id": ["Employee ID", 30],
            "name": ["Name", 100],
            "telephone": ["Telephone", 100],
            "created_at": ["Created At", 100],
      
        }

        style = ttk.Style()
        style.theme_use("default")

# Configure the Treeview heading
        style.configure("Treeview.Heading", background="#173c5c", foreground="#171c0c", font=("Montserrat Bold", 12))

        self.treeview = Treeview(
            self,
            columns=list(self.columns.keys()),
            show="headings",
            height=200,
            selectmode="browse",
            # ="#FFFFFF",
            # fg="#5E95FF",
            # font=("Montserrat Bold", 18 * -1)
        )

        # Show the headings
        for idx, txt in self.columns.items():
            self.treeview.heading(idx, text=txt[0])
            # Set the column widths
            self.treeview.column(idx, width=txt[1], anchor='center')
        
            

        self.treeview.place(x=40.0, y=101.0, width=700.0, height=229.0)

        # Insert data
        self.handle_refresh()

        # Add selection event
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def filter_treeview_records(self, query):
        self.treeview.delete(*self.treeview.get_children())
        # run for loop from original data
        for row in self.guest_data:
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
        # Get the guest id
        self.parent.selected_rid = self.treeview.item(item, "values")[0]
        # Enable the buttons
        self.delete_btn.config(state="normal")
        self.edit_btn.config(state="normal")

    def handle_refresh(self):
        self.treeview.delete(*self.treeview.get_children())
        self.guest_data = db_controller.get_all_employees()
        for row in self.guest_data:
            self.treeview.insert("", "end", values=row)

    def handle_navigate_back(self):
        self.parent.navigate("view")

    from tkinter import messagebox

    def handle_delete(self):
       print('🐊🐊🐊id to delete : ', self.parent.selected_rid)
    
    # Ask the user for confirmation before deleting
       confirm = messagebox.askokcancel("Confirm Delete", "Are you sure you want to delete this employee?")
    
       if confirm:
        if db_controller.delete_employee(self.parent.selected_rid):
            messagebox.showinfo("Info", "Successfully Deleted the employee" + " " * 20)  # Added spaces for width
        else:
            messagebox.showerror("Error", "Unable to delete employee" + " " * 20)  # Added spaces for width

        self.handle_refresh()

    def handle_edit(self):
        self.parent.navigate("edit")
        self.parent.windows["edit"].initialize()
