from abc import ABC, abstractmethod
from gearpy.units import UnitBase


class OperatorBase(ABC):

    @abstractmethod
    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        if not isinstance(sensor_value, UnitBase):
            raise TypeError(f"Parameter 'sensor_value' must be an instance of {UnitBase.__name__!r}.")

        if not isinstance(threshold, UnitBase):
            raise TypeError(f"Parameter 'threshold' must be an instance of {UnitBase.__name__!r}.")
