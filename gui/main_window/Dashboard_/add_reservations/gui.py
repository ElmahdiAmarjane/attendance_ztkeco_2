from pathlib import Path
from tkinter import Button, Frame, Canvas, Entry, PhotoImage, Tk
import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class AddReservations(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.data = {"g_id": "", "check_in": "", "meal": "", "r_id": ""}

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
        self.canvas.pack(fill="both", expand=True)

        # Create the first image and text
        self.canvas.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        image_id_2 = self.canvas.create_image(115.0, 81.0, image=self.canvas.entry_image_1)
        self.canvas.tag_bind(image_id_2, "<Button-1>", self.to_view_employees_in)

        # self.canvas.create_text(
        #     56.0,
        #     45.0,
        #     anchor="nw",
        #     text="🟢",
        #     fill="#008000",
        #     font=("Montserrat Bold", 10),
        # )
        self.canvas.create_text(
            70.0,
            45.0,
            anchor="nw",
            text="Employees in",
            fill="#008000",
            font=("Montserrat Bold", 10),
        )

        self.canvas.create_text(
            164.0,
            63.0,
            anchor="ne",
            text=db_controller.count_in_employees(),
            fill="#008000",
            font=("Montserrat Bold", 28),
            justify="right",
        )

        # Create the second image and text
        self.canvas.entry_image_2 = PhotoImage(file=relative_to_assets("entry_1.png"))
        image_id_3 = self.canvas.create_image(400.0, 81.0, image=self.canvas.entry_image_2)
        self.canvas.tag_bind(image_id_3, "<Button-1>", self.to_view_employees_out)

        # self.canvas.create_text(
        #     340.0,
        #     45.0,
        #     anchor="nw",
        #     text="🔴",
        #     fill="#FF0000",
        #     font=("Montserrat Bold", 10),
        # )
        self.canvas.create_text(
            355.0,
            45.0,
            anchor="nw",
            text="Employees out",
            fill="#FF0000",
            font=("Montserrat Bold", 12),
        )

        self.canvas.create_text(
            446.0,
            63.0,
            anchor="ne",
            text=db_controller.count_out_employees(),
            fill="#FF0000",
            font=("Montserrat Bold", 28),
            justify="right",
        )
    #    ################
        self.canvas.entry_image_5 = PhotoImage(file=relative_to_assets("entry_1.png"))
        image_id_4 = self.canvas.create_image(670.0, 81.0, image=self.canvas.entry_image_5)
        self.canvas.tag_bind(image_id_4, "<Button-1>", self.to_view_employees_all)
        self.canvas.create_text(
            610.0,
            45.0,
            anchor="nw",
            text="Total employees",
            fill="#a456e3",
            font=("Montserrat Bold", 12),
        )

        self.canvas.create_text(
            720.0,
            65.0,
            anchor="ne",
            text=db_controller.count_all_employees(),
            fill="#a456e3",
            font=("Montserrat Bold", 28),
            justify="right",
        )

    #    #################
        # Create the third image and text
        self.canvas.entry_image_3 = PhotoImage(file=relative_to_assets("entry_1.png"))
        image_id_5 = self.canvas.create_image(115.0, 220.0, image=self.canvas.entry_image_3)
        self.canvas.tag_bind(image_id_5, "<Button-1>", self.to_view_employees_compl)

        self.canvas.create_text(
            45.0,
            190.0,
            anchor="nw",
            text="8h Completed",
            fill="#3b82c4",
            font=("Montserrat Bold", 12),
        )
        results,nbremployeesmore = db_controller.get_employees_with_average_hours()
        self.canvas.create_text(
            160.0,
            215.0,
            anchor="ne",
            text=nbremployeesmore,
            fill="#3b82c4",
            font=("Montserrat Bold", 28),
            justify="right",
        )

        # Create the fourth image and text
        self.canvas.entry_image_4 = PhotoImage(file=relative_to_assets("entry_1.png"))
        image_id_6 = self.canvas.create_image(400.0, 220.0, image=self.canvas.entry_image_4)
        self.canvas.tag_bind(image_id_6, "<Button-1>", self.on_image_click)

        self.canvas.create_text(
            330.0,
            190.0,
            anchor="nw",
            text="8h NOT Completed",
            fill="#c9c54d",
            font=("Montserrat Bold", 12),
        )
        results,nbremployeesless = db_controller.get_employees_with_less_than_8_hours()
        self.canvas.create_text(
            440.0,
            215.0,
            anchor="ne",
            text=nbremployeesless,
            fill="#c9c54d",
            font=("Montserrat Bold", 28),
            justify="right",
        )
#  ########################
 # Create the fourth image and text
        self.canvas.entry_image_6 = PhotoImage(file=relative_to_assets("entry_1.png"))
        image_id_7 = self.canvas.create_image(675.0, 220.0, image=self.canvas.entry_image_6)
        # self.canvas.tag_bind(image_id_7, "<Button-1>", self.on_image_click)

        self.canvas.create_text(
            590.0,
            190.0,
            anchor="nw",
            text="Total Average Work Hours",
            fill="#173c5c",
            font=("Montserrat Bold", 12),
        )
        result = db_controller.get_average_total_hours_per_employee()
        self.canvas.create_text(
            720.0,
            215.0,
            anchor="ne",
            text=result,
            fill="#173c5c",
            font=("Montserrat Bold", 20),
            justify="right",
        )
# ####################
# ####################

      #  button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            text='More stats',
            borderwidth=0,
            highlightthickness=0,
            command=self.to_view_employees_graph,
            relief="flat",
        )
        button_1.place(x=300.0, y=330.0, width=190.0, height=48.0)

# #########################
        self.canvas.pack(fill="both", expand=True)
        
    def on_image_click(self, event):
        # Callback function for image click event
        print("Image clicked")
        # Perform any actions you want to trigger on click here
        self.parent.navigate("view")
    def to_view_employees_in(self, event):
        # Callback function for image click event
        print("Image clicked")
        # Perform any actions you want to trigger on click here
        self.parent.navigate("emplin")
    def to_view_employees_out(self, event):
        # Callback function for image click event
        print("Image clicked")
        # Perform any actions you want to trigger on click here
        self.parent.navigate("emplout")
    def to_view_employees_all(self, event):
        # Callback function for image click event
        print("Image clicked")
        # Perform any actions you want to trigger on click here
        self.parent.navigate("emplall")
    def to_view_employees_compl(self, event):
        # Callback function for image click event
        print("Image clicked")
        # Perform any actions you want to trigger on click here
        self.parent.navigate("emplcompl")
    def to_view_employees_graph(self):
        # Callback function for image click event
        print("Image clicked")
        # Perform any actions you want to trigger on click here
        self.parent.navigate("emplgraph")


# # Example usage
# if __name__ == "__main__":
#     root = Tk()
#     add_reservations_frame = AddReservations(root)
#     add_reservations_frame.pack(fill="both", expand=True)
#     root.mainloop()
