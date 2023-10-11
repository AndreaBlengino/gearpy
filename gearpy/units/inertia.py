from typing import Union
from .unit_base import UnitBase


class Inertia(UnitBase):

    __UNITS = {'kgm^2': 1,
               'gm^2': 1e-3,
               'gcm^2': 1e-7}

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(f"Inertia unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        if value <= 0:
            raise ValueError("Parameter 'value' must be positive.")

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

    def to(self, target_unit: str) -> 'Inertia':
        super().to(target_unit = target_unit)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(f"Inertia unit '{target_unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = self.__value*self.__UNITS[self.__unit]/self.__UNITS[target_unit]
        self.__unit = target_unit

        return self
