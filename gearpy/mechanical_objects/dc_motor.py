from gearpy.units import (
    AngularPosition,
    AngularSpeed,
    AngularAcceleration,
    Current,
    InertiaMoment,
    Torque,
    UnitBase
)
from .mechanical_object_base import RotatingObject, MotorBase
from typing import Optional


class DCMotor(MotorBase):
    r""":py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>`
    object.

    Attributes
    ----------
    :py:attr:`name` : :py:class:`str`
        Name of the DC motor.
    :py:attr:`drives` : :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
        Rotating object driven by DC motor, it can be a
        :py:class:`Flywheel <gearpy.mechanical_objects.flywheel.Flywheel>` or a
        gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
    :py:attr:`angular_position` : :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`
        Angular position of the DC motor.
    :py:attr:`angular_speed` : :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`
        Angular speed of the DC motor.
    :py:attr:`angular_acceleration` : :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`
        Angular acceleration of the DC motor.
    :py:attr:`no_load_speed` : :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`
        No load angular speed of the DC motor.
    :py:attr:`maximum_torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Maximum torque developed by the DC motor.
    :py:attr:`torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Net torque applied on the DC motor.
    :py:attr:`driving_torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Driving torque developed by the DC motor.
    :py:attr:`load_torque` : :py:class:`Torque <gearpy.units.units.Torque>`
        Load torque applied on the DC motor by its driven gear.
    :py:attr:`inertia_moment` : :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`
        Moment of inertia of the DC motor.
    :py:attr:`no_load_electric_current` : :py:class:`Current <gearpy.units.units.Current>`
        No load electric current absorbed by the DC motor.
    :py:attr:`maximum_electric_current` : :py:class:`Current <gearpy.units.units.Current>`
        Maximum electric current absorbed by the DC motor.
    :py:attr:`electric_current_is_computable` : :py:class:`bool`
        Whether is possible to compute the :py:attr:`electric_current`
        absorbed by the DC motor.
    :py:attr:`electric_current` : :py:class:`Current <gearpy.units.units.Current>`
        Electric current absorbed by the DC motor.
    :py:attr:`pwm` : :py:class:`float` or :py:class:`int`
        Pulse Width Modulation duty cycle of the supply voltage of the DC
        motor.
    :py:attr:`time_variables` : :py:class:`dict`
        Time variables of the DC motor.

    Methods
    -------
    :py:meth:`compute_torque`
        It computes the :py:attr:`driving_torque` developed by the DC motor.
    :py:meth:`compute_electric_current`
        It computes the :py:attr:`electric_current` absorbed by the DC motor.
    :py:meth:`update_time_variables`
        It updates :py:attr:`time_variables` dictionary by appending the last
        value of each time variable to corresponding list.
    """

    def __init__(
        self,
        name: str,
        inertia_moment: InertiaMoment,
        no_load_speed: AngularSpeed,
        maximum_torque: Torque,
        no_load_electric_current: Optional[Current] = None,
        maximum_electric_current: Optional[Current] = None
    ):
        super().__init__(name=name, inertia_moment=inertia_moment)

        if not isinstance(no_load_speed, AngularSpeed):
            raise TypeError(
                f"Parameter 'no_load_speed' must be an instance of "
                f"{AngularSpeed.__name__!r}."
            )

        if not isinstance(maximum_torque, Torque):
            raise TypeError(
                f"Parameter 'maximum_torque' must be an instance of "
                f"{Torque.__name__!r}."
            )

        if no_load_speed.value <= 0:
            raise ValueError("Parameter 'no_load_speed' must be positive.")

        if maximum_torque.value <= 0:
            raise ValueError("Parameter 'maximum_torque' must be positive.")

        if no_load_electric_current is not None:
            if not isinstance(no_load_electric_current, Current):
                raise TypeError(
                    f"Parameter 'no_load_electric_current' must be an "
                    f"instance of {Current.__name__!r}."
                )

            if no_load_electric_current.value < 0:
                raise ValueError(
                    "Parameter 'no_load_electric_current' must be positive or "
                    "null."
                )

        if maximum_electric_current is not None:
            if not isinstance(maximum_electric_current, Current):
                raise TypeError(
                    f"Parameter 'maximum_electric_current' must be an "
                    f"instance of {Current.__name__!r}."
                )

            if maximum_electric_current.value <= 0:
                raise ValueError(
                    "Parameter 'maximum_electric_current' must be positive."
                )

        if no_load_electric_current is not None and \
                maximum_electric_current is not None:
            if no_load_electric_current >= maximum_electric_current:
                raise ValueError(
                    "Parameter 'no_load_electric_current' cannot be higher "
                    "than 'maximum_electric_current'."
                )

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
        """Name of the DC motor. It must be a non-empty :py:class:`str`. \n
        It must be a unique name, not shared by other elements in the
        powertrain elements. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        :py:class:`str`
            Name of the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`name` is not a :py:class:`str`.
           ``ValueError``
               If :py:attr:`name` is an empty :py:class:`str`.
        """
        return super().name

    @property
    def drives(self) -> RotatingObject:
        """Rotating object driven by DC motor, it can be a
        :py:class:`Flywheel <gearpy.mechanical_objects.flywheel.Flywheel>` or
        a gear
        (:py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>`,
        :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>`,
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>`,
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`).
        It must be an instance of
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`. \n
        To set this property use
        :py:func:`add_fixed_joint <gearpy.utils.relations.add_fixed_joint>`.

        Returns
        -------
        :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
            Rotating object driven by the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`drives` is not an instance of
               :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`.
        """
        return super().drives

    @drives.setter
    def drives(self, drives: RotatingObject):
        super(DCMotor, type(self)).drives.fset(self, drives)

    @property
    def angular_position(self) -> AngularPosition:
        """Angular position of the DC motor. It must be an instance of
        :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`.

        Returns
        -------
        :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`
            Angular position of the DC motor.

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
            DCMotor,
            type(self)
        ).angular_position.fset(self, angular_position)

    @property
    def angular_speed(self) -> AngularSpeed:
        """Angular speed of the DC motor.
        It must be an instance of
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`.

        Returns
        -------
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`
            Angular speed of the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`angular_speed` is not an instance of
               :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`.
        """
        return super().angular_speed

    @angular_speed.setter
    def angular_speed(self, angular_speed: AngularSpeed):
        super(DCMotor, type(self)).angular_speed.fset(self, angular_speed)

    @property
    def angular_acceleration(self) -> AngularAcceleration:
        """Angular acceleration of the DC motor. It must be an instance of
        :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`.

        Returns
        -------
        :py:class:`AngularAcceleration <gearpy.units.units.AngularAcceleration>`
            Angular acceleration of the DC motor.

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
            DCMotor,
            type(self)
        ).angular_acceleration.fset(self, angular_acceleration)

    @property
    def no_load_speed(self) -> AngularSpeed:
        """No load angular speed of the DC motor. It must be an instance of
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`. Its value
        must be positive. \n
        It is the angular speed at which the DC motor rotates when no load is
        applied to its rotor. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`
            No load angular speed of the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`no_load_speed` is not an instance of
               :py:class:`AngularSpeed <gearpy.units.units.AngularSpeed>`.
           ``ValueError``
               If :py:attr:`no_load_speed` is negative or null.
        """
        return self.__no_load_speed

    @property
    def maximum_torque(self) -> Torque:
        """Maximum torque developed by the DC motor. It must be an instance of
        :py:class:`Torque <gearpy.units.units.Torque>`. Its value must be
        positive. \n
        It is the maximum torque the DC motor can develop when its rotor is
        kept still by the load. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Maximum torque developed by the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`maximum_torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.
           ``ValueError``
               If :py:attr:`maximum_torque` is negative or null.
        """
        return self.__maximum_torque

    @property
    def torque(self) -> Torque:
        """Net torque applied on the DC motor. It must be an instance of
        :py:class:`Torque <gearpy.units.units.Torque>`. \n
        It is computed as the difference between :py:attr:`driving_torque` and
        :py:attr:`load_torque`.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Net torque applied on the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.
        """
        return super().torque

    @torque.setter
    def torque(self, torque: Torque):
        super(DCMotor, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Torque:
        """Driving torque developed by the DC motor. It must be an instance of
        :py:class:`Torque <gearpy.units.units.Torque>`.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Driving torque developed by the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`driving_torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.

        .. admonition:: See Also
           :class: seealso

           :py:meth:`compute_torque`
        """
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Torque):
        super(DCMotor, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Torque:
        """Load torque applied on the DC motor by its driven gear. It must be
        an instance of :py:class:`Torque <gearpy.units.units.Torque>`.

        Returns
        -------
        :py:class:`Torque <gearpy.units.units.Torque>`
            Load torque applied on the DC motor by its driven gear.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`load_torque` is not an instance of
               :py:class:`Torque <gearpy.units.units.Torque>`.
        """
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Torque):
        super(DCMotor, type(self)).load_torque.fset(self, load_torque)

    @property
    def inertia_moment(self) -> InertiaMoment:
        """Moment of inertia of the DC motor's rotor. It must be an instance of
        :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`
            Moment of inertia of the DC motor's rotor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`inertia_moment` is not an instance of
               :py:class:`InertiaMoment <gearpy.units.units.InertiaMoment>`.
        """
        return super().inertia_moment

    def compute_torque(self) -> None:
        """It computes the :py:attr:`driving_torque` developed by the DC
        motor. \n
        The driving torque depends on the two constants
        :py:attr:`no_load_speed` and :py:attr:`maximum_torque` and the two
        variables :py:attr:`angular_speed` and :py:attr:`pwm` of the
        DCMotor. \n
        The computed torque has the same unit of :py:attr:`maximum_torque`.
        """\
        r"""
        .. admonition:: Notes
           :class: tip

           The computation is based on the following relationship:

           .. math::
               T \left( \dot{\theta} , T_{max}^D , \dot{\theta}_0^D \right) =
               T_{max}^D \left( 1 - \frac{\dot{\theta}}{\dot{\theta}_0^D}
               \right)

           where:

           - :math:`T` is the DC motor developed driving torque
             :py:attr:`driving_torque`,
           - :math:`\dot{\theta}` is the actual DC motor angular speed
             :py:attr:`angular_speed`,
           - :math:`T_{max}^D` is the DC motor maximum torque developed by the
             DC motor **keeping into account** :py:attr:`pwm`,
           - :math:`\dot{\theta}_0^D` is the DC motor no load angular speed
             **keeping into account** :py:attr:`pwm`.

           The maximum torque can be computed as:

           .. math::
               T_{max}^D \left( D \right) = T_{max}
               \frac{D \, i_{max} - i_0}{i_{max} - i_0}

           and the no load angular speed can be computed as:

           .. math::
               \dot{\theta}_0^D \left( D \right) = D \, \dot{\theta}_0

           where:

           - :math:`D` is the DC motor supply voltage PWM duty cycle
             (:py:attr:`pwm`),
           - :math:`T_{max}` is the DC motor :py:attr:`maximum_torque`,
           - :math:`i_{max}` is the DC motor
             :py:attr:`maximum_electric_current`,
           - :math:`i_0` is the DC motor :py:attr:`no_load_electric_current`,
           - :math:`\dot{\theta}_0` is the DC motor :py:attr:`no_load_speed`.

           If the :py:attr:`pwm` is lower than a critical threshold, then the
           motor cannot develop any torque, so the :py:attr:`driving_torque`
           will be null. The critical :py:attr:`pwm` value can be computed as:

           .. math::
               D_{lim} = \frac{i_0}{i_{max}}
        """
        if not self.electric_current_is_computable:
            self.driving_torque = Torque(
                value=(1 - self.angular_speed /
                       self.no_load_speed)*self.maximum_torque.value,
                unit=self.maximum_torque.unit
            )
            return

        pwm_min = self.no_load_electric_current/self.maximum_electric_current \
            if self.electric_current_is_computable else 0
        if abs(self.pwm) <= pwm_min:
            self.driving_torque = Torque(0, unit=self.maximum_torque.unit)
            return
        elif self.pwm > pwm_min:
            maximum_torque = \
                self.maximum_torque*(
                    (self.pwm*self.maximum_electric_current -
                        self.no_load_electric_current) /
                    (self.maximum_electric_current -
                        self.no_load_electric_current)
                )
            no_load_speed = self.pwm*self.no_load_speed
        else:
            maximum_torque = \
                self.maximum_torque*(
                    (self.pwm*self.maximum_electric_current +
                        self.no_load_electric_current) /
                    (self.maximum_electric_current -
                        self.no_load_electric_current)
                )
            no_load_speed = self.pwm*self.no_load_speed

        self.driving_torque = Torque(
            value=(1 - self.angular_speed/no_load_speed)*maximum_torque.value,
            unit=self.maximum_torque.unit
        )

    @property
    def no_load_electric_current(self) -> Optional[Current]:
        """No load electric current absorbed by the DC motor. It must be an
        instance of :py:class:`Current <gearpy.units.units.Current>`. Its value
        must be positive or null and lower than
        :py:attr:`maximum_electric_current`. \n
        It is the electric current absorbed by the DC motor when no load is
        applied to its rotor. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        :py:class:`Current <gearpy.units.units.Current>`
            No load electric current of the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`no_load_electric_current` is not an instance of
               :py:class:`Current <gearpy.units.units.Current>`.
           ``ValueError``
               - If :py:attr:`no_load_electric_current` is negative,
               - if :py:attr:`no_load_electric_current` is higher than or equal
                 to :py:attr:`maximum_electric_current`.
        """
        return self.__no_load_electric_current

    @property
    def maximum_electric_current(self) -> Optional[Current]:
        """Maximum electric current absorbed by the DC motor. It must be an
        instance of :py:class:`Current <gearpy.units.units.Current>`. Its value
        must be positive and greater than
        :py:attr:`no_load_electric_current`. \n
        It is the maximum electric current the DC motor can absorb when its
        rotor is kept still by the load. \n
        Once set at the DC motor instantiation, it cannot be changed afterward.

        Returns
        -------
        :py:class:`Current <gearpy.units.units.Current>`
            Maximum electric current absorbed by the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`maximum_electric_current` is not an instance of
               :py:class:`Current <gearpy.units.units.Current>`.
           ``ValueError``
               - If :py:attr:`maximum_electric_current` is negative or null,
               - if :py:attr:`maximum_electric_current` is lower than or equal
                 to :py:attr:`no_load_electric_current`.
        """
        return self.__maximum_electric_current

    def compute_electric_current(self) -> None:
        """It computes the :py:attr:`electric_current` absorbed by the DC
        motor. \n
        The absorbed electric current depends on the two constants
        :py:attr:`no_load_electric_current` and
        :py:attr:`maximum_electric_current` and the two variables
        :py:attr:`driving_torque` and :py:attr:`pwm` of the DC motor. \n
        The computed electric current has the same unit of
        :py:attr:`maximum_electric_current`.
        """ \
        r"""
        .. admonition:: Notes
           :class: tip

           The computation is based on the following relationship:

           .. math::
               i \left( T \right) = \left( i_{max}^D - i_0 \right)
               \frac{T}{T_{max}^D} + i_0

           where:

           - :math:`i` is the :py:attr:`electric_current` absorbed by the DC
             motor,
           - :math:`T` is the DC motor developed :py:attr:`driving_torque`,
           - :math:`i_{max}^D` is the maximum electric current absorbed by the
             DC motor **keeping into account** :py:attr:`pwm`,
           - :math:`i_0` is the :py:attr:`no_load_electric_current` absorbed by
             the DC motor,
           - :math:`T_{max}^D` is the DC motor maximum torque developed by the
             DC motor **keeping into account** :py:attr:`pwm`.

           The maximum torque can be computed as:

           .. math::
               T_{max}^D \left( D \right) = T_{max}
               \frac{D \, i_{max} - i_0}{i_{max} - i_0}

           and the maximum electric current can be computed as:

           .. math::
               i_{max}^D \left( D \right) = D \, i_{max}

           where:

           - :math:`D` is the DC motor supply voltage PWM duty cycle
             (:py:attr:`pwm`),
           - :math:`T_{max}` is the DC motor :py:attr:`maximum_torque`,
           - :math:`i_{max}` is the DC motor
             :py:attr:`maximum_electric_current`,
           - :math:`i_0` is the DC motor :py:attr:`no_load_electric_current`.

           If the :py:attr:`pwm` is lower than a critical threshold, then the
           motor cannot develop any torque, so the :py:attr:`electric_current`
           will depend only on :py:attr:`pwm` value. The critical
           :py:attr:`pwm` value can be computed as:

           .. math::
               D_{lim} = \frac{i_0}{i_{max}}

           and the relative electric current can be computed as:

           .. math::
               i_{lim} \left( D \right) = D \, i_{max}
        """
        maximum_electric_current = self.pwm*self.maximum_electric_current
        pwm_min = self.no_load_electric_current/self.maximum_electric_current
        if abs(self.pwm) <= pwm_min:
            if pwm_min == 0:
                self.electric_current = Current(
                    value=0,
                    unit=self.maximum_electric_current.unit
                )
            else:
                self.electric_current = \
                    self.pwm/pwm_min*self.no_load_electric_current.to(
                        self.maximum_electric_current.unit
                    )
            return
        elif self.pwm > pwm_min:
            no_load_electric_current = self.no_load_electric_current
            maximum_torque = \
                self.maximum_torque*(
                    (maximum_electric_current -
                        self.no_load_electric_current) /
                    (self.maximum_electric_current -
                        self.no_load_electric_current)
                )
        else:
            no_load_electric_current = -self.no_load_electric_current
            maximum_torque = \
                self.maximum_torque*(
                    (maximum_electric_current +
                        self.no_load_electric_current) /
                    (self.maximum_electric_current -
                        self.no_load_electric_current)
                )

        self.electric_current = Current(
            value=(
                (maximum_electric_current - no_load_electric_current) *
                (self.driving_torque/maximum_torque) + no_load_electric_current
            ).value,
            unit=self.maximum_electric_current.unit
        )

    @property
    def electric_current_is_computable(self) -> bool:
        """Whether is possible to compute the :py:attr:`electric_current`
        absorbed by the DC motor. \n
        The electric current computation depends on the value of
        :py:attr:`no_load_electric_current` and
        :py:attr:`maximum_electric_current`, so if these optional parameters
        have been set at DC motor instantiation, then it is possible to compute
        the absorbed electric current and this property is ``True``, otherwise
        is ``False``.

        Returns
        -------
        :py:class:`bool`
            Whether is possible to compute the electric current absorbed by the
            DC motor.

        .. admonition:: See Also
           :class: seealso

           :py:meth:`compute_electric_current`
        """
        return (self.__no_load_electric_current is not None) and \
            (self.__maximum_electric_current is not None)

    @property
    def electric_current(self) -> Optional[Current]:
        """Electric current absorbed by the DC motor. It must be an instance of
        :py:class:`Current <gearpy.units.units.Current>`.

        Returns
        -------
        :py:class:`Current <gearpy.units.units.Current>`
            Electric current absorbed by the DC motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`electric_current` is not an instance of
               :py:class:`Current <gearpy.units.units.Current>`.

        .. admonition:: See Also
           :class: seealso

           :py:meth:`compute_electric_current`
        """
        return self.__electric_current

    @electric_current.setter
    def electric_current(self, electric_current: Current):
        if not isinstance(electric_current, Current):
            raise TypeError(
                f"Parameter 'electric_current' must be an instance of "
                f"{Current.__name__!r}."
            )

        self.__electric_current = electric_current

    @property
    def time_variables(self) -> dict[str, list[UnitBase]]:
        """Time variables of the DC motor. Each time variable is stored as a
        dictionary key-value pair. The available time variables are:

        - :py:attr:`angular_position`: ``'angular position'``,
        - :py:attr:`angular_speed`: ``'angular speed'``,
        - :py:attr:`angular_acceleration`: ``'angular acceleration'``,
        - :py:attr:`torque`: ``'torque'``,
        - :py:attr:`driving_torque`: ``'driving torque'``,
        - :py:attr:`load_torque`: ``'load torque'``,
        - :py:attr:`electric_current`: ``'electric current'``,
        - :py:attr:`pwm`: ``'pwm'``.

        ``'electric current'`` is listed among time variables only if it is
        computable indeed, depending on which motor parameters was set at DC
        motor instantiation; see :py:attr:`electric_current_is_computable` for
        more details. \n
        Corresponding values of the dictionary are lists of the respective time
        variable values. \n
        At each time iteration, the :py:class:`Solver <gearpy.solver.Solver>`
        appends every time variables' values to the relative list in the
        dictionary.

        Returns
        -------
        :py:class:`dict`
            Time variables of the DC motor.

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
        if self.electric_current_is_computable:
            self.time_variables['electric current'].append(
                self.electric_current
            )
        if 'pwm' not in self.time_variables.keys():
            self.time_variables['pwm'] = [self.pwm]
        else:
            self.time_variables['pwm'].append(self.pwm)

    @property
    def pwm(self) -> float | int:
        """Pulse Width Modulation duty cycle of the supply voltage of the DC
        motor. \n
        It must be a :py:class:`float` or an :py:class:`int` within ``-1`` and
        ``1``. \n
        In general the duty cycle can be between ``0`` and ``1``, but
        :py:attr:`pwm` can be between ``-1`` and ``1``, in order to take into
        account the voltage sign with respect to the direction of rotation:

        - if :py:attr:`pwm` is positive, then the supply voltage pushes the
          motor to rotate in the `positive` direction,
        - if :py:attr:`pwm` is negative, then the supply voltage pushes the
          motor to rotate in the `negative` direction,
        - if :py:attr:`pwm` is null, then the supply voltage is null to and the
          motor does not develop any driving torque.

        The :py:attr:`pwm` value has an impact on the :py:attr:`driving_torque`
        developed and the :py:attr:`electric_current` absorbed by the DC motor.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Pulse Width Modulation duty cycle of the supply voltage of the DC
            motor.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`pwm` is not a :py:class:`float` or an
               :py:class:`int`.
           ``ValueError``
               If :py:attr:`pwm` is not within ``-1`` and ``1``.

        .. admonition:: See Also
           :class: seealso

           :py:meth:`compute_torque` \n
           :py:meth:`compute_electric_current`
        """
        return self.__pwm

    @pwm.setter
    def pwm(self, pwm: float | int):
        if not isinstance(pwm, float | int):
            raise TypeError("Parameter 'pwm' must be a float or an integer.")

        if (pwm > 1) or (pwm < -1):
            raise ValueError(
                "Pulse Width Modulation (PWM) must be within -1 and 1."
            )

        self.__pwm = pwm
