class Movie:
    def __init__(self, title: str, year: str, imdb_id: str, poster: str):
        self.title: str = title
        self.year: str = year
        self.poster: str = poster
        self.imdb_id: str = imdb_id
