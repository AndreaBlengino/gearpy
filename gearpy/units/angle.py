from math import pi
from typing import Union
from .unit_base import UnitBase


class Angle(UnitBase):

    __UNITS = {'rad': 1,
               'deg': pi/180,
               'arcmin': pi/180/60,
               'arcsec': pi/180/60/60}

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(f"Angle unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'Angle') -> 'Angle':
        super().__add__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'It is not allowed to sum an Angle and a {other.__class__.__name__}.')

        return Angle(value = self.__value + other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit],
                     unit = self.__unit)

    def __sub__(self, other: 'Angle') -> 'Angle':
        super().__sub__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'It is not allowed to subtract a {other.__class__.__name__} from an Angle.')

        return Angle(value = self.__value - other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit],
                     unit = self.__unit)

    def __mul__(self, other: Union[float, int]) -> 'Angle':
        super().__mul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply an Angle by a {other.__class__.__name__}.')

        return Angle(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[float, int]) -> 'Angle':
        super().__rmul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by an Angle.')

        return Angle(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['Angle', float, int]) -> Union['Angle', float]:
        super().__truediv__(other = other)

        if not isinstance(other, Angle) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide an Angle by a {other.__class__.__name__}.')

        if isinstance(other, Angle):
            return self.__value/(other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit])
        else:
            return Angle(value = self.__value/other, unit = self.__unit)

    @property
    def value(self) -> Union[float, int]:
        return self.__value

    @property
    def unit(self) -> str:
        return self.__unit

    def to(self, target_unit: str) -> 'Angle':
        super().to(target_unit = target_unit)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(f"Angle unit '{target_unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = self.__value*self.__UNITS[self.__unit]/self.__UNITS[target_unit]
        self.__unit = target_unit

        return self
