from math import pi
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
