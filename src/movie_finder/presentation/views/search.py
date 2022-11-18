import tkinter as tk


class Search:
    search_bar: tk.Entry
    search_button: tk.Button

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Movie Finder")
        self.root.geometry("200x100")
        self.root.resizable(False, False)
        self.query = None
        self.init()
        self.root.mainloop()

    def init(self):
        self.search_bar = tk.Entry(self.root)
        self.search_bar.pack()
        self.search_button = tk.Button(self.root, text="Search", command=self.search)
        show_top_100 = tk.Button(self.root, text="Show Top 100", command=self.search)
        self.search_button.pack()
        show_top_100.pack()

    def show_top_100(self):
        self.query = ""
        self.root.destroy()

    def search(self):
        self.query = self.search_bar.get()
        self.root.destroy()
