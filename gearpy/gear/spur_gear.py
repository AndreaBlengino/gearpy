from gearpy.gear import GearBase
from gearpy.mechanical_object import RotatingObject
from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, InertiaMoment, Torque
from typing import Callable, Union


class SpurGear(GearBase):
    r"""gearpy.gear.spur_gear.SpurGear object.

    Attributes
    ----------
    :py:attr:`name` : str
        Name of the spur gear.
    :py:attr:`n_teeth` : int
        Number of gear teeth.
    :py:attr:`driven_by` : RotatingObject
        Rotating object that drives the gear, for example a motor or another gear.
    :py:attr:`drives` : RotatingObject
        Rotating object driven by the gear, it can be another gear.
    :py:attr:`master_gear_ratio` : float
        Gear ratio of the mating between the gear and its driving gear.
    :py:attr:`master_gear_efficiency` : float or int
        Efficiency of the gear mating between the gear and its driving gear.
    :py:attr:`angular_position` : AngularPosition
        Angular position of the gear.
    :py:attr:`angular_speed` : AngularSpeed
        Angular speed of the gear.
    :py:attr:`angular_acceleration` : AngularAcceleration
        Angular acceleration of the gear.
    :py:attr:`torque` : Torque
        Net torque applied on the gear.
    :py:attr:`driving_torque` : Torque
        Driving torque applied on the gear by its driving gear.
    :py:attr:`load_torque` : Torque
        Load torque applied on the gear by its driven gear or an external load.
    :py:attr:`inertia_moment` : InertiaMoment
        Moment of inertia of the gear.
    :py:attr:`time_variables` : dict
        Time variables of the gear.

    Methods
    -------
    :py:meth:`external_torque`
        Custom function to compute the external torque applied on the gear.
    :py:meth:`update_time_variables`
        Updates ``time_variables`` dictionary by appending the last value of each time variable to corresponding list.
    """

    def __init__(self, name: str, n_teeth: int, inertia_moment: InertiaMoment):
        super().__init__(name = name, n_teeth = n_teeth, inertia_moment = inertia_moment)

    @property
    def name(self) -> str:
        """Name of the spur gear. It must be a non-empty string. \n
        Once set at the spur gear instantiation, it cannot be further changed.

        Returns
        -------
        str
            Name of the spur gear.

        Raises
        ------
        TypeError
            If ``name`` is not a string.
        ValueError
            If ``name`` is an empty string.
        """
        return super().name

    @property
    def n_teeth(self) -> int:
        """Number of gear teeth. It must be a positive integer. \n
        Once set at the spur gear instantiation, it cannot be further changed.

        Returns
        -------
        int
            Number of gear teeth.

        Raises
        ------
        TypeError
            If ``n_teeth`` is not an integer.
        ValueError
            If ``n_teeth`` is not positive.
        """
        return super().n_teeth

    @property
    def driven_by(self) -> RotatingObject:
        """Rotating object that drives the gear, for example a motor or another gear. It must be a ``RotatingObject``.

        Returns
        -------
        RotatingObject
            Master rotating object that drives the gear.

        Raises
        ------
        TypeError
            If ``driven_by`` is not an instance of ``RotatingObject``.
        """
        return super().driven_by

    @driven_by.setter
    def driven_by(self, driven_by: RotatingObject):
        super(SpurGear, type(self)).driven_by.fset(self, driven_by)

    @property
    def drives(self) -> RotatingObject:
        """Rotating object driven by the gear, it can be another gear. It must be a ``RotatingObject``.

        Returns
        -------
        RotatingObject
            Master rotating object driven by the gear.

        Raises
        ------
        TypeError
            If ``drives`` is not an instance of ``RotatingObject``.
        """
        return super().drives

    @drives.setter
    def drives(self, drives: RotatingObject):
        super(SpurGear, type(self)).drives.fset(self, drives)

    @property
    def master_gear_ratio(self) -> float:
        """Gear ratio of the mating between the gear and its driving gear. It must be a positive a float.
        It is defined as the ratio between the gear number of teeth ``n_teeth`` and the same parameter of the master
        (driving) gear. \n
        To set this property use :py:func:`gearpy.utils.relations.add_gear_mating` or
        :py:func:`gearpy.utils.relations.add_fixed_joint`.

        Returns
        -------
        float
            Gear ratio of the mating between the gear and its driving gear.

        Raises
        ------
        TypeError
            If ``master_gear_ratio`` is not a float.
        ValueError
            If ``master_gear_ratio`` is not positive.
        """
        return super().master_gear_ratio

    @master_gear_ratio.setter
    def master_gear_ratio(self, master_gear_ratio: float):
        super(SpurGear, type(self)).master_gear_ratio.fset(self, master_gear_ratio)

    @property
    def master_gear_efficiency(self) -> Union[float, int]:
        """Efficiency of the gear mating between the gear and its driving gear. It must be a float or an integer within
        ``0`` and ``1``. \n
        To set this property use :py:func:`gearpy.utils.relations.add_gear_mating` or
        :py:func:`gearpy.utils.relations.add_fixed_joint`.

        Returns
        -------
        float or int
            Efficiency of the gear mating between the gear and its driving gear.

        Raises
        ------
        TypeError
            If ``master_gear_efficiency`` is not a float or an integer.
        ValueError
            If ``master_gear_efficiency`` is not within ``0`` and ``1``.
        """
        return super().master_gear_efficiency

    @master_gear_efficiency.setter
    def master_gear_efficiency(self, master_gear_efficiency: Union[float, int]):
        super(SpurGear, type(self)).master_gear_efficiency.fset(self, master_gear_efficiency)

    @property
    def angular_position(self) -> AngularPosition:
        """Angular position of the gear. It must be an instance of ``AngularPosition``.

        Returns
        -------
        AngularPosition
            Angular position of the gear.

        Raises
        ------
        TypeError
            If ``angular_position`` is not an instance of ``AngularPosition``.

        See Also
        --------
        :py:class:`gearpy.units.concrete_units.AngularPosition`
        """
        return super().angular_position

    @angular_position.setter
    def angular_position(self, angular_position: AngularPosition):
        super(SpurGear, type(self)).angular_position.fset(self, angular_position)

    @property
    def angular_speed(self) -> AngularSpeed:
        """Angular speed of the gear. It must be an instance of ``AngularSpeed``.

        Returns
        -------
        AngularSpeed
            Angular speed of the gear.

        Raises
        ------
        TypeError
            If ``angular_speed`` is not an instance of ``AngularSpeed``.

        See Also
        --------
        :py:class:`gearpy.units.concrete_units.AngularSpeed`
        """
        return super().angular_speed

    @angular_speed.setter
    def angular_speed(self, angular_speed: AngularSpeed):
        super(SpurGear, type(self)).angular_speed.fset(self, angular_speed)

    @property
    def angular_acceleration(self) -> AngularAcceleration:
        """Angular acceleration of the gear. It must be an instance of ``AngularAcceleration``.

        Returns
        -------
        AngularAcceleration
            Angular acceleration of the gear.

        Raises
        ------
        TypeError
            If ``angular_acceleration`` is not an instance of ``AngularAcceleration``.

        See Also
        --------
        :py:class:`gearpy.units.concrete_units.AngularAcceleration`
        """
        return super().angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        super(SpurGear, type(self)).angular_acceleration.fset(self, angular_acceleration)

    @property
    def torque(self) -> Torque:
        """Net torque applied on the gear. It must be an instance of ``Torque``. \n
        It is computed as the difference between ``driving_torque`` and ``load_torque``.

        Returns
        -------
        Torque
            Net torque applied on the gear.

        Raises
        ------
        TypeError
            If ``torque`` is not an instance of ``Torque``.

        See Also
        --------
        :py:class:`gearpy.units.concrete_units.Torque`
        """
        return super().torque

    @torque.setter
    def torque(self, torque: Torque):

        super(SpurGear, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Torque:
        """Driving torque applied on the gear by its driving gear. It must be an instance of ``Torque``.

        Returns
        -------
        Torque
            Driving torque applied on the gear by its driving gear.

        Raises
        ------
        TypeError
            If ``driving_torque`` is not an instance of ``Torque``.

        See Also
        --------
        :py:class:`gearpy.units.concrete_units.Torque`
        """
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Torque):
        super(SpurGear, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Torque:
        """Load torque applied on the gear by its driven gear or an external load. It must be an instance of ``Torque``.

        Returns
        -------
        Torque
            Load torque applied on the gear by its driven gear or an external load.

        Raises
        ------
        TypeError
            If ``load_torque`` is not an instance of ``Torque``.

        See Also
        --------
        :py:class:`gearpy.units.concrete_units.Torque`
        """
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Torque):
        super(SpurGear, type(self)).load_torque.fset(self, load_torque)

    @property
    def inertia_moment(self) -> InertiaMoment:
        """Moment of inertia of the gear. It must be an instance of ``InertiaMoment``. \n
        Once set at the spur gear instantiation, it cannot be further changed.

        Returns
        -------
        InertiaMoment
            Moment of inertia of the gear.

        Raises
        ------
        TypeError
            If ``inertia_moment`` is not an instance of ``InertiaMoment``.

        See Also
        --------
        :py:class:`gearpy.units.concrete_units.InertiaMoment`
        """
        return super().inertia_moment

    @property
    def external_torque(self) -> Callable:
        """Custom function to compute the external torque applied on the gear. It must be a function with parameters
        ``angular_position``, ``angular_speed`` and ``time``. The function must return an instance of ``Torque``.

        Returns
        -------
        Callable
            The function to compute the external torque applied on the gear.

        Raises
        ------
        TypeError
            If ``external_torque`` is not callable.

        Examples
        --------
        Constant torque, not dependent on ``angular_position``, ``angular_speed`` or ``time``.

        >>> from gearpy.gear import SpurGear
        >>> from gearpy.units import InertiaMoment, Torque
        >>> gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
        >>> gear.external_torque = lambda angular_position, angular_speed, time: Torque(5, 'Nm')

        Torque dependent on ``angular_position`` and ``time``. \n
        In this case the gear gets a periodic load, dependent on time, and an extra load dependent on its angular
        position. The dependence by angular position may be used to model cases where cams are involved.

        >>> import numpy as np
        >>> from gearpy.units import AngularPosition, AngularSpeed, Time
        >>> def custom_external_torque(angular_position: AngularPosition,
        ...                            angular_speed: AngularSpeed,
        ...                            time: Time):
        ...     return Torque(value = np.sin(angular_position.to('rad').value) +
        ...                           np.cos(time.to('sec').value),
        ...                   unit = 'Nm')
        >>> gear.external_torque = custom_external_torque

        Torque dependent on ``angular_position``, ``angular_speed`` and ``time``. \n
        With respect ot the previous case, the gear gets an extra load dependent on its angular speed. The dependence by
        angular speed may be used to model cases where air friction is not negligible.

        >>> def complex_external_torque(angular_position: AngularPosition,
        ...                             angular_speed: AngularSpeed,
        ...                             time: Time):
        ...     return Torque(value = np.sin(angular_position.to('rad').value) +
        ...                           0.001*(angular_speed.to('rad/s').value)**2 +
        ...                           np.cos(time.to('sec').value),
        ...                   unit = 'Nm')
        >>> gear.external_torque = complex_external_torque
        """
        return super().external_torque

    @external_torque.setter
    def external_torque(self, external_torque: Callable):
        super(SpurGear, type(self)).external_torque.fset(self, external_torque)

    @property
    def time_variables(self) -> dict:
        """Time variables of the gear. Each time variable is stored as a dictionary key-value pair. The available time
        variables are:

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
            Time variables of the gear.

        See Also
        --------
        :py:meth:`update_time_variables`
        """
        return super().time_variables

    def update_time_variables(self) -> None:
        """Updates ``time_variables`` dictionary by appending the last value of each time variable (key of the
        dictionary) to corresponding list (value of the dictionary). \n
        Time variables are ``angular_position``, ``angular_speed``, ``angular_acceleration``, ``torque``,
        ``driving_torque`` and ``load_torque`` of the gear.

        See Also
        --------
        :py:attr:`time_variables`
        """
        super().update_time_variables()
