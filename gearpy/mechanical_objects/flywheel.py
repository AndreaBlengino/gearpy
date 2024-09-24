from gearpy.units import (
    AngularPosition,
    AngularSpeed,
    AngularAcceleration,
    InertiaMoment,
    Torque,
    UnitBase
)
from .mechanical_object_base import RotatingObject


class Flywheel(RotatingObject):
    r""":py:class:`Flywheel <gearpy.mechanical_objects.flywheel.Flywheel>`
    object.

    Attributes
    ----------
    :py:attr:`name` : :py:class:`str`
        Name of the flywheel.
    :py:attr:`driven_by` : :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
        Rotating object that drives the flywheel, for example a
        :py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>` or a
        gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
    :py:attr:`drives` : :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
        Rotating object driven by the flywheel, it can be a gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
    :py:attr:`master_gear_ratio` : :py:class:`float`
        Gear ratio of the fixed joint between the flywheel and its driving
        rotating object.
    :py:attr:`master_gear_efficiency` : :py:class:`float` or :py:class:`int`
        Efficiency of the fixed joint between the flywheel and its driving
        rotating object.
    :py:attr:`angular_position` : :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`
        Angular position of the flywheel.
    :py:attr:`angular_speed` : :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`
        Angular speed of the flywheel.
    :py:attr:`angular_acceleration` : :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`
        Angular acceleration of the flywheel.
    :py:attr:`torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Net torque applied on the flywheel.
    :py:attr:`driving_torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Driving torque applied on the flywheel by its driving rotating object.
    :py:attr:`load_torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Load torque applied on the flywheel by its driven rotating object.
    :py:attr:`inertia_moment` : :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`
        Moment of inertia of the flywheel.
    :py:attr:`time_variables` : :py:class:`dict`
        Time variables of the flywheel.

    Methods
    -------
    :py:meth:`update_time_variables`
        It updates :py:attr:`time_variables` dictionary by appending the last
        value of each time variable to corresponding list.
    """

    def __init__(self, name: str, inertia_moment: InertiaMoment):
        super().__init__(name=name, inertia_moment=inertia_moment)

        self.__driven_by = None
        self.__drives = None
        self.__master_gear_ratio = None
        self.__master_gear_efficiency = 1

    @property
    def name(self) -> str:
        """Name of the flywheel. It must be a non-empty :py:class:`str`. \n
        It must be a unique name, not shared by other elements in the
        powertrain elements. \n
        Once set at the flywheel instantiation, it cannot be changed afterward.

        Returns
        -------
        :py:class:`str`
            Name of the flywheel.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`name` is not a :py:class:`str`.
           ``ValueError``
               If :py:attr:`name` is an empty :py:class:`str`.
        """
        return super().name

    @property
    def driven_by(self) -> RotatingObject:
        """Rotating object that drives the flywheel, for example a
        :py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>` or a
        gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
        It must be a
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`. \n
        To set this property use
        :py:func:`add_fixed_joint <gearpy.utils.relations.add_fixed_joint>`.

        Returns
        -------
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
            Master rotating object that drives the flywheel.

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
        """Rotating object driven by the flywheel, it can be a gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
        It must be a
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`. \n
        To set this property use :py:func:`add_fixed_joint <gearpy.utils.relations.add_fixed_joint>`.

        Returns
        -------
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
            Rotating object driven by the flywheel.

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
    def angular_position(self) -> AngularPosition:
        """Angular position of the flywheel. It must be an instance of
        :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`.

        Returns
        -------
        :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`
            Angular position of the flywheel.

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
            Flywheel,
            type(self)
        ).angular_position.fset(self, angular_position)

    @property
    def angular_speed(self) -> AngularSpeed:
        """Angular speed of the flywheel. It must be an instance of
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`.

        Returns
        -------
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`
            Angular speed of the flywheel.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`angular_speed` is not an instance of
               :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`.
        """
        return super().angular_speed

    @angular_speed.setter
    def angular_speed(self, angular_speed: AngularSpeed):
        super(Flywheel, type(self)).angular_speed.fset(self, angular_speed)

    @property
    def angular_acceleration(self) -> AngularAcceleration:
        """Angular acceleration of the flywheel. It must be an instance of
        :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`.

        Returns
        -------
        :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`
            Angular acceleration of the flywheel.

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
            Flywheel,
            type(self)
        ).angular_acceleration.fset(self, angular_acceleration)

    @property
    def torque(self) -> Torque:
        """Net torque applied on the flywheel. It must be an instance of
        :py:class:`Torque <gearpy.units.units.Torque>`. \n
        It is computed as the difference between :py:attr:`driving_torque` and
        :py:attr:`load_torque`.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Net torque applied on the flywheel.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.
        """
        return super().torque

    @torque.setter
    def torque(self, torque: Torque):
        super(Flywheel, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Torque:
        """Driving torque applied on the flywheel by its driving rotating
        object. It must be an instance of
        :py:class:`Torque <gearpy.units.units.Torque>`.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Driving torque applied on the flywheel by its driving rotating
            object.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`driving_torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.
        """
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Torque):
        super(Flywheel, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Torque:
        """Load torque applied on the flywheel by its driven rotating object.
        It must be an instance of
        :py:class:`Torque <gearpy.units.units.Torque>`.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Load torque applied on the flywheel by its driven rotating object.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`load_torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.
        """
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Torque):
        super(Flywheel, type(self)).load_torque.fset(self, load_torque)

    @property
    def master_gear_ratio(self) -> float:
        """Gear ratio of the fixed joint between the flywheel and its driving
        rotating object. It must be a positive a float. Since the relation
        between the flywheel and its neighbor elements in the powertrain
        elements is always a fixed joint, the gear ratio will be always set to
        ``1`` by
        :py:func:`add_fixed_joint <gearpy.utils.relations.add_fixed_joint>`. \n
        To set this property use
        :py:func:`add_fixed_joint <gearpy.utils.relations.add_fixed_joint>`.

        Returns
        -------
        :py:class:`float`
            Gear ratio of the fixed joint between the flywheel and its driving
            rotating object.

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
        """Efficiency of the fixed joint between the flywheel and its driving
        rotating object. Since the relation between the flywheel and its
        neighbor elements in the powertrain elements is always a fixed joint,
        the efficiency is always equal to ``1`` and cannot be overwritten. \n

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Efficiency of the fixed joint between the flywheel and its driving
            rotating object.
        """
        return self.__master_gear_efficiency

    @property
    def inertia_moment(self) -> InertiaMoment:
        """Moment of inertia of the flywheel. It must be an instance of
        :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`. \n
        Once set at the flywheel instantiation, it cannot be changed afterward.

        Returns
        -------
        :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`
            Moment of inertia of the flywheel.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`inertia_moment` is not an instance of
               :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`.
        """
        return super().inertia_moment

    @property
    def time_variables(self) -> dict[str, list[UnitBase]]:
        """Time variables of the flywheel. Each time variable is stored as a
        dictionary key-value pair. The available time variables are:

        - :py:attr:`angular_position`: ``'angular position'``,
        - :py:attr:`angular_speed`: ``'angular speed'``,
        - :py:attr:`angular_acceleration`: ``'angular acceleration'``,
        - :py:attr:`torque`: ``'torque'``,
        - :py:attr:`driving_torque`: ``'driving torque'``,
        - :py:attr:`load_torque`: ``'load torque'``.

        Corresponding values of the dictionary are lists of the respective time
        variable values. \n
        At each time iteration, the :py:class:`Solver <gearpy.solver.Solver>`
        appends every time variables' values to the relative list in the
        dictionary.

        Returns
        -------
        :py:class:`dict`
            Time variables of the flywheel.

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
