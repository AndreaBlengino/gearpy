from abc import abstractmethod
from gearpy.mechanical_object import RotatingObject
from gearpy.units import Acceleration, Angle, Inertia, Speed, Torque


class MotorBase(RotatingObject):

    @abstractmethod
    def __init__(self, name: str, inertia: Inertia):
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
    def angle(self) -> Angle:
        return super().angle

    @angle.setter
    @abstractmethod
    def angle(self, angle: Angle):
        super(MotorBase, type(self)).angle.fset(self, angle)

    @property
    @abstractmethod
    def speed(self) -> Speed:
        return super().speed

    @speed.setter
    @abstractmethod
    def speed(self, speed: Speed):
        super(MotorBase, type(self)).speed.fset(self, speed)

    @property
    @abstractmethod
    def acceleration(self) -> Acceleration:
        return super().acceleration

    @acceleration.setter
    @abstractmethod
    def acceleration(self, acceleration: Acceleration):
        super(MotorBase, type(self)).acceleration.fset(self, acceleration)

    @property
    @abstractmethod
    def torque(self) -> Torque:
        return super().torque

    @torque.setter
    @abstractmethod
    def torque(self, torque: Torque):
        super(MotorBase, type(self)).torque.fset(self, torque)

    @property
    @abstractmethod
    def driving_torque(self) -> Torque:
        return super().driving_torque

    @driving_torque.setter
    @abstractmethod
    def driving_torque(self, driving_torque: Torque):
        super(MotorBase, type(self)).driving_torque.fset(self, driving_torque)

    @property
    @abstractmethod
    def load_torque(self) -> Torque:
        return super().load_torque

    @load_torque.setter
    @abstractmethod
    def load_torque(self, load_torque: Torque):
        super(MotorBase, type(self)).load_torque.fset(self, load_torque)

    @abstractmethod
    def compute_torque(self): ...
