from gearpy.mechanical_objects import (
    RotatingObject,
    MotorBase,
    GearBase,
    MatingMaster,
    MatingSlave,
    WormGear,
    WormWheel
)


def add_gear_mating(
    master: GearBase,
    slave: GearBase,
    efficiency: float | int
) -> None:
    """It creates a gear mating between two existing gears. This mating is used
    to compose the :py:class:`Powertrain <gearpy.powertrain.Powertrain>`. \n
    The ratio of the angular speed of the ``master`` gear over the angular
    speed of the ``slave`` gear is equal to the ratio of the ``slave`` gear
    number of teeth over the ``master`` gear number of teeth. \n
    The ``master`` gear is closest to the motor and transfers a fraction of the
    driving torque to the ``slave`` one, based on the ``efficiency`` value: the
    higher the ``efficiency``, the higher the fraction of transferred driving
    torque.

    Parameters
    ----------
    ``master`` : :py:class:`GearBase <gearpy.mechanical_objects.mechanical_object_base.GearBase>`
        Driving gear. It must be an instance of
        :py:class:`GearBase <gearpy.mechanical_objects.mechanical_object_base.GearBase>`.
    ``slave`` : :py:class:`GearBase <gearpy.mechanical_objects.mechanical_object_base.GearBase>`
        Driven gear. It must be an instance of
        :py:class:`GearBase <gearpy.mechanical_objects.mechanical_object_base.GearBase>`.
    ``efficiency`` : :py:class:`float` or :py:class:`int`
        Mechanical efficiency of the gear mating. It must be a
        :py:class:`float` or an :py:class:`int` between ``0`` and ``1``.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``master`` is not an instance of
             :py:class:`GearBase <gearpy.mechanical_objects.mechanical_object_base.GearBase>`,
           - if ``slave`` is not an instance of
             :py:class:`GearBase <gearpy.mechanical_objects.mechanical_object_base.GearBase>`,
           - if ``efficiency`` is not a :py:class:`float` or an
             :py:class:`int`.
       ``ValueError``
           - If ``master`` and ``slave`` are the same gear,
           - if ``efficiency`` is not within ``0`` and ``1``,
           - if ``master`` and ``slave`` have different values for ``module``
             (see
             :py:attr:`SpurGear.module <gearpy.mechanical_objects.spur_gear.SpurGear.module>`
             or
             :py:attr:`HelicalGear.module <gearpy.mechanical_objects.helical_gear.HelicalGear.module>`)
           - if ``master`` is an instance of
             :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`
             but ``slave`` is not,
           - if ``slave`` is an instance of
             :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`
             but ``master`` is not,
           - if both ``master`` and ``slave`` are instances of
             :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
             but they have different
             :py:attr:`HelicalGear.helix_angle <gearpy.mechanical_objects.helical_gear.HelicalGear.helix_angle>`.

    .. admonition:: See Also
       :class: seealso

       :py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>` \n
       :py:attr:`SpurGear.master_gear_ratio <gearpy.mechanical_objects.spur_gear.SpurGear.master_gear_ratio>` \n
       :py:attr:`SpurGear.master_gear_efficiency <gearpy.mechanical_objects.spur_gear.SpurGear.master_gear_efficiency>` \n
       :py:attr:`SpurGear.mating_role <gearpy.mechanical_objects.spur_gear.SpurGear.mating_role>` \n
       :py:attr:`SpurGear.drives <gearpy.mechanical_objects.spur_gear.SpurGear.drives>` \n
       :py:attr:`SpurGear.driven_by <gearpy.mechanical_objects.spur_gear.SpurGear.driven_by>` \n
       :py:attr:`SpurGear.module <gearpy.mechanical_objects.spur_gear.SpurGear.module>` \n
       :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>` \n
       :py:attr:`HelicalGear.master_gear_ratio <gearpy.mechanical_objects.helical_gear.HelicalGear.master_gear_ratio>` \n
       :py:attr:`HelicalGear.master_gear_efficiency <gearpy.mechanical_objects.helical_gear.HelicalGear.master_gear_efficiency>` \n
       :py:attr:`HelicalGear.mating_role <gearpy.mechanical_objects.helical_gear.HelicalGear.mating_role>` \n
       :py:attr:`HelicalGear.drives <gearpy.mechanical_objects.helical_gear.HelicalGear.drives>` \n
       :py:attr:`HelicalGear.driven_by <gearpy.mechanical_objects.helical_gear.HelicalGear.driven_by>` \n
       :py:attr:`HelicalGear.module <gearpy.mechanical_objects.helical_gear.HelicalGear.module>`
    """
    if not isinstance(master, GearBase):
        raise TypeError(
            f"Parameter 'master' must be an instance of {GearBase.__name__!r}."
        )

    if not isinstance(slave, GearBase):
        raise TypeError(
            f"Parameter 'slave' must be an instance of {GearBase.__name__!r}."
        )

    if master == slave:
        raise ValueError(
            "Parameters 'master' and 'slave' cannot be the same gear."
        )

    if not isinstance(efficiency, float | int):
        raise TypeError(
            "Parameter 'efficiency' must be a float or an integer."
        )

    if efficiency > 1 or efficiency < 0:
        raise ValueError("Parameter 'efficiency' must be within 0 and 1.")

    if master.module is not None and slave.module is not None:
        if master.module != slave.module:
            raise ValueError(
                f"Gears {master.name!r} and {slave.name!r} have different "
                f"modules, so they cannot mate together."
            )

    if hasattr(master, 'helix_angle'):
        if hasattr(slave, 'helix_angle'):
            if master.helix_angle != slave.helix_angle:
                raise ValueError(
                    f"Helical gears {master.name!r} and {slave.name!r} have "
                    f"different helix angles, so they cannot mate together."
                )
        else:
            raise ValueError(
                f"Gear {master.name!r} is an helical gear but {slave.name!r} "
                f"is not, so they cannot mate together."
            )
    else:
        if hasattr(slave, 'helix_angle'):
            raise ValueError(
                f"Gear {slave.name!r} is an helical gear but {master.name!r} "
                f"is not, so they cannot mate together."
            )

    master.drives = slave
    master.mating_role = MatingMaster
    slave.driven_by = master
    slave.mating_role = MatingSlave
    slave.master_gear_ratio = slave.n_teeth/master.n_teeth
    slave.master_gear_efficiency = efficiency


