import abc


class SubscriptableABCMeta(abc.ABCMeta):
    def __getitem__(cls, item):
        return cls


class Either(metaclass=SubscriptableABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'map') and callable(subclass.map) or
                hasattr(subclass, 'fold') and callable(subclass.fold) or
                NotImplemented)

    @abc.abstractmethod
    def map(self, fn):
        pass

    @abc.abstractmethod
    def fold(self, fn_l, fn_r):
        pass

    def __getitem__(self, item):
        return self


class Left(Either):
    def __init__(self, value):
        self.value = value

    def map(self, fn):
        return self

    def fold(self, fn_l, fn_r):
        return fn_l(self.value)


class Right(Either):
    def __init__(self, value):
        self.value = value

    def map(self, fn):
        return Right(fn(self.value))

    def fold(self, fn_l, fn_r):
        return fn_r(self.value)
