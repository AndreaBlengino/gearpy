from abc import abstractmethod
from gearpy.mechanical_object import RotatingObject
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

    @property
    @abstractmethod
    def angle(self) -> Union[float, int]:
        return super().angle

    @angle.setter
    @abstractmethod
    def angle(self, angle: Union[float, int]):
        super(MotorBase, type(self)).angle.fset(self, angle)

    @property
    @abstractmethod
    def speed(self) -> Union[float, int]:
        return super().speed

    @speed.setter
    @abstractmethod
    def speed(self, speed: Union[float, int]):
        super(MotorBase, type(self)).speed.fset(self, speed)

    @property
    @abstractmethod
    def acceleration(self) -> Union[float, int]:
        return super().acceleration

    @acceleration.setter
    @abstractmethod
    def acceleration(self, acceleration: Union[float, int]):
        super(MotorBase, type(self)).acceleration.fset(self, acceleration)

    @property
    @abstractmethod
    def torque(self) -> Union[float, int]:
        return super().torque

    @torque.setter
    @abstractmethod
    def torque(self, torque: Union[float, int]):
        super(MotorBase, type(self)).torque.fset(self, torque)

    @property
    @abstractmethod
    def driving_torque(self) -> Union[float, int]:
        return super().driving_torque

    @driving_torque.setter
    @abstractmethod
    def driving_torque(self, driving_torque: Union[float, int]):
        super(MotorBase, type(self)).driving_torque.fset(self, driving_torque)

    @property
    @abstractmethod
    def load_torque(self) -> Union[float, int]:
        return super().load_torque

    @load_torque.setter
    @abstractmethod
    def load_torque(self, load_torque: Union[float, int]):
        super(MotorBase, type(self)).load_torque.fset(self, load_torque)

    @abstractmethod
    def compute_torque(self): ...
