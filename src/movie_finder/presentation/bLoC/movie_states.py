import abc

from src.movie_finder.domain.entities.movie import Movie


class MovieState(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'is_state') and callable(subclass.is_state) or NotImplemented

    def is_state(self, state):
        pass


class MovieNotFound(MovieState):
    def __init__(self, message: str):
        self.message = message

    def is_state(self, state):
        return state == MovieNotFound or state == MovieState

    def __eq__(self, other):
        return isinstance(other, MovieNotFound)


class MovieFound(MovieState):
    def __init__(self, movies: list[Movie]):
        self.movie = movies

    def is_state(self, state):
        return state == MovieFound or state == MovieState

    def __eq__(self, other):
        return isinstance(other, MovieFound)


