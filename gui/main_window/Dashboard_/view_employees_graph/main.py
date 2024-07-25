from logging import disable
from pathlib import Path
from matplotlib import pyplot as plt
import pandas as pd
import controller as db_controller
import tkinter as tk
from tkinter import (
    Frame,
    Canvas,
    Entry,
    Button,
    PhotoImage,
    StringVar,
)
from tkinter.ttk import Treeview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def view_employees_graph():
    ViewEmployeesGraph()

class ViewEmployeesGraph(Frame):
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

        self.canvas.create_text(
            116.0,
            20.0,
            anchor="nw",
            text="Graph",
            fill="#5E95FF",
            font=("Montserrat Bold", 26 * -1),
        )

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.refresh_btn = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.handle_refresh,
            relief="flat",
        )
        self.refresh_btn.place(x=720.0, y=10.0, width=40.0, height=40.0)

        # Fetch data
        data = db_controller.get_total_hours_worked_by_day()

        # Convert data to pandas DataFrame
        df = pd.DataFrame(list(data.items()), columns=['date', 'hours_worked'])
        df['date'] = pd.to_datetime(df['date'])  # Convert date column to datetime

        # Chart 4: Line chart of total hours worked per day
        fig4, ax4 = plt.subplots()
        ax4.plot(df['date'], df['hours_worked'], marker='o')
        ax4.set_title("Total Hours Worked Per Day")
        ax4.set_xlabel("Date")
        ax4.set_ylabel("Hours Worked")

        # Create a frame for charts
        charts_frame = Frame(self.canvas, bg="#FFFFFF")
        charts_frame.place(x=20, y=60, width=760, height=350)

        # Embed the figure into the Tkinter window
        canvas4 = FigureCanvasTkAgg(fig4, charts_frame)
        canvas4.draw()
        canvas4.get_tk_widget().pack(side="left", fill="both", expand=True)

    def handle_refresh(self):
        # Add refresh logic here
        pass

    def handle_navigate_back(self):
        self.parent.navigate("add")
