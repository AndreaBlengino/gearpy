from gearpy.mechanical_objects import MotorBase
from gearpy.units import Current
from .sensor_base import SensorBase
from typing import Optional, Union


class Amperometer(SensorBase):
    r"""``gearpy.sensors.amperometer.Amperometer`` object.

    Attributes
    ----------
    :py:attr:`target` : MotorBase
        Target motor object whose electric current is probed by the sensor.

    Methods
    -------
    :py:meth:`get_value`
        Gets the electric current of the ``target`` motor object.
    """

    def __init__(self, target: MotorBase):
        if not isinstance(target, MotorBase):
            raise TypeError(f"Parameter 'target' must be an instance of {MotorBase.__name__!r}.")

        if not target.electric_current_is_computable:
            raise ValueError(f"Target motor {target.name!r} cannot compute 'electric_current' property.")

        self.__target = target

    @property
    def target(self) -> MotorBase:
        """Target motor object whose electric current is probed by the sensor.

        Returns
        -------
        MotorBase
            Target motor object whose electric current is probed by the sensor.

        Raises
        ------
        TypeError
            If ``target`` is not an instance of ``MotorBase``.
        """
        return self.__target

    def get_value(self, unit: Optional[str] = None) -> Union[Current, float, int]:
        """Gets the electric current of the ``target`` motor object. \n
         If a ``unit`` is set, then it converts the electric current to that unit and returns only the numerical value
         as float or integer.

         Parameters
         ----------
         unit : str, optional
             The unit to which convert the ``target`` electric current. If specified, it converts the electric current
             and returns only the numerical value as float or integer, otherwise it returns a ``Current``. Default is
             ``None``, so it returns an ``Current``.

         Returns
         -------
         Current or float or int
             Electric Current of the ``target`` motor object.

         Raises
         ------
         TypeError
             If ``unit`` is not a string.

         See Also
         --------
         :py:func:`gearpy.units.units.Current`
         """
        if not isinstance(unit, str) and unit is not None:
            raise TypeError("Parameter 'unit' must be a string.")

        if unit is None:
            return self.__target.electric_current
        else:
            return self.__target.electric_current.to(unit).value
