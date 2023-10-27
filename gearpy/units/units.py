from math import pi, fabs
from typing import Union
from .unit_base import UnitBase


COMPARISON_TOLERANCE = 1e-12


class AngularPosition(UnitBase):
    r"""``gearpy.units.units.AngularPosition`` object.

    Attributes
    ----------
    :py:attr:`unit` : str
        Symbol of the unit of measurement for angular position.
    :py:attr:`value` : float or int
        Angular position numerical value.

    Methods
    -------
    :py:meth:`to`
        Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {'rad': 1,
               'deg': pi/180,
               'arcmin': pi/180/60,
               'arcsec': pi/180/60/60,
               'rot': 2*pi}

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
        """Angular position numerical value. The relative unit is expressed by the ``unit`` property.

        Returns
        -------
        float or int
            Angular position numerical value.

        Raises
        ------
        TypeError
            If ``value`` is not a float or an integer.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for angular position. It must be a string.
        Available units are:

            - ``'rad'`` for radian,
            - ``'deg'`` for degree,
            - ``'arcmin'`` for minute of arc,
            - ``'armsec'`` for second of arc,
            - ``'rot'`` for rotation.

        Returns
        -------
        str
            Symbol of the unit of measurement for angular position.

        Raises
        ------
        TypeError
            If ``unit`` is not a string.
        KeyError
            If the ``unit`` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'AngularPosition':
        """Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
        If ``inplace`` is ``True``, it overrides actual ``value`` and ``unit``, otherwise it returns a new instance with
        the converted ``value`` and the ``target_unit`` as ``unit``.

        Parameters
        ----------
        target_unit : str
            Target unit to which convert the current value.
        inplace : bool, optional
            Whether or not to override the current instance value. Default is ``False``, so it does not override the
            current value.

        Returns
        -------
        AngularPosition
            Converted angular position.

        Raises
        ------
        TypeError
            - If ``target_unit`` is not a string,
            - if ``inplace`` is not a bool.
        KeyError
            If the ``target_unit`` is not among available ones.

        Examples
        --------
        ``AngularPosition`` instantiation.

        >>> from gearpy.units import AngularPosition
        >>> p = AngularPosition(180, 'deg')
        >>> p
        ... 180 deg

        Conversion from degree to radian with ``inplace = False`` by default, so it does not override the current value.

        >>> p.to('rad')
        ... 3.141592653589793 rad
        >>> p
        ... 180 deg

        Conversion from degree to minute of arc with ``inplace = True``, in order to override the current value.

        >>> p.to('arcmin', inplace = True)
        ... 10800.0 arcmin
        >>> p
        ... 10800.0 arcmin
        """
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
    r"""``gearpy.units.units.AngularSpeed`` object.

    Attributes
    ----------
    :py:attr:`unit` : str
        Symbol of the unit of measurement for angular speed.
    :py:attr:`value` : float or int
        Angular speed numerical value.

    Methods
    -------
    :py:meth:`to`
        Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
    """

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
        """Angular speed numerical value. The relative unit is expressed by the ``unit`` property.

        Returns
        -------
        float or int
            Angular speed numerical value.

        Raises
        ------
        TypeError
            If ``value`` is not a float or an integer.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for angular speed. It must be a string.
        Available units are:

            - ``'rad/s'`` for radian per second,
            - ``'rad/min'`` for radian per minute,
            - ``'rad/h'`` for radian per hour,
            - ``'deg/s'`` for degree per second,
            - ``'deg/min'`` for degree per minute,
            - ``'deg/h'`` for degree per hour,
            - ``'rps'`` for revolutions per second,
            - ``'rpm'`` for revolutions per minute,
            - ``'rph'`` for revolutions per hour.

        Returns
        -------
        str
            Symbol of the unit of measurement for angular speed.

        Raises
        ------
        TypeError
            If ``unit`` is not a string.
        KeyError
            If the ``unit`` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'AngularSpeed':
        """Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
        If ``inplace`` is ``True``, it overrides actual ``value`` and ``unit``, otherwise it returns a new instance with
        the converted ``value`` and the ``target_unit`` as ``unit``.

        Parameters
        ----------
        target_unit : str
            Target unit to which convert the current value.
        inplace : bool, optional
            Whether or not to override the current instance value. Default is ``False``, so it does not override the
            current value.

        Returns
        -------
        AngularSpeed
            Converted angular speed.

        Raises
        ------
        TypeError
            - If ``target_unit`` is not a string,
            - if ``inplace`` is not a bool.
        KeyError
            If the ``target_unit`` is not among available ones.

        Examples
        --------
        ``AngularSpeed`` instantiation.

        >>> from gearpy.units import AngularSpeed
        >>> s = AngularSpeed(1000, 'rpm')
        >>> s
        ... 1000 rpm

        Conversion from revolutions per minute to radian per second with ``inplace = False`` by default, so it does not
        override the current value.

        >>> s.to('rad/s')
        ... 104.71975511965977 rad/s
        >>> s
        ... 1000 rpm

        Conversion from revolutions per minute to revolutions per second with ``inplace = True``, in order to override
        the current value.

        >>> s.to('rps', inplace = True)
        ... 16.666666666666664 rps
        >>> s
        ... 16.666666666666664 rps
        """
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
    r"""``gearpy.units.units.AngularAcceleration`` object.

    Attributes
    ----------
    :py:attr:`unit` : str
        Symbol of the unit of measurement for angular acceleration.
    :py:attr:`value` : float or int
        Angular acceleration numerical value.

    Methods
    -------
    :py:meth:`to`
        Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {'rad/s^2': 1,
               'deg/s^2': pi/180,
               'rot/s^2': 2*pi}

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
        """Angular acceleration numerical value. The relative unit is expressed by the ``unit`` property.

        Returns
        -------
        float or int
            Angular acceleration numerical value.

        Raises
        ------
        TypeError
            If ``value`` is not a float or an integer.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for angular acceleration. It must be a string.
        Available units are:

            - ``'rad/s^2'`` for radian per second squared,
            - ``'deg/s^2'`` for degree per second squared,
            - ``'rot/s^2'`` for rotation per second squared.

        Returns
        -------
        str
            Symbol of the unit of measurement for angular acceleration.

        Raises
        ------
        TypeError
            If ``unit`` is not a string.
        KeyError
            If the ``unit`` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'AngularAcceleration':
        """Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
        If ``inplace`` is ``True``, it overrides actual ``value`` and ``unit``, otherwise it returns a new instance with
        the converted ``value`` and the ``target_unit`` as ``unit``.

        Parameters
        ----------
        target_unit : str
            Target unit to which convert the current value.
        inplace : bool, optional
            Whether or not to override the current instance value. Default is ``False``, so it does not override the
            current value.

        Returns
        -------
        AngularAcceleration
            Converted angular acceleration.

        Raises
        ------
        TypeError
            - If ``target_unit`` is not a string,
            - if ``inplace`` is not a bool.
        KeyError
            If the ``target_unit`` is not among available ones.

        Examples
        --------
        ``AngularAcceleration`` instantiation.

        >>> from gearpy.units import AngularAcceleration
        >>> a = AngularAcceleration(180, 'deg/s^2')
        >>> a
        ... 180 deg/s^2

        Conversion from degree per second squared to radian per second squared with ``inplace = False`` by default, so
        it does not override the current value.

        >>> a.to('rad/s^2')
        ... 3.141592653589793 rad/s^2
        >>> a
        ... 180 deg/s^2

        Conversion from degree per second squared to radian per second squared with ``inplace = True``, in order to
        override the current value.

        >>> a.to('rad/s^2', inplace = True)
        ... 3.141592653589793 rad/s^2
        >>> a
        ... 3.141592653589793 rad/s^2
        """
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
    r"""``gearpy.units.units.InertiaMoment`` object.

    Attributes
    ----------
    :py:attr:`unit` : str
        Symbol of the unit of measurement for moment of inertia.
    :py:attr:`value` : float or int
        Moment of inertia numerical value.

    Methods
    -------
    :py:meth:`to`
        Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {'kgm^2': 1,
               'kgdm^2': 1e-2,
               'kgcm^2': 1e-4,
               'kgmm^2': 1e-6,
               'gm^2': 1e-3,
               'gdm^2': 1e-5,
               'gcm^2': 1e-7,
               'gmm^2': 1e-9}

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
        """Moment of inertia numerical value. The relative unit is expressed by the ``unit`` property. It must be
        positive.

        Returns
        -------
        float or int
            Moment of inertia numerical value.

        Raises
        ------
        TypeError
            If ``value`` is not a float or an integer.
        ValueError
            If ``value`` is not positive.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for moment of inertia. It must be a string.
        Available units are:

            - ``'kgm^2'`` for kilogram-square meter,
            - ``'kgdm^2'`` for kilogram-square decimeter,
            - ``'kgcm^2'`` for kilogram-square centimeter,
            - ``'kgmm^2'`` for kilogram-square millimeter,
            - ``'gm^2'`` for gram-square meter,
            - ``'gdm^2'`` for gram-square decimeter,
            - ``'gcm^2'`` for gram-square centimeter,
            - ``'gmm^2'`` for gram-square millimeter.

        Returns
        -------
        str
            Symbol of the unit of measurement for moment of inertia.

        Raises
        ------
        TypeError
            If ``unit`` is not a string.
        KeyError
            If the ``unit`` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'InertiaMoment':
        """Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
        If ``inplace`` is ``True``, it overrides actual ``value`` and ``unit``, otherwise it returns a new instance with
        the converted ``value`` and the ``target_unit`` as ``unit``.

        Parameters
        ----------
        target_unit : str
            Target unit to which convert the current value.
        inplace : bool, optional
            Whether or not to override the current instance value. Default is ``False``, so it does not override the
            current value.

        Returns
        -------
        InertiaMoment
            Converted moment of inertia.

        Raises
        ------
        TypeError
            - If ``target_unit`` is not a string,
            - if ``inplace`` is not a bool.
        KeyError
            If the ``target_unit`` is not among available ones.

        Examples
        --------
        ``InertiaMoment`` instantiation.

        >>> from gearpy.units import InertiaMoment
        >>> i = InertiaMoment(1, 'kgm^2')
        >>> i
        ... 1 kgm^2

        Conversion from kilogram-square meter to gram-square meter with ``inplace = False`` by default, so it does not
        override the current value.

        >>> i.to('gm^2')
        ... 1000.0 gm^2
        >>> i
        ... 1 kgm^2

        Conversion from kilograms-square meter to gram-square meter with ``inplace = True``, in order to override the
        current value.

        >>> i.to('gm^2', inplace = True)
        ... 1000.0 gm^2
        >>> i
        ... 1000.0 gm^2
        """
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
    r"""``gearpy.units.units.Torque`` object.

    Attributes
    ----------
    :py:attr:`unit` : str
        Symbol of the unit of measurement for torque.
    :py:attr:`value` : float or int
        Torque numerical value.

    Methods
    -------
    :py:meth:`to`
        Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {'Nm': 1,
               'mNm': 1e-3,
               'mNdm': 1e-4,
               'mNcm': 1e-5,
               'mNmm': 1e-6,
               'kNm': 1e3,
               'kNdm': 1e2,
               'kNcm': 1e1,
               'kNmm': 1,
               'kgfm': 9.80665,
               'kgfdm': 9.80665e-1,
               'kgfcm': 9.80665e-2,
               'kgfmm': 9.80665e-3,
               'gfm': 9.80665e-3,
               'gfdm': 9.80665e-4,
               'gfcm': 9.80665e-5,
               'gfmm': 9.80665e-6}

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
        """Torque numerical value. The relative unit is expressed by the ``unit`` property.

        Returns
        -------
        float or int
            Torque numerical value.

        Raises
        ------
        TypeError
            If ``value`` is not a float or an integer.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for Torque. It must be a string.
        Available units are:

            - ``'Nm'`` for newton-meter,
            - ``'mNm'`` for milli-newton-meter,
            - ``'mNdm'`` for milli-newton-decimeter,
            - ``'mNcm'`` for milli-newton-centimeter,
            - ``'mNmm'`` for milli-newton-millimeter,
            - ``'kNm'`` for kilo-newton-meter,
            - ``'kNdm'`` for kilo-newton-decimeter,
            - ``'kNcm'`` for kilo-newton-centimeter,
            - ``'kNmm'`` for kilo-newton-millimeter,
            - ``'kgfm'`` for kilogram force-meter,
            - ``'kgfdm'`` for kilogram force-decimeter,
            - ``'kgfcm'`` for kilogram force-centimeter,
            - ``'kgfmm'`` for kilogram force-millimeter,
            - ``'gfm'`` for gram force-meter,
            - ``'gfdm'`` for gram force-decimeter,
            - ``'gfcm'`` for gram force-centimeter,
            - ``'gfmm'`` for gram force-millimeter.

        Returns
        -------
        str
            Symbol of the unit of measurement for torque.

        Raises
        ------
        TypeError
            If ``unit`` is not a string.
        KeyError
            If the ``unit`` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'Torque':
        """Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
        If ``inplace`` is ``True``, it overrides actual ``value`` and ``unit``, otherwise it returns a new instance with
        the converted ``value`` and the ``target_unit`` as ``unit``.

        Parameters
        ----------
        target_unit : str
            Target unit to which convert the current value.
        inplace : bool, optional
            Whether or not to override the current instance value. Default is ``False``, so it does not override the
            current value.

        Returns
        -------
        Torque
            Converted torque.

        Raises
        ------
        TypeError
            - If ``target_unit`` is not a string,
            - if ``inplace`` is not a bool.
        KeyError
            If the ``target_unit`` is not among available ones.

        Examples
        --------
        ``Torque`` instantiation.

        >>> from gearpy.units import Torque
        >>> T = Torque(1, 'Nm')
        >>> T
        ... 1 Nm

        Conversion from newton-meter to kilogram force-meter with ``inplace = False`` by default, so it does not
        override the current value.

        >>> T.to('kgfm')
        ... 0.10197162129779283 kgfm
        >>> T
        ... 1 Nm

        Conversion from newton-meter to kilogram force-meter with ``inplace = True``, in order to override the current
        value.

        >>> T.to('kgfm', inplace = True)
        ... 0.10197162129779283 kgfm
        >>> T
        ... 0.10197162129779283 kgfm
        """
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
    r"""``gearpy.units.units.Time`` object.

    Attributes
    ----------
    :py:attr:`unit` : str
        Symbol of the unit of measurement for time.
    :py:attr:`value` : float or int
        Time numerical value.

    Methods
    -------
    :py:meth:`to`
        Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {'sec': 1,
               'min': 60,
               'hour': 60*60,
               'ms': 1e-3}

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
        """Time numerical value. The relative unit is expressed by the ``unit`` property.

        Returns
        -------
        float or int
            Time numerical value.

        Raises
        ------
        TypeError
            If ``value`` is not a float or an integer.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for time. It must be a string.
        Available units are:

            - ``'sec'`` for second,
            - ``'min'`` for minute,
            - ``'hour'`` for hour,
            - ``'ms'`` for millisecond.

        Returns
        -------
        str
            Symbol of the unit of measurement for time.

        Raises
        ------
        TypeError
            If ``unit`` is not a string.
        KeyError
            If the ``unit`` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> 'Time':
        """Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
        If ``inplace`` is ``True``, it overrides actual ``value`` and ``unit``, otherwise it returns a new instance with
        the converted ``value`` and the ``target_unit`` as ``unit``.

        Parameters
        ----------
        target_unit : str
            Target unit to which convert the current value.
        inplace : bool, optional
            Whether or not to override the current instance value. Default is ``False``, so it does not override the
            current value.

        Returns
        -------
        Time
            Converted time.

        Raises
        ------
        TypeError
            - If ``target_unit`` is not a string,
            - if ``inplace`` is not a bool.
        KeyError
            If the ``target_unit`` is not among available ones.

        Examples
        --------
        ``Time`` instantiation.

        >>> from gearpy.units import Time
        >>> t = Time(1, 'hour')
        >>> t
        ... 1 hour

        Conversion from hour to second with ``inplace = False`` by default, so it does not override the current value.

        >>> t.to('sec')
        ... 3600.0 sec
        >>> t
        ... 1 hour

        Conversion from hour to second with ``inplace = True``, in order to override the current value.

        >>> t.to('sec', inplace = True)
        ... 3600.0 sec
        >>> t
        ... 3600.0 sec
        """
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
    r"""``gearpy.units.units.TimeInterval`` object.

    Attributes
    ----------
    :py:attr:`unit` : str
        Symbol of the unit of measurement for time interval.
    :py:attr:`value` : float or int
        Time interval numerical value.

    Methods
    -------
    :py:meth:`to`
        Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
    """

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

    @property
    def value(self) -> Union[float, int]:
        """Time interval numerical value. The relative unit is expressed by the ``unit`` property. It must be positive.

        Returns
        -------
        float or int
            Time interval numerical value.

        Raises
        ------
        TypeError
            If ``value`` is not a float or an integer.
        ValueError
            If ``value`` is not positive.
        """
        return super().value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for time interval. It must be a string.
        Available units are:

            - ``'sec'`` for second,
            - ``'min'`` for minute,
            - ``'hour'`` for hour,
            - ``'ms'`` for millisecond.

        Returns
        -------
        str
            Symbol of the unit of measurement for time interval.

        Raises
        ------
        TypeError
            If ``unit`` is not a string.
        KeyError
            If the ``unit`` is not among available ones.
        """
        return super().unit

    def to(self, target_unit: str, inplace: bool = False) -> 'TimeInterval':
        """Converts actual ``value`` to a new value computed using ``target_unit`` as the reference unit of measurement.
        If ``inplace`` is ``True``, it overrides actual ``value`` and ``unit``, otherwise it returns a new instance with
        the converted ``value`` and the ``target_unit`` as ``unit``.

        Parameters
        ----------
        target_unit : str
            Target unit to which convert the current value.
        inplace : bool, optional
            Whether or not to override the current instance value. Default is ``False``, so it does not override the
            current value.

        Returns
        -------
        TimeInterval
            Converted time interval.

        Raises
        ------
        TypeError
            - If ``target_unit`` is not a string,
            - if ``inplace`` is not a bool.
        KeyError
            If the ``target_unit`` is not among available ones.

        Examples
        --------
        ``TimeInterval`` instantiation.

        >>> from gearpy.units import TimeInterval
        >>> dt = TimeInterval(1, 'hour')
        >>> dt
        ... 1 hour

        Conversion from hour to second with ``inplace = False`` by default, so it does not override the current value.

        >>> dt.to('sec')
        ... 3600.0 sec
        >>> dt
        ... 1 hour

        Conversion from hour to second with ``inplace = True``, in order to override the current value.

        >>> dt.to('sec', inplace = True)
        ... 3600.0 sec
        >>> dt
        ... 3600.0 sec
        """
        converted = super().to(target_unit = target_unit, inplace = inplace)

        if inplace:
            self.__value = converted.value
            self.__unit = converted.unit
            return self
        else:
            return TimeInterval(value = converted.value, unit = converted.unit)
