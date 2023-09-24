from .motor import MotorBase


class DCMotor(MotorBase):

    def __init__(self, name, inertia, no_load_speed, maximum_torque):
        super().__init__(name = name, inertia = inertia)
        self.__no_load_speed = no_load_speed
        self.__maximum_torque = maximum_torque

    @property
    def name(self):
        return super().name

    @property
    def drives(self):
        return super().drives

    @drives.setter
    def drives(self, drives):
        super(DCMotor, type(self)).drives.fset(self, drives)

    @property
    def angle(self):
        return super().angle

    @angle.setter
    def angle(self, angle):
        super(DCMotor, type(self)).angle.fset(self, angle)

    @property
    def speed(self):
        return super().speed

    @speed.setter
    def speed(self, speed):
        super(DCMotor, type(self)).speed.fset(self, speed)

    @property
    def acceleration(self):
        return super().acceleration

    @acceleration.setter
    def acceleration(self, acceleration):
        super(DCMotor, type(self)).acceleration.fset(self, acceleration)

    @property
    def no_load_speed(self):
        return self.__no_load_speed

    @property
    def maximum_torque(self):
        return self.__maximum_torque

    @property
    def torque(self):
        return super().torque

    @torque.setter
    def torque(self, torque):
        super(DCMotor, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self):
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque):
        super(DCMotor, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self):
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque):
        super(DCMotor, type(self)).load_torque.fset(self, load_torque)

    @property
    def inertia(self):
        return super().inertia

    def compute_torque(self):
        return (1 - self.speed/self.__no_load_speed)*self.__maximum_torque

    @property
    def time_variables(self):
        return super().time_variables

    def update_time_variables(self):
        super().update_time_variables()
