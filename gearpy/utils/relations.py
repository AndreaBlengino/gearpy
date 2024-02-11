from gearpy.mechanical_objects import MotorBase, GearBase, Flywheel, MatingMaster, MatingSlave
from typing import Union


def add_gear_mating(master: GearBase, slave: GearBase, efficiency: Union[float, int]):
    """Creates a gear mating between two existing gears. This mating is used to compose the ``Powertrain``. \n
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
        - if ``master`` and ``slave`` have different values for ``module``,
        - if ``master`` is an instance of ``HelicalGear`` but ``slave`` is not,
        - if ``slave`` is an instance of ``HelicalGear`` but ``master`` is not,
        - if both ``master`` and ``slave`` are instances of ``HelicalGear``, but they have different ``helix_angle``.

    See Also
    --------
    :py:class:`gearpy.mechanical_objects.spur_gear.SpurGear`
    :py:attr:`gearpy.mechanical_objects.spur_gear.SpurGear.master_gear_ratio`
    :py:attr:`gearpy.mechanical_objects.spur_gear.SpurGear.master_gear_efficiency`
    :py:attr:`gearpy.mechanical_objects.spur_gear.SpurGear.mating_role`
    :py:attr:`gearpy.mechanical_objects.spur_gear.SpurGear.drives`
    :py:attr:`gearpy.mechanical_objects.spur_gear.SpurGear.driven_by`
    :py:class:`gearpy.mechanical_objects.helical_gear.HelicalGear`
    :py:attr:`gearpy.mechanical_objects.helical_gear.HelicalGear.master_gear_ratio`
    :py:attr:`gearpy.mechanical_objects.helical_gear.HelicalGear.master_gear_efficiency`
    :py:attr:`gearpy.mechanical_objects.helical_gear.HelicalGear.mating_role`
    :py:attr:`gearpy.mechanical_objects.helical_gear.HelicalGear.drives`
    :py:attr:`gearpy.mechanical_objects.helical_gear.HelicalGear.driven_by`
    """
    if not isinstance(master, GearBase):
        raise TypeError(f"Parameter 'master' must be an instance of {GearBase.__name__!r}.")

    if not isinstance(slave, GearBase):
        raise TypeError(f"Parameter 'slave' must be an instance of {GearBase.__name__!r}.")

    if not isinstance(efficiency, float) and not isinstance(efficiency, int):
        raise TypeError("Parameter 'efficiency' must be a float or an integer.")

    if efficiency > 1 or efficiency < 0:
        raise ValueError("Parameter 'efficiency' must be within 0 and 1.")

    if master.module is not None and slave.module is not None:
        if master.module != slave.module:
            raise ValueError(f"Gears {master.name!r} and {slave.name!r} have different modules, "
                             f"so they cannot mate together.")

    if hasattr(master, 'helix_angle'):
        if hasattr(slave, 'helix_angle'):
            if master.helix_angle != slave.helix_angle:
                raise ValueError(f"Helical gears {master.name!r} and {slave.name!r} have different helix angles, "
                                 f"so they cannot mate together.")
        else:
            raise ValueError(f"Gear {master.name!r} is an helical gear but {slave.name!r} is not, "
                             f"so they cannot mate together.")
    else:
        if hasattr(slave, 'helix_angle'):
            raise ValueError(f"Gear {slave.name!r} is an helical gear but {master.name!r} is not, "
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
    The ``master`` rotating object is closest to the powertrain driving motor (or it is actually it) and transfers the
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

    See Also
    --------
    :py:attr:`gearpy.mechanical_objects.dc_motor.DCMotor.drives`
    :py:attr:`gearpy.mechanical_objects.flywheel.Flywheel.drives`
    :py:attr:`gearpy.mechanical_objects.flywheel.Flywheel.driven_by`
    :py:attr:`gearpy.mechanical_objects.flywheel.Flywheel.master_gear_ratio`
    :py:attr:`gearpy.mechanical_objects.spur_gear.SpurGear.drives`
    :py:attr:`gearpy.mechanical_objects.spur_gear.SpurGear.driven_by`
    :py:attr:`gearpy.mechanical_objects.spur_gear.SpurGear.master_gear_ratio`
    :py:attr:`gearpy.mechanical_objects.helical_gear.HelicalGear.drives`
    :py:attr:`gearpy.mechanical_objects.helical_gear.HelicalGear.driven_by`
    :py:attr:`gearpy.mechanical_objects.helical_gear.HelicalGear.master_gear_ratio`
    """
    if not isinstance(master, MotorBase) and not isinstance(master, GearBase) and not isinstance(master, Flywheel):
        raise TypeError(f"Parameter 'master' must be an instance of {MotorBase.__name__!r}, {GearBase.__name__!r} or "
                        f"{Flywheel.__name__!r}.")

    if not isinstance(slave, GearBase) and not isinstance(slave, Flywheel):
        raise TypeError(f"Parameter 'slave' must be an instance of {GearBase.__name__!r} or {Flywheel.__name__!r}.")

    master.drives = slave
    slave.driven_by = master
    slave.master_gear_ratio = 1.0
