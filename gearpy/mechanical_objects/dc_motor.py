from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, Current, InertiaMoment, Torque, UnitBase
from .mechanical_object_base import RotatingObject, MotorBase
from typing import Dict, List, Union, Optional


class DCMotor(MotorBase):
    r"""``gearpy.mechanical_objects.dc_motor.DCMotor`` object.

    Attributes
    ----------
    :py:attr:`name` : str
        Name of the DC motor.
    :py:attr:`drives` : RotatingObject
        Rotating object driven by DC motor, it can be a flywheel or a gear.
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
    :py:attr:`no_load_electric_current` : Current
        No load electric current absorbed by the DC motor.
    :py:attr:`maximum_electric_current` : Current
        Maximum electric current absorbed by the DC motor.
    :py:attr:`electric_current_is_computable` : bool
        Whether is possible to compute the electric current absorbed by the DC motor.
    :py:attr:`electric_current` : Current
        Electric current absorbed by the DC motor.
    :py:attr:`pwm` : float or int
        Pulse Width Modulation duty cycle of the supply voltage of the DC motor.
    :py:attr:`time_variables` : dict
        Time variables of the DC motor.

    Methods
    -------
    :py:meth:`compute_torque`
        Computes the driving torque developed by the DC motor.
    :py:meth:`compute_electric_current`
        Computes the electric current absorbed by the DC motor.
    :py:meth:`update_time_variables`
        Updates ``time_variables`` dictionary by appending the last value of each time variable to corresponding list.
    """

    def __init__(self,
                 name: str,
                 inertia_moment: InertiaMoment,
                 no_load_speed: AngularSpeed,
                 maximum_torque: Torque,
                 no_load_electric_current: Optional[Current] = None,
                 maximum_electric_current: Optional[Current] = None):
        super().__init__(name = name, inertia_moment = inertia_moment)

        if not isinstance(no_load_speed, AngularSpeed):
            raise TypeError(f"Parameter 'no_load_speed' must be an instance of {AngularSpeed.__name__!r}.")

        if not isinstance(maximum_torque, Torque):
            raise TypeError(f"Parameter 'maximum_torque' must be an instance of {Torque.__name__!r}.")

        if no_load_speed.value <= 0:
            raise ValueError("Parameter 'no_load_speed' must be positive.")

        if maximum_torque.value <= 0:
            raise ValueError("Parameter 'maximum_torque' must be positive.")

        if no_load_electric_current is not None:
            if not isinstance(no_load_electric_current, Current):
                raise TypeError(f"Parameter 'no_load_electric_current' must be an instance of {Current.__name__!r}.")

            if no_load_electric_current.value < 0:
                raise ValueError("Parameter 'no_load_electric_current' must be positive or null.")

        if maximum_electric_current is not None:
            if not isinstance(maximum_electric_current, Current):
                raise TypeError(f"Parameter 'maximum_electric_current' must be an instance of {Current.__name__!r}.")

            if maximum_electric_current.value <= 0:
                raise ValueError("Parameter 'maximum_electric_current' must be positive.")

        if no_load_electric_current is not None and maximum_electric_current is not None:
            if no_load_electric_current >= maximum_electric_current:
                raise ValueError("Parameter 'no_load_electric_current' cannot be higher than "
                                 "'maximum_electric_current'.")

        self.__no_load_speed = no_load_speed
        self.__maximum_torque = maximum_torque
        self.__no_load_electric_current = no_load_electric_current
        self.__maximum_electric_current = maximum_electric_current
        self.__pwm = 1

        if self.electric_current_is_computable:
            self.__electric_current = None
            self.time_variables['electric current'] = []

    @property
    def name(self) -> str:
        """Name of the DC motor. It must be a non-empty string. \n
        It must be a unique name, not shared by other elements in the powertrain elements. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

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
        """Rotating object driven by DC motor, it can be a flywheel or a gear. It must be a ``RotatingObject``. \n
        To set this property use :py:func:`gearpy.utils.relations.add_fixed_joint`.

        Returns
        -------
        RotatingObject
            Rotating object driven by the DC motor.

        Raises
        ------
        TypeError
            If ``drives`` is not an instance of ``RotatingObject``.

        See Also
        --------
        :py:func:`gearpy.utils.relations.add_fixed_joint`
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
        :py:class:`gearpy.units.units.AngularPosition`
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
        :py:class:`gearpy.units.units.AngularSpeed`
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
        :py:class:`gearpy.units.units.AngularAcceleration`
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
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        AngularSpeed
            No load angular speed of the DC motor.

        Raises
        ------
        TypeError
            If ``no_load_speed`` is not an instance of ``AngularSpeed``.
        ValueError
            If ``no_load_speed`` is negative or null.

        Se Also
        -------
        :py:class:`gearpy.units.units.AngularSpeed`
        """
        return self.__no_load_speed

    @property
    def maximum_torque(self) -> Torque:
        """Maximum torque developed by the DC motor. It must be an instance of ``Torque``. Its value must be
        positive. \n
        It is the maximum torque the DC motor can develop when its rotor is kept still by the load. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        Torque
            Maximum torque developed by the DC motor.

        Raises
        ------
        TypeError
            If ``maximum_torque`` is not an instance of ``Torque``.
        ValueError
            If ``maximum_torque`` is negative or null.

        Se Also
        -------
        :py:class:`gearpy.units.units.Torque`
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
        :py:class:`gearpy.units.units.Torque`
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
        :py:class:`gearpy.units.units.Torque`
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
        :py:class:`gearpy.units.units.Torque`
        """
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Torque):
        super(DCMotor, type(self)).load_torque.fset(self, load_torque)

    @property
    def inertia_moment(self) -> InertiaMoment:
        """Moment of inertia of the DC motor's rotor. It must be an instance of ``InertiaMoment``. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

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
        :py:class:`gearpy.units.units.InertiaMoment`
        """
        return super().inertia_moment

    def compute_torque(self):
        r"""Computes the driving torque developed by the DC motor. \n
        The driving torque depends on the two constants ``no_load_speed`` and ``maximum_torque`` and the two variables
        ``angular_speed`` and ``pwm`` of the DCMotor.
        The computed torque has the same unit of ``maximum_torque``.

        Notes
        -----
        The computation is based on the following relationship:

        .. math::
            T \left( \dot{\theta} , T_{max}^D , \dot{\theta}_0^D \right) =
            T_{max}^D \left( 1 - \frac{\dot{\theta}}{\dot{\theta}_0^D} \right)

        where:

        - :math:`T` is the DC motor developed driving torque,
        - :math:`\dot{\theta}` is the actual DC motor angular speed,
        - :math:`T_{max}^D` is the DC motor maximum torque developed by the DC motor keeping into account ``pwm``,
        - :math:`\dot{\theta}_0^D` is the DC motor no load angular speed keeping into account ``pwm``.

        The maximum torque can be computed as:

        .. math::
            T_{max}^D \left( D \right) = T_{max} \frac{D \, i_{max} - i_0}{i_{max} - i_0}

        and the no load angular speed can be computed as:

        .. math::
            \dot{\theta}_0^D \left( D \right) = D \, \dot{\theta}_0

        where:

        - :math:`D` is the DC motor supply voltage PWM duty cycle (``pwm``),
        - :math:`T_{max}` is the DC motor maximum torque (``maximum_torque``),
        - :math:`i_{max}` is the DC motor maximum electric current (``maximum_electric_current``),
        - :math:`i_0` is the DC motor no load electric current (``no_load_electric_current``),
        - :math:`\dot{\theta}_0` is the DC motor no load angular speed (``no_load_speed``).

        If the ``pwm`` is lower than a critical threshold, then the motor cannot develop any torque, so the
        ``driving_torque`` will be null. The critical ``pwm`` value can be computed as:

        .. math::
            D_{lim} = \frac{i_0}{i_{max}}

        See Also
        --------
        :py:attr:`driving_torque`
        :py:attr:`pwm`
        """
        if not self.electric_current_is_computable:
            self.driving_torque = Torque(value = (1 - self.angular_speed/self.no_load_speed)*self.maximum_torque.value,
                                         unit = self.maximum_torque.unit)
            return

        pwm_min = self.no_load_electric_current/self.maximum_electric_current \
                  if self.electric_current_is_computable else 0
        if abs(self.pwm) <= pwm_min:
            self.driving_torque = Torque(0, unit = self.maximum_torque.unit)
            return
        elif self.pwm > pwm_min:
            maximum_torque = \
                self.maximum_torque*((self.pwm*self.maximum_electric_current - self.no_load_electric_current)/
                                     (self.maximum_electric_current - self.no_load_electric_current))
            no_load_speed = self.pwm*self.no_load_speed
        else:
            maximum_torque = \
                self.maximum_torque*((self.pwm*self.maximum_electric_current + self.no_load_electric_current)/
                                     (self.maximum_electric_current - self.no_load_electric_current))
            no_load_speed = self.pwm*self.no_load_speed

        self.driving_torque = Torque(value = (1 - self.angular_speed/no_load_speed)*maximum_torque.value,
                                     unit = self.maximum_torque.unit)

    @property
    def no_load_electric_current(self) -> Optional[Current]:
        """No load electric current absorbed by the DC motor. It must be an instance of ``Current``. Its value must be
        positive or null and lower than ``maximum_electric_current``. \n
        It is the electric current absorbed by the DC motor when no load is applied to its rotor. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        Current
            No load electric current of the DC motor.

        Raises
        ------
        TypeError
            If ``no_load_electric_current`` is not an instance of ``Current``.
        ValueError
            - If ``no_load_electric_current`` is negative,
            - if ``no_load_electric_current`` is higher than or equal to ``maximum_electric_current``.

        Se Also
        -------
        :py:class:`gearpy.units.units.Current`
        """
        return self.__no_load_electric_current

    @property
    def maximum_electric_current(self) -> Optional[Current]:
        """Maximum electric current absorbed by the DC motor. It must be an instance of ``Current``. Its value must be
        positive and greater than ``no_load_electric_current``. \n
        It is the maximum electric current the DC motor can absorb when its rotor is kept still by the load. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        Current
            Maximum electric current absorbed by the DC motor.

        Raises
        ------
        TypeError
            If ``maximum_electric_current`` is not an instance of ``Current``.
        ValueError
            - If ``maximum_electric_current`` is negative or null,
            - if ``maximum_electric_current`` is lower than or equal to ``no_load_electric_current``.

        Se Also
        -------
        :py:class:`gearpy.units.units.Current`
        """
        return self.__maximum_electric_current

    def compute_electric_current(self):
        r"""Computes the electric current absorbed by the DC motor. The absorbed electric current depends on the two
        constants ``no_load_electric_current`` and ``maximum_electric_current`` and the two variables ``driving_torque``
        and ``pwm`` of the DC motor.
        The computed electric current has the same unit of ``maximum_electric_current``.

        Notes
        -----
        The computation is based on the following relationship:

        .. math::
            i \left( T \right) = \left( i_{max}^D - i_0 \right) \frac{T}{T_{max}^D} + i_0

        where:

        - :math:`i` is the electric current absorbed by the DC motor,
        - :math:`T` is the DC motor developed driving torque,
        - :math:`i_{max}^D` is the maximum electric current absorbed by the DC motor keeping into account ``pwm``,
        - :math:`i_0` is the no load electric current absorbed by the DC motor (``no_load_electric_current``),
        - :math:`T_{max}^D` is the DC motor maximum torque developed by the DC motor keeping into account ``pwm``.

        The maximum torque can be computed as:

        .. math::
            T_{max}^D \left( D \right) = T_{max} \frac{D \, i_{max} - i_0}{i_{max} - i_0}

        and the maximum electric current can be computed as:

        .. math::
            i_{max}^D \left( D \right) = D \, i_{max}

        where:

        - :math:`D` is the DC motor supply voltage PWM duty cycle (``pwm``),
        - :math:`T_{max}` is the DC motor maximum torque (``maximum_torque``),
        - :math:`i_{max}` is the DC motor maximum electric current (``maximum_electric_current``),
        - :math:`i_0` is the DC motor no load electric current (``no_load_electric_current``).

        If the ``pwm`` is lower than a critical threshold, then the motor cannot develop any torque, so the
        ``electrical_current`` will depend only on ``pwm`` value. The critical ``pwm`` value can be computed as:

        .. math::
            D_{lim} = \frac{i_0}{i_{max}}

        and the relative electric current can be computed as:

        .. math::
            i_{lim} \left( D \right) = D \, i_{max}

        See Also
        --------
        :py:attr:`no_load_electric_current`
        :py:attr:`maximum_electric_current`
        :py:attr:`electric_current`
        :py:attr:`pwm`
        """
        maximum_electric_current = self.pwm*self.maximum_electric_current
        pwm_min = self.no_load_electric_current/self.maximum_electric_current
        if abs(self.pwm) <= pwm_min:
            if pwm_min == 0:
                self.electric_current = Current(value = 0, unit = self.maximum_electric_current.unit)
            else:
                self.electric_current = self.pwm/pwm_min*\
                                          self.no_load_electric_current.to(self.maximum_electric_current.unit)
            return
        elif self.pwm > pwm_min:
            no_load_electric_current = self.no_load_electric_current
            maximum_torque = \
                self.maximum_torque*((maximum_electric_current - self.no_load_electric_current)/
                                     (self.maximum_electric_current - self.no_load_electric_current))
        else:
            no_load_electric_current = -self.no_load_electric_current
            maximum_torque = \
                self.maximum_torque*((maximum_electric_current + self.no_load_electric_current)/
                                     (self.maximum_electric_current - self.no_load_electric_current))

        self.electric_current = Current(value = ((maximum_electric_current - no_load_electric_current)*
                                                   (self.driving_torque/maximum_torque) +
                                                   no_load_electric_current).value,
                                          unit = self.maximum_electric_current.unit)

    @property
    def electric_current_is_computable(self) -> bool:
        """Whether is possible to compute the electric current absorbed by the DC motor. The electric current
        computation depends on the value of ``no_load_electric_current`` and ``maximum_electric_current``, so if
        these optional parameters have been set at DC motor instantiation, then it is possible to compute the absorbed
        electric current and this property is ``True``, otherwise is ``False``.

        Returns
        -------
        bool
            Whether is possible to compute the electric current absorbed by the DC motor.

        See Also
        --------
        :py:attr:`no_load_electric_current`
        :py:attr:`maximum_electric_current`
        :py:meth:`compute_electric_current`
        """
        return (self.__no_load_electric_current is not None) and (self.__maximum_electric_current is not None)

    @property
    def electric_current(self) -> Optional[Current]:
        """Electric current absorbed by the DC motor. It must be an instance of ``Current``.

        Returns
        -------
        Current
            Electric current absorbed by the DC motor.

        Raises
        ------
        TypeError
            If ``electric_current`` is not an instance of ``Current``.

        See Also
        --------
        :py:class:`gearpy.units.units.Current`
        """
        return self.__electric_current

    @electric_current.setter
    def electric_current(self, electric_current: Current):
        if not isinstance(electric_current, Current):
            raise TypeError(f"Parameter 'electric_current' must be an instance of {Current.__name__!r}.")

        self.__electric_current = electric_current

    @property
    def time_variables(self) -> Dict[str, List[UnitBase]]:
        """Time variables of the DC motor. Each time variable is stored as a dictionary key-value pair. The available
        time variables are:

        - ``angular position``,
        - ``angular speed``,
        - ``angular acceleration``,
        - ``torque``,
        - ``driving torque``,
        - ``load torque``,
        - ``electric current``,
        - ``pwm``.

        ``electric current`` is listed among time variables only if it is computable indeed, depending on which motor
        parameters was set at DC motor instantiation. \n
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
        dictionary) to corresponding list (value of the dictionary).

        See Also
        --------
        :py:attr:`time_variables`
        """
        super().update_time_variables()
        if self.electric_current_is_computable:
            self.time_variables['electric current'].append(self.electric_current)
        if 'pwm' not in self.time_variables.keys():
            self.time_variables['pwm'] = [self.pwm]
        else:
            self.time_variables['pwm'].append(self.pwm)

    @property
    def pwm(self) -> Union[float, int]:
        """Pulse Width Modulation duty cycle of the supply voltage of the DC motor. \n
        It must be a float or an integer within ``-1`` and ``1``. \n
        In general the duty cycle can be between ``0`` and ``1``, but ``pwm`` can be between ``-1`` and ``1``, in order
        to take into account the voltage sign with respect to the direction of rotation:

        - if ``pwm`` is positive, then the supply voltage pushes the motor to rotate in the `positive` direction,
        - if ``pwm`` is negative, then the supply voltage pushes the motor to rotate in the `negative` direction,
        - if ``pwm`` is null, then the supply voltage is null to and the motor does not develop any driving torque.

        The ``pwm`` value has an impact on the ``driving_torque`` developed and the ``electric_current`` absorbed by
        the DC motor.

        Returns
        -------
        float or int
            Pulse Width Modulation duty cycle of the supply voltage of the DC motor.

        Raises
        ------
        TypeError
            If ``pwm`` is not a float or an integer.
        ValueError
            If ``pwm`` is not within ``-1`` and ``1``.

        See Also
        --------
        :py:meth:`compute_torque`
        :py:meth:`compute_electric_current`
        """
        return self.__pwm

    @pwm.setter
    def pwm(self, pwm: Union[float, int]):
        if not isinstance(pwm, float) and not isinstance(pwm, int):
            raise TypeError("Parameter 'pwm' must be a float or an integer.")

        if (pwm > 1) or (pwm < -1):
            raise ValueError("Pulse Width Modulation (PWM) must be within -1 and 1.")

        self.__pwm = pwm
