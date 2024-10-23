from __future__ import annotations
from math import pi, sin, cos, tan
from typing import Optional
from .unit_base import UnitBase


class AngularPosition(UnitBase):
    r""":py:class:`AngularPosition <gearpy.units.units.AngularPosition>`
    object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for angular position.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Angular position numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    :py:meth:`sin`
        It computes the sine of the angular position at a given frequency.
    :py:meth:`cos`
        It computes the cosine of the angular position at a given frequency.
    :py:meth:`tan`
        It computes the tangent of the angular position at a given frequency.
    """

    __UNITS = {
        'rad': 1,
        'deg': pi/180,
        'arcmin': pi/180/60,
        'arcsec': pi/180/60/60,
        'rot': 2*pi
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        self.__value = value
        self.__unit = unit

    def __mul__(self, other: float | int) -> AngularPosition:
        super().__mul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply an {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        return AngularPosition(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> AngularPosition:
        super().__rmul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by an {self.__class__.__name__}."
            )

        return AngularPosition(value=self.__value*other, unit=self.__unit)

    def __truediv__(
        self,
        other: AngularPosition | float | int
    ) -> AngularPosition | float:
        super().__truediv__(other=other)

        if not isinstance(other, AngularPosition | float | int):
            raise TypeError(
                f"It is not allowed to divide an {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, AngularPosition):
            return self.__value/other.to(self.__unit).value
        else:
            return AngularPosition(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Angular position numerical value. The relative unit is expressed by
        the :py:attr:`unit` property.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Angular position numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for angular position. It must be a
        :py:class:`str`. Available units are:

        - ``'rad'`` for radian,
        - ``'deg'`` for degree,
        - ``'arcmin'`` for minute of arc,
        - ``'arcsec'`` for second of arc,
        - ``'rot'`` for rotation.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for angular position.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> AngularPosition:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`
            Converted angular position.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``AngularPosition`` instantiation.

           >>> from gearpy.units import AngularPosition
           >>> p = AngularPosition(180, 'deg')
           >>> p
           180 deg

           Conversion from degree to radian with ``inplace=False`` by
           default, so it does not override the current value.

           >>> p.to('rad')
           3.141592653589793 rad
           >>> p
           180 deg

           Conversion from degree to minute of arc with ``inplace=True``, in
           order to override the current value.

           >>> p.to('arcmin', inplace=True)
           10800.0 arcmin
           >>> p
           10800.0 arcmin
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return AngularPosition(value=target_value, unit=target_unit)

    def sin(self, frequency: Optional[float | int] = 1/2/pi) -> float:
        r"""It computes the sine of the angular position at a given frequency.

        Parameters
        ----------
        ``frequency`` : :py:class:`float` or :py:class:`int`, optional
            Frequency to multiply by before computing the sine. Default is
            :math:`\frac{1}{2 \pi}`.

        Returns
        -------
        :py:class:`float`
            Computed sine of the angular position.
        """
        return sin(2*pi*frequency*self.to('rad').value)

    def cos(self, frequency: Optional[float | int] = 1/2/pi) -> float:
        r"""It computes the cosine of the angular position at a given
        frequency.

        Parameters
        ----------
        ``frequency`` : :py:class:`float` or :py:class:`int`, optional
            Frequency to multiply by before computing the cosine. Default is
            :math:`\frac{1}{2 \pi}`.

        Returns
        -------
        :py:class:`float`
            Computed cosine of the angular position.
        """
        return cos(2*pi*frequency*self.to('rad').value)

    def tan(self, frequency: Optional[float | int] = 1/2/pi) -> float:
        r"""It computes the tangent of the angular position at a given
        frequency.

        Parameters
        ----------
        ``frequency`` : :py:class:`float` or :py:class:`int`, optional
            Frequency to multiply by before computing the tangent. Default is
            :math:`\frac{1}{2 \pi}`.

        Returns
        -------
        :py:class:`float`
            Computed tangent of the angular position.
        """
        return tan(2*pi*frequency*self.to('rad').value)


class Angle(AngularPosition):
    r""":py:class:`Angle <gearpy.units.units.Angle>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for angle.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Angle numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    :py:meth:`sin`
        It computes the sine of the angle at a given frequency.
    :py:meth:`cos`
        It computes the cosine of the angle at a given frequency.
    :py:meth:`tan`
        It computes the tangent of the angle at a given frequency.
    """

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if value < 0:
            raise ValueError("Parameter 'value' must be positive or null.")

        self.__value = value
        self.__unit = unit

    def __add__(
        self,
        other: AngularPosition | Angle
    ) -> AngularPosition | Angle:
        super().__add__(other=other)

        if isinstance(other, Angle):
            return Angle(
                value=self.__value + other.to(self.__unit).value,
                unit=self.__unit
            )
        else:
            return AngularPosition(
                value=self.__value + other.to(self.__unit).value,
                unit=self.__unit
            )

    def __sub__(
        self,
        other: AngularPosition | Angle
    ) -> AngularPosition | Angle:
        super().__sub__(other=other)

        if isinstance(other, Angle):
            return Angle(
                value=self.__value - other.to(self.__unit).value,
                unit=self.__unit
            )
        else:
            return AngularPosition(
                value=self.__value + other.to(self.__unit).value,
                unit=self.__unit
            )

    def __mul__(self, other: float | int) -> Angle:
        super().__mul__(other=other)

        if other < 0:
            raise ValueError(
                "Cannot perform a multiplication by a negative number."
            )

        return Angle(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> Angle:
        super().__rmul__(other=other)

        if other < 0:
            raise ValueError(
                "Cannot perform a multiplication by a negative number."
            )

        return Angle(value=self.__value*other, unit=self.__unit)

    def __truediv__(
        self,
        other: AngularPosition | float | int
    ) -> AngularPosition | float:
        super().__truediv__(other=other)

        if isinstance(other, AngularPosition):
            return self.__value/other.to(self.__unit).value
        else:
            return Angle(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Angle numerical value. The relative unit is expressed by the
        :py:attr:`unit` property. It must be positive or null.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Angle numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
           ``ValueError``
               If :py:attr:`value` is negative.
        """
        return super().value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for angle. It must be a
        :py:class:`str`. Available units are:

        - ``'rad'`` for radian,
        - ``'deg'`` for degree,
        - ``'arcmin'`` for minute of arc,
        - ``'arcsec'`` for second of arc,
        - ``'rot'`` for rotation.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for angle.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return super().unit

    def to(self, target_unit: str, inplace: bool = False) -> Angle:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`Angle <gearpy.units.units.Angle>`
            Converted angle.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``Angle`` instantiation.

           >>> from gearpy.units import Angle
           >>> a = Angle(180, 'deg')
           >>> a
           180 deg

           Conversion from degree to radian with ``inplace=False`` by default,
           so it does not override the current value.

           >>> a.to('rad')
           3.141592653589793 rad
           >>> a
           180 deg

           Conversion from degree to minute of arc with ``inplace=True``, in
           order to override the current value.

           >>> a.to('arcmin', inplace=True)
           10800.0 arcmin
           >>> a
           10800.0 arcmin
        """
        converted = super().to(target_unit=target_unit, inplace=inplace)

        if inplace:
            self.__value = converted.value
            self.__unit = converted.unit
            return self
        else:
            return Angle(value=converted.value, unit=converted.unit)

    def sin(self, frequency: Optional[float | int] = 1/2/pi) -> float:
        r"""It computes the sine of the angle at a given frequency.

        Parameters
        ----------
        ``frequency`` : :py:class:`float` or :py:class:`int`, optional
            Frequency to multiply by before computing the sine. Default is
            :math:`\frac{1}{2 \pi}`.

        Returns
        -------
        :py:class:`float`
            Computed sine of the angle.
        """
        return super().sin(frequency=frequency)

    def cos(self, frequency: Optional[float | int] = 1/2/pi) -> float:
        r"""It computes the cosine of the angle at a given frequency.

        Parameters
        ----------
        ``frequency`` : :py:class:`float` or :py:class:`int`, optional
            Frequency to multiply by before computing the cosine. Default is
            :math:`\frac{1}{2 \pi}`.

        Returns
        -------
        :py:class:`float`
            Computed cosine of the angle.
        """
        return super().cos(frequency=frequency)

    def tan(self, frequency: Optional[float | int] = 1/2/pi) -> float:
        r"""It computes the tangent of the angle at a given frequency.

        Parameters
        ----------
        ``frequency`` : :py:class:`float` or :py:class:`int`, optional
            Frequency to multiply by before computing the tangent. Default is
            :math:`\frac{1}{2 \pi}`.

        Returns
        -------
        :py:class:`float`
            Computed tangent of the angle.
        """
        return super().tan(frequency=frequency)


class AngularSpeed(UnitBase):
    r""":py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for angular speed.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Angular speed numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {
        'rad/s': 1,
        'rad/min': 1/60,
        'rad/h': 1/60/60,
        'deg/s': pi/180,
        'deg/min': pi/180/60,
        'deg/h': pi/180/60/60,
        'rps': 2*pi,
        'rpm': 2*pi/60,
        'rph': 2*pi/60/60
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        self.__value = value
        self.__unit = unit

    def __mul__(
        self,
        other: Time | float | int
    ) -> AngularPosition | AngularSpeed:
        super().__mul__(other=other)

        if not isinstance(other, Time | float | int):
            raise TypeError(
                f"It is not allowed to multiply a {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        if isinstance(other, Time):
            return AngularPosition(
                value=self.to('rad/s').value*other.to('sec').value,
                unit='rad'
            )
        else:
            return AngularSpeed(value=self.__value*other, unit=self.__unit)

    def __rmul__(
        self,
        other: Time | float | int
    ) -> AngularPosition | AngularSpeed:
        super().__rmul__(other=other)

        if not isinstance(other, Time | float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by a {self.__class__.__name__}."
            )

        if isinstance(other, Time):
            return AngularPosition(
                value=self.to('rad/s').value*other.to('sec').value,
                unit='rad'
            )
        else:
            return AngularSpeed(value=self.__value*other, unit=self.__unit)

    def __truediv__(
        self,
        other: AngularSpeed | float | int
    ) -> AngularSpeed | float:
        super().__truediv__(other=other)

        if not isinstance(other, AngularSpeed | float | int):
            raise TypeError(
                f"It is not allowed to divide a {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, AngularSpeed):
            return self.__value/other.to(self.__unit).value
        else:
            return AngularSpeed(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Angular speed numerical value. The relative unit is expressed by
        the :py:attr:`unit` property.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Angular speed numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for angular speed. It must be a
        :py:class:`str`.
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
        :py:class:`str`
            Symbol of the unit of measurement for angular speed.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> AngularSpeed:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`
            Converted angular speed.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``AngularSpeed`` instantiation.

           >>> from gearpy.units import AngularSpeed
           >>> s = AngularSpeed(1000, 'rpm')
           >>> s
           1000 rpm

           Conversion from revolutions per minute to radian per second with
           ``inplace=False`` by default, so it does not override the current
           value.

           >>> s.to('rad/s')
           104.71975511965977 rad/s
           >>> s
           1000 rpm

           Conversion from revolutions per minute to revolutions per second
           with ``inplace=True``, in order to override the current value.

           >>> s.to('rps', inplace=True)
           16.666666666666664 rps
           >>> s
           16.666666666666664 rps
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return AngularSpeed(value=target_value, unit=target_unit)


class AngularAcceleration(UnitBase):
    r""":py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`
    object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for angular acceleration.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Angular acceleration numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of
        measurement.
    """

    __UNITS = {
        'rad/s^2': 1,
        'deg/s^2': pi/180,
        'rot/s^2': 2*pi
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        self.__value = value
        self.__unit = unit

    def __mul__(
        self,
        other: Time | float | int
    ) -> AngularAcceleration | AngularSpeed:
        super().__mul__(other=other)

        if not isinstance(other, Time | float | int):
            raise TypeError(
                f"It is not allowed to multiply an {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        if isinstance(other, Time):
            return AngularSpeed(
                value=self.to('rad/s^2').value*other.to('sec').value,
                unit='rad/s'
            )
        else:
            return AngularAcceleration(
                value=self.__value*other,
                unit=self.__unit
            )

    def __rmul__(
        self,
        other: Time | float | int
    ) -> AngularAcceleration | AngularSpeed:
        super().__rmul__(other=other)

        if not isinstance(other, Time | float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by an {self.__class__.__name__}."
            )

        if isinstance(other, Time):
            return AngularSpeed(
                value=self.to('rad/s^2').value*other.to('sec').value,
                unit='rad/s'
            )
        else:
            return AngularAcceleration(
                value=self.__value*other,
                unit=self.__unit
            )

    def __truediv__(
        self,
        other: AngularAcceleration | float | int
    ) -> AngularAcceleration | float:
        super().__truediv__(other=other)

        if not isinstance(other, AngularAcceleration | float | int):
            raise TypeError(
                f"It is not allowed to divide an {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, AngularAcceleration):
            return self.__value/other.to(self.__unit).value
        else:
            return AngularAcceleration(
                value=self.__value/other,
                unit=self.__unit
            )

    @property
    def value(self) -> float | int:
        """Angular acceleration numerical value. The relative unit is
        expressed by the :py:attr:`unit` property.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Angular acceleration numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for angular acceleration. It must
        be a :py:class:`str`. Available units are:

        - ``'rad/s^2'`` for radian per second squared,
        - ``'deg/s^2'`` for degree per second squared,
        - ``'rot/s^2'`` for rotation per second squared.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for angular acceleration.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(
        self,
        target_unit: str,
        inplace: bool = False
    ) -> AngularAcceleration:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`
            Converted angular acceleration.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``AngularAcceleration`` instantiation.

           >>> from gearpy.units import AngularAcceleration
           >>> a = AngularAcceleration(180, 'deg/s^2')
           >>> a
           180 deg/s^2

           Conversion from degree per second squared to radian per second
           squared with ``inplace=False`` by default, so it does not override
           the current value.

           >>> a.to('rad/s^2')
           3.141592653589793 rad/s^2
           >>> a
           180 deg/s^2

           Conversion from degree per second squared to radian per second
           squared with ``inplace=True``, in order to override the current
           value.

           >>> a.to('rad/s^2', inplace=True)
           3.141592653589793 rad/s^2
           >>> a
           3.141592653589793 rad/s^2
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return AngularAcceleration(value=target_value, unit=target_unit)


class InertiaMoment(UnitBase):
    r""":py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for moment of inertia.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Moment of inertia numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {
        'kgm^2': 1,
        'kgdm^2': 1e-2,
        'kgcm^2': 1e-4,
        'kgmm^2': 1e-6,
        'gm^2': 1e-3,
        'gdm^2': 1e-5,
        'gcm^2': 1e-7,
        'gmm^2': 1e-9
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        if value <= 0:
            raise ValueError("Parameter 'value' must be positive.")

        self.__value = value
        self.__unit = unit

    def __mul__(self, other: float | int) -> InertiaMoment:
        super().__mul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply an {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        if other <= 0:
            raise ValueError(
                "Cannot perform a multiplication by a negative number or by "
                "zero."
            )

        return InertiaMoment(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> InertiaMoment:
        super().__rmul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by an {self.__class__.__name__}."
            )

        if other <= 0:
            raise ValueError(
                "Cannot perform a multiplication by a negative number or by "
                "zero."
            )

        return InertiaMoment(value=self.__value*other, unit=self.__unit)

    def __truediv__(
        self,
        other: InertiaMoment | float | int
    ) -> InertiaMoment | float:
        super().__truediv__(other=other)

        if not isinstance(other, InertiaMoment | float | int):
            raise TypeError(
                f"It is not allowed to divide an {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, InertiaMoment):
            return self.__value/other.to(self.__unit).value
        else:
            return InertiaMoment(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Moment of inertia numerical value. The relative unit is expressed
        by the :py:attr:`unit` property. It must be positive.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Moment of inertia numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
           ``ValueError``
               If :py:attr:`value` is negative or null.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for moment of inertia. It must be
        a :py:class:`str`. Available units are:

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
        :py:class:`str`
            Symbol of the unit of measurement for moment of inertia.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> InertiaMoment:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`
            Converted moment of inertia.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``InertiaMoment`` instantiation.

           >>> from gearpy.units import InertiaMoment
           >>> i = InertiaMoment(1, 'kgm^2')
           >>> i
           1 kgm^2

           Conversion from kilogram-square meter to gram-square meter with
           ``inplace=False`` by default, so it does not override the current
           value.

           >>> i.to('gm^2')
           1000.0 gm^2
           >>> i
           1 kgm^2

           Conversion from kilograms-square meter to gram-square meter with
           ``inplace=True``, in order to override the current value.

           >>> i.to('gm^2', inplace=True)
           1000.0 gm^2
           >>> i
           1000.0 gm^2
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return InertiaMoment(value=target_value, unit=target_unit)


class Torque(UnitBase):
    r""":py:class:`Torque <gearpy.units.units.Torque>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for torque.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Torque numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {
        'Nm': 1,
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
        'gfmm': 9.80665e-6
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        self.__value = value
        self.__unit = unit

    def __mul__(self, other: float | int) -> Torque:
        super().__mul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply a {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        return Torque(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> Torque:
        super().__rmul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by a {self.__class__.__name__}."
            )

        return Torque(value=self.__value*other, unit=self.__unit)

    def __truediv__(
        self,
        other: InertiaMoment | Length | Torque | float | int
    ) -> AngularAcceleration | Force | float | Torque:
        super().__truediv__(other=other)

        if not isinstance(
            other,
            InertiaMoment | Length | Torque | float | int
        ):
            raise TypeError(
                f"It is not allowed to divide a {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, InertiaMoment):
            return AngularAcceleration(
                value=self.to('Nm').value/other.to('kgm^2').value,
                unit='rad/s^2'
            )
        elif isinstance(other, Length):
            return Force(
                value=self.to('Nm').value/other.to('m').value,
                unit='N'
            )
        elif isinstance(other, Torque):
            return self.__value/other.to(self.__unit).value
        else:
            return Torque(
                value=self.__value/other,
                unit=self.__unit
            )

    @property
    def value(self) -> float | int:
        """Torque numerical value. The relative unit is expressed by the
        :py:attr:`unit` property.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Torque numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for Torque. It must be a
        :py:class:`str`. Available units are:

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
        :py:class:`str`
            Symbol of the unit of measurement for torque.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> Torque:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Converted torque.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``Torque`` instantiation.

           >>> from gearpy.units import Torque
           >>> T = Torque(1, 'Nm')
           >>> T
           1 Nm

           Conversion from newton-meter to kilogram force-meter with
           ``inplace=False`` by default, so it does not override the current
           value.

           >>> T.to('kgfm')
           0.10197162129779283 kgfm
           >>> T
           1 Nm

           Conversion from newton-meter to kilogram force-meter with
           ``inplace=True``, in order to override the current value.

           >>> T.to('kgfm', inplace=True)
           0.10197162129779283 kgfm
           >>> T
           0.10197162129779283 kgfm
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return Torque(value=target_value, unit=target_unit)


class Time(UnitBase):
    r""":py:class:`Time <gearpy.units.units.Time>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for time.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Time numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {
        'sec': 1,
        'min': 60,
        'hour': 60*60,
        'ms': 1e-3
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        self.__value = value
        self.__unit = unit

    def __mul__(
        self,
        other: AngularAcceleration | AngularSpeed | float | int
    ) -> AngularPosition | AngularSpeed | Time:
        super().__mul__(other=other)

        if not isinstance(
            other,
            AngularAcceleration | AngularSpeed | float | int
        ):
            raise TypeError(
                f"It is not allowed to multiply a {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        if isinstance(other, AngularAcceleration):
            return AngularSpeed(
                value=self.to('sec').value*other.to('rad/s^2').value,
                unit='rad/s'
            )
        elif isinstance(other, AngularSpeed):
            return AngularPosition(
                value=self.to('sec').value*other.to('rad/s').value,
                unit='rad'
            )
        else:
            return Time(value=self.__value*other, unit=self.__unit)

    def __rmul__(
        self,
        other: AngularAcceleration | AngularSpeed | float | int
    ) -> AngularPosition | AngularSpeed | Time:
        super().__rmul__(other=other)

        if not isinstance(
            other,
            AngularAcceleration | AngularSpeed | float | int
        ):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by a {self.__class__.__name__}."
            )

        if isinstance(other, AngularAcceleration):
            return AngularSpeed(
                value=self.to('sec').value*other.to('rad/s^2').value,
                unit='rad/s'
            )
        elif isinstance(other, AngularSpeed):
            return AngularPosition(
                value=self.to('sec').value*other.to('rad/s').value,
                unit='rad'
            )
        else:
            return Time(value=self.__value*other, unit=self.__unit)

    def __truediv__(self, other: Time | float | int) -> Time | float:
        super().__truediv__(other=other)

        if not isinstance(other, Time | float | int):
            raise TypeError(
                f"It is not allowed to divide a {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        if isinstance(other, Time):
            return self.__value/other.to(self.__unit).value
        else:
            return Time(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Time numerical value. The relative unit is expressed by the
        :py:attr:`unit` property.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Time numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for time. It must be a
        :py:class:`str`. Available units are:

        - ``'sec'`` for second,
        - ``'min'`` for minute,
        - ``'hour'`` for hour,
        - ``'ms'`` for millisecond.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for time.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> Time:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`Time <gearpy.units.units.Time>`
            Converted time.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``Time`` instantiation.

           >>> from gearpy.units import Time
           >>> t = Time(1, 'hour')
           >>> t
           1 hour

           Conversion from hour to second with ``inplace=False`` by default, so
           it does not override the current
           value.

           >>> t.to('sec')
           3600.0 sec
           >>> t
           1 hour

           Conversion from hour to second with ``inplace=True``, in order to
           override the current value.

           >>> t.to('sec', inplace=True)
           3600.0 sec
           >>> t
           3600.0 sec
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return Time(value=target_value, unit=target_unit)


class TimeInterval(Time):
    r""":py:class:`TimeInterval <gearpy.units.units.TimeInterval>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for time interval.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Time interval numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if value <= 0:
            raise ValueError("Parameter 'value' must be positive.")

        self.__value = value
        self.__unit = unit

    def __add__(self, other: Time | TimeInterval) -> Time | TimeInterval:
        super().__add__(other=other)

        if isinstance(other, TimeInterval):
            return TimeInterval(
                value=self.__value + other.to(self.__unit).value,
                unit=self.__unit
            )
        else:
            return Time(
                value=self.__value + other.to(self.__unit).value,
                unit=self.__unit
            )

    def __sub__(self, other: Time | TimeInterval) -> Time | TimeInterval:
        super().__sub__(other=other)

        if isinstance(other, TimeInterval):
            return TimeInterval(
                value=self.__value - other.to(self.__unit).value,
                unit=self.__unit
            )
        else:
            return Time(
                value=self.__value + other.to(self.__unit).value,
                unit=self.__unit
            )

    def __mul__(self, other: float | int) -> TimeInterval:
        super().__mul__(other=other)

        if other <= 0:
            raise ValueError(
                "Cannot perform a multiplication by a negative number or by "
                "zero."
            )

        return TimeInterval(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> TimeInterval:
        super().__rmul__(other=other)

        if other <= 0:
            raise ValueError(
                "Cannot perform a multiplication by a negative number or by "
                "zero."
            )

        return TimeInterval(value=self.__value*other, unit=self.__unit)

    def __truediv__(self, other: Time | float | int) -> Time | float:
        super().__truediv__(other=other)

        if isinstance(other, Time):
            return self.__value/other.to(self.__unit).value
        else:
            return TimeInterval(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Time interval numerical value. The relative unit is expressed by the
        :py:attr:`unit` property. It must be positive.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Time interval numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
           ``ValueError``
               If :py:attr:`value` is negative or null.
        """
        return super().value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for time interval. It must be a
        :py:class:`str`. Available units are:

        - ``'sec'`` for second,
        - ``'min'`` for minute,
        - ``'hour'`` for hour,
        - ``'ms'`` for millisecond.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for time interval.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return super().unit

    def to(self, target_unit: str, inplace: bool = False) -> TimeInterval:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`TimeInterval <gearpy.units.units.TimeInterval>`
            Converted time interval.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``TimeInterval`` instantiation.

           >>> from gearpy.units import TimeInterval
           >>> dt = TimeInterval(1, 'hour')
           >>> dt
           1 hour

           Conversion from hour to second with ``inplace=False`` by default, so
           it does not override the current value.

           >>> dt.to('sec')
           3600.0 sec
           >>> dt
           1 hour

           Conversion from hour to second with ``inplace=True``, in order to
           override the current value.

           >>> dt.to('sec', inplace=True)
           3600.0 sec
           >>> dt
           3600.0 sec
        """
        converted = super().to(target_unit=target_unit, inplace=inplace)

        if inplace:
            self.__value = converted.value
            self.__unit = converted.unit
            return self
        else:
            return TimeInterval(value=converted.value, unit=converted.unit)


class Length(UnitBase):
    r""":py:class:`Length <gearpy.units.units.Length>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for length.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Length numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {
        'm': 1,
        'dm': 1e-1,
        'cm': 1e-2,
        'mm': 1e-3
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        if value <= 0:
            raise ValueError("Parameter 'value' must be positive.")

        self.__value = value
        self.__unit = unit

    def __mul__(self, other: Length | float | int) -> Surface | Length:
        super().__mul__(other=other)

        if not isinstance(other, Length | float | int):
            raise TypeError(
                f"It is not allowed to multiply an {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        if isinstance(other, Length):
            return Surface(
                value=self.to('m').value*other.to('m').value,
                unit='m^2'
            )
        else:
            return Length(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> Length:
        super().__rmul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by an {self.__class__.__name__}."
            )

        return Length(value=self.__value*other, unit=self.__unit)

    def __truediv__(self, other: Length | float | int) -> Length | float:
        super().__truediv__(other=other)

        if not isinstance(other, Length | float | int):
            raise TypeError(
                f"It is not allowed to divide an {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, Length):
            return self.__value/other.to(self.__unit).value
        else:
            return Length(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Length numerical value. The relative unit is expressed by the
        :py:attr:`unit` property. It must be positive.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Length numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
           ``ValueError``
               If :py:attr:`value` is negative or null.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for length. It must be a
        :py:class:`str`. Available units are:

        - ``'m'`` for meter,
        - ``'dm'`` for decimeter,
        - ``'cm'`` for centimeter,
        - ``'mm'`` for millimeter.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for length.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> Length:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`Length <gearpy.units.units.Length>`
            Converted length.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``Length`` instantiation.

           >>> from gearpy.units import Length
           >>> l = Length(1, 'm')
           >>> l
           1 m

           Conversion from meter to centimeter with ``inplace=False`` by
           default, so it does not override the current value.

           >>> l.to('cm')
           100.0 cm
           >>> l
           1 m

           Conversion from meter to centimeter with ``inplace=True``, in order
           to override the current value.

           >>> l.to('cm', inplace=True)
           100.0 cm
           >>> l
           100.0 cm
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return Length(value=target_value, unit=target_unit)


class Surface(UnitBase):
    r""":py:class:`Surface <gearpy.units.units.Surface>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for surface.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Surface numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {
        'm^2': 1,
        'dm^2': 1e-2,
        'cm^2': 1e-4,
        'mm^2': 1e-6
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        if value <= 0:
            raise ValueError("Parameter 'value' must be positive.")

        self.__value = value
        self.__unit = unit

    def __mul__(self, other: float | int) -> Surface:
        super().__mul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply an {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        return Surface(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> Surface:
        super().__rmul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by an {self.__class__.__name__}."
            )

        return Surface(value=self.__value*other, unit=self.__unit)

    def __truediv__(self, other: Surface | float | int) -> Surface | float:
        super().__truediv__(other=other)

        if not isinstance(other, Surface | float | int):
            raise TypeError(
                f"It is not allowed to divide an {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, Surface):
            return self.__value/other.to(self.__unit).value
        else:
            return Surface(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Surface numerical value. The relative unit is expressed by the
        :py:attr:`unit` property. It must be positive.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Surface numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
           ``ValueError``
               If :py:attr:`value` is negative or null.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for surface. It must be a
        :py:class:`str`. Available units are:

        - ``'m^2'`` for square meter,
        - ``'dm^2'`` for square decimeter,
        - ``'cm^2'`` for square centimeter,
        - ``'mm^2'`` for square millimeter.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for surface.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> Surface:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`Surface <gearpy.units.units.Surface>`
            Converted surface.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``Surface`` instantiation.

           >>> from gearpy.units import Surface
           >>> s = Surface(1, 'm^2')
           >>> s
           1 m^2

           Conversion from square meter to square millimeter with
           ``inplace=False`` by default, so it does not override the current
           value.

           >>> s.to('mm^2')
           1000000.0 mm^2
           >>> s
           1 m^2

           Conversion from square meter to square millimeter with
           ``inplace=True``, in order to override the current value.

           >>> s.to('mm^2', inplace=True)
           1000000.0 mm^2
           >>> s
           1000000.0 mm^2
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return Surface(value=target_value, unit=target_unit)


class Force(UnitBase):
    r""":py:class:`Force <gearpy.units.units.Force>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for force.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Force numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {
        'N': 1,
        'mN': 1e-3,
        'kN': 1e3,
        'kgf': 9.80665,
        'gf': 9.80665e-3
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        self.__value = value
        self.__unit = unit

    def __mul__(self, other: float | int) -> Force:
        super().__mul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply an {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        return Force(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> Force:
        super().__rmul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by an {self.__class__.__name__}."
            )

        return Force(value=self.__value*other, unit=self.__unit)

    def __truediv__(
        self,
        other: Force | Surface | float | int
    ) -> Force | Stress | float:
        super().__truediv__(other=other)

        if not isinstance(other, Force | Surface | float | int):
            raise TypeError(
                f"It is not allowed to divide an {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, Force):
            return self.__value/other.to(self.__unit).value
        elif isinstance(other, Surface):
            return Stress(
                value=self.to('N').value/other.to('m^2').value,
                unit='Pa'
            )
        else:
            return Force(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Force numerical value. The relative unit is expressed by the
        :py:attr:`unit` property.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Force numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for force. It must be a
        :py:class:`str`. Available units are:

        - ``'N'`` for newton,
        - ``'mN'`` for milli-newton,
        - ``'kN'`` for kilo-newton,
        - ``'kgf'`` for kilogram force,
        - ``'gf'`` for gram force.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for force.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> Force:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`Force <gearpy.units.units.Force>`
            Converted force.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``Force`` instantiation.

           >>> from gearpy.units import Force
           >>> f = Force(1, 'N')
           >>> f
           1 N

           Conversion from newton to kilogram force with ``inplace=False`` by
           default, so it does not override the current value.

           >>> f.to('kgf')
           0.10197162129779283 kgf
           >>> f
           1 N

           Conversion from newton to kilogram force with ``inplace=True``, in
           order to override the current value.

           >>> f.to('kgf', inplace=True)
           0.10197162129779283 kgf
           >>> f
           0.10197162129779283 kgf
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return Force(value=target_value, unit=target_unit)


class Stress(UnitBase):
    r""":py:class:`Stress <gearpy.units.units.Stress>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for stress.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Stress numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {
        'Pa': 1,
        'kPa': 1e3,
        'MPa': 1e6,
        'GPa': 1e9
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        self.__value = value
        self.__unit = unit

    def __mul__(self, other: float | int) -> Stress:
        super().__mul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply an {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        return Stress(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> Stress:
        super().__rmul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by an {self.__class__.__name__}."
            )

        return Stress(value=self.__value*other, unit=self.__unit)

    def __truediv__(self, other: Stress | float | int) -> Stress | float:
        super().__truediv__(other=other)

        if not isinstance(other, Stress | float | int):
            raise TypeError(
                f"It is not allowed to divide an {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, Stress):
            return self.__value/other.to(self.__unit).value
        else:
            return Stress(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Stress numerical value. The relative unit is expressed by the
        :py:attr:`unit` property.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Stress numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for stress. It must be a
        :py:class:`str`. Available units are:

        - ``'Pa'`` for pascal,
        - ``'kPa'`` for kilo-pascal,
        - ``'MPa'`` for mega-pascal,
        - ``'GPa'`` for giga-pascal.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for stress.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> Stress:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`Stress <gearpy.units.units.Stress>`
            Converted stress.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``Stress`` instantiation.

           >>> from gearpy.units import Stress
           >>> s = Stress(1, 'GPa')
           >>> s
           1 GPa

           Conversion from giga-pascal to mega-pascal with ``inplace=False`` by
           default, so it does not override the current value.

           >>> s.to('MPa')
           1000.0 MPa
           >>> s
           1 GPa

           Conversion from giga-pascal to mega-pascal with ``inplace=True``, in
           order to override the current value.

           >>> s.to('MPa', inplace=True)
           1000.0 MPa
           >>> s
           1000.0 MPa
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return Stress(value=target_value, unit=target_unit)


class Current(UnitBase):
    r""":py:class:`Current <gearpy.units.units.Current>` object.

    Attributes
    ----------
    :py:attr:`unit` : :py:class:`str`
        Symbol of the unit of measurement for electrical current.
    :py:attr:`value` : :py:class:`float` or :py:class:`int`
        Electrical current numerical value.

    Methods
    -------
    :py:meth:`to`
        It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement.
    """

    __UNITS = {
        'A': 1,
        'mA': 1e-3,
        'uA': 1e-6
    }

    def __init__(self, value: float | int, unit: str):
        super().__init__(value=value, unit=unit)

        if unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{unit}' not available. "
                f"Available units are: {list(self.__UNITS.keys())}."
            )

        self.__value = value
        self.__unit = unit

    def __mul__(self, other: float | int) -> Current:
        super().__mul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply an {self.__class__.__name__} "
                f"by a {other.__class__.__name__}."
            )

        return Current(value=self.__value*other, unit=self.__unit)

    def __rmul__(self, other: float | int) -> Current:
        super().__rmul__(other=other)

        if not isinstance(other, float | int):
            raise TypeError(
                f"It is not allowed to multiply a {other.__class__.__name__} "
                f"by an {self.__class__.__name__}."
            )

        return Current(value=self.__value*other, unit=self.__unit)

    def __truediv__(self, other: Current | float | int) -> Current | float:
        super().__truediv__(other=other)

        if not isinstance(other, Current | float | int):
            raise TypeError(
                f"It is not allowed to divide an {self.__class__.__name__} by "
                f"a {other.__class__.__name__}."
            )

        if isinstance(other, Current):
            return self.__value/other.to(self.__unit).value
        else:
            return Current(value=self.__value/other, unit=self.__unit)

    @property
    def value(self) -> float | int:
        """Electrical current numerical value. The relative unit is expressed
        by the :py:attr:`unit` property.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Electrical current numerical value.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`value` is not a :py:class:`float` or an
               :py:class:`int`.
        """
        return self.__value

    @property
    def unit(self) -> str:
        """Symbol of the unit of measurement for electrical current. It must be
        a :py:class:`str`. Available units are:

        - ``'A'`` for ampere,
        - ``'mA'`` for milli-ampere,
        - ``'uA'`` for micro-ampere.

        Returns
        -------
        :py:class:`str`
            Symbol of the unit of measurement for electrical current.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`unit` is not a :py:class:`str`.
           ``KeyError``
               If the :py:attr:`unit` is not among available ones.
        """
        return self.__unit

    def to(self, target_unit: str, inplace: bool = False) -> Current:
        """It converts actual :py:attr:`value` to a new value computed using
        ``target_unit`` as the reference unit of measurement. \n
        If ``inplace`` is ``True``, it overrides actual :py:attr:`value` and
        :py:attr:`unit`, otherwise it returns a new instance with the converted
        :py:attr:`value` and the ``target_unit`` as :py:attr:`unit`.

        Parameters
        ----------
        ``target_unit`` : :py:class:`str`
            Target unit to which convert the current value.
        ``inplace`` : :py:class:`bool`, optional
            Whether to override the current instance value. Default is
            ``False``, so it does not override the current value.

        Returns
        -------
        :py:class:`Current <gearpy.units.units.Current>`
            Converted electrical current.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``target_unit`` is not a :py:class:`str`,
               - if ``inplace`` is not a :py:class:`bool`.
           ``KeyError``
               If the ``target_unit`` is not among available ones.

        .. admonition:: Examples
           :class: important

           ``Current`` instantiation.

           >>> from gearpy.units import Current
           >>> i = Current(1, 'A')
           >>> i
           1 A

           Conversion from ampere to milli-ampere with ``inplace=False`` by
           default, so it does not override the current value.

           >>> i.to('mA')
           1000.0 mA
           >>> i
           1 A

           Conversion from ampere to milli-ampere with ``inplace=True``, in
           order to override the current value.

           >>> i.to('mA', inplace=True)
           1000.0 mA
           >>> i
           1000.0 mA
        """
        super().to(target_unit=target_unit, inplace=inplace)

        if target_unit not in self.__UNITS.keys():
            raise KeyError(
                f"{self.__class__.__name__} unit '{target_unit}' not "
                f"available. Available units are: {list(self.__UNITS.keys())}."
            )

        if target_unit != self.__unit:
            target_value = self.__value*self.__UNITS[self.__unit] / \
                self.__UNITS[target_unit]
        else:
            target_value = self.__value

        if inplace:
            self.__value = target_value
            self.__unit = target_unit
            return self
        else:
            return Current(value=target_value, unit=target_unit)
