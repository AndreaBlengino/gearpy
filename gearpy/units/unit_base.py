from abc import ABC, abstractmethod
from typing import Union


class UnitBase(ABC):

    __UNITS = {}

    @abstractmethod
    def __init__(self, value: Union[float, int], unit: str):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Parameter 'value' must be a float or an integer.")

        if not isinstance(unit, str):
            raise TypeError("Parameter 'unit' must be a string.")

    @abstractmethod
    def __repr__(self): ...

    @property
    @abstractmethod
    def value(self) -> None: ...

    @property
    @abstractmethod
    def unit(self) -> None: ...

    @abstractmethod
    def to(self, target_unit: str) -> None:
        if not isinstance(target_unit, str):
            raise TypeError("Parameter 'target_unit' must be a string.")
