from gearpy.mechanical_object import RotatingObject
from gearpy.units import AngularPosition, AngularSpeed
from typing import Optional, Union


class AbsoluteRotaryEncoder:

    def __init__(self, target: RotatingObject):
        if not isinstance(target, RotatingObject):
            raise TypeError(f"Parameter 'target' must be an instance of {RotatingObject.__name__!r}.")

        self.__target = target

    @property
    def target(self) -> RotatingObject:
        return self.__target

    def get_value(self, unit: Optional[str] = None) -> Union[AngularPosition, float, int]:
        if not isinstance(unit, str) and unit is not None:
            raise TypeError("Parameter 'unit' must be a string.")

        if unit is None:
            return self.__target.angular_position
        else:
            return self.__target.angular_position.to(unit).value


class Tachometer:

    def __init__(self, target: RotatingObject):
        if not isinstance(target, RotatingObject):
            raise TypeError(f"Parameter 'target' must be an instance of {RotatingObject.__name__!r}.")

        self.__target = target

    @property
    def target(self) -> RotatingObject:
        return self.__target

    def get_value(self, unit: Optional[str] = None) -> Union[AngularSpeed, float, int]:
        if not isinstance(unit, str) and unit is not None:
            raise TypeError("Parameter 'unit' must be a string.")

        if unit is None:
            return self.__target.angular_speed
        else:
            return self.__target.angular_speed.to(unit).value
