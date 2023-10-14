from math import pi, fabs
from typing import Union
from .unit_base import UnitBase


COMPARISON_TOLERANCE = 1e-12


class AngularPosition(UnitBase):

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

    def __add__(self, other: 'AngularPosition') -> 'AngularPosition':
        super().__add__(other = other)

        return AngularPosition(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'AngularPosition') -> 'AngularPosition':
        super().__sub__(other = other)

        return AngularPosition(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union[float, int]) -> 'AngularPosition':
        super().__mul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        return AngularPosition(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[float, int]) -> 'AngularPosition':
        super().__rmul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by an '
                            f'{self.__class__.__name__}.')

        return AngularPosition(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['AngularPosition', float, int]) -> Union['AngularPosition', float]:
        super().__truediv__(other = other)

        if not isinstance(other, AngularPosition) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, AngularPosition):
            return self.__value/other.to(self.__unit).value
        else:
            return AngularPosition(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'AngularPosition') -> bool:
        super().__eq__(other = other)

        if self.__unit == other.unit:
            return self.__value == other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) < COMPARISON_TOLERANCE

    def __ne__(self, other: 'AngularPosition') -> bool:
        super().__ne__(other = other)

        if self.__unit == other.unit:
            return self.__value != other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) > COMPARISON_TOLERANCE

    def __gt__(self, other: 'AngularPosition') -> bool:
        super().__gt__(other = other)

        if self.__unit == other.unit:
            return self.__value > other.value
        else:
            return self.__value - other.to(self.__unit).value > COMPARISON_TOLERANCE

    def __ge__(self, other: 'AngularPosition') -> bool:
        super().__ge__(other = other)

        if self.__unit == other.unit:
            return self.__value >= other.value
        else:
            return self.__value - other.to(self.__unit).value >= -COMPARISON_TOLERANCE

    def __lt__(self, other: 'AngularPosition') -> bool:
        super().__lt__(other = other)

        if self.__unit == other.unit:
            return self.__value < other.value
        else:
            return self.__value - other.to(self.__unit).value < -COMPARISON_TOLERANCE

    def __le__(self, other: 'AngularPosition') -> bool:
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

    def to(self, target_unit: str, inplace: bool = False) -> 'AngularPosition':
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
            return AngularPosition(value = target_value, unit = target_unit)


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

    def __mul__(self, other: Union['Time', float, int]) -> Union['AngularPosition', 'AngularSpeed']:
        super().__mul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, Time):
            return AngularPosition(value = self.to('rad/s').value*other.to('sec').value, unit = 'rad')
        else:
            return AngularSpeed(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union['Time', float, int]) -> Union['AngularPosition', 'AngularSpeed']:
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


class AngularAcceleration(UnitBase):

    __UNITS = {'rad/s^2': 1,
               'deg/s^2': pi/180}

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(f"{self.__class__.__name__} unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'AngularAcceleration') -> 'AngularAcceleration':
        super().__add__(other = other)

        return AngularAcceleration(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'AngularAcceleration') -> 'AngularAcceleration':
        super().__sub__(other = other)

        return AngularAcceleration(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union['Time', float, int]) -> Union['AngularAcceleration', 'AngularSpeed']:
        super().__mul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, Time):
            return AngularSpeed(value = self.to('rad/s^2').value*other.to('sec').value, unit = 'rad/s')
        else:
            return AngularAcceleration(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union['Time', float, int]) -> Union['AngularAcceleration', 'AngularSpeed']:
        super().__rmul__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by an '
                            f'{self.__class__.__name__}.')

        if isinstance(other, Time):
            return AngularSpeed(value = self.to('rad/s^2').value*other.to('sec').value, unit = 'rad/s')
        else:
            return AngularAcceleration(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['AngularAcceleration', float, int]) -> Union['AngularAcceleration', float]:
        super().__truediv__(other = other)

        if not isinstance(other, AngularAcceleration) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, AngularAcceleration):
            return self.__value/other.to(self.__unit).value
        else:
            return AngularAcceleration(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'AngularAcceleration') -> bool:
        super().__eq__(other = other)

        if self.__unit == other.unit:
            return self.__value == other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) < COMPARISON_TOLERANCE

    def __ne__(self, other: 'AngularAcceleration') -> bool:
        super().__ne__(other = other)

        if self.__unit == other.unit:
            return self.__value != other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) > COMPARISON_TOLERANCE

    def __gt__(self, other: 'AngularAcceleration') -> bool:
        super().__gt__(other = other)

        if self.__unit == other.unit:
            return self.__value > other.value
        else:
            return self.__value - other.to(self.__unit).value > COMPARISON_TOLERANCE

    def __ge__(self, other: 'AngularAcceleration') -> bool:
        super().__ge__(other = other)

        if self.__unit == other.unit:
            return self.__value >= other.value
        else:
            return self.__value - other.to(self.__unit).value >= -COMPARISON_TOLERANCE

    def __lt__(self, other: 'AngularAcceleration') -> bool:
        super().__lt__(other = other)

        if self.__unit == other.unit:
            return self.__value < other.value
        else:
            return self.__value - other.to(self.__unit).value < -COMPARISON_TOLERANCE

    def __le__(self, other: 'AngularAcceleration') -> bool:
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

    def to(self, target_unit: str, inplace: bool = False) -> 'AngularAcceleration':
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
            return AngularAcceleration(value = target_value, unit = target_unit)