def add_worm_gear_mating(
    master: WormGear | WormWheel,
    slave: WormGear | WormWheel,
    friction_coefficient: float | int
) -> None:
    """It creates a gear mating between a worm gear and a worm wheel. This
    mating is used to compose the
    :py:class:`Powertrain <gearpy.powertrain.Powertrain>`. \n
    The ``master`` gear is closest to the motor and transfers a fraction of the
    driving torque to the ``slave`` one, based on the mating efficiency, which
    depends on the ``friction_coefficient``: the higher the
    ``friction_coefficient``, the lower the fraction of transferred driving
    torque.

    Parameters
    ----------
    ``master`` : :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>` or :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`
        Driving gear. It must be an instance of
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>` or
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`,
        but different from ``slave``.
    ``slave`` : :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>` or :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`
        Driven gear. It must be an instance of
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>` or
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`,
        but different from ``master``.
    ``friction_coefficient`` : :py:class:`float` or :py:class:`int`
        Static friction coefficient of the gear mating. It must be a
        :py:class:`float` or an :py:class:`int` between ``0`` and ``1``.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``master`` is not an instance of
             :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`
             or
             :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`,
           - if ``slave`` is not an instance of
             :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`
             or
             :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`,
           - if both ``master`` and ``slave`` are instances of
             :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
           - if both ``master`` and ``slave`` are instances of
             :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`,
           - if ``friction_coefficient`` is not a :py:class:`float` or an
             :py:class:`int`.
       ``ValueError``
           - If ``friction_coefficient`` is not within ``0`` and ``1``,
           - if ``master`` and ``slave`` have different values for
             ``pressure_angle`` (see 
             :py:attr:`WormGear.pressure_angle <gearpy.mechanical_objects.worm_gear.WormGear.pressure_angle>`
             or
             :py:class:`WormWheel.pressure_angle <gearpy.mechanical_objects.worm_wheel.WormWheel.pressure_angle>`)
    """ \
    r"""
    .. admonition:: Notes
       :class: tip

       The gear ratio of the mating can be computed with the following
       relationship, regardless of ``master`` or ``slave`` roles:

       .. math::
           \tau = \frac{n_z}{n_s}

       where:

       - :math:`\tau` is the gear ratio, the ratio between the worm gear
         angular speed and the worm wheel angular speed,
       - :math:`n_z` is the worm wheel number of teeth,
       - :math:`n_s` is the worm gear number of starts.

       If the
       :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>` is
       the ``master`` and the
       :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`
       is the ``slave``, then the gear mating efficiency can be computed with
       the relationship:

       .. math::
           \eta = \frac{\cos \alpha - f \, \tan \beta}{\cos \alpha +
           \frac{f}{\tan \beta}}

       otherwise, if the
       :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>` is
       the ``slave`` and the
       :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`
       is the ``master``, then the gear mating efficiency can be computed with
       the relationship:

       .. math::
           \eta = \frac{\cos \alpha - \frac{f}{\tan \beta}}{\cos \alpha + f \,
           \tan \beta}

       where:

       - :math:`\eta` is the gear mating efficiency,
       - :math:`\alpha` is the gear pressure angle, equal for both worm gear
         and worm wheel
         (:py:attr:`WormGear.pressure_angle <gearpy.mechanical_objects.worm_gear.WormGear.pressure_angle>`
         or
         :py:class:`WormWheel.pressure_angle <gearpy.mechanical_objects.worm_wheel.WormWheel.pressure_angle>`),
       - :math:`f` is the ``friction_coefficient``,
       - :math:`\beta` is the gear helix angle
         (:py:attr:`WormGear.helix_angle <gearpy.mechanical_objects.worm_gear.WormGear.helix_angle>`
         or
         :py:class:`WormWheel.helix_angle <gearpy.mechanical_objects.worm_wheel.WormWheel.helix_angle>`).

       The mating self-locking condition can be checked as:

       .. math::
           f > \cos \alpha \, \tan \beta
    """ \
    """
    .. admonition:: See Also
       :class: seealso

       :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>` \n
       :py:attr:`WormGear.master_gear_ratio <gearpy.mechanical_objects.worm_gear.WormGear.master_gear_ratio>` \n
       :py:attr:`WormGear.master_gear_efficiency <gearpy.mechanical_objects.worm_gear.WormGear.master_gear_efficiency>` \n
       :py:attr:`WormGear.mating_role <gearpy.mechanical_objects.worm_gear.WormGear.mating_role>` \n
       :py:attr:`WormGear.drives <gearpy.mechanical_objects.worm_gear.WormGear.drives>` \n
       :py:attr:`WormGear.driven_by <gearpy.mechanical_objects.worm_gear.WormGear.driven_by>` \n
       :py:attr:`WormGear.pressure_angle <gearpy.mechanical_objects.worm_gear.WormGear.pressure_angle>` \n
       :py:attr:`WormGear.helix_angle <gearpy.mechanical_objects.worm_gear.WormGear.helix_angle>` \n
       :py:attr:`WormGear.self_locking <gearpy.mechanical_objects.worm_gear.WormGear.self_locking>` \n
       :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>` \n
       :py:attr:`WormWheel.master_gear_ratio <gearpy.mechanical_objects.worm_wheel.WormWheel.master_gear_ratio>` \n
       :py:attr:`WormWheel.master_gear_efficiency <gearpy.mechanical_objects.worm_wheel.WormWheel.master_gear_efficiency>` \n
       :py:attr:`WormWheel.mating_role <gearpy.mechanical_objects.worm_wheel.WormWheel.mating_role>` \n
       :py:attr:`WormWheel.drives <gearpy.mechanical_objects.worm_wheel.WormWheel.drives>` \n
       :py:attr:`WormWheel.driven_by <gearpy.mechanical_objects.worm_wheel.WormWheel.driven_by>` \n
       :py:attr:`WormWheel.pressure_angle <gearpy.mechanical_objects.worm_wheel.WormWheel.pressure_angle>` \n
       :py:attr:`WormWheel.helix_angle <gearpy.mechanical_objects.worm_wheel.WormWheel.helix_angle>`
    """
    if not isinstance(master, WormGear | WormWheel):
        raise TypeError(
            f"Parameter 'master' must be an instance of {WormGear.__name__!r} "
            f"or {WormWheel.__name__!r}."
        )

    if not isinstance(slave, WormGear | WormWheel):
        raise TypeError(
            f"Parameter 'slave' must be an instance of {WormGear.__name__!r} "
            f"or {WormWheel.__name__!r}."
        )

    if isinstance(master, WormGear) and isinstance(slave, WormGear):
        raise TypeError(
            f"Both 'master' and 'slave' are instances of "
            f"{WormGear.__name__!r}, so they cannot mate together. One element"
            f" has to be a {WormGear.__name__!r} and the other one has to be a"
            f" {WormWheel!r}."
        )

    if isinstance(master, WormWheel) and isinstance(slave, WormWheel):
        raise TypeError(
            f"Both 'master' and 'slave' are instances of "
            f"{WormWheel.__name__!r}, so they cannot mate together. One "
            f"element has to be a {WormGear.__name__!r} and the other one has "
            f"to be a {WormWheel!r}."
        )

    if not isinstance(friction_coefficient, float | int):
        raise TypeError(
            "Parameter 'friction_coefficient' must be a float or an integer."
        )

    if friction_coefficient > 1 or friction_coefficient < 0:
        raise ValueError(
            "Parameter 'friction_coefficient' must be within 0 and 1."
        )

    if master.pressure_angle != slave.pressure_angle:
        raise ValueError(
            f"Gears {master.name!r} and {slave.name!r} have different "
            f"pressure angles, so they cannot mate together."
        )

    master.drives = slave
    master.mating_role = MatingMaster
    slave.driven_by = master
    slave.mating_role = MatingSlave
    if isinstance(master, WormGear) and isinstance(slave, WormWheel):
        slave.master_gear_ratio = slave.n_teeth/master.n_starts
        efficiency = \
            (master.pressure_angle.cos() -
                friction_coefficient*master.helix_angle.tan()) / \
            (master.pressure_angle.cos() +
                friction_coefficient/master.helix_angle.tan())
        master.self_locking = \
            friction_coefficient > master.pressure_angle.cos() * \
            master.helix_angle.tan()
    else:
        slave.master_gear_ratio = slave.n_starts/master.n_teeth
        efficiency = \
            (master.pressure_angle.cos() -
                friction_coefficient/master.helix_angle.tan()) / \
            (master.pressure_angle.cos() +
                friction_coefficient*master.helix_angle.tan())
        slave.self_locking = \
            friction_coefficient > slave.pressure_angle.cos() * \
            slave.helix_angle.tan()
    slave.master_gear_efficiency = efficiency


