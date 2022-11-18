import time

from src.movie_finder.presentation.views.home import Main
from src.movie_finder.presentation.views.search import Search

if __name__ == '__main__':
    search = Search()
    if search.query is not None:
        if search.query.strip() == "":
            Main().start()
        else:
            query = search.query.title()
            Main(query).start()


