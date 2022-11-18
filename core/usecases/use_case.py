import abc


class UseCase(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'execute') and callable(subclass.execute) or NotImplemented

    @abc.abstractmethod
    def exec(self, request=None):
        pass
