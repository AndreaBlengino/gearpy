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
            raise KeyError(f"{self.__class__.__name__} unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'Angle') -> 'Angle':
        super().__add__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'It is not allowed to sum an {self.__class__.__name__} and a {other.__class__.__name__}.')

        return Angle(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'Angle') -> 'Angle':
        super().__sub__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'It is not allowed to subtract a {other.__class__.__name__} from an '
                            f'{self.__class__.__name__}.')

        return Angle(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union[float, int]) -> 'Angle':
        super().__mul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        return Angle(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[float, int]) -> 'Angle':
        super().__rmul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by an '
                            f'{self.__class__.__name__}.')

        return Angle(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['Angle', float, int]) -> Union['Angle', float]:
        super().__truediv__(other = other)

        if not isinstance(other, Angle) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, Angle):
            return self.__value/other.to(self.__unit).value
        else:
            return Angle(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'Angle') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value == other.to(self.__unit).value

    def __ne__(self, other: 'Angle') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value != other.to(self.__unit).value

    def __gt__(self, other: 'Angle') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value > other.to(self.__unit).value

    def __ge__(self, other: 'Angle') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value >= other.to(self.__unit).value

    def __lt__(self, other: 'Angle') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value < other.to(self.__unit).value

    def __le__(self, other: 'Angle') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Angle):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value <= other.to(self.__unit).value

    @property
    def value(self) -> Union[float, int]:
        return self.__value

    @property
    def unit(self) -> str:
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'Angle':
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
            return Angle(value = target_value, unit = target_unit)
