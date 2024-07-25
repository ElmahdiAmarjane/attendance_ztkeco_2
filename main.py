import tkinter as tk
from gui.login.gui import loginWindow
from gui.main_window.main import mainWindow
from pyzk.example.live_capture import live_capture
from pyzk.example.get_attendence import get_attendence
# Main window constructor
root = tk.Tk()  # Make temporary window for app to start
root.withdraw()  # WithDraw the window


if __name__ == "__main__":

    #loginWindow()
    #get_attendence()
    mainWindow()
    #live_capture()
    


    root.mainloop()
 