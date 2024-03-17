from abc import ABC, abstractmethod
from gearpy.mechanical_objects import MotorBase, RotatingObject
from gearpy.powertrain import Powertrain
from gearpy.motor_control.rules.rules_base import RuleBase


class MotorControlBase(ABC):

    @abstractmethod
    def __init__(self, powertrain: Powertrain):
        if not isinstance(powertrain, Powertrain):
            raise TypeError(f"Parameter 'powertrain' must be an instance of {Powertrain.__name__!r}.")

        if not powertrain.elements:
            raise ValueError("Parameter 'powertrain.elements' cannot be an empty tuple.")

        if not isinstance(powertrain.elements[0], MotorBase):
            raise TypeError(f"First element in 'powertrain' must be an instance of {MotorBase.__name__!r}.")

        if not all([isinstance(item, RotatingObject) for item in powertrain.elements]):
            raise TypeError(f"All elements of 'powertrain' must be instances of {RotatingObject.__name__!r}.")

        self.__powertrain = powertrain
        self.__rules = []

    @property
    @abstractmethod
    def powertrain(self) -> Powertrain:
        return self.__powertrain

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
