from gearpy.mechanical_objects import RotatingObject
from gearpy.units import AngularSpeed
from .sensor_base import SensorBase
from typing import Optional


class Tachometer(SensorBase):
    r""":py:class:`Tachometer <gearpy.sensors.tachometer.Tachometer>` object.

    Attributes
    ----------
    :py:attr:`target` : :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
        Target rotating object whose angular speed is probed by the sensor.

    Methods
    -------
    :py:meth:`get_value`
        It gets the angular speed of the :py:attr:`target` rotating object.
    """

    def __init__(self, target: RotatingObject):
        if not isinstance(target, RotatingObject):
            raise TypeError(
                f"Parameter 'target' must be an instance of "
                f"{RotatingObject.__name__!r}."
            )

        self.__target = target

    @property
    def target(self) -> RotatingObject:
        """Target rotating object whose angular speed is probed by the sensor.

        Returns
        -------
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
            Target rotating object whose angular speed is probed by the sensor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`target` is not an instance of
               :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`.
        """
        return self.__target

    def get_value(
        self,
        unit: Optional[str] = None
    ) -> AngularSpeed | float | int:
        """It gets the angular speed of the :py:attr:`target` rotating
        object. \n
        If a ``unit`` is set, then it converts the angular speed to that unit
        and returns only the numerical value as float or integer.

        Parameters
        ----------
        ``unit`` : :py:class:`str`, optional
            The unit to which convert the :py:attr:`target` angular speed. If
            specified, it converts the angular speed and returns only the
            numerical value as float or integer, otherwise it returns an
            :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`. Default
            is :py:obj:`None`, so it returns an
            :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`.

        Returns
        -------
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>` or :py:class:`float` or :py:class:`int`
            Angular speed of the :py:attr:`target` rotating object.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If ``unit`` is not a :py:class:`str`.
        """
        if not isinstance(unit, str) and unit is not None:
            raise TypeError("Parameter 'unit' must be a string.")

        if unit is None:
            return self.__target.angular_speed
        else:
            return self.__target.angular_speed.to(unit).value