def add_fixed_joint(
    master: RotatingObject,
    slave: RotatingObject
) -> None:
    """It creates a fixed joint between a ``master`` rotating object and a
    ``slave`` one. The fixed joint forces the two elements to rotate at the
    same angular position, speed and acceleration. \n
    The ``master`` rotating object is closest to the powertrain driving motor
    (or it is actually it) and transfers the whole driving torque to the
    ``slave`` one.

    Parameters
    ----------
    ``master`` : :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
        Driving rotating object, it must be an instance of
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`.
    ``slave`` : :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
        Driven rotating object, it must be an instance of
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`,
        but not an instance of
        :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``master`` is not an instance of
             :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`,
           - if ``slave`` is not an instance of
             :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`,
           - if ``slave`` is an instance of
             :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`.
       ``ValueError``
           If ``master`` and ``slave`` are the same rotating object.

    .. admonition:: See Also
       :class: seealso

       :py:attr:`DCMotor.drives <gearpy.mechanical_objects.dc_motor.DCMotor.drives>` \n
       :py:attr:`Flywheel.drives <gearpy.mechanical_objects.flywheel.Flywheel.drives>` \n
       :py:attr:`Flywheel.driven_by <gearpy.mechanical_objects.flywheel.Flywheel.driven_by>` \n
       :py:attr:`Flywheel.master_gear_ratio <gearpy.mechanical_objects.flywheel.Flywheel.master_gear_ratio>` \n
       :py:attr:`SpurGear.drives <gearpy.mechanical_objects.spur_gear.SpurGear.drives>` \n
       :py:attr:`SpurGear.driven_by <gearpy.mechanical_objects.spur_gear.SpurGear.driven_by>` \n
       :py:attr:`SpurGear.master_gear_ratio <gearpy.mechanical_objects.spur_gear.SpurGear.master_gear_ratio>` \n
       :py:attr:`HelicalGear.drives <gearpy.mechanical_objects.helical_gear.HelicalGear.drives>` \n
       :py:attr:`HelicalGear.driven_by <gearpy.mechanical_objects.helical_gear.HelicalGear.driven_by>` \n
       :py:attr:`HelicalGear.master_gear_ratio <gearpy.mechanical_objects.helical_gear.HelicalGear.master_gear_ratio>` \n
       :py:attr:`WormGear.drives <gearpy.mechanical_objects.worm_gear.WormGear.drives>` \n
       :py:attr:`WormGear.driven_by <gearpy.mechanical_objects.worm_gear.WormGear.driven_by>` \n
       :py:attr:`WormGear.master_gear_ratio <gearpy.mechanical_objects.worm_gear.WormGear.master_gear_ratio>` \n
       :py:attr:`WormWheel.drives <gearpy.mechanical_objects.worm_wheel.WormWheel.drives>` \n
       :py:attr:`WormWheel.driven_by <gearpy.mechanical_objects.worm_wheel.WormWheel.driven_by>` \n
       :py:attr:`WormWheel.master_gear_ratio <gearpy.mechanical_objects.worm_wheel.WormWheel.master_gear_ratio>`
    """
    if not isinstance(master, RotatingObject):
        raise TypeError(
            f"Parameter 'master' must be an instance of "
            f"{RotatingObject.__name__!r}."
        )

    if not isinstance(slave, RotatingObject):
        raise TypeError(
            f"Parameter 'slave' must be an instance of {GearBase.__name__!r}."
        )

    if isinstance(slave, MotorBase):
        raise TypeError(
            f"Parameter 'slave' is an instance of {MotorBase.__name__!r}, but "
            f"motor can only be 'master'."
        )

    if master == slave:
        raise ValueError(
            "Parameters 'master' and 'slave' cannot be the same rotating "
            "object."
        )

    master.drives = slave
    slave.driven_by = master
    slave.master_gear_ratio = 1.0
