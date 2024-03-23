from gearpy.mechanical_objects import MotorBase
from gearpy.units import Current
from .sensor_base import SensorBase
from typing import Optional, Union


class Amperometer(SensorBase):

    def __init__(self, target: MotorBase):
        if not isinstance(target, MotorBase):
            raise TypeError(f"Parameter 'target' must be an instance of {MotorBase.__name__!r}.")

        if not target.electric_current_is_computable:
            raise ValueError(f"Target motor {target.name!r} cannot compute 'electric_current' property.")

        self.__target = target

    @property
    def target(self) -> MotorBase:
        return self.__target

    def get_value(self, unit: Optional[str] = None) -> Union[Current, float, int]:
        if not isinstance(unit, str) and unit is not None:
            raise TypeError("Parameter 'unit' must be a string.")

        if unit is None:
            return self.__target.electric_current
        else:
            return self.__target.electric_current.to(unit).value
