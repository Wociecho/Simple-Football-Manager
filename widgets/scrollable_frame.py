import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#9DADC5")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, background="#9DADC5")
        self.scrollable_frame = tk.Frame(self.canvas, background="#9DADC5", borderwidth=0)

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=0, sticky="nse")  # Dodaj grid do Scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind('<Configure>', self.FrameWidth)

    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_scrollable_frame(self):
        self.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def hide(self):
        self.pack_forget()