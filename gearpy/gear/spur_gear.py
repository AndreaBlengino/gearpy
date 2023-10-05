from .gear import GearBase
from gearpy.mechanical_object.rotating_object import RotatingObject
from typing import Callable, Union


class SpurGear(GearBase):

    def __init__(self, name: str, n_teeth: int, inertia: float):
        super().__init__(name = name, n_teeth = n_teeth, inertia = inertia)

    @property
    def name(self) -> str:
        return super().name

    @property
    def n_teeth(self) -> int:
        return super().n_teeth

    @property
    def driven_by(self) -> RotatingObject:
        return super().driven_by

    @driven_by.setter
    def driven_by(self, driven_by: RotatingObject):
        super(SpurGear, type(self)).driven_by.fset(self, driven_by)

    @property
    def drives(self) -> RotatingObject:
        return super().drives

    @drives.setter
    def drives(self, drives: RotatingObject):
        super(SpurGear, type(self)).drives.fset(self, drives)

    @property
    def master_gear_ratio(self) -> float:
        return super().master_gear_ratio

    @master_gear_ratio.setter
    def master_gear_ratio(self, master_gear_ratio: float):
        super(SpurGear, type(self)).master_gear_ratio.fset(self, master_gear_ratio)

    @property
    def master_gear_efficiency(self) -> Union[float, int]:
        return super().master_gear_efficiency

    @master_gear_efficiency.setter
    def master_gear_efficiency(self, master_gear_efficiency: Union[float, int]):
        super(SpurGear, type(self)).master_gear_efficiency.fset(self, master_gear_efficiency)

    @property
    def angle(self) -> Union[float, int]:
        return super().angle

    @angle.setter
    def angle(self, angle: Union[float, int]):
        super(SpurGear, type(self)).angle.fset(self, angle)

    @property
    def speed(self) -> Union[float, int]:
        return super().speed

    @speed.setter
    def speed(self, speed: Union[float, int]):
        super(SpurGear, type(self)).speed.fset(self, speed)

    @property
    def acceleration(self) -> Union[float, int]:
        return super().acceleration

    @acceleration.setter
    def acceleration(self, acceleration: Union[float, int]):
        super(SpurGear, type(self)).acceleration.fset(self, acceleration)

    @property
    def torque(self) -> Union[float, int]:
        return super().torque

    @torque.setter
    def torque(self, torque: Union[float, int]):
        super(SpurGear, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Union[float, int]:
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Union[float, int]):
        super(SpurGear, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Union[float, int]:
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Union[float, int]):
        super(SpurGear, type(self)).load_torque.fset(self, load_torque)

    @property
    def inertia(self) -> Union[float, int]:
        return super().inertia

    @property
    def external_torque(self) -> Callable:
        return super().external_torque

    @external_torque.setter
    def external_torque(self, external_torque: Callable):
        super(SpurGear, type(self)).external_torque.fset(self, external_torque)

    @property
    def time_variables(self) -> dict:
        return super().time_variables

    def update_time_variables(self):
        super().update_time_variables()
