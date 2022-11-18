import json
import os
from tkinter import ttk
from urllib.request import urlopen
import tkinter as tk
from PIL import ImageTk, Image

from core.platform.platform import Platform
from default import Default
from src.movie_finder.data.datasources.remote_data_source import RemoteDataSourceImpl
from src.movie_finder.data.models.movie_model import MovieModel
from src.movie_finder.data.repos.movie_repo_impl import MovieFinderRepoImpl
from src.movie_finder.domain.entities.movie import Movie
from src.movie_finder.domain.usecases.get_movie import GetMovie
from src.movie_finder.presentation.bLoC.movie_bLoC import MovieBLoC
from src.movie_finder.presentation.bLoC.movie_states import MovieState, MovieNotFound, MovieFound
from src.movie_finder.presentation.widgets.dynamic_grid import DynamicGrid


class Main:
    def __init__(self, movie_id: str | None = None):
        self.movie_id = movie_id
        self.movies: list[Movie] = []
        self.bLoC = MovieBLoC(GetMovie(MovieFinderRepoImpl(RemoteDataSourceImpl())))
        if movie_id is None:
            self.default = Default()
            self.default_titles = self.default.get_titles
        self.root = tk.Tk()
        self.root.title("Movie Finder")
        # self.root.geometry("500x500")
        # self.root.resizable(False, False)
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

        self.dg.pack(side="top", fill="both", expand=True)

        # add a few boxes to start

        # data = urlopen(movie.poster)
        # image = ImageTk.PhotoImage(data=data.read())
        #
        # tk.Label(self.root, image=image).pack()
        # tk.Label(self.root, text=movie.title).pack()
        # tk.Label(self.root, text=movie.year).pack()
        # tk.Label(self.root, text=movie.imdb_id).pack()

        # create an image box using the image object above

        self.init()

    def start(self):
        self.container.pack()
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.root.mainloop()

    # using tkinter to display image, title and year of movie
    def init(self):
        if self.movie_id is None:
            self._get_default_movies_from_cache()
            return self.display_movies(self.movies)
        state: MovieState = self.bLoC.get_movie(self.movie_id)
        if state.is_state(MovieNotFound):
            # clear tkinter window and show error message on screen
            assert isinstance(state, MovieNotFound)
            message = state.message
            # use tkinter to display error message
            return self.dg.add_box(tk.Label(text=message))

        else:
            assert isinstance(state, MovieFound)
            movies: list[Movie] = state.movie
            # use tkinter to display image, title and year of each movie in grids

            return self.display_movies(movies)

    def display_movies(self, movies: list[Movie]):
        for idx, movie in enumerate(movies):
            try:
                data = urlopen(
                    movie.poster)
            except ValueError:
                data = urlopen("https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg")
            n_image = Image.open(data)
            n_image.resize((300, 500), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(n_image)
            self.dg.add_box(box(self.root, image, movie))
            os.system("cls" if os.name in ("nt", "dos") else "clear")
            loading_percentage = round((idx + 1) / len(movies) * 100, 1)
            print("Loading movies: {}%".format(loading_percentage))

    def _get_default_movies_from_cache(self):
        while True:
            try:
                print("\nLoading from cache")
                with open("assets/default.json", "r") as file:
                    json_string = file.read()
                    default_list = json.loads(json_string)
                    for movie in default_list:
                        self.movies.append(MovieModel.from_dict(movie))
                print("\nLoaded from cache")
                break
            except FileNotFoundError:
                print("\nFile not found")
                print("\nGenerating default movies")
                default_movies = self._get_default_from_bLoC()
                with Platform.write("assets/default.json") as file:
                    json_string = json.dumps(default_movies, indent=4)
                    file.write(json_string)
                print("\nSaved to cache")

    def _get_default_from_bLoC(self) -> list[dict]:
        default_list = []
        for movie_id in self.default_titles:
            state = self.bLoC.get_movie(movie_id)
            if state.is_state(MovieFound):
                assert isinstance(state, MovieFound)
                movie = state.movie[0]
                assert isinstance(movie, MovieModel)
                default_list.append(movie.to_dict())
                print(f"\n{movie.title} added to default list")
        print(f"\n{len(default_list)} movies generated")
        return default_list


def box(root, image, movie: Movie):
    font = ("TkDefaultFont", 20)
    image_label = tk.Canvas(root, width=300, height=600)
    image_label.itemconfig(image_label.create_image(0, 0, anchor="nw", image=image))
    # add a text below to the canvas below the image
    image_label.create_text(300 / len(movie.title), 450, anchor="nw", text=movie.title, font=font, fill="black")
    image_label.create_text(
        300 / len(f"{movie.year}-{movie.type}"),
        500,
        anchor="nw",
        text=f"{movie.year}-{movie.type}",
        font=font,
        fill="black",
    )
    image_label.create_text(300 / len(movie.imdb_id), 550, anchor="nw", text=movie.imdb_id, font=font, fill="black")
    image_label.image = image

    return image_label
