from abc import abstractmethod
from gearpy.mechanical_object.rotating_object import RotatingObject
from typing import Union


class MotorBase(RotatingObject):

    @abstractmethod
    def __init__(self, name: str, inertia: Union[float, int]):
        super().__init__(name = name, inertia = inertia)
        self.__drives = None

    @property
    @abstractmethod
    def drives(self) -> RotatingObject:
        return self.__drives

    @drives.setter
    @abstractmethod
    def drives(self, drives: RotatingObject):
        if not isinstance(drives, RotatingObject):
            raise TypeError("Parameter 'drives' must be a RotatingObject")

        self.__drives = drives

    @abstractmethod
    def compute_torque(self): ...
