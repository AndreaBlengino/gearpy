from typing import Union
from .unit_base import UnitBase


class Inertia(UnitBase):

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

    def __add__(self, other: 'Inertia') -> 'Inertia':
        super().__add__(other = other)

        if not isinstance(other, Inertia):
            raise TypeError(f'It is not allowed to sum an {self.__class__.__name__} and a {other.__class__.__name__}.')

        return Inertia(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'Inertia') -> 'Inertia':
        super().__sub__(other = other)

        if not isinstance(other, Inertia):
            raise TypeError(f'It is not allowed to subtract a {other.__class__.__name__} from an '
                            f'{self.__class__.__name__}.')

        if self.__value - other.to(self.__unit).value <= 0:
            raise ValueError('Cannot perform the subtraction because the result is not positive.')

        return Inertia(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union[float, int]) -> 'Inertia':
        super().__mul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if other <= 0:
            raise ValueError('Cannot perform a multiplication by a non-positive number.')

        return Inertia(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[float, int]) -> 'Inertia':
        super().__rmul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by an '
                            f'{self.__class__.__name__}.')

        if other <= 0:
            raise ValueError('Cannot perform a multiplication by a non-positive number.')

        return Inertia(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['Inertia', float, int]) -> Union['Inertia', float]:
        super().__truediv__(other = other)

        if not isinstance(other, Inertia) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, Inertia):
            return self.__value/other.to(self.__unit).value
        else:
            return Inertia(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'Inertia') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Inertia):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value == other.to(self.__unit).value

    def __ne__(self, other: 'Inertia') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Inertia):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value != other.to(self.__unit).value

    def __gt__(self, other: 'Inertia') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Inertia):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value > other.to(self.__unit).value

    def __ge__(self, other: 'Inertia') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Inertia):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value >= other.to(self.__unit).value

    def __lt__(self, other: 'Inertia') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Inertia):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value < other.to(self.__unit).value

    def __le__(self, other: 'Inertia') -> bool:
        super().__eq__(other = other)

        if not isinstance(other, Inertia):
            raise TypeError(f'Cannot compare {self.__class__.__name__} and {other.__class__.__name__}')

        return self.__value <= other.to(self.__unit).value

    @property
    def value(self) -> Union[float, int]:
        return self.__value

    @property
    def unit(self) -> str:
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'Inertia':
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
            return Inertia(value = target_value, unit = target_unit)
