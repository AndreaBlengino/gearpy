from .gear import GearBase


class SpurGear(GearBase):

    def __init__(self, name, n_teeth, inertia):
        super().__init__(name = name, n_teeth = n_teeth, inertia = inertia)

    @property
    def name(self):
        return super().name

    @property
    def n_teeth(self):
        return super().n_teeth

    @property
    def driven_by(self):
        return super().driven_by

    @driven_by.setter
    def driven_by(self, driven_by):
        super(SpurGear, type(self)).driven_by.fset(self, driven_by)

    @property
    def drives(self):
        return super().drives

    @drives.setter
    def drives(self, drives):
        super(SpurGear, type(self)).drives.fset(self, drives)

    @property
    def master_gear_ratio(self):
        return super().master_gear_ratio

    @master_gear_ratio.setter
    def master_gear_ratio(self, master_gear_ratio):
        super(SpurGear, type(self)).master_gear_ratio.fset(self, master_gear_ratio)

    @property
    def angle(self):
        return super().angle

    @angle.setter
    def angle(self, angle):
        super(SpurGear, type(self)).angle.fset(self, angle)

    @property
    def speed(self):
        return super().speed

    @speed.setter
    def speed(self, speed):
        super(SpurGear, type(self)).speed.fset(self, speed)

    @property
    def acceleration(self):
        return super().acceleration

    @acceleration.setter
    def acceleration(self, acceleration):
        super(SpurGear, type(self)).acceleration.fset(self, acceleration)

    @property
    def torque(self):
        return super().torque

    @torque.setter
    def torque(self, torque):
        super(SpurGear, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self):
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque):
        super(SpurGear, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self):
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque):
        super(SpurGear, type(self)).load_torque.fset(self, load_torque)

    @property
    def inertia(self):
        return super().inertia

    @property
    def external_torque(self):
        return super().external_torque

    @external_torque.setter
    def external_torque(self, external_torque):
        super(SpurGear, type(self)).external_torque.fset(self, external_torque)

    @property
    def time_variables(self):
        return super().time_variables

    def update_time_variables(self):
        super().update_time_variables()