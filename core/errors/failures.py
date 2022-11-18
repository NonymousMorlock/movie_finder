import abc


class Failure(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'message') and callable(subclass.message) or NotImplemented

    @abc.abstractmethod
    def message(self):
        pass


class MovieNotFoundFailure(Failure):
    def __init__(self, error_message):
        self._message = error_message

    @property
    def message(self):
        return self._message
