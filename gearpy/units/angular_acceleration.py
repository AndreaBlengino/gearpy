from math import pi
from .angular_speed import AngularSpeed
from .time import Time
from typing import Union
from .unit_base import UnitBase


class AngularAcceleration(UnitBase):

    __UNITS = {'rad/s^2': 1,
               'deg/s^2': pi/180}

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(f"{self.__class__.__name__} unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'AngularAcceleration') -> 'AngularAcceleration':
        super().__add__(other = other)

        return AngularAcceleration(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'AngularAcceleration') -> 'AngularAcceleration':
        super().__sub__(other = other)

        return AngularAcceleration(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union[Time, float, int]) -> Union[AngularSpeed, 'AngularAcceleration']:
        super().__mul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, Time):
            return AngularSpeed(value = self.to('rad/s^2').value*other.to('sec').value, unit = 'rad/s')
        else:
            return AngularAcceleration(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[Time, float, int]) -> Union[AngularSpeed, 'AngularAcceleration']:
        super().__rmul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by an '
                            f'{self.__class__.__name__}.')

        if isinstance(other, Time):
            return AngularSpeed(value = self.to('rad/s^2').value*other.to('sec').value, unit = 'rad/s')
        else:
            return AngularAcceleration(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['AngularAcceleration', float, int]) -> Union['AngularAcceleration', float]:
        super().__truediv__(other = other)

        if not isinstance(other, AngularAcceleration) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, AngularAcceleration):
            return self.__value/other.to(self.__unit).value
        else:
            return AngularAcceleration(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'AngularAcceleration') -> bool:
        super().__eq__(other = other)

        return self.__value == other.to(self.__unit).value

    def __ne__(self, other: 'AngularAcceleration') -> bool:
        super().__ne__(other = other)

        return self.__value != other.to(self.__unit).value

    def __gt__(self, other: 'AngularAcceleration') -> bool:
        super().__gt__(other = other)

        return self.__value > other.to(self.__unit).value

    def __ge__(self, other: 'AngularAcceleration') -> bool:
        super().__ge__(other = other)

        return self.__value >= other.to(self.__unit).value

    def __lt__(self, other: 'AngularAcceleration') -> bool:
        super().__lt__(other = other)

        return self.__value < other.to(self.__unit).value

    def __le__(self, other: 'AngularAcceleration') -> bool:
        super().__le__(other = other)

        return self.__value <= other.to(self.__unit).value

    @property
    def value(self) -> Union[float, int]:
        return self.__value

    @property
    def unit(self) -> str:
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'AngularAcceleration':
        super().to(target_unit = target_unit, inplace = inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(f"{self.__class__.__name__} unit '{target_unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        target_value = self.__value*self.__UNITS[self.__unit]/self.__UNITS[target_unit]

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return AngularAcceleration(value = target_value, unit = target_unit)
