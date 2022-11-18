
class MovieNotFoundException(Exception):
    def __init__(self, movie_id=None, error_message=None):
        self.movie_id = movie_id
        self.error_message = error_message

    def __str__(self):
        return "Movie with id %s not found" % self.movie_id if self.error_message is None else self.error_message

