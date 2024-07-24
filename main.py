import tkinter as tk
from gui.login.gui import loginWindow
from gui.main_window.main import mainWindow
from pyzk.example.live_capture import live_capture
# Main window constructor
root = tk.Tk()  # Make temporary window for app to start
root.withdraw()  # WithDraw the window


if __name__ == "__main__":

    #loginWindow()
    mainWindow()
    #live_capture()

    root.mainloop()
 