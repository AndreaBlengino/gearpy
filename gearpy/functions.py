from gearpy.gear.gear import GearBase


def add_gear_mating(master: GearBase, slave: GearBase):
    master.drives = slave
    slave.driven_by = master
    slave.master_gear_ratio = slave.n_teeth/master.n_teeth


def add_fixed_joint(master, slave: GearBase):
    master.drives = slave
    slave.driven_by = master
    slave.master_gear_ratio = 1.0
