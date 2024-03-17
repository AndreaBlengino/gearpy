from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, InertiaMoment, Torque, UnitBase
from .mechanical_object_base import RotatingObject
from typing import Dict, List


class Flywheel(RotatingObject):
    r"""``gearpy.mechanical_objects.flywheel.Flywheel`` object.

    Attributes
    ----------
    :py:attr:`name` : str
        Name of the flywheel.
    :py:attr:`driven_by` : RotatingObject
        Rotating object that drives the flywheel, for example a motor or a gear.
    :py:attr:`drives` : RotatingObject
        Rotating object driven by the flywheel, it can be a gear.
    :py:attr:`master_gear_ratio` : float
        Gear ratio of the fixed joint between the flywheel and its driving rotating object.
    :py:attr:`master_gear_efficiency` : float or int
        Efficiency of the fixed joint between the flywheel and its driving rotating object.
    :py:attr:`angular_position` : AngularPosition
        Angular position of the flywheel.
    :py:attr:`angular_speed` : AngularSpeed
        Angular speed of the flywheel.
    :py:attr:`angular_acceleration` : AngularAcceleration
        Angular acceleration of the flywheel.
    :py:attr:`torque` : Torque
        Net torque applied on the flywheel.
    :py:attr:`driving_torque` : Torque
        Driving torque applied on the flywheel by its driving rotating object.
    :py:attr:`load_torque` : Torque
        Load torque applied on the flywheel by its driven rotating object.
    :py:attr:`inertia_moment` : InertiaMoment
        Moment of inertia of the flywheel.
    :py:attr:`time_variables` : dict
        Time variables of the flywheel.

    Methods
    -------
    :py:meth:`update_time_variables`
        Updates ``time_variables`` dictionary by appending the last value of each time variable to corresponding list.
    """

    def __init__(self, name: str, inertia_moment: InertiaMoment):
        super().__init__(name = name, inertia_moment = inertia_moment)

        self.__driven_by = None
        self.__drives = None
        self.__master_gear_ratio = None
        self.__master_gear_efficiency = 1

    @property
    def name(self) -> str:
        """Name of the flywheel. It must be a non-empty string. \n
        It must be a unique name, not shared by other elements in the powertrain elements. \n
        Once set at the flywheel instantiation, it cannot be changed afterward.

        Returns
        -------
        str
            Name of the flywheel.

        Raises
        ------
        TypeError
            If ``name`` is not a string.
        ValueError
            If ``name`` is an empty string.
        """
        return super().name

    @property
    def driven_by(self) -> RotatingObject:
        """Rotating object that drives the flywheel, for example a motor or a gear. It must be a ``RotatingObject``. \n
        To set this property use :py:func:`gearpy.utils.relations.add_fixed_joint`.

        Returns
        -------
        RotatingObject
            Master rotating object that drives the flywheel.

        Raises
        ------
        TypeError
            If ``driven_by`` is not an instance of ``RotatingObject``.

        See Also
        --------
        :py:func:`gearpy.utils.relations.add_fixed_joint`
        """
        return self.__driven_by

    @driven_by.setter
    def driven_by(self, driven_by: RotatingObject):
        if not isinstance(driven_by, RotatingObject):
            raise TypeError(f"Parameter 'driven_by' must be an instance of {RotatingObject.__name__!r}.")

        self.__driven_by = driven_by

    @property
    def drives(self) -> RotatingObject:
        """Rotating object driven by the flywheel, it can be a gear. It must be a ``RotatingObject``. \n
        To set this property use :py:func:`gearpy.utils.relations.add_fixed_joint`.

        Returns
        -------
        RotatingObject
            Rotating object driven by the flywheel.

        Raises
        ------
        TypeError
            If ``drives`` is not an instance of ``RotatingObject``.

        See Also
        --------
        :py:func:`gearpy.utils.relations.add_fixed_joint`
        """
        return self.__drives

    @drives.setter
    def drives(self, drives: RotatingObject):
        if not isinstance(drives, RotatingObject):
            raise TypeError(f"Parameter 'drives' must be an instance of {RotatingObject.__name__!r}.")

        self.__drives = drives

    @property
    def angular_position(self) -> AngularPosition:
        """Angular position of the flywheel. It must be an instance of ``AngularPosition``.

        Returns
        -------
        AngularPosition
            Angular position of the flywheel.

        Raises
        ------
        TypeError
            If ``angular_position`` is not an instance of ``AngularPosition``.

        See Also
        --------
        :py:class:`gearpy.units.units.AngularPosition`
        """
        return super().angular_position

    @angular_position.setter
    def angular_position(self, angular_position: AngularPosition):
        super(Flywheel, type(self)).angular_position.fset(self, angular_position)

    @property
    def angular_speed(self) -> AngularSpeed:
        """Angular speed of the flywheel. It must be an instance of ``AngularSpeed``.

        Returns
        -------
        AngularSpeed
            Angular speed of the flywheel.

        Raises
        ------
        TypeError
            If ``angular_speed`` is not an instance of ``AngularSpeed``.

        See Also
        --------
        :py:class:`gearpy.units.units.AngularSpeed`
        """
        return super().angular_speed

    @angular_speed.setter
    def angular_speed(self, angular_speed: AngularSpeed):
        super(Flywheel, type(self)).angular_speed.fset(self, angular_speed)

    @property
    def angular_acceleration(self) -> AngularAcceleration:
        """Angular acceleration of the flywheel. It must be an instance of ``AngularAcceleration``.

        Returns
        -------
        AngularAcceleration
            Angular acceleration of the flywheel.

        Raises
        ------
        TypeError
            If ``angular_acceleration`` is not an instance of ``AngularAcceleration``.

        See Also
        --------
        :py:class:`gearpy.units.units.AngularAcceleration`
        """
        return super().angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        super(Flywheel, type(self)).angular_acceleration.fset(self, angular_acceleration)

    @property
    def torque(self) -> Torque:
        """Net torque applied on the flywheel. It must be an instance of ``Torque``. \n
        It is computed as the difference between ``driving_torque`` and ``load_torque``.

        Returns
        -------
        Torque
            Net torque applied on the flywheel.

        Raises
        ------
        TypeError
            If ``torque`` is not an instance of ``Torque``.

        See Also
        --------
        :py:class:`gearpy.units.units.Torque`
        """
        return super().torque

    @torque.setter
    def torque(self, torque: Torque):
        super(Flywheel, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Torque:
        """Driving torque applied on the flywheel by its driving rotating object. It must be an instance of ``Torque``.

        Returns
        -------
        Torque
            Driving torque applied on the flywheel by its driving rotating object.

        Raises
        ------
        TypeError
            If ``driving_torque`` is not an instance of ``Torque``.

        See Also
        --------
        :py:class:`gearpy.units.units.Torque`
        """
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Torque):
        super(Flywheel, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Torque:
        """Load torque applied on the flywheel by its driven rotating object. It must be an instance of ``Torque``.

        Returns
        -------
        Torque
            Load torque applied on the flywheel by its driven rotating object.

        Raises
        ------
        TypeError
            If ``load_torque`` is not an instance of ``Torque``.

        See Also
        --------
        :py:class:`gearpy.units.units.Torque`
        """
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Torque):
        super(Flywheel, type(self)).load_torque.fset(self, load_torque)

    @property
    def master_gear_ratio(self) -> float:
        """Gear ratio of the fixed joint between the flywheel and its driving rotating object. It must be a positive a
        float. Since the relation between the flywheel and its neighbor elements in the powertrain elements is always a
        fixed joint, the gear ratio will be set to ``1`` by :py:func:`gearpy.utils.relations.add_fixed_joint`. \n
        To set this property use :py:func:`gearpy.utils.relations.add_fixed_joint`.

        Returns
        -------
        float
            Gear ratio of the fixed joint between the flywheel and its driving rotating object.

        Raises
        ------
        TypeError
            If ``master_gear_ratio`` is not a float.
        ValueError
            If ``master_gear_ratio`` is negative or null.

        See Also
        --------
        :py:func:`gearpy.utils.relations.add_fixed_joint`
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
    def master_gear_efficiency(self) -> float:
        """Efficiency of the fixed joint between the flywheel and its driving rotating object. Since the relation
        between the flywheel and its neighbor elements in the powertrain elements is always a fixed joint, the
        efficiency is always equal to ``1`` and cannot be overwritten.

        Returns
        -------
        float or int
            Efficiency of the fixed joint between the flywheel and its driving rotating object.

        See Also
        --------
        :py:func:`gearpy.utils.relations.add_fixed_joint`
        """
        return self.__master_gear_efficiency

    @property
    def inertia_moment(self) -> InertiaMoment:
        """Moment of inertia of the flywheel. It must be an instance of ``InertiaMoment``. \n
        Once set at the flywheel instantiation, it cannot be changed afterward.

        Returns
        -------
        InertiaMoment
            Moment of inertia of the flywheel.

        Raises
        ------
        TypeError
            If ``inertia_moment`` is not an instance of ``InertiaMoment``.

        See Also
        --------
        :py:class:`gearpy.units.units.InertiaMoment`
        """
        return super().inertia_moment

    @property
    def time_variables(self) -> Dict[str, List[UnitBase]]:
        """Time variables of the flywheel. Each time variable is stored as a dictionary key-value pair. The available
        time variables are:

        - ``angular_position``,
        - ``angular_speed``,
        - ``angular_acceleration``,
        - ``torque``,
        - ``driving_torque``,
        - ``load_torque``.

        Corresponding values of the dictionary are lists of the respective time variable values. \n
        At each time iteration, the ``Solver`` appends every time variables' values to the relative list in the
        dictionary.

        Returns
        -------
        dict
            Time variables of the flywheel.

        See Also
        --------
        :py:meth:`update_time_variables`
        """
        return super().time_variables

    def update_time_variables(self) -> None:
        """Updates ``time_variables`` dictionary by appending the last value of each time variable (key of the
        dictionary) to corresponding list (value of the dictionary).

        See Also
        --------
        :py:attr:`time_variables`
        """
        super().update_time_variables()
