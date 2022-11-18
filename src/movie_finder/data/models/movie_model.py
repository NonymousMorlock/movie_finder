from src.movie_finder.domain.entities.movie import Movie
from core.models.model import Model


class MovieModel(Movie, Model):
    def __init__(self, title: str, year: str, imdb_id: str, poster: str, category: str):
        super().__init__(title=title, year=year, imdb_id=imdb_id, poster=poster, category=category)

    @staticmethod
    def from_dict(hash_map):
        return MovieModel(
            title=hash_map['title'],
            year=hash_map['year'],
            imdb_id=hash_map['imdb_id'],
            category=hash_map['type'],
            poster=hash_map['poster'],
        )

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return self.__dict__

    @classmethod
    def from_json(cls, json):
        return cls(**json)

    def __repr__(self):
        return f"MovieModel(title={self.title}, year={self.year}, type={self.type}, imdb_id={self.imdb_id}, poster={self.poster})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


if __name__ == '__main__':
    movie = MovieModel(title='The Matrix', year="1999", imdb_id='tt0133093', poster='https://www.imdb.com/title/tt0133093/mediaviewer/rm1828758528', category="movie")
    print(movie)
    print(movie.to_dict())
    print(movie.to_json())
    print(movie.from_json(movie.to_json()))
    print(movie.from_dict(movie.to_dict()))
    print(movie == movie.from_dict(movie.to_dict()))
    print(movie == movie.from_json(movie.to_json()))
    print(issubclass(MovieModel, Model))
    print(issubclass(MovieModel, Movie))
