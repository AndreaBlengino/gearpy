from abc import ABC, abstractmethod


class MechanicalObject(ABC):

    @abstractmethod
    def __init__(self, name):
        self.__name = name

    @property
    @abstractmethod
    def name(self) -> str:
        return self.__name
