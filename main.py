from tkinter import ttk
from urllib.request import urlopen

from PIL import ImageTk

from src.movie_finder.presentation.views.home import Main
from src.movie_finder.presentation.views.search import Search

# if __name__ == '__main__':
#     search = Search()
#     if search.query is None or search.query.strip() == "":
#         Main()
#     else:
#         query = search.query.title()
#         Main(query)


import tkinter as tk
import random


class DynamicGrid(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0,
                            state="disabled")
        self.text.pack(fill="both", expand=True)
        self.boxes = []

    def add_box(self, box: tk.Misc):
        self.boxes.append(box)
        self.text.configure(state="normal")
        self.text.window_create("end", window=box)
        self.text.configure(state="disabled")


class Example(object):
    def __init__(self):
        self.root = tk.Tk()
        self.container = ttk.Frame(self.root)
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        scrollable_frame = ttk.Frame(self.canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.dg = DynamicGrid(self.root, width=500, height=200)
        add_button = tk.Button(self.root, text="Add", command=lambda: self.dg.add_box(box(self.root, image)))
        remove_button = tk.Button(self.root, text="Remove", command=lambda: self.dg.remove_box())

        add_button.pack()
        remove_button.pack()
        self.dg.pack(side="top", fill="both", expand=True)

        # add a few boxes to start
        data = urlopen("https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg")
        image = ImageTk.PhotoImage(data=data.read())

        # data = urlopen(movie.poster)
        # image = ImageTk.PhotoImage(data=data.read())
        #
        # tk.Label(self.root, image=image).pack()
        # tk.Label(self.root, text=movie.title).pack()
        # tk.Label(self.root, text=movie.year).pack()
        # tk.Label(self.root, text=movie.imdb_id).pack()

        # create an image box using the image object above

        for i in range(10):
            self.dg.add_box(box(self.root, image))

    def start(self):
        self.container.pack()
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.root.mainloop()


def box(root, image):
    image_label = tk.Canvas(root, width=300, height=800)
    image_label.itemconfig(image_label.create_image(0, 0, anchor="nw", image=image))
    # add a text below to the canvas below the image
    image_label.create_text(300 / len("Hello World"), 450, anchor="nw", text="Hello World", font=("TkDefaultFont", 20), fill="black")
    image_label.create_text(300 / len("Hello World"), 500, anchor="nw", text="Hello World", font=("TkDefaultFont", 20), fill="black")

    return image_label



Example().start()
