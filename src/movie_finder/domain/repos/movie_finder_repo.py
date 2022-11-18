import abc
import typing

from core.components.either import Either
from core.errors.failures import MovieNotFoundFailure
from src.movie_finder.domain.entities.movie import Movie


class MovieFinderRepo(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'get_movie') and callable(subclass.get_movie) or NotImplemented

    @abc.abstractmethod
    def get_movie(self, movie_id) -> Either[MovieNotFoundFailure, list[Movie]]:
        pass
