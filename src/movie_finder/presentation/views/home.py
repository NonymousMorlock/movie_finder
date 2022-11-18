from urllib.request import urlopen
import tkinter as tk
from PIL import ImageTk

from default import Default
from src.movie_finder.data.datasources.remote_data_source import RemoteDataSourceImpl
from src.movie_finder.data.repos.movie_repo_impl import MovieFinderRepoImpl
from src.movie_finder.domain.entities.movie import Movie
from src.movie_finder.domain.usecases.get_movie import GetMovie
from src.movie_finder.presentation.bLoC.movie_bLoC import MovieBLoC
from src.movie_finder.presentation.bLoC.movie_states import MovieState, MovieNotFound, MovieFound


class Main:
    def __init__(self, movie_id: str | None = None):
        self.movie_id = movie_id
        self.movies: list[Movie] = []
        self.bLoC = MovieBLoC(GetMovie(MovieFinderRepoImpl(RemoteDataSourceImpl())))
        self.default = Default()
        self.default_titles = self.default.get_titles
        self.root = tk.Tk()
        self.root.title("Movie Finder")
        # self.root.geometry("500x500")
        # self.root.resizable(False, False)
        self.init()

    # using tkinter to display image, title and year of movie
    def init(self):
        if self.movie_id is None:
            self.movie_id = self.default_titles[0]
        state: MovieState = self.bLoC.get_movie(self.movie_id)
        if state.is_state(MovieNotFound):
            # clear tkinter window and show error message on screen
            assert isinstance(state, MovieNotFound)
            message = state.message
            # use tkinter to display error message

        else:
            assert isinstance(state, MovieFound)
            movies: list[Movie] = state.movie
            # use tkinter to display image, title and year of each movie in grids

            self.display_movies(movies)

    def display_movies(self, movies: list[Movie]):
        # display each movie in its own grid
        # get each cell dynamically
        for movie in movies:
            # get image from url
            image = ImageTk.PhotoImage(data=urlopen(movie.poster).read())
            # create label for image
            image_label = tk.Label(image=image)
            # display image in grid and make sure grid isn't occupied
            image_label.grid(row=0, column=0, sticky="nsew")
            # create label for title
            title_label = tk.Label(text=movie.title)
            # display title in grid and make sure grid isn't occupied
            title_label.grid(row=1, column=0, sticky="nsew")
            # create label for year
            year_label = tk.Label(text=movie.year)
            # display year in grid and make sure grid isn't occupied
            year_label.grid(row=2, column=0, sticky="nsew")


        self.root.mainloop()
