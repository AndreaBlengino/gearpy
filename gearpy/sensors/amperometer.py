from gearpy.mechanical_objects import MotorBase
from gearpy.units import Current
from .sensor_base import SensorBase
from typing import Optional


class Amperometer(SensorBase):
    r""":py:class:`Amperometer <gearpy.sensors.amperometer.Amperometer>`
    object.

    Attributes
    ----------
    :py:attr:`target` : :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`
        Target motor object whose electric current is probed by the sensor.

    Methods
    -------
    :py:meth:`get_value`
        It gets the electric current of the :py:attr:`target` motor object.
    """

    def __init__(self, target: MotorBase):
        if not isinstance(target, MotorBase):
            raise TypeError(
                f"Parameter 'target' must be an instance of "
                f"{MotorBase.__name__!r}."
            )

        if not target.electric_current_is_computable:
            raise ValueError(
                f"Target motor {target.name!r} cannot compute "
                f"'electric_current' property."
            )

        self.__target = target

    @property
    def target(self) -> MotorBase:
        """Target motor object whose electric current is probed by the sensor.

        Returns
        -------
        :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`
            Target motor object whose electric current is probed by the sensor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`target` is not an instance of
               :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`.
        """
        return self.__target

    def get_value(self, unit: Optional[str] = None) -> Current | float | int:
        """It gets the electric current of the :py:attr:`target` motor
        object. \n
        If a ``unit`` is set, then it converts the electric current to that
        unit and returns only the numerical value as float or integer.

        Parameters
        ----------
        ``unit`` : :py:class:`str`, optional
            The unit to which convert the :py:attr:`target` electric current.
            If specified, it converts the electric current and returns only the
            numerical value as float or integer, otherwise it returns a
            :py:class:`Current <gearpy.units.units.Current>`. Default is
            :py:obj:`None`, so it returns a
            :py:class:`Current <gearpy.units.units.Current>`.

        Returns
        -------
        :py:class:`Current <gearpy.units.units.Current>` or :py:class:`float`or :py:class:`int`
            Electric Current of the :py:attr:`target` motor object.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If ``unit`` is not a :py:class:`str`.
         """
        if not isinstance(unit, str) and unit is not None:
            raise TypeError("Parameter 'unit' must be a string.")

        if unit is None:
            return self.__target.electric_current
        else:
            return self.__target.electric_current.to(unit).value
