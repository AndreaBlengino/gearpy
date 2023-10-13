from .time import Time
from typing import Union


class TimeInterval(Time):

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if value <= 0:
            raise ValueError("Parameter 'value' must be positive.")

        self.__value = value
        self.__unit = unit

    def __add__(self, other: Union['TimeInterval', 'Time']) -> Union['TimeInterval', 'Time']:
        super().__add__(other = other)

        if isinstance(other, TimeInterval):
            return TimeInterval(value = self.__value + other.to(self.__unit).value, unit = self.__unit)
        else:
            return Time(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: Union['TimeInterval', 'Time']) -> Union['TimeInterval', 'Time']:
        super().__sub__(other = other)

        if self.__value - other.to(self.__unit).value <= 0:
            raise ValueError('Cannot perform the subtraction because the result is not positive.')

        if isinstance(other, TimeInterval):
            return TimeInterval(value = self.__value - other.to(self.__unit).value, unit = self.__unit)
        else:
            return Time(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union[float, int]) -> 'TimeInterval':
        super().__mul__(other = other)

        if other <= 0:
            raise ValueError('Cannot perform a multiplication by a non-positive number.')

        return TimeInterval(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[float, int]) -> 'TimeInterval':
        super().__rmul__(other = other)

        if other <= 0:
            raise ValueError('Cannot perform a multiplication by a non-positive number.')

        return TimeInterval(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['Time', float, int]) -> Union['Time', float]:
        super().__truediv__(other = other)

        if isinstance(other, Time):
            return self.__value/other.to(self.__unit).value
        else:
            return TimeInterval(value = self.__value/other, unit = self.__unit)

    def to(self, target_unit: str, inplace: bool = False) -> 'TimeInterval':
        converted = super().to(target_unit = target_unit, inplace = inplace)

        if inplace:
            self.__value = converted.value
            self.__unit = converted.unit
            return self
        else:
            return TimeInterval(value = converted.value, unit = converted.unit)
