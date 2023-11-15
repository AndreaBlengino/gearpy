from abc import ABC, abstractmethod
from math import fabs
from typing import Union


COMPARISON_TOLERANCE = 1e-12


class UnitBase(ABC):

    __UNITS = {}

    @abstractmethod
    def __init__(self, value: Union[float, int], unit: str):
        if not isinstance(value, float) and not isinstance(value, int):
            raise TypeError("Parameter 'value' must be a float or an integer.")

        if not isinstance(unit, str):
            raise TypeError("Parameter 'unit' must be a string.")

    def __repr__(self):
        return f'{self.value} {self.unit}'

    def __abs__(self):
        return self.__class__(abs(self.value), self.unit)

    def __add__(self, other: 'UnitBase') -> None:
        if not isinstance(other, self.__class__) and not issubclass(self.__class__, other.__class__):
            raise TypeError(f'It is not allowed to sum a {self.__class__.__name__} and a {other.__class__.__name__}.')

        return self.__class__(value = self.value + other.to(self.unit).value, unit = self.unit)

    def __sub__(self, other: 'UnitBase') -> None:
        if not isinstance(other, self.__class__) and not issubclass(self.__class__, other.__class__):
            raise TypeError(f'It is not allowed to subtract a {other.__class__.__name__} '
                            f'from a {self.__class__.__name__}.')

        try:
            return self.__class__(value = self.value - other.to(self.unit).value, unit = self.unit)
        except ValueError:
            if self.value - other.to(self.unit).value <= 0:
                raise ValueError('Cannot perform the subtraction because the result is not positive.')

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

    def __eq__(self, other: 'UnitBase') -> None:
        if not isinstance(other, self.__class__) and not issubclass(self.__class__, other.__class__):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        if self.unit == other.unit:
            return self.value == other.value
        else:
            return fabs(self.value - other.to(self.unit).value) < COMPARISON_TOLERANCE

    def __ne__(self, other: 'UnitBase') -> None:
        if not isinstance(other, self.__class__) and not issubclass(self.__class__, other.__class__):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        if self.unit == other.unit:
            return self.value != other.value
        else:
            return fabs(self.value - other.to(self.unit).value) > COMPARISON_TOLERANCE

    def __gt__(self, other: 'UnitBase') -> None:
        if not isinstance(other, self.__class__) and not issubclass(self.__class__, other.__class__):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        if self.unit == other.unit:
            return self.value > other.value
        else:
            return self.value - other.to(self.unit).value > COMPARISON_TOLERANCE

    def __ge__(self, other: 'UnitBase') -> None:
        if not isinstance(other, self.__class__) and not issubclass(self.__class__, other.__class__):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        if self.unit == other.unit:
            return self.value >= other.value
        else:
            return self.value - other.to(self.unit).value >= -COMPARISON_TOLERANCE

    def __lt__(self, other: 'UnitBase') -> None:
        if not isinstance(other, self.__class__) and not issubclass(self.__class__, other.__class__):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        if self.unit == other.unit:
            return self.value < other.value
        else:
            return self.value - other.to(self.unit).value < -COMPARISON_TOLERANCE

    def __le__(self, other: 'UnitBase') -> None:
        if not isinstance(other, self.__class__) and not issubclass(self.__class__, other.__class__):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        if self.unit == other.unit:
            return self.value <= other.value
        else:
            return self.value - other.to(self.unit).value <= COMPARISON_TOLERANCE

    @property
    @abstractmethod
    def value(self) -> None: ...

    @property
    @abstractmethod
    def unit(self) -> None: ...

    @abstractmethod
    def to(self, target_unit: str, inplace: bool = False) -> None:
        if not isinstance(target_unit, str):
            raise TypeError("Parameter 'target_unit' must be a string.")

        if not isinstance(inplace, bool):
            raise TypeError("Parameter 'inplace' must be a bool.")
