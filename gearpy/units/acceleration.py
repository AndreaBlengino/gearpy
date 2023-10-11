from math import pi
from .speed import Speed
from .time import Time
from typing import Union
from .unit_base import UnitBase


class Acceleration(UnitBase):

    __UNITS = {'rad/s^2': 1,
               'deg/s^2': pi/180}

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(f"Acceleration unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'Acceleration') -> 'Acceleration':
        super().__add__(other = other)

        if not isinstance(other, Acceleration):
            raise TypeError(f'It is not allowed to sum an Acceleration and a {other.__class__.__name__}.')

        return Acceleration(value = self.__value + other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit],
                            unit = self.__unit)

    def __sub__(self, other: 'Acceleration') -> 'Acceleration':
        super().__sub__(other = other)

        if not isinstance(other, Acceleration):
            raise TypeError(f'It is not allowed to subtract a {other.__class__.__name__} from an Acceleration.')

        return Acceleration(value = self.__value - other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit],
                            unit = self.__unit)

    def __mul__(self, other: Union[Time, float, int]) -> Union[Speed, 'Acceleration']:
        super().__mul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply an Acceleration by a {other.__class__.__name__}.')

        if isinstance(other, Time):
            time = Time(value = other.value, unit = other.unit)
            time.to('sec')
            return Speed(value = self.__value*self.__UNITS[self.__unit]/self.__UNITS['rad/s^2']*time.value,
                         unit = 'rad/s')
        return Acceleration(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[Time, float, int]) -> Union[Speed, 'Acceleration']:
        super().__rmul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by an Acceleration.')

        if isinstance(other, Time):
            time = Time(value = other.value, unit = other.unit)
            time.to('sec')
            return Speed(value = self.__value*self.__UNITS[self.__unit]/self.__UNITS['rad/s^2']*time.value,
                         unit = 'rad/s')
        return Acceleration(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['Acceleration', float, int]) -> Union['Acceleration', float]:
        super().__truediv__(other = other)

        if not isinstance(other, Acceleration) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide an Acceleration by a {other.__class__.__name__}.')

        if isinstance(other, Acceleration):
            return self.__value/(other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit])
        else:
            return Acceleration(value = self.__value/other, unit = self.__unit)

    @property
    def value(self) -> Union[float, int]:
        return self.__value

    @property
    def unit(self) -> str:
        return self.__unit

    def to(self, target_unit: str) -> 'Acceleration':
        super().to(target_unit = target_unit)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(f"Acceleration unit '{target_unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = self.__value*self.__UNITS[self.__unit]/self.__UNITS[target_unit]
        self.__unit = target_unit

        return self
