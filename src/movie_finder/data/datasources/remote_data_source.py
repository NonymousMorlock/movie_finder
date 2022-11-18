import abc
import os

import requests
from dotenv import load_dotenv

from core.errors.exceptions import MovieNotFoundException
from src.movie_finder.data.models.movie_model import MovieModel
from src.movie_finder.domain.entities.movie import Movie

load_dotenv()

API_KEY = os.environ["X_RAPIDAPI_KEY"]
API_HOST = os.environ["X_RAPIDAPI_HOST"]
ENDPOINT = "https://movie-database-alternative.p.rapidapi.com/"


class RemoteDataSource(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'get_movie') and callable(subclass.get_movie) or NotImplemented

    @abc.abstractmethod
    def get_movie(self, movie_id) -> list[MovieModel]:
        pass


class RemoteDataSourceImpl(RemoteDataSource):
    def __init__(self, client=requests):
        self.client = client

    def get_movie(self, movie_id) -> list[MovieModel]:
        params = {"s": movie_id, "r": "json", "page": "1"}
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": API_HOST
        }

        movies: list[MovieModel] = []
        try:
            response = self.client.get(ENDPOINT, params=params, headers=headers)
            response.raise_for_status()
            if response.json()["Response"] == "False":
                raise MovieNotFoundException(movie_id=movie_id)
            for movie in response.json()["Search"]:
                movies.append(
                    MovieModel(
                        title=movie["Title"],
                        year=movie["Year"],
                        imdb_id=movie["imdbID"],
                        poster=movie["Poster"],
                    )
                )
            return movies
        except requests.exceptions.HTTPError as err:
            raise MovieNotFoundException(error_message=err)
