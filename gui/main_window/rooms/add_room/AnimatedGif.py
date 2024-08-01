import tkinter as tk
from PIL import Image, ImageTk
import itertools

class AnimatedGIF(tk.Label):
    def __init__(self, master, path, delay=100):
        im = Image.open(path)
        self.frames = []
        try:
            while True:
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(len(self.frames))  # move to the next frame
        except EOFError:
            pass

        self.delay = delay
        self.frames_cycle = itertools.cycle(self.frames)
        self.label = tk.Label(master)
        self._running = False

    def start_animation(self):
        self._running = True
        self.animate()

    def animate(self):
        if self._running:
            self.label.config(image=next(self.frames_cycle))
            self.label.after(self.delay, self.animate)

    def stop_animation(self):
        self._running = False

    def place(self, **kwargs):
        self.label.place(**kwargs)

    def place_forget(self):
        self.label.place_forget()
