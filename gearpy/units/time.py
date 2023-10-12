from typing import Union
from .unit_base import UnitBase


class Time(UnitBase):

    __UNITS = {'sec': 1,
               'min': 60,
               'hour': 60*60}

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(f"{self.__class__.__name__} unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'Time') -> 'Time':
        super().__add__(other = other)

        if not isinstance(other, Time):
            raise TypeError(f'It is not allowed to sum a {self.__class__.__name__} and a {other.__class__.__name__}.')

        return Time(value = self.__value + other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit],
                     unit = self.__unit)

    def __sub__(self, other: 'Time') -> 'Time':
        super().__sub__(other = other)

        if not isinstance(other, Time):
            raise TypeError(f'It is not allowed to subtract a {other.__class__.__name__} from an '
                            f'{self.__class__.__name__}.')

        return Time(value = self.__value - other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit],
                     unit = self.__unit)

    def __mul__(self, other: Union[float, int]) -> 'Time':
        super().__mul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        return Time(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[float, int]) -> 'Time':
        super().__rmul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by a '
                            f'{self.__class__.__name__}.')

        return Time(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['Time', float, int]) -> Union['Time', float]:
        super().__truediv__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide a {self.__class__.__name__} by a {other.__class__.__name__}.')

        if isinstance(other, Time):
            return self.__value/(other.value*self.__UNITS[other.unit]/self.__UNITS[self.__unit])
        else:
            return Time(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'Time') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Time):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        angle = Time(value = other.value, unit = other.unit)
        angle.to(self.__unit)
        return self.__value == angle.value

    def __ne__(self, other: 'Time') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Time):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')


        angle = Time(value = other.value, unit = other.unit)
        angle.to(self.__unit)
        return self.__value != angle.value

    def __gt__(self, other: 'Time') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Time):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        angle = Time(value = other.value, unit = other.unit)
        angle.to(self.__unit)
        return self.__value > angle.value

    def __ge__(self, other: 'Time') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Time):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        angle = Time(value = other.value, unit = other.unit)
        angle.to(self.__unit)
        return self.__value >= angle.value

    def __lt__(self, other: 'Time') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Time):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        angle = Time(value = other.value, unit = other.unit)
        angle.to(self.__unit)
        return self.__value < angle.value

    def __le__(self, other: 'Time') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Time):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        angle = Time(value = other.value, unit = other.unit)
        angle.to(self.__unit)
        return self.__value <= angle.value

    @property
    def value(self) -> Union[float, int]:
        return self.__value

    @property
    def unit(self) -> str:
        return self.__unit

    def to(self, target_unit: str) -> 'Time':
        super().to(target_unit = target_unit)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(f"{self.__class__.__name__} unit '{target_unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = self.__value*self.__UNITS[self.__unit]/self.__UNITS[target_unit]
        self.__unit = target_unit

        return self
