from abc import ABC, abstractmethod
from gearpy.mechanical_object import MotorBase, RotatingObject
from gearpy.transmission import Transmission
from .rules_base import RuleBase


class MotorControlBase(ABC):

    @abstractmethod
    def __init__(self, transmission: Transmission):
        if not isinstance(transmission, Transmission):
            raise TypeError(f"Parameter 'transmission' must be an instance of {Transmission.__name__!r}.")

        if not transmission.chain:
            raise ValueError("Parameter 'transmission.chain' cannot be an empty tuple.")

        if not isinstance(transmission.chain[0], MotorBase):
            raise TypeError(f"First element in 'transmission' must be an instance of {MotorBase.__name__!r}.")

        if not all([isinstance(item, RotatingObject) for item in transmission.chain]):
            raise TypeError(f"All elements of 'transmission' must be instances of {RotatingObject.__name__!r}.")

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
    def add_rule(self, rule: RuleBase):
        if not isinstance(rule, RuleBase):
            raise TypeError(f"Parameter 'rule' must be an instance of {RuleBase.__name__!r}.")

        self.__rules.append(rule)

    @abstractmethod
    def apply_rules(self): ...
