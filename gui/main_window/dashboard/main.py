# from pathlib import Path

# from tkinter import Frame, Canvas, Entry, Text, Button, PhotoImage, messagebox
# import controller as db_controller

# from .gui import Dashboard
# from  .gui_empl import EmployeesDetails

# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path("./assets")


# def relative_to_assets(path: str) -> Path:
#     return ASSETS_PATH / Path(path)


# def dash():
#     DASh()


# class DASh(Frame):
#     def __init__(self, parent, controller=None, *args, **kwargs):
#         Frame.__init__(self, parent, *args, **kwargs)
#         self.parent = parent
#         self.selected_rid = None
#         self.guest_data = db_controller.count_all_employees()

#         self.configure(bg="#FFFFFF")

#         # Loop through windows and place them
#         self.windows = {
#             "gui": Dashboard(self),
#             "guiempl": EmployeesDetails(self),
#         }

#         self.current_window = self.windows["gui"]
#         self.current_window.place(x=0, y=0, width=1013.0, height=506.0)

#         self.current_window.tkraise()

#     def navigate(self, name):
#         # Hide all screens
#         for window in self.windows.values():
#             window.place_forget()

#         # Show the screen of the button pressed
#         self.windows[name].place(x=0, y=0, width=1013.0, height=506.0)
