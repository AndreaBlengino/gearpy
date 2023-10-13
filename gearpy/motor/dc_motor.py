from gearpy.mechanical_object import RotatingObject
from gearpy.motor import MotorBase
from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, InertiaMoment, Torque


class DCMotor(MotorBase):

    def __init__(self, name: str, inertia_moment: InertiaMoment, no_load_speed: AngularSpeed, maximum_torque: Torque):
        super().__init__(name = name, inertia_moment = inertia_moment)

        if not isinstance(no_load_speed, AngularSpeed):
            raise TypeError(f"Parameter 'no_load_speed' must be an instance of {AngularSpeed.__name__!r}")

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
    def angular_position(self) -> AngularPosition:
        return super().angular_position

    @angular_position.setter
    def angular_position(self, angular_position: AngularPosition):
        super(DCMotor, type(self)).angular_position.fset(self, angular_position)

    @property
    def angular_speed(self) -> AngularSpeed:
        return super().angular_speed

    @angular_speed.setter
    def angular_speed(self, angular_speed: AngularSpeed):
        super(DCMotor, type(self)).angular_speed.fset(self, angular_speed)

    @property
    def angular_acceleration(self) -> AngularAcceleration:
        return super().angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        super(DCMotor, type(self)).angular_acceleration.fset(self, angular_acceleration)

    @property
    def no_load_speed(self) -> AngularSpeed:
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
    def inertia_moment(self) -> InertiaMoment:
        return super().inertia_moment

    def compute_torque(self) -> Torque:
        return Torque(value = (1 - self.angular_speed.to('rad/s').value/self.__no_load_speed.to('rad/s').value)*
                              self.__maximum_torque.value,
                      unit = self.__maximum_torque.unit)

    @property
    def time_variables(self) -> dict:
        return super().time_variables

    def update_time_variables(self):
        super().update_time_variables()
