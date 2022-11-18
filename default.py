from bs4 import BeautifulSoup

from networking import Networking
from core.platform.platform import Platform

MOVIES_ENDPOINT = "https://web.archive.org/web/20200518073855/" \
                  "https://www.empireonline.com/movies/features/best-movies-2/"


class Default:
    def __init__(self):
        self.movies = []
        while True:
            try:
                self.movies = Platform.read_file("assets/100_movies_list.txt")
                print("Movies file read successfully")
                break
            except FileNotFoundError:
                print("Movies list not found")
                movie_response = Networking.get(MOVIES_ENDPOINT)
                soup = BeautifulSoup(movie_response.text, "html.parser")
                movies = soup.find_all("h3", class_="title")[::-1]
                movies = [movie.getText() for movie in movies]
                with Platform.write("./assets/100_movies_list.txt") as file:
                    list(map(file.write, [f"{movie}\n" for movie in movies]))
                    print("Movies list retrieved and stored successfully")

    @property
    def get_titles(self):
        titles = []
        for movie in self.movies:
            title_split = movie.split(") ")
            if len(title_split) < 2:
                title_split = movie.split(": ")
                # incase there is a movie title that doesn't have a ) nor a : between number and title but has a : in
                # the title itself e.g 16 The Lord Of The Rings: The Return Of The King
                try:
                    int(title_split[0])
                except ValueError:
                    raise Exception("[get_titles] error: the movie title does not have a \")\" after it's number "
                                    "neither does it have a \":\"\nPlease Check movies List for movie number "
                                    f"{self.movies.index(movie) + 1}")
            titles.append(title_split[1])

        return [title.replace("\n", "") for title in titles]
