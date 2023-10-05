from gearpy.gear.gear import GearBase
from gearpy.motor.motor import MotorBase
from typing import Union


def add_gear_mating(master: GearBase, slave: GearBase, efficiency: Union[float, int]):
    if not isinstance(master, GearBase):
        raise TypeError("Parameter 'master' must be an instance of GearBase.")

    if not isinstance(slave, GearBase):
        raise TypeError("Parameter 'slave' must be an instance of GearBase.")

    if not isinstance(efficiency, float) and not isinstance(efficiency, int):
        raise TypeError("Parameter 'efficiency' must be a float or an integer.")

    if efficiency > 1 or efficiency < 0:
        raise ValueError("Parameter 'efficiency' must be within 0 and 1.")

    master.drives = slave
    slave.driven_by = master
    slave.master_gear_ratio = slave.n_teeth/master.n_teeth
    slave.master_gear_efficiency = efficiency


def add_fixed_joint(master: Union[MotorBase, GearBase], slave: GearBase):
    if not isinstance(master, MotorBase) and not isinstance(master, GearBase):
        raise TypeError("Parameter 'master' must be an instance of MotorBase or GearBase.")

    if not isinstance(slave, GearBase):
        raise TypeError("Parameter 'slave' must be an instance of GearBase.")

    master.drives = slave
    slave.driven_by = master
    slave.master_gear_ratio = 1.0
