from abc import ABC, abstractmethod


class MechanicalObject(ABC):

    @abstractmethod
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Parameter 'name' must be a string.")

        if name == '':
            raise ValueError("Parameter 'name' cannot be an empty string")

        self.__name = name

    @property
    @abstractmethod
    def name(self) -> str:
        return self.__name