class InertiaMoment(UnitBase):

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

    def __add__(self, other: 'InertiaMoment') -> 'InertiaMoment':
        super().__add__(other = other)

        return InertiaMoment(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'InertiaMoment') -> 'InertiaMoment':
        super().__sub__(other = other)

        if self.__value - other.to(self.__unit).value <= 0:
            raise ValueError('Cannot perform the subtraction because the result is not positive.')

        return InertiaMoment(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union[float, int]) -> 'InertiaMoment':
        super().__mul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if other <= 0:
            raise ValueError('Cannot perform a multiplication by a non-positive number.')

        return InertiaMoment(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[float, int]) -> 'InertiaMoment':
        super().__rmul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by an '
                            f'{self.__class__.__name__}.')

        if other <= 0:
            raise ValueError('Cannot perform a multiplication by a non-positive number.')

        return InertiaMoment(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['InertiaMoment', float, int]) -> Union['InertiaMoment', float]:
        super().__truediv__(other = other)

        if not isinstance(other, InertiaMoment) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide an {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, InertiaMoment):
            return self.__value/other.to(self.__unit).value
        else:
            return InertiaMoment(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'InertiaMoment') -> bool:
        super().__eq__(other = other)

        if self.__unit == other.unit:
            return self.__value == other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) < COMPARISON_TOLERANCE

    def __ne__(self, other: 'InertiaMoment') -> bool:
        super().__ne__(other = other)

        if self.__unit == other.unit:
            return self.__value != other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) > COMPARISON_TOLERANCE

    def __gt__(self, other: 'InertiaMoment') -> bool:
        super().__gt__(other = other)

        if self.__unit == other.unit:
            return self.__value > other.value
        else:
            return self.__value - other.to(self.__unit).value > COMPARISON_TOLERANCE

    def __ge__(self, other: 'InertiaMoment') -> bool:
        super().__ge__(other = other)

        if self.__unit == other.unit:
            return self.__value >= other.value
        else:
            return self.__value - other.to(self.__unit).value >= -COMPARISON_TOLERANCE

    def __lt__(self, other: 'InertiaMoment') -> bool:
        super().__lt__(other = other)

        if self.__unit == other.unit:
            return self.__value < other.value
        else:
            return self.__value - other.to(self.__unit).value < -COMPARISON_TOLERANCE

    def __le__(self, other: 'InertiaMoment') -> bool:
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

    def to(self, target_unit: str, inplace: bool = False) -> 'InertiaMoment':
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
            return InertiaMoment(value = target_value, unit = target_unit)


