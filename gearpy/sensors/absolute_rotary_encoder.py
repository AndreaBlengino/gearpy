from gearpy.mechanical_objects import RotatingObject
from gearpy.units import AngularPosition
from typing import Optional, Union


class AbsoluteRotaryEncoder:
    r"""``gearpy.sensors.absolute_rotary_encoder.AbsoluteRotaryEncoder`` object.

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
