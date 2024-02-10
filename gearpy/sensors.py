from gearpy.mechanical_object import RotatingObject, MotorBase
from gearpy.units import AngularPosition, AngularSpeed, Current, Time, TimeInterval
from typing import Optional, Union


class AbsoluteRotaryEncoder:
    r"""``gearpy.sensors.AbsoluteRotaryEncoder`` object.

    Attributes
    ----------
    :py:attr:`target` : RotatingObject
        Target rotating object whose angular position is probed by the sensor.

    Methods
    -------
    :py:meth:`get_value`
        Gets the angular position of the ``target`` rotating object.
    """

    def __init__(self, target: RotatingObject):
        if not isinstance(target, RotatingObject):
            raise TypeError(f"Parameter 'target' must be an instance of {RotatingObject.__name__!r}.")

        self.__target = target

    @property
    def target(self) -> RotatingObject:
        """Target rotating object whose angular position is probed by the sensor.

        Returns
        -------
        RotatingObject
            Target rotating object whose angular position is probed by the sensor.

        Raises
        ------
        TypeError
            If ``target`` is not an instance of ``RotatingObject``.
        """
        return self.__target

    def get_value(self, unit: Optional[str] = None) -> Union[AngularPosition, float, int]:
        """Gets the angular position of the ``target`` rotating object. \n
        If a ``unit`` is set, then it converts the angular position to that unit and returns only the numerical value as
        float or integer.

        Parameters
        ----------
        unit : str, optional
            The unit to which convert the ``target`` angular position. If specified, it converts the angular position
            and returns only the numerical value as float or integer, otherwise it returns an ``AngularPosition``.
            Default is ``None``, so it returns an ``AngularPosition``.

        Returns
        -------
        AngularPosition or float or int
            Angular position of the ``target`` rotating object.

        Raises
        ------
        TypeError
            If ``unit`` is not a string.

        See Also
        --------
        :py:func:`gearpy.units.units.AngularPosition`
        """
        if not isinstance(unit, str) and unit is not None:
            raise TypeError("Parameter 'unit' must be a string.")

        if unit is None:
            return self.__target.angular_position
        else:
            return self.__target.angular_position.to(unit).value


class Tachometer:
    r"""``gearpy.sensors.Tachometer`` object.

    Attributes
    ----------
    :py:attr:`target` : RotatingObject
        Target rotating object whose angular speed is probed by the sensor.

    Methods
    -------
    :py:meth:`get_value`
        Gets the angular speed of the ``target`` rotating object.
    """

    def __init__(self, target: RotatingObject):
        if not isinstance(target, RotatingObject):
            raise TypeError(f"Parameter 'target' must be an instance of {RotatingObject.__name__!r}.")

        self.__target = target

    @property
    def target(self) -> RotatingObject:
        """Target rotating object whose angular speed is probed by the sensor.

        Returns
        -------
        RotatingObject
            Target rotating object whose angular speed is probed by the sensor.

        Raises
        ------
        TypeError
            If ``target`` is not an instance of ``RotatingObject``.
        """
        return self.__target

    def get_value(self, unit: Optional[str] = None) -> Union[AngularSpeed, float, int]:
        """Gets the angular speed of the ``target`` rotating object. \n
        If a ``unit`` is set, then it converts the angular speed to that unit and returns only the numerical value as
        float or integer.

        Parameters
        ----------
        unit : str, optional
            The unit to which convert the ``target`` angular speed. If specified, it converts the angular speed and
            returns only the numerical value as float or integer, otherwise it returns an ``AngularSpeed``. Default is
            ``None``, so it returns an ``AngularSpeed``.

        Returns
        -------
        AngularSpeed or float or int
            Angular speed of the ``target`` rotating object.

        Raises
        ------
        TypeError
            If ``unit`` is not a string.

        See Also
        --------
        :py:func:`gearpy.units.units.AngularSpeed`
        """
        if not isinstance(unit, str) and unit is not None:
            raise TypeError("Parameter 'unit' must be a string.")

        if unit is None:
            return self.__target.angular_speed
        else:
            return self.__target.angular_speed.to(unit).value


class Timer:
    r"""``gearpy.sensors.Timer`` object.

    Attributes
    ----------
    :py:attr:`start_time` : Time
        Start time after which the timer is active.
    :py:attr:`duration` : TimeInterval
        Time duration of the timer, starting from ``start_time``

    Methods
    -------
    :py:meth:`is_active`
        Checks if the simulation ``current_time`` is greater than or equal to ``start_time`` but lower than or equal
        to ``current_time`` + ``duration``.
    """

    def __init__(self, start_time: Time, duration: TimeInterval):
        if not isinstance(start_time, Time):
            raise TypeError(f"Parameter 'start_time' must be an instance of {Time.__name__!r}.")

        if not isinstance(duration, TimeInterval):
            raise TypeError(f"Parameter 'duration' must be an instance of {TimeInterval.__name__!r}.")

        self.__start_time = start_time
        self.__duration = duration

    @property
    def start_time(self) -> Time:
        """Start time after which the timer is active.

        Returns
        -------
        Time
            Start time after which the timer is active.

        Raises
        ------
        TypeError
            If ``start_time`` is not an instance of ``Time``.
        """
        return self.__start_time

    @property
    def duration(self) -> TimeInterval:
        """Time duration of the timer, starting from ``start_time``.

        Returns
        -------
        TimeInterval
            Time duration of the timer, starting from ``start_time``

        Raises
        ------
        TypeError
            If ``duration`` is not an instance of ``TimeInterval``.
        """
        return self.__duration

    def is_active(self, current_time: Time) -> bool:
        """Checks if the simulation ``current_time`` is greater than or equal to ``start_time`` but lower than or equal
        to ``current_time`` + ``duration``.

        Parameters
        ----------
        current_time : Time
            Current time of the simulation, to be compared with ``start_time`` and ``duration``.

        Returns
        -------
        bool
            Whether ``current_time`` is greater than or equal to ``start_time`` but lower than or equal to
            ``start_time`` + ``durtation``.

        Raises
        ------
        TypeError
            If ``current_time`` is not an instance of ``Time``.
        """
        if not isinstance(current_time, Time):
            raise TypeError(f"Parameter 'current_time' must be an instance of {Time.__name__!r}.")

        return (current_time >= self.start_time) and ((current_time - self.start_time) <= self.duration)
