from math import fabs
from .settings import COMPARISON_TOLERANCE
from typing import Union
from .unit_base import UnitBase


class InertiaMoment(UnitBase):

    __UNITS = {'kgm^2': 1,
               'gm^2': 1e-3,
               'gcm^2': 1e-7}

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(f"{self.__class__.__name__} unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        if value <= 0:
            raise ValueError("Parameter 'value' must be positive.")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'InertiaMoment') -> 'InertiaMoment':
        super().__add__(other = other)

        return InertiaMoment(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'InertiaMoment') -> 'InertiaMoment':
        super().__sub__(other = other)

        if self.__value - other.to(self.__unit).value <= 0:
            raise ValueError('Cannot perform the subtraction because the result is not positive.')

        return InertiaMoment(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union[float, int]) -> 'InertiaMoment':
        super().__mul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if other <= 0:
            raise ValueError('Cannot perform a multiplication by a non-positive number.')

        return InertiaMoment(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[float, int]) -> 'InertiaMoment':
        super().__rmul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by an '
                            f'{self.__class__.__name__}.')

        if other <= 0:
            raise ValueError('Cannot perform a multiplication by a non-positive number.')

        return InertiaMoment(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['InertiaMoment', float, int]) -> Union['InertiaMoment', float]:
        super().__truediv__(other = other)

        if not isinstance(other, InertiaMoment) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, InertiaMoment):
            return self.__value/other.to(self.__unit).value
        else:
            return InertiaMoment(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'InertiaMoment') -> bool:
        super().__eq__(other = other)

        if self.__unit == other.unit:
            return self.__value == other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) < COMPARISON_TOLERANCE

    def __ne__(self, other: 'InertiaMoment') -> bool:
        super().__ne__(other = other)

        if self.__unit == other.unit:
            return self.__value != other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) > COMPARISON_TOLERANCE

    def __gt__(self, other: 'InertiaMoment') -> bool:
        super().__gt__(other = other)

        if self.__unit == other.unit:
            return self.__value > other.value
        else:
            return self.__value - other.to(self.__unit).value > COMPARISON_TOLERANCE

    def __ge__(self, other: 'InertiaMoment') -> bool:
        super().__ge__(other = other)

        if self.__unit == other.unit:
            return self.__value >= other.value
        else:
            return self.__value - other.to(self.__unit).value >= -COMPARISON_TOLERANCE

    def __lt__(self, other: 'InertiaMoment') -> bool:
        super().__lt__(other = other)

        if self.__unit == other.unit:
            return self.__value < other.value
        else:
            return self.__value - other.to(self.__unit).value < -COMPARISON_TOLERANCE

    def __le__(self, other: 'InertiaMoment') -> bool:
        super().__le__(other = other)

        if self.__unit == other.unit:
            return self.__value <= other.value
        else:
            return self.__value - other.to(self.__unit).value <= COMPARISON_TOLERANCE

    @property
    def value(self) -> Union[float, int]:
        return self.__value

    @property
    def unit(self) -> str:
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'InertiaMoment':
        super().to(target_unit = target_unit, inplace = inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(f"{self.__class__.__name__} unit '{target_unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit]/self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return InertiaMoment(value = target_value, unit = target_unit)
