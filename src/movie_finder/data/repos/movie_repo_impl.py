from core.components.either import Right, Left, Either
from core.errors.exceptions import MovieNotFoundException
from core.errors.failures import MovieNotFoundFailure
from src.movie_finder.data.datasources.remote_data_source import RemoteDataSource
from src.movie_finder.data.models.movie_model import MovieModel
from src.movie_finder.domain.repos.movie_finder_repo import MovieFinderRepo


class MovieFinderRepoImpl(MovieFinderRepo):
    def __init__(self, remote_data_source: RemoteDataSource):
        self.data_source = remote_data_source

    def get_movie(self, movie_id):  # -> Either[MovieNotFoundFailure, Movie]:
        try:
            movies = self.data_source.get_movie(movie_id)
            assert (isinstance(movies[0], MovieModel))
            return Right(movies)
        except MovieNotFoundException as err:
            return Left(MovieNotFoundFailure(err))


if __name__ == '__main__':
    from src.movie_finder.data.datasources.remote_data_source import RemoteDataSourceImpl, RemoteDataSource
    from src.movie_finder.domain.usecases.get_movie import GetMovie

    movie_repo = MovieFinderRepoImpl(RemoteDataSourceImpl())
    get_movie = GetMovie(movie_repo)
    result: Either = get_movie.execute("batman")

    print(result.fold(
        fn_l=lambda failure: failure.message,
        fn_r=lambda movies: movies,
    ), ),
