import abc


class Model(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'to_dict') and callable(subclass.to_dict) or NotImplemented

    @abc.abstractmethod
    def to_dict(self):
        pass

    @abc.abstractmethod
    def from_dict(self, hash_map):
        pass

    @abc.abstractmethod
    def to_json(self):
        pass

    @abc.abstractmethod
    def from_json(self, json):
        pass
