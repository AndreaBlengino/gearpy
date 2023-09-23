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
    def inertia(self):
        return super().inertia
