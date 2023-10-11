from .angle import Angle
from math import pi
from .time import Time
from typing import Union
from .unit_base import UnitBase


class Speed(UnitBase):

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
            raise KeyError(f"Speed unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'Speed') -> 'Speed':
        super().__add__(other = other)

        if not isinstance(other, Speed):
            raise TypeError(f'It is not allowed to sum a Speed and a {other.__class__.__name__}.')

        return Speed(value = self.__value + other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit],
                     unit = self.__unit)

    def __sub__(self, other: 'Speed') -> 'Speed':
        super().__sub__(other = other)

        if not isinstance(other, Speed):
            raise TypeError(f'It is not allowed to subtract a {other.__class__.__name__} from a Speed.')

        return Speed(value = self.__value - other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit],
                     unit = self.__unit)

    def __mul__(self, other: Union[Time, float, int]) -> Union[Angle, 'Speed']:
        super().__mul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a Speed by a {other.__class__.__name__}.')

        if isinstance(other, Time):
            time = Time(value = other.value, unit = other.unit)
            time.to('sec')
            return Angle(value = self.__value*self.__UNITS[self.__unit]/self.__UNITS['rad/s']*time.value,
                         unit = 'rad')
        return Speed(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[Time, float, int]) -> Union[Angle, 'Speed']:
        super().__rmul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by a Speed.')

        if isinstance(other, Time):
            time = Time(value = other.value, unit = other.unit)
            time.to('sec')
            return Angle(value = self.__value*self.__UNITS[self.__unit]/self.__UNITS['rad/s']*time.value,
                         unit = 'rad')
        return Speed(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['Speed', float, int]) -> Union['Speed', float]:
        super().__truediv__(other = other)

        if not isinstance(other, Speed) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide a Speed by a {other.__class__.__name__}.')

        if isinstance(other, Speed):
            return self.__value/(other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit])
        else:
            return Speed(value = self.__value/other, unit = self.__unit)

    @property
    def value(self) -> Union[float, int]:
        return self.__value

    @property
    def unit(self) -> str:
        return self.__unit

    def to(self, target_unit: str) -> 'Speed':
        super().to(target_unit = target_unit)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(f"Speed unit '{target_unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = self.__value*self.__UNITS[self.__unit]/self.__UNITS[target_unit]
        self.__unit = target_unit

        return self