class Torque(UnitBase):

    __UNITS = {'Nm': 1,
               'mNm': 1e-3,
               'kNm': 1e3,
               'kgfm': 9.80665,
               'kgfcm': 9.80665e-2}

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(f"{self.__class__.__name__} unit '{unit}' not available. "
                           f"Available units are: {list(self.__UNITS.keys())}")

        self.__value = value
        self.__unit = unit

    def __repr__(self) -> str:
        return f'{self.__value} {self.__unit}'

    def __add__(self, other: 'Torque') -> 'Torque':
        super().__add__(other = other)

        return Torque(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'Torque') -> 'Torque':
        super().__sub__(other = other)

        return Torque(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union[float, int]) -> 'Torque':
        super().__mul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        return Torque(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union[float, int]) -> 'Torque':
        super().__rmul__(other = other)

        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by a '
                            f'{self.__class__.__name__}.')

        return Torque(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['InertiaMoment', 'Torque', float, int]) -> Union['AngularAcceleration', 'Torque', float]:
        super().__truediv__(other = other)

        if not isinstance(other, Torque) and not isinstance(other, float) and not isinstance(other, int) \
                and not isinstance(other, InertiaMoment):
            raise TypeError(f'It is not allowed to divide a {self.__class__.__name__} by a {other.__class__.__name__}.')

        if isinstance(other, Torque):
            return self.__value/other.to(self.__unit).value
        elif isinstance(other, InertiaMoment):
            return AngularAcceleration(value = self.to('Nm').value/other.to('kgm^2').value, unit = 'rad/s^2')
        else:
            return Torque(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'Torque') -> bool:
        super().__eq__(other = other)

        if self.__unit == other.unit:
            return self.__value == other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) < COMPARISON_TOLERANCE

    def __ne__(self, other: 'Torque') -> bool:
        super().__ne__(other = other)

        if self.__unit == other.unit:
            return self.__value != other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) > COMPARISON_TOLERANCE

    def __gt__(self, other: 'Torque') -> bool:
        super().__gt__(other = other)

        if self.__unit == other.unit:
            return self.__value > other.value
        else:
            return self.__value - other.to(self.__unit).value > COMPARISON_TOLERANCE

    def __ge__(self, other: 'Torque') -> bool:
        super().__ge__(other = other)

        if self.__unit == other.unit:
            return self.__value >= other.value
        else:
            return self.__value - other.to(self.__unit).value >= -COMPARISON_TOLERANCE

    def __lt__(self, other: 'Torque') -> bool:
        super().__lt__(other = other)

        if self.__unit == other.unit:
            return self.__value < other.value
        else:
            return self.__value - other.to(self.__unit).value < -COMPARISON_TOLERANCE

    def __le__(self, other: 'Torque') -> bool:
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

    def to(self, target_unit: str, inplace: bool = False) -> 'Torque':
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
            return Torque(value = target_value, unit = target_unit)


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

        return Time(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: 'Time') -> 'Time':
        super().__sub__(other = other)

        return Time(value = self.__value - other.to(self.__unit).value, unit = self.__unit)

    def __mul__(self, other: Union['AngularAcceleration', 'AngularSpeed', float, int]) -> Union['AngularPosition', 'AngularSpeed', 'Time']:
        super().__mul__(other = other)

        if not isinstance(other, AngularAcceleration) and not isinstance(other, AngularSpeed) \
                and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {self.__class__.__name__} by a '
                            f'{other.__class__.__name__}.')

        if isinstance(other, AngularAcceleration):
            return AngularSpeed(value = self.to('sec').value*other.to('rad/s^2').value, unit = 'rad/s')
        elif isinstance(other, AngularSpeed):
            return AngularPosition(value = self.to('sec').value*other.to('rad/s').value, unit = 'rad')
        else:
            return Time(value = self.__value*other, unit = self.__unit)

    def __rmul__(self, other: Union['AngularAcceleration', 'AngularSpeed', float, int]) -> Union['AngularPosition', 'AngularSpeed', 'Time']:
        super().__rmul__(other = other)

        if not isinstance(other, AngularAcceleration) and not isinstance(other, AngularSpeed) \
                and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to multiply a {other.__class__.__name__} by a '
                            f'{self.__class__.__name__}.')

        if isinstance(other, AngularAcceleration):
            return AngularSpeed(value = self.to('sec').value*other.to('rad/s^2').value, unit = 'rad/s')
        elif isinstance(other, AngularSpeed):
            return AngularPosition(value = self.to('sec').value*other.to('rad/s').value, unit = 'rad')
        else:
            return Time(value = self.__value*other, unit = self.__unit)

    def __truediv__(self, other: Union['Time', float, int]) -> Union['Time', float]:
        super().__truediv__(other = other)

        if not isinstance(other, Time) and not isinstance(other, float) and not isinstance(other, int):
            raise TypeError(f'It is not allowed to divide a {self.__class__.__name__} by a {other.__class__.__name__}.')

        if isinstance(other, Time):
            return self.__value/other.to(self.__unit).value
        else:
            return Time(value = self.__value/other, unit = self.__unit)

    def __eq__(self, other: 'Time') -> bool:
        super().__eq__(other = other)

        if self.__unit == other.unit:
            return self.__value == other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) < COMPARISON_TOLERANCE

    def __ne__(self, other: 'Time') -> bool:
        super().__ne__(other = other)

        if self.__unit == other.unit:
            return self.__value != other.value
        else:
            return fabs(self.__value - other.to(self.__unit).value) > COMPARISON_TOLERANCE

    def __gt__(self, other: 'Time') -> bool:
        super().__gt__(other = other)

        if self.__unit == other.unit:
            return self.__value > other.value
        else:
            return self.__value - other.to(self.__unit).value > COMPARISON_TOLERANCE

    def __ge__(self, other: 'Time') -> bool:
        super().__ge__(other = other)

        if self.__unit == other.unit:
            return self.__value >= other.value
        else:
            return self.__value - other.to(self.__unit).value >= -COMPARISON_TOLERANCE

    def __lt__(self, other: 'Time') -> bool:
        super().__lt__(other = other)

        if self.__unit == other.unit:
            return self.__value < other.value
        else:
            return self.__value - other.to(self.__unit).value < -COMPARISON_TOLERANCE

    def __le__(self, other: 'Time') -> bool:
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

    def to(self, target_unit: str, inplace: bool = False) -> 'Time':
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
            return Time(value = target_value, unit = target_unit)


class TimeInterval(Time):

    def __init__(self, value: Union[float, int], unit: str):
        super().__init__(value = value, unit = unit)

        if value <= 0:
            raise ValueError("Parameter 'value' must be positive.")

        self.__value = value
        self.__unit = unit

    def __add__(self, other: Union['Time', 'TimeInterval']) -> Union['Time', 'TimeInterval']:
        super().__add__(other = other)

        if isinstance(other, TimeInterval):
            return TimeInterval(value = self.__value + other.to(self.__unit).value, unit = self.__unit)
        else:
            return Time(value = self.__value + other.to(self.__unit).value, unit = self.__unit)

    def __sub__(self, other: Union['Time', 'TimeInterval']) -> Union['Time', 'TimeInterval']:
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
