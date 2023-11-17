from gearpy.mechanical_object import MotorBase, GearBase, Flywheel, MatingMaster, MatingSlave
from typing import Union


def add_gear_mating(master: GearBase, slave: GearBase, efficiency: Union[float, int]):
    """Creates a gear mating between two existing gears. This mating is used to compose the mechanical Transmission. \n
    The ratio of the angular speed of the ``master`` gear over the angular speed of the ``slave`` gear is equal to the
    ratio of the ``slave`` gear number of teeth over the ``master`` gear number of teeth. \n
    The ``master`` gear is closest to the motor and transfers a fraction of the driving torque to the ``slave`` one,
    based on the ``efficiency`` value: the higher the ``efficiency``, the higher the fraction of transferred driving
    torque.

    Parameters
    ----------
    master : GearBase
        Driving gear.
    slave : GearBase
        Driven gear.
    efficiency : float or int
        Mechanical efficiency of the gear mating.

    Raises
    ------
    TypeError
        - If ``master`` is not an instance of ``GearBase``,
        - if ``slave`` is not an instance of ``GearBase``,
        - if ``efficiency`` is not a float or an integer.
    ValueError
        - If ``efficiency`` is not within ``0`` and ``1``,
        - if ``master`` and ``slave`` have different values for ``module``.
    """
    if not isinstance(master, GearBase):
        raise TypeError("Parameter 'master' must be an instance of GearBase.")

    if not isinstance(slave, GearBase):
        raise TypeError("Parameter 'slave' must be an instance of GearBase.")

    if not isinstance(efficiency, float) and not isinstance(efficiency, int):
        raise TypeError("Parameter 'efficiency' must be a float or an integer.")

    if efficiency > 1 or efficiency < 0:
        raise ValueError("Parameter 'efficiency' must be within 0 and 1.")

    if master.module is not None and slave.module is not None:
        if master.module != slave.module:
            raise ValueError(f"Gears {master.name!r} and {slave.name!r} have different modules, "
                             f"so they cannot mate together.")

    master.drives = slave
    master.mating_role = MatingMaster
    slave.driven_by = master
    slave.mating_role = MatingSlave
    slave.master_gear_ratio = slave.n_teeth/master.n_teeth
    slave.master_gear_efficiency = efficiency


def add_fixed_joint(master: Union[MotorBase, GearBase, Flywheel], slave: Union[GearBase, Flywheel]):
    """Creates a fixed joint between a ``master`` rotating object and a ``slave`` one. The fixed joint forces the two
    elements to rotate at the same angular position, speed and acceleration. \n
    The ``master`` rotating object is closest to the transmission driving motor (or it is actually it) and transfers the
    whole driving torque to the ``slave`` one.

    Parameters
    ----------
    master : MotorBase or GearBase or Flywheel
        Driving rotating object, it must be an instance of MotorBase, GearBase or Flywheel.
    slave : GearBase or Flywheel
        Driven rotating object, it must be an instance of GearBase or Flywheel.

    Raises
    ------
    TypeError
        - If ``master`` is not an instance of ``MotorBase`` or ``GearBase`` or ``Flywheel``,
        - it ``slave`` is not an instance of ``GearBase`` or ``Flywheel``.
    """
    if not isinstance(master, MotorBase) and not isinstance(master, GearBase) and not isinstance(master, Flywheel):
        raise TypeError("Parameter 'master' must be an instance of MotorBase, GearBase or Flywheel.")

    if not isinstance(slave, GearBase) and not isinstance(slave, Flywheel):
        raise TypeError("Parameter 'slave' must be an instance of GearBase or Flywheel.")

    master.drives = slave
    slave.driven_by = master
    slave.master_gear_ratio = 1.0
