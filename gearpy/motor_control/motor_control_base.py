from abc import ABC, abstractmethod
from gearpy.transmission import Transmission
from typing import Callable, Any, Union


class MotorControlBase(ABC):

    @abstractmethod
    def __init__(self, transmission: Transmission):
        if not isinstance(transmission, Transmission):
            raise TypeError(f"Parameter 'transmission' must be an instance of {Transmission.__name__!r}.")

        self.__transmission = transmission
        self.__rules = []

    @property
    @abstractmethod
    def transmission(self) -> Transmission:
        return self.__transmission

    @property
    @abstractmethod
    def rules(self) -> list:
        return self.__rules

    @abstractmethod
    def add_rule(self, rule: Callable[Any, Union[float, int]]):
        if not isinstance(rule, Callable):
            raise TypeError(f"Parameter 'rule' must be callable.")

        self.__rules.append(rule)

    @abstractmethod
    def apply_rules(self): ...
