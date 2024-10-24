from abc import ABC, abstractmethod
from gearpy.mechanical_objects import RotatingObject
from gearpy.units import UnitBase


class SensorBase(ABC):
    """:py:class:`SensorBase <gearpy.sensors.sensor_base.SensorBase>`
    object. \n
    Abstract base class for creating sensor objects.

    .. admonition:: See Also
       :class: seealso

       :py:class:`AbsoluteRotaryEncoder <gearpy.sensors.absolute_rotary_encoder.AbsoluteRotaryEncoder>` \n
       :py:class:`Amperometer <gearpy.sensors.amperometer.Amperometer>` \n
       :py:class:`Tachometer <gearpy.sensors.tachometer.Tachometer>`
    """

    @property
    @abstractmethod
    def target(self) -> RotatingObject: ...

    @abstractmethod
    def get_value(self) -> UnitBase | float | int: ...
