import errno
import os


class Platform:
    @staticmethod
    def mkdir(path: str):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    @staticmethod
    def write(path: str):
        Platform.mkdir(os.path.dirname(path))
        return open(path, "w", encoding="UTF-8")

    @staticmethod
    def read_file(path: str):
        with open(path, "r", encoding="UTF-8") as file:
            return file.readlines()
