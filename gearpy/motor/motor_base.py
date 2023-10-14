from abc import abstractmethod
from gearpy.mechanical_object import RotatingObject
from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, InertiaMoment, Torque


class MotorBase(RotatingObject):

    @abstractmethod
    def __init__(self, name: str, inertia_moment: InertiaMoment):
        super().__init__(name = name, inertia_moment = inertia_moment)
        self.__drives = None

    @property
    @abstractmethod
    def drives(self) -> RotatingObject:
        return self.__drives

    @drives.setter
    @abstractmethod
    def drives(self, drives: RotatingObject):
        if not isinstance(drives, RotatingObject):
            raise TypeError(f"Parameter 'drives' must be a {RotatingObject.__name__!r}")

        self.__drives = drives

    @property
    @abstractmethod
    def angular_position(self) -> AngularPosition:
        return super().angular_position

    @angular_position.setter
    @abstractmethod
    def angular_position(self, angular_position: AngularPosition):
        super(MotorBase, type(self)).angular_position.fset(self, angular_position)

    @property
    @abstractmethod
    def angular_speed(self) -> AngularSpeed:
        return super().angular_speed

    @angular_speed.setter
    @abstractmethod
    def angular_speed(self, angular_speed: AngularSpeed):
        super(MotorBase, type(self)).angular_speed.fset(self, angular_speed)

    @property
    @abstractmethod
    def angular_acceleration(self) -> AngularAcceleration:
        return super().angular_acceleration

    @angular_acceleration.setter
    @abstractmethod
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        super(MotorBase, type(self)).angular_acceleration.fset(self, angular_acceleration)

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
