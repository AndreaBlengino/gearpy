from gearpy.mechanical_object import RotatingObject
from gearpy.motor import MotorBase
from gearpy.units import Acceleration, Angle, Inertia, Speed, Torque


class DCMotor(MotorBase):

    def __init__(self, name: str, inertia: Inertia, no_load_speed: Speed, maximum_torque: Torque):
        super().__init__(name = name, inertia = inertia)

        if not isinstance(no_load_speed, Speed):
            raise TypeError(f"Parameter 'no_load_speed' must be an instance of {Speed.__name__!r}")

        if not isinstance(maximum_torque, Torque):
            raise TypeError(f"Parameter 'maximum_torque' must be an instance of {Torque.__name__!r}.")

        if no_load_speed.value <= 0:
            raise ValueError("Parameter 'no_load_speed' must be positive.")

        if maximum_torque.value <= 0:
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
    def angle(self) -> Angle:
        return super().angle

    @angle.setter
    def angle(self, angle: Angle):
        super(DCMotor, type(self)).angle.fset(self, angle)

    @property
    def speed(self) -> Speed:
        return super().speed

    @speed.setter
    def speed(self, speed: Speed):
        super(DCMotor, type(self)).speed.fset(self, speed)

    @property
    def acceleration(self) -> Acceleration:
        return super().acceleration

    @acceleration.setter
    def acceleration(self, acceleration: Acceleration):
        super(DCMotor, type(self)).acceleration.fset(self, acceleration)

    @property
    def no_load_speed(self) -> Speed:
        return self.__no_load_speed

    @property
    def maximum_torque(self) -> Torque:
        return self.__maximum_torque

    @property
    def torque(self) -> Torque:
        return super().torque

    @torque.setter
    def torque(self, torque: Torque):
        super(DCMotor, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Torque:
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Torque):
        super(DCMotor, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Torque:
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Torque):
        super(DCMotor, type(self)).load_torque.fset(self, load_torque)

    @property
    def inertia(self) -> Inertia:
        return super().inertia

    def compute_torque(self) -> Torque:
        return Torque(value = (1 - self.speed.to('rad/s').value/self.__no_load_speed.to('rad/s').value)*
                              self.__maximum_torque.value,
                      unit = self.__maximum_torque.unit)

    @property
    def time_variables(self) -> dict:
        return super().time_variables

    def update_time_variables(self):
        super().update_time_variables()
