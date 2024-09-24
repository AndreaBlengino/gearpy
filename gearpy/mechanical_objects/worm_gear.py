from gearpy.units import (
    AngularPosition,
    AngularSpeed,
    AngularAcceleration,
    Angle,
    Force,
    InertiaMoment,
    Length,
    Time,
    Torque,
    UnitBase
)
from inspect import signature
from .mating_roles import MatingMaster, MatingSlave
from .mechanical_object_base import (
    RotatingObject,
    Role,
    WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES,
    worm_gear_and_wheel_maximum_helix_angle_function
)
from typing import Callable, Optional


class WormGear(RotatingObject):
    r""":py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`
    object.

    Attributes
    ----------
    :py:attr:`name` : :py:class:`str`
        Name of the worm gear.
    :py:attr:`n_starts` : :py:class:`int`
        Number of starts, which refers to the number of independent threads
        running around the length of the thread.
    :py:attr:`inertia_moment` : :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`
        Moment of inertia of the gear.
    :py:attr:`helix_angle` : :py:class:`Angle <gearpy.units.units.Angle>`
        Helix angle of the worm gear.
    :py:attr:`pressure_angle` : :py:class:`Angle <gearpy.units.units.Angle>`
        Pressure angle of the worm gear.
    :py:attr:`reference_diameter` : :py:class:`Length <gearpy.units.units.Length>`
        Reference diameter of the gear.
    :py:attr:`self_locking` : :py:class:`bool`
        Whether the :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`
        cannot be moved by the mating
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`.
    :py:attr:`driven_by` : :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
        Rotating object that drives the gear, for example a
        :py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>`, a
        :py:class:`Flywheel <gearpy.mechanical_objects.flywheel.Flywheel>` or
        another gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
    :py:attr:`drives` : :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
        Rotating object driven by the gear, it can be a
        :py:class:`Flywheel <gearpy.mechanical_objects.flywheel.Flywheel>` or
        another gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
    :py:attr:`master_gear_ratio` : :py:class:`float`
        Gear ratio of the mating between the gear and its driving gear.
    :py:attr:`master_gear_efficiency` : :py:class:`float` or :py:class:`int`
        Efficiency of the gear mating between the gear and its driving gear.
    :py:attr:`mating_role`: :py:class:`Role <gearpy.mechanical_objects.mechanical_object_base.Role>`
        The role of the gear in the gear mating.
    :py:attr:`angular_position` : :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`
        Angular position of the gear.
    :py:attr:`angular_speed` : :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`
        Angular speed of the gear.
    :py:attr:`angular_acceleration` : :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`
        Angular acceleration of the gear.
    :py:attr:`torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Net torque applied on the gear.
    :py:attr:`driving_torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Driving torque applied on the gear by its driving gear.
    :py:attr:`load_torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Load torque applied on the gear by its driven gear or an external load.
    :py:attr:`tangential_force` : :py:class:`Force <gearpy.units.units.Force>`
        Tangential force applied on the gear threads by the mating gear.
    :py:attr:`tangential_force_is_computable` : :py:class:`bool`
        Whether is possible to compute the :py:attr:`tangential_force` on the
        gear threads.
    :py:attr:`time_variables` : :py:class:`dict`
        Time variables of the gear.

    Methods
    -------
    :py:meth:`compute_tangential_force`
        It computes the :py:attr:`tangential_force` applied on the gear threads
        by the mating gear.
    :py:meth:`external_torque`
        Custom function to compute the external torque applied on the gear.
    :py:meth:`update_time_variables`
        It updates :py:attr:`time_variables` dictionary by appending the last
        value of each time variable to
        corresponding list.
    """

    def __init__(
        self,
        name: str,
        n_starts: int,
        inertia_moment: InertiaMoment,
        helix_angle: Angle,
        pressure_angle: Angle,
        reference_diameter: Optional[Length] = None
    ):
        super().__init__(name=name, inertia_moment=inertia_moment)

        if not isinstance(n_starts, int):
            raise TypeError("Parameter 'n_starts' must be an integer.")

        if n_starts < 1:
            raise ValueError(
                "Parameter 'n_starts' must be equal to or greater than one."
            )

        if not isinstance(helix_angle, Angle):
            raise TypeError(
                f"Parameter 'helix_angle' must be an instance of "
                f"{Angle.__name__!r}."
            )

        if not isinstance(pressure_angle, Angle):
            raise TypeError(
                f"Parameter 'pressure_angle' must be an instance of "
                f"{Angle.__name__!r}."
            )

        if pressure_angle not in WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES:
            raise ValueError(
                f"Value {pressure_angle!r} for parameter 'pressure_angle' not "
                f"available. Available pressure angles are: "
                f"{WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES}"
            )

        maximum_helix_angle = worm_gear_and_wheel_maximum_helix_angle_function(
            pressure_angle=pressure_angle
        )
        if helix_angle > maximum_helix_angle:
            raise ValueError(
                f"Parameter 'helix_angle' too high. For a {pressure_angle} "
                f"'pressure_angle', the maximum 'helix_angle' is "
                f"{maximum_helix_angle}."
            )

        if reference_diameter is not None:
            if not isinstance(reference_diameter, Length):
                raise TypeError(
                    f"Parameter 'reference_diameter' must be an instance of "
                    f"{Length.__name__!r}."
                )

        self.__n_starts = n_starts
        self.__helix_angle = helix_angle
        self.__pressure_angle = pressure_angle
        self.__reference_diameter = reference_diameter
        self.__self_locking = None
        self.__driven_by = None
        self.__drives = None
        self.__master_gear_ratio = None
        self.__master_gear_efficiency = 1
        self.__mating_role = None
        self.__external_torque = None

        if self.tangential_force_is_computable:
            self.__tangential_force = None
            self.time_variables['tangential force'] = []

    @property
    def name(self) -> str:
        """Name of the worm gear. It must be a non-empty :py:class:`str`. \n
        It must be a unique name, not shared by other elements in the
        powertrain elements. \n
        Once set at the worm gear instantiation, it cannot be changed
        afterward.

        Returns
        -------
        :py:class:`str`
            Name of the worm gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`name` is not a :py:class:`str`.
           ``ValueError``
               If :py:attr:`name` is an empty :py:class:`str`.
        """
        return super().name

    @property
    def n_starts(self) -> int:
        """Number of starts, which refers to the number of independent threads
        running around the length of the thread.
        It must be a positive :py:class:`int` equal to or greater than
        ``1``. \n
        Once set at the worm gear instantiation, it cannot be changed
        afterward.

        Returns
        -------
        :py:class:`int`
            Number of starts, which refers to the number of independent threads
            running around the length of the thread.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`n_starts` is not an :py:class:`int`.
           ``ValueError``
               If :py:attr:`n_starts` is lower than ``1``.
        """
        return self.__n_starts

    @property
    def inertia_moment(self) -> InertiaMoment:
        """Moment of inertia of the gear. It must be an instance of
        :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`. \n
        Once set at the worm gear instantiation, it cannot be changed
        afterward.

        Returns
        -------
        :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`
            Moment of inertia of the gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`inertia_moment` is not an instance of
               :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`.
        """
        return super().inertia_moment

    @property
    def helix_angle(self) -> Angle:
        """Helix angle of the worm gear. It must be an instance of
        :py:class:`Angle <gearpy.units.units.Angle>`. \n
        The maximum allowable value of helix angle depends on the
        :py:attr:`pressure_angle`. \n
        Once set at the worm gear instantiation, it cannot be changed
        afterward.

        Returns
        -------
        :py:class:`Angle <gearpy.units.units.Angle>`
            The helix angle of the worm gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`helix_angle` is not an instance of
               :py:class:`Angle <gearpy.units.units.Angle>`.
           ``ValueError``
               If :py:attr:`helix_angle` is greater than the maximum allowable
               helix angle, depending on :py:attr:`pressure_angle` value.
        """
        return self.__helix_angle

    @property
    def pressure_angle(self) -> Angle:
        """Pressure angle of the worm gear. It must be an instance of
        :py:class:`Angle <gearpy.units.units.Angle>` and its value must be one
        of: 14.5 deg, 20 deg, 25 deg or 30 deg. \n
        Once set at the worm gear instantiation, it cannot be changed
        afterward.

        Returns
        -------
        :py:class:`Angle <gearpy.units.units.Angle>`
            The pressure angle of the worm gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`pressure_angle` is not an instance of
               :py:class:`Angle <gearpy.units.units.Angle>`.
           ``ValueError``
               If :py:attr:`pressure_angle` value is not among available ones:
               14.5 deg, 20 deg, 25 deg or 30 deg.
        """
        return self.__pressure_angle

    @property
    def reference_diameter(self) -> Optional[Length]:
        """Reference diameter of the gear. It must be an instance of
        :py:class:`Length <gearpy.units.units.Length>`. \n
        Once set at the worm gear instantiation, it cannot be changed
        afterward.

        Returns
        -------
        :py:class:`Length <gearpy.units.units.Length>`
            Reference diameter of the gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`reference_diameter` is not an instance of
               :py:class:`Length <gearpy.units.units.Length>`.
        """
        return self.__reference_diameter

    @property
    def self_locking(self) -> bool:
        """Whether the
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`
        cannot be moved by the mating
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`. \n
        The gear mating can be self-locking if the amount of friction is high
        enough with respect to the gear pressure and helix angles. \n
        If the mating is self-locking, then the
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`
        cannot be moved by the mating
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`. \n
        To set this property use
        :py:func:`add_worm_gear_mating <gearpy.utils.relations.add_worm_gear_mating>`.

        Returns
        -------
        :py:class:`bool`
            Whether the :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`
            cannot be moved by the mating
            :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`.
        """
        return self.__self_locking

    @self_locking.setter
    def self_locking(self, self_locking: bool):
        if not isinstance(self_locking, bool):
            raise TypeError("Parameter 'self_locking' must be a boolean.")

        self.__self_locking = self_locking

    @property
    def driven_by(self) -> RotatingObject:
        """Rotating object that drives the gear, for example a
        :py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>`, a
        :py:class:`Flywheel <gearpy.mechanical_objects.flywheel.Flywheel>` or
        another gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
        It must be a
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`. \n
        To set this property use
        :py:func:`add_worm_gear_mating <gearpy.utils.relations.add_worm_gear_mating>`
        or :py:func:`add_fixed_joint <gearpy.utils.relations.add_fixed_joint>`.

        Returns
        -------
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
            Master rotating object that drives the gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`driven_by` is not an instance of
               :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`.
        """
        return self.__driven_by

    @driven_by.setter
    def driven_by(self, driven_by: RotatingObject):
        if not isinstance(driven_by, RotatingObject):
            raise TypeError(
                f"Parameter 'driven_by' must be an instance of "
                f"{RotatingObject.__name__!r}."
            )

        self.__driven_by = driven_by

    @property
    def drives(self) -> RotatingObject:
        """Rotating object driven by the gear, it can be a
        :py:class:`Flywheel <gearpy.mechanical_objects.flywheel.Flywheel>` or
        another gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
        It must be a
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`. \n
        To set this property use
        :py:func:`add_worm_gear_mating <gearpy.utils.relations.add_worm_gear_mating>`
        or :py:func:`add_fixed_joint <gearpy.utils.relations.add_fixed_joint>`.

        Returns
        -------
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
            Rotating object driven by the gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`drives` is not an instance of
               :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`.
        """
        return self.__drives

    @drives.setter
    def drives(self, drives: RotatingObject):
        if not isinstance(drives, RotatingObject):
            raise TypeError(
                f"Parameter 'drives' must be an instance of "
                f"{RotatingObject.__name__!r}."
            )

        self.__drives = drives

    @property
    def master_gear_ratio(self) -> float:
        """Gear ratio of the mating between the gear and its driving gear. It
        must be a positive a :py:class:`float`. \n
        If the worm gear is fixed to another driving
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`,
        then the ratio is ``1``, otherwise it is defined as the ratio between
        the worm gear number of starts :py:attr:`n_starts` and the driving
        wheel gear number of teeth
        :py:attr:`WormWheel.n_teeth <gearpy.mechanical_objects.worm_wheel.WormWheel.n_teeth>`. \n
        To set this property use
        :py:func:`add_worm_gear_mating <gearpy.utils.relations.add_worm_gear_mating>`
        or :py:func:`add_fixed_joint <gearpy.utils.relations.add_fixed_joint>`.

        Returns
        -------
        :py:class:`float`
            Gear ratio of the mating between the gear and its driving gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`master_gear_ratio` is not a :py:class:`float`.
           ``ValueError``
               If :py:attr:`master_gear_ratio` is negative or null.
        """
        return self.__master_gear_ratio

    @master_gear_ratio.setter
    def master_gear_ratio(self, master_gear_ratio: float):
        if not isinstance(master_gear_ratio, float):
            raise TypeError("Parameter 'master_gear_ratio' must be a float.")

        if master_gear_ratio <= 0:
            raise ValueError("Parameter 'master_gear_ratio' must be positive.")

        self.__master_gear_ratio = master_gear_ratio

    @property
    def master_gear_efficiency(self) -> float | int:
        """Efficiency of the gear mating between the gear and its driving gear.
        It must be a :py:class:`float` or an :py:class:`int` within ``0`` and
        ``1``. \n
        To set this property use
        :py:func:`add_worm_gear_mating <gearpy.utils.relations.add_worm_gear_mating>`
        or :py:func:`add_fixed_joint <gearpy.utils.relations.add_fixed_joint>`.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Efficiency of the gear mating between the gear and its driving
            gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`master_gear_efficiency` is not a :py:class:`float`
               or an :py:class:`int`.
           ``ValueError``
               If :py:attr:`master_gear_efficiency` is not within ``0`` and
               ``1``.
        """
        return self.__master_gear_efficiency

    @master_gear_efficiency.setter
    def master_gear_efficiency(self, master_gear_efficiency: float | int):
        if not isinstance(master_gear_efficiency, float | int):
            raise TypeError(
                "Parameter 'master_gear_efficiency' must be a float or an "
                "integer."
            )

        if master_gear_efficiency > 1 or master_gear_efficiency < 0:
            raise ValueError(
                "Parameter 'master_gear_efficiency' must be within 0 and 1."
            )

        self.__master_gear_efficiency = master_gear_efficiency

    @property
    def mating_role(self) -> Role:
        """Role of the gear in the gear mating. \n
        If the gear drives the mate one, then it is the "master" gear and its
        role is
        :py:class:`MatingMaster <gearpy.mechanical_objects.mating_roles.MatingMaster>`,
        otherwise it is the "slave" one and its role is
        :py:class:`MatingSlave <gearpy.mechanical_objects.mating_roles.MatingSlave>`. \n
        To set this parameter use
        :py:func:`add_worm_gear_mating <gearpy.utils.relations.add_worm_gear_mating>`.

        Returns
        -------
        :py:class:`Role <gearpy.mechanical_objects.mechanical_object_base.Role>`
            The role of the gear in the gear mating.

        .. admonition:: Raises
           :class: warning

           ``ValueError``
               If :py:attr:`mating_role` is not a subclass of
               :py:class:`Role <gearpy.mechanical_objects.mechanical_object_base.Role>`.
        """
        return self.__mating_role

    @mating_role.setter
    def mating_role(self, mating_role: Role):
        if hasattr(mating_role, '__name__'):
            if not issubclass(mating_role, Role):
                raise TypeError(
                    f"Parameter 'mating_role' must be a subclass of "
                    f"{Role.__name__!r}."
                )
        else:
            raise TypeError(
                f"Parameter 'mating_role' must be a subclass of "
                f"{Role.__name__!r}."
            )

        self.__mating_role = mating_role

    @property
    def angular_position(self) -> AngularPosition:
        """Angular position of the gear. It must be an instance of
        :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`.

        Returns
        -------
        :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`
            Angular position of the gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`angular_position` is not an instance of
               :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`.
        """
        return super().angular_position

    @angular_position.setter
    def angular_position(self, angular_position: AngularPosition):
        super(
            WormGear,
            type(self)
        ).angular_position.fset(self, angular_position)

    @property
    def angular_speed(self) -> AngularSpeed:
        """Angular speed of the gear. It must be an instance of
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`.

        Returns
        -------
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`
            Angular speed of the gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`angular_speed` is not an instance of
               :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`.
        """
        return super().angular_speed

    @angular_speed.setter
    def angular_speed(self, angular_speed: AngularSpeed):
        super(WormGear, type(self)).angular_speed.fset(self, angular_speed)

    @property
    def angular_acceleration(self) -> AngularAcceleration:
        """Angular acceleration of the gear. It must be an instance of
        :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`.

        Returns
        -------
        :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`
            Angular acceleration of the gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`angular_acceleration` is not an instance of
               :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`.
        """
        return super().angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        super(
            WormGear,
            type(self)
        ).angular_acceleration.fset(self, angular_acceleration)

    @property
    def torque(self) -> Torque:
        """Net torque applied on the gear. It must be an instance of
        :py:class:`Torque <gearpy.units.units.Torque>`. \n
        It is computed as the difference between :py:attr:`driving_torque` and
        :py:attr:`load_torque`.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Net torque applied on the gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.
        """
        return super().torque

    @torque.setter
    def torque(self, torque: Torque):
        super(WormGear, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Torque:
        """Driving torque applied on the gear by its driving gear. It must be
        an instance of :py:class:`Torque <gearpy.units.units.Torque>`.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Driving torque applied on the gear by its driving gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`driving_torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.
        """
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Torque):
        super(WormGear, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Torque:
        """Load torque applied on the gear by its driven gear or an external
        load. It must be an instance of
        :py:class:`Torque <gearpy.units.units.Torque>`.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Load torque applied on the gear by its driven gear or an external
            load.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`load_torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.
        """
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Torque):
        super(WormGear, type(self)).load_torque.fset(self, load_torque)

    @property
    def tangential_force(self) -> Force:
        """Tangential force applied on the gear threads by the mating gear. It
        must be an instance of :py:class:`Force <gearpy.units.units.Force>`.

        Returns
        -------
        :py:class:`Force <gearpy.units.units.Force>`
            Tangential force applied on the gear threads by the mating gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`tangential_force` is not an instance of
               :py:class:`Force <gearpy.units.units.Force>`.

        .. admonition:: See Also
           :class: seealso

           :py:meth:`compute_tangential_force`
        """
        return self.__tangential_force

    @tangential_force.setter
    def tangential_force(self, tangential_force: Force):
        if not isinstance(tangential_force, Force):
            raise TypeError(
                f"Parameter 'tangential_force' must be an instance of "
                f"{Force.__name__!r}."
            )

        self.__tangential_force = tangential_force

    def compute_tangential_force(self) -> None:
        """It computes the :py:attr:`tangential_force` applied on the gear
        threads by the mating gear. \n
        Considering a gear mating:

        - if the gear is the master one, then it takes into account the
          :py:attr:`load_torque` for the computation,
        - if the gear is the slave one, then it take into account the
          :py:attr:`driving_torque` for the computation.

        The tangential force is computed dividing the just described reference
        torque by the reference radius (half of the
        :py:attr:`reference_diameter`).

        .. admonition:: Raises
           :class: warning

           ``ValueError``
               If a gear mating between two gears has not been set.
        """
        if self.mating_role == MatingMaster:
            self.tangential_force = \
                abs(self.load_torque)/(self.reference_diameter/2) * \
                self.helix_angle.tan()
        elif self.mating_role == MatingSlave:
            self.tangential_force = abs(self.driving_torque) / \
                (self.reference_diameter/2)*self.helix_angle.tan()
        else:
            raise ValueError(
                "Gear mating not defined. Use "
                "'gearpy.utils.add_worm_gear_mating' to set up a mating "
                "between two gears."
            )

    @property
    def tangential_force_is_computable(self) -> bool:
        """Whether is possible to compute the :py:attr:`tangential_force` on
        the gear threads. \n
        The tangential force computation depends on the value of
        :py:attr:`reference_diameter`, so if this optional parameter has been
        set at worm gear instantiation, then it is possible to compute the
        tangential force and this property is ``True``, otherwise is ``False``.

        Returns
        -------
        :py:class:`bool`
            Whether is possible to compute the tangential force on the gear
            threads.

        .. admonition:: See Also
           :class: seealso

           :py:meth:`compute_tangential_force`
        """
        return self.__reference_diameter is not None

    @property
    def external_torque(
        self
    ) -> Callable[[AngularPosition, AngularSpeed, Time], Torque]:
        """Custom function to compute the external torque applied on the gear.
        It must be a function with parameters ``angular_position``,
        ``angular_speed`` and ``time``. The function must return an instance of
        :py:class:`Torque <gearpy.units.units.Torque>`.

        Returns
        -------
        :py:obj:`Callable <typing.Callable>`
            The function to compute the external torque applied on the gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:meth:`external_torque` is not callable.
           ``KeyError``
               If :py:meth:`external_torque` misses parameters
               ``angular_position``, ``angular_speed`` or ``time``.

        .. admonition:: Examples
           :class: important

           Constant torque, not dependent on ``angular_position``,
           ``angular_speed`` or ``time``.

           >>> from gearpy.mechanical_objects import WormGear
           >>> from gearpy.units import InertiaMoment, Torque, Angle
           >>> gear = WormGear(
           ...     name='gear',
           ...     n_starts=1,
           ...     inertia_moment=InertiaMoment(1, 'kgm^2'),
           ...     pressure_angle = Angle(20, 'deg'),
           ...     helix_angle = Angle(10, 'deg')
           ... )
           >>> gear.external_torque = \\
           ...     lambda angular_position, angular_speed, time: Torque(5, 'Nm')

           Torque dependent on ``angular_position`` and ``time``. \n
           In this case the gear gets a periodic load, dependent on time, and
           an extra load dependent on its angular position. The dependence by
           angular position may be used to model cases where cams are involved.

           >>> import numpy as np
           >>> from gearpy.units import AngularPosition, AngularSpeed, Time
           >>> def custom_external_torque(
           ...     angular_position: AngularPosition,
           ...     angular_speed: AngularSpeed,
           ...     time: Time
           ... ) -> Torque:
           >>>     return Torque(
           ...         value=angular_position.sin() +
           ...         np.cos(time.to('sec').value),
           ...         unit='Nm'
           ...     )
           >>> gear.external_torque = custom_external_torque

           Torque dependent on ``angular_position``, ``angular_speed`` and
           ``time``. \n
           With respect ot the previous case, the gear gets an extra load
           dependent on its angular speed. The dependence by angular speed may
           be used to model cases where air friction is not negligible.

           >>> def complex_external_torque(
           ...     angular_position: AngularPosition,
           ...     angular_speed: AngularSpeed,
           ...     time: Time
           ... ) -> Torque:
           >>>     return Torque(
           ...         value=angular_position.sin() +
           ...         0.001*(angular_speed.to('rad/s').value)**2 +
           ...         np.cos(time.to('sec').value),
           ...         unit='Nm'
           ...     )
           >>> gear.external_torque = complex_external_torque
        """
        return self.__external_torque

    @external_torque.setter
    def external_torque(
        self,
        external_torque: Callable[
            [AngularPosition, AngularSpeed, Time],
            Torque
        ]
    ):
        if not isinstance(external_torque, Callable):
            raise TypeError("Parameter 'external_torque' must be callable.")

        sig = signature(external_torque)
        for parameter in ['angular_position', 'angular_speed', 'time']:
            if parameter not in sig.parameters.keys():
                raise KeyError(
                    f"Function 'external_torque' misses parameter "
                    f"{parameter!r}."
                )

        self.__external_torque = external_torque

    @property
    def time_variables(self) -> dict[str, list[UnitBase]]:
        """Time variables of the gear. Each time variable is stored as a
        dictionary key-value pair. The available time variables are:

        - :py:attr:`angular_position`: ``'angular position'``,
        - :py:attr:`angular_speed`: ``'angular speed'``,
        - :py:attr:`angular_acceleration`: ``'angular acceleration'``,
        - :py:attr:`torque`: ``'torque'``,
        - :py:attr:`driving_torque`: ``'driving torque'``,
        - :py:attr:`load_torque`: ``'load torque'``,
        - :py:attr:`tangential_force`: ``'tangential force'``

        ``'tangential force'`` is listed among time variables only if they are
        computable indeed, depending on which gear parameters are set at gear
        instantiation; see :py:attr:`tangential_force_is_computable`. \n
        Corresponding values of the dictionary are lists of the respective time
        variable values. \n
        At each time iteration, the :py:class:`Solver <gearpy.solver.Solver>`
        appends every time variables' values to the relative list in the
        dictionary.

        Returns
        -------
        :py:class:`dict`
            Time variables of the gear.

        .. admonition:: See Also
           :class: seealso

           :py:meth:`update_time_variables`
        """
        return super().time_variables

    def update_time_variables(self) -> None:
        """It updates :py:attr:`time_variables` dictionary by appending the
        last value of each time variable (key of the dictionary) to
        corresponding list (value of the dictionary).
        """
        super().update_time_variables()
        if self.tangential_force_is_computable:
            self.time_variables['tangential force'].append(
                self.tangential_force
            )
