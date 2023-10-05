from gearpy.mechanical_object.rotating_object import RotatingObject
from .motor import MotorBase
from typing import Union


class DCMotor(MotorBase):

    def __init__(self, name: str, inertia: Union[float, int], no_load_speed: Union[float, int],
                 maximum_torque: Union[float, int]):
        super().__init__(name = name, inertia = inertia)

        if not isinstance(no_load_speed, float) and not isinstance(no_load_speed, int):
            raise TypeError("Parameter 'no_load_speed' must be a float or an integer.")

        if not isinstance(maximum_torque, float) and not isinstance(maximum_torque, int):
            raise TypeError("Parameter 'maximum_torque' must be a float or an integer.")

        if no_load_speed <= 0:
            raise ValueError("Parameter 'no_load_speed' must be positive.")

        if maximum_torque <= 0:
            raise ValueError("Parameter 'maximum_torque' must be positive.")

        self.__no_load_speed = no_load_speed
        self.__maximum_torque = maximum_torque

    @property
    def name(self) -> str:
        return super().name

    @property
    def drives(self) -> RotatingObject:
        return super().drives

    @drives.setter
    def drives(self, drives: RotatingObject):
        super(DCMotor, type(self)).drives.fset(self, drives)

    @property
    def angle(self) -> Union[float, int]:
        return super().angle

    @angle.setter
    def angle(self, angle: Union[float, int]):
        super(DCMotor, type(self)).angle.fset(self, angle)

    @property
    def speed(self) -> Union[float, int]:
        return super().speed

    @speed.setter
    def speed(self, speed: Union[float, int]):
        super(DCMotor, type(self)).speed.fset(self, speed)

    @property
    def acceleration(self) -> Union[float, int]:
        return super().acceleration

    @acceleration.setter
    def acceleration(self, acceleration: Union[float, int]):
        super(DCMotor, type(self)).acceleration.fset(self, acceleration)

    @property
    def no_load_speed(self) -> Union[float, int]:
        return self.__no_load_speed

    @property
    def maximum_torque(self) -> Union[float, int]:
        return self.__maximum_torque

    @property
    def torque(self) -> Union[float, int]:
        return super().torque

    @torque.setter
    def torque(self, torque: Union[float, int]):
        super(DCMotor, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Union[float, int]:
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Union[float, int]):
        super(DCMotor, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Union[float, int]:
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Union[float, int]):
        super(DCMotor, type(self)).load_torque.fset(self, load_torque)

    @property
    def inertia(self) -> Union[float, int]:
        return super().inertia

    def compute_torque(self) -> Union[float, int]:
        return (1 - self.speed/self.__no_load_speed)*self.__maximum_torque

    @property
    def time_variables(self) -> dict:
        return super().time_variables

    def update_time_variables(self):
        super().update_time_variables()
