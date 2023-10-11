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

    @abstractmethod
    def __add__(self, other: 'UnitBase') -> None: ...

    @abstractmethod
    def __sub__(self, other: 'UnitBase') -> None: ...

    @abstractmethod
    def __mul__(self, other: Union[float, int]) -> None: ...

    @abstractmethod
    def __rmul__(self, other: Union[float, int]) -> None: ...

    @abstractmethod
    def __truediv__(self, other: Union['UnitBase', float, int]) -> None:
        if not isinstance(other, UnitBase) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide a Unit by a {other.__class__.__name__}.')

        if isinstance(other, UnitBase):
            if other.value == 0:
                raise ZeroDivisionError('It is not allowed to divide a Unit by zero.')
        else:
            if other == 0:
                raise ZeroDivisionError('It is not allowed to divide a Unit by zero.')

    @abstractmethod
    def __eq__(self, other: 'UnitBase') -> None: ...

    @abstractmethod
    def __ne__(self, other: 'UnitBase') -> None: ...

    @abstractmethod
    def __gt__(self, other: 'UnitBase') -> None: ...

    @abstractmethod
    def __ge__(self, other: 'UnitBase') -> None: ...

    @abstractmethod
    def __lt__(self, other: 'UnitBase') -> None: ...

    @abstractmethod
    def __le__(self, other: 'UnitBase') -> None: ...

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
