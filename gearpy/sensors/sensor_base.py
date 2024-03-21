from abc import ABC, abstractmethod
from gearpy.mechanical_objects import RotatingObject
from gearpy.units import UnitBase
from typing import Union


class SensorBase(ABC):

    @property
    @abstractmethod
    def target(self) -> RotatingObject: ...

    @abstractmethod
    def get_value(self) -> Union[UnitBase, float, int]: ...
