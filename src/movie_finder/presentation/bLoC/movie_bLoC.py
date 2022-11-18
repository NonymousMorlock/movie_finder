from core.components.either import Either
from src.movie_finder.domain.usecases.get_movie import GetMovie
from src.movie_finder.presentation.bLoC.movie_states import *


class MovieBLoC:

    def __init__(self, use_case: GetMovie):
        self._use_case = use_case

    def get_movie(self, movie_id: str) -> MovieState:
        result: Either = self._use_case.exec(movie_id)
        return result.fold(
            fn_l=lambda failure: MovieNotFound(failure.message),
            fn_r=lambda movies: MovieFound(movies)
        )


if __name__ == '__main__':
    print(MovieNotFound("").is_state(MovieNotFound))
    print(MovieFound([Movie("", "", "", "")]).is_state(MovieState))
