from core.components.either import Either
from core.errors.failures import MovieNotFoundFailure
from src.movie_finder.domain.entities.movie import Movie
from src.movie_finder.domain.repos.movie_finder_repo import MovieFinderRepo
from core.usecases.use_case import UseCase


class GetMovie(UseCase):
    def __init__(self, movie_repository: MovieFinderRepo):
        self.movie_repository = movie_repository

    def exec(self, request=None):  # -> Either[MovieNotFoundFailure, list[Movie]]
        return self.movie_repository.get_movie(request)
