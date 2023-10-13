from .angular_position import AngularPosition
from math import pi, fabs
from .settings import COMPARISON_TOLERANCE
from .time import Time
from typing import Union
from .unit_base import UnitBase


class AngularSpeed(UnitBase):

    __UNITS = {'rad/s': 1,
               'rad/min': 1/60,
               'rad/h': 1/60/60,
               'deg/s': pi/180,
               'deg/min': pi/180/60,
               'deg/h': pi/180/60/60,
               'rps': 2*pi,
               'rpm': 2*pi/60,
               'rph': 2*pi/60/60}

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(f"{self.__class__.__name__} unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'AngularSpeed') -> 'AngularSpeed':
        super().__add__(other = other)

        return AngularSpeed(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'AngularSpeed') -> 'AngularSpeed':
        super().__sub__(other = other)

        return AngularSpeed(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union[Time, float, int]) -> Union[AngularPosition, 'AngularSpeed']:
        super().__mul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, Time):
            return AngularPosition(value = self.to('rad/s').value*other.to('sec').value, unit = 'rad')
        else:
            return AngularSpeed(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[Time, float, int]) -> Union[AngularPosition, 'AngularSpeed']:
        super().__rmul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by a '
                            f'{self.__class__.__name__}.')

        if isinstance(other, Time):
            return AngularPosition(value = self.to('rad/s').value*other.to('sec').value, unit = 'rad')
        else:
            return AngularSpeed(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['AngularSpeed', float, int]) -> Union['AngularSpeed', float]:
        super().__truediv__(other = other)

        if not isinstance(other, AngularSpeed) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide a {self.__class__.__name__} by a {other.__class__.__name__}.')

        if isinstance(other, AngularSpeed):
            return self.__value/other.to(self.__unit).value
        else:
            return AngularSpeed(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'AngularSpeed') -> bool:
        super().__eq__(other = other)

        if self.__unit == other.unit:
            return self.__value == other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) < COMPARISON_TOLERANCE

    def __ne__(self, other: 'AngularSpeed') -> bool:
        super().__ne__(other = other)

        if self.__unit == other.unit:
            return self.__value != other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) > COMPARISON_TOLERANCE

    def __gt__(self, other: 'AngularSpeed') -> bool:
        super().__gt__(other = other)

        if self.__unit == other.unit:
            return self.__value > other.value
        else:
            return self.__value - other.to(self.__unit).value > COMPARISON_TOLERANCE

    def __ge__(self, other: 'AngularSpeed') -> bool:
        super().__ge__(other = other)

        if self.__unit == other.unit:
            return self.__value >= other.value
        else:
            return self.__value - other.to(self.__unit).value >= -COMPARISON_TOLERANCE

    def __lt__(self, other: 'AngularSpeed') -> bool:
        super().__lt__(other = other)

        if self.__unit == other.unit:
            return self.__value < other.value
        else:
            return self.__value - other.to(self.__unit).value < -COMPARISON_TOLERANCE

    def __le__(self, other: 'AngularSpeed') -> bool:
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

    def to(self, target_unit: str, inplace: bool = False) -> 'AngularSpeed':
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
            return AngularSpeed(value = target_value, unit = target_unit)
