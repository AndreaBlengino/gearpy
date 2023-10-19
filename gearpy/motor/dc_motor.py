from gearpy.mechanical_object import RotatingObject
from gearpy.motor import MotorBase
from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, InertiaMoment, Torque


class DCMotor(MotorBase):
    r"""gearpy.motor.dc_motor.DCMotor object.

    Attributes
    ----------
    :py:attr:`name` : str
        Name of the DC motor.
    :py:attr:`drives` : RotatingObject
        Rotating object driven by DC motor, it can be another gear.
    :py:attr:`angular_position` : AngularPosition
        Angular position of the DC motor.
    :py:attr:`angular_speed` : AngularSpeed
        Angular speed of the DC motor.
    :py:attr:`angular_acceleration` : AngularAcceleration
        Angular acceleration of the DC motor.
    :py:attr:`no_load_speed` : AngularSpeed
        No load angular speed of the DC motor.
    :py:attr:`maximum_torque` : Torque
        Maximum torque developed by the DC motor.
    :py:attr:`torque` : Torque
        Net torque applied on the DC motor.
    :py:attr:`driving_torque` : Torque
        Driving torque developed by the DC motor.
    :py:attr:`load_torque` : Torque
        Load torque applied on the DC motor by its driven gear.
    :py:attr:`inertia_moment` : InertiaMoment
        Moment of inertia of the DC motor.
    :py:attr:`time_variables` : dict
        Time variables of the DC motor.

    Methods
    -------
    :py:meth:`compute_torque`
        Computes the driving torque developed by the DC motor.
    :py:meth:`update_time_variables`
        Updates ``time_variables`` dictionary by appending the last value of each time variable to corresponding list.
    """

    def __init__(self, name: str, inertia_moment: InertiaMoment, no_load_speed: AngularSpeed, maximum_torque: Torque):
        super().__init__(name = name, inertia_moment = inertia_moment)

        if not isinstance(no_load_speed, AngularSpeed):
            raise TypeError(f"Parameter 'no_load_speed' must be an instance of {AngularSpeed.__name__!r}")

        if not isinstance(maximum_torque, Torque):
            raise TypeError(f"Parameter 'maximum_torque.rst' must be an instance of {Torque.__name__!r}.")

        if no_load_speed.value <= 0:
            raise ValueError("Parameter 'no_load_speed' must be positive.")

        if maximum_torque.value <= 0:
            raise ValueError("Parameter 'maximum_torque.rst' must be positive.")

        self.__no_load_speed = no_load_speed
        self.__maximum_torque = maximum_torque

    @property
    def name(self) -> str:
        """Name of the DC motor. It must be a non-empty string. \n
        Once set at the DC motor instantiation, it cannot be further changed.

        Returns
        -------
        str
            Name of the DC motor.

        Raises
        ------
        TypeError
            If ``name`` is not a string.
        ValueError
            If ``name`` is an empty string.
        """
        return super().name

    @property
    def drives(self) -> RotatingObject:
        """Rotating object driven by DC motor, it can be another gear. It must be a ``RotatingObject``.

        Returns
        -------
        RotatingObject
            Master rotating object driven by the DC motor.

        Raises
        ------
        TypeError
            If ``drives`` is not an instance of ``RotatingObject``.
        """
        return super().drives

    @drives.setter
    def drives(self, drives: RotatingObject):
        super(DCMotor, type(self)).drives.fset(self, drives)

    @property
    def angular_position(self) -> AngularPosition:
        """Angular position of the DC motor. It must be an instance of ``AngularPosition``.

        Returns
        -------
        AngularPosition
            Angular position of the DC motor.

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
        super(DCMotor, type(self)).angular_position.fset(self, angular_position)

    @property
    def angular_speed(self) -> AngularSpeed:
        """Angular speed of the DC motor. It must be an instance of ``AngularSpeed``.

        Returns
        -------
        AngularSpeed
            Angular speed of the DC motor.

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
        super(DCMotor, type(self)).angular_speed.fset(self, angular_speed)

    @property
    def angular_acceleration(self) -> AngularAcceleration:
        """Angular acceleration of the DC motor. It must be an instance of ``AngularAcceleration``.

        Returns
        -------
        AngularAcceleration
            Angular acceleration of the DC motor.

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
        super(DCMotor, type(self)).angular_acceleration.fset(self, angular_acceleration)

    @property
    def no_load_speed(self) -> AngularSpeed:
        """No load angular speed of the DC motor. It must be an instance of ``AngularSpeed``. Its value must be
        positive. \n
        It is the angular speed at which the DC motor rotates when no load is applied to its rotor. \n
        Once set at the DC motor instantiation, it cannot be further changed.

        Returns
        -------
        AngularSpeed
            No load angular speed of the DC motor.

        Raises
        ------
        TypeError
            If ``no_load_speed`` is not an instance of ``AngularSpeed``.
        ValueError
            If ``no_load_speed`` is not positive.

        Se Also
        -------
        :py:class:`gearpy.units.concrete_units.AngularSpeed`
        """
        return self.__no_load_speed

    @property
    def maximum_torque(self) -> Torque:
        """Maximum torque developed by the DC motor. It must be an instance of ``Torque``. Its value must be positive. \n
        It is the maximum torque the DC motor can develop when its rotor is kept still by the load. \n
        Once set at the DC motor instantiation, it cannot be further changed.

        Returns
        -------
        Torque
            Maximum torque developed by the DC motor.

        Raises
        ------
        TypeError
            If ``maximum_torque`` is not an instance of ``Torque``.
        ValueError
            If ``maximum_torque`` is not positive.

        Se Also
        -------
        :py:class:`gearpy.units.concrete_units.Torque`
        """
        return self.__maximum_torque

    @property
    def torque(self) -> Torque:
        """Net torque applied on the DC motor. It must be an instance of ``Torque``. \n
        It is computed as the difference between ``driving_torque`` and ``load_torque``.

        Returns
        -------
        Torque
            Net torque applied on the DC motor.

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
        super(DCMotor, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Torque:
        """Driving torque developed by the DC motor. It must be an instance of ``Torque``.

        Returns
        -------
        Torque
            Driving torque developed by the DC motor.

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
        super(DCMotor, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Torque:
        """Load torque applied on the DC motor by its driven gear. It must be an instance of ``Torque``.

        Returns
        -------
        Torque
            Load torque applied on the DC motor by its driven gear.

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
        super(DCMotor, type(self)).load_torque.fset(self, load_torque)

    @property
    def inertia_moment(self) -> InertiaMoment:
        """Moment of inertia of the DC motor's rotor. It must be an instance of ``InertiaMoment``. \n
        Once set at the DC motor instantiation, it cannot be further changed.

        Returns
        -------
        InertiaMoment
            Moment of inertia of the DC motor's rotor.

        Raises
        ------
        TypeError
            If ``inertia_moment`` is not an instance of ``InertiaMoment``.

        See Also
        --------
        :py:class:`gearpy.units.concrete_units.InertiaMoment`
        """
        return super().inertia_moment

    def compute_torque(self) -> Torque:
        r"""Computes the driving torque developed by the DC motor. The driving torque depends on ``no_load_speed`` and
        ``maximum_torque.rst`` of the DC motor and its instantaneous ``angular_speed``.
        The returned computed torque has the same unit of ``maximum_torque.rst``.

        Returns
        -------
        Torque
            The driving torque developed by the DC motor.

        Notes
        -----
        The computation is based on the following relationship:

        .. math::
            T \left( \dot{\theta} \right) = T_{max} \left( 1 - \frac{\dot{\theta}}{\dot{\theta}_0} \right)

        where:

            - :math:`T` is the DC motor developed driving torque,
            - :math:`\dot{\theta}` is the actual DC motor angular speed,
            - :math:`T_{max}` is the DC motor maximum torque (``maximum_torque.rst``),
            - :math:`\dot{\theta}_0` is the DC motor no load angular speed (``no_load_speed``).
        """
        return Torque(value = (1 - self.angular_speed.to('rad/s').value/self.__no_load_speed.to('rad/s').value)*
                              self.__maximum_torque.value,
                      unit = self.__maximum_torque.unit)

    @property
    def time_variables(self) -> dict:
        """Time variables of the DC motor. Each time variable is stored as a dictionary key-value pair. The available
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
            Time variables of the DC motor.

        See Also
        --------
        :py:meth:`update_time_variables`
        """
        return super().time_variables

    def update_time_variables(self) -> None:
        """Updates ``time_variables`` dictionary by appending the last value of each time variable (key of the
        dictionary) to corresponding list (value of the dictionary). \n
        Time variables are ``angular_position``, ``angular_speed``, ``angular_acceleration``, ``torque``,
        ``driving_torque`` and ``load_torque`` of the DC motor.

        See Also
        --------
        :py:attr:`time_variables`
        """
        super().update_time_variables()
