from gearpy.mechanical_object import SpurGear, MotorBase, RotatingObject, DCMotor
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from gearpy.transmission import Transmission
from gearpy.units import AngularPosition, Angle, Current
import numpy as np
from .rules_base import RuleBase
from typing import Union, Optional


class ReachAngularPosition(RuleBase):
    """gearpy.motor_control.rules.ReachAngularPosition object. \n
    It can be used to make the ``encoder``'s ``target`` reach a ``target_angular_position`` within a ``braking_angle``.

    Attributes
    ----------
    :py:attr:`encoder` : AbsoluteRotaryEncoder
        Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
        ``target_angular_position``.
    :py:attr:`transmission` : Transmission
        Transmission whose motor's ``pwm`` is controlled in order to reach a specific angular position.
    :py:attr:`target_angular_position` : AngularPosition
        Angular position to be reached by the ``encoder``'s target.
    :py:attr:`braking_angle` : Angle
        Angle within which the motor's ``pwm`` is controlled in order to brake and reach the
        ``target_angular_position``.

    Methods
    -------
    :py:meth:`apply`
        Computes the ``pwm`` to apply to the ``transmission``'s motor in order to reach a ``target_angular_position`` by
        the ``target`` rotating object of the ``encoder``, within a specific ``braking_angle``.

    Raises
    ------
    TypeError
        - If ``encoder`` is not an instance of ``AbsoluteRotaryEncoder``,
        - if ``transmission`` is not an instance of ``Transmission``,
        - if the first element in ``transmission`` is not an instance of ``MotorBase``,
        - if an element of ``transmission`` is not an instance of ``RotatingObject``,
        - if ``target_angular_position`` is not an instance of ``AngularPosition``,
        - if ``braking_angle`` is not an instance of ``Angle``.
    ValueError
        If ``transmission.chain`` is an empty tuple.

    See Also
    --------
    :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.pwm`
    """

    def __init__(self,
                 encoder: AbsoluteRotaryEncoder,
                 transmission: Transmission,
                 target_angular_position: AngularPosition,
                 braking_angle: Angle):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(f"Parameter 'encoder' must be an instance of {AbsoluteRotaryEncoder.__name__!r}.")

        if not isinstance(transmission, Transmission):
            raise TypeError(f"Parameter 'transmission' must be an instance of {Transmission.__name__!r}.")

        if not transmission.chain:
            raise ValueError("Parameter 'transmission.chain' cannot be an empty tuple.")

        if not isinstance(transmission.chain[0], MotorBase):
            raise TypeError(f"First element in 'transmission' must be an instance of {MotorBase.__name__!r}.")

        if not all([isinstance(item, RotatingObject) for item in transmission.chain]):
            raise TypeError(f"All elements of 'transmission' must be instances of {RotatingObject.__name__!r}.")

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(f"Parameter 'target_angular_position' must be an instance of {AngularPosition.__name__!r}.")

        if not isinstance(braking_angle, Angle):
            raise TypeError(f"Parameter 'braking_angle' must be an instance of {Angle.__name__!r}.")

        self.__encoder = encoder
        self.__transmission = transmission
        self.__target_angular_position = target_angular_position
        self.__braking_angle = braking_angle

    @property
    def encoder(self) -> AbsoluteRotaryEncoder:
        """Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
        ``target_angular_position``.

        Returns
        -------
        AbsoluteRotaryEncoder
            Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
            ``target_angular_position``.

        Notes
        -----
        This parameter serves as a remainder for the user about the need to use an encoder in the mechanism, otherwise
        this type of control cannot be applied.

        See Also
        --------
        :py:class:`gearpy.sensors.AbsoluteRotaryEncoder`
        """
        return self.__encoder

    @property
    def transmission(self) -> Transmission:
        """Transmission whose motor's ``pwm`` is controlled in order to reach a specific angular position.

        Returns
        -------
        Transmission
            Transmission whose motor's ``pwm`` is controlled in order to reach a specific angular position.

        See Also
        --------
        :py:class:`gearpy.transmission.Transmission`
        """
        return self.__transmission

    @property
    def target_angular_position(self) -> AngularPosition:
        """Angular position to be reached by the ``encoder``'s target. The rule is applied up until the ``encoder``'s
        target's ``angular_position`` equals the ``target_angular_position``.

        Returns
        -------
        AngularPosition
            Angular position to be reached by the ``encoder``'s target.

        See Also
        --------
        :py:class:`gearpy.units.units.AngularPosition`
        """
        return self.__target_angular_position

    @property
    def braking_angle(self) -> Angle:
        """Angle within which the motor's ``pwm`` is controlled in order to brake and reach the
        ``target_angular_position``. \n
        The rule is applied only if the difference between ``target_angular_position`` and the ``encoder``'s target
        ``angular_position`` is lower than or equal to the ``braking_angle``. \n
        The lower the ``braking_angle`` the higher the deceleration of the system, thus the higher the vibrations
        produced.

        Returns
        -------
        Angle
            Angle within which the motor's ``pwm`` is controlled in order to brake and reach the
            ``target_angular_position``.

        See Also
        --------
        :py:class:`gearpy.units.units.Angle`
        """
        return self.__braking_angle

    def apply(self) -> Union[None, float, int]:
        r"""Computes the ``pwm`` to apply to the ``transmission``'s DC motor in order to reach a
        ``target_angular_position`` by the ``target`` rotating object of the ``encoder``, within a specific
        ``braking_angle``.

        Returns
        -------
        float or int or None
            PWM value to apply to the motor in order to reach the target angular position.

        Notes
        -----
        It computes the ``transmission``'s *static error* according to the following formula:

        .. math::
            \theta_{err} \left( T_l \right) = \frac{T_l}{T_{max}} \, \frac{\theta_b}{\eta_t}

        where:

        - :math:`\theta_{err}` is the ``transmission`` static error,
        - :math:`T_l` is the load torque on the ``transmission`` DC motor,
        - :math:`T_{max}` is the maximum torque developed by the ``transmission`` DC motor,
        - :math:`\theta_b` is the ``braking_angle`` parameter,
        - :math:`\eta_t` is the ``transmission`` overall efficiency, computed as:

        .. math::
            \eta_t = \prod_{i = 1}^N \eta_i

        where:

        - :math:`\eta_i` is the mechanical mating efficiency of the mating between two gears,
        - :math:`N` is the total number of gear matings in the ``transmission``.

        Then it checks the applicability condition, defined as:

        .. math::
            \theta \ge \theta_s = \theta_t - \theta_b + \theta_{err}

        where:

        - :math:`\theta` is the ``encoder``'s ``target`` ``angular_position``,
        - :math:`\theta_s` is the braking starting angle,
        - :math:`\theta_t` is the ``target_angular_position`` parameter.

        If the applicability condition is not met, then it returns ``None``, otherwise it computes the ``pwm`` as:

        .. math::
            D \left( \theta \right) = 1 - \frac{\theta - \theta_s}{\theta_b}

        where :math:`D` is the supply voltage PWM duty cycle (``pwm``) to apply to the DC motor in order to reach the
        ``target_angular_position`` by the ``encoder``'s ``target`` rotating object.
        """
        angular_position = self.encoder.get_value()

        regime_angular_position_error = _compute_static_error(braking_angle = self.braking_angle,
                                                              transmission = self.transmission)
        braking_starting_angle = self.target_angular_position - self.braking_angle + regime_angular_position_error

        if angular_position >= braking_starting_angle:
            return 1 - (angular_position - braking_starting_angle)/self.braking_angle


class StartProportionalToAngularPosition(RuleBase):
    """gearpy.motor_control.rules.StartProportionalToAngularPosition object. \n
    It can be used to make a gradual start of the ``transmission``'s motion, in order to avoid a peak in the
    ``transmission``'s DC motor absorbed electric current. \n
    It computes a ``pwm`` to apply to the ``transmission``'s DC motor which increases linearly with the ``encoder``'s
    ``target`` rotating object's ``angular_position``. The computed ``pwm`` starts from a minimum value, based on
    ``transmission``'s elements properties and ``pwm_min_multiplier`` or solely on ``pwm_min`` parameter. The computed
    ``pwm`` increases up to ``1`` when the ``encoder``'s ``target``'s ``angular_position`` equals
    ``target_angular_position``.

    Attributes
    ----------
    :py:attr:`encoder` : AbsoluteRotaryEncoder
        Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
        ``target_angular_position``.
    :py:attr:`transmission` : Transmission
        Transmission whose motor's ``pwm`` is controlled proportionally to the ``encoder``'s target
        ``angular_position``.
    :py:attr:`target_angular_position` : AngularPosition
        Angular position to be reached by the ``encoder``'s target.
    :py:attr:`pwm_min_multiplier` : float or int
        Multiplication factor of motor's minimum ``pwm``.
    :py:attr:`pwm_min` : float or int, optional
        Minimum ``pwm`` to be used in case the ``transmission``'s motor minimum ``pwm`` is null.

    Methods
    -------
    :py:meth:`apply`
        Computes the ``pwm`` to apply to the ``transmission`` motor, proportional to the ``encoder``'s ``target``
        ``angular_position`` until it reaches the ``target_angular_position``.

    Raises
    ------
    TypeError
        - If ``encoder`` is not an instance of ``AbsoluteRotaryEncoder``,
        - if ``transmission`` is not an instance of ``Transmission``,
        - if the first element in ``transmission`` is not an instance of ``MotorBase``,
        - if an element of ``transmission`` is not an instance of ``RotatingObject``,
        - if ``target_angular_position`` is not an instance of ``AngularPosition``,
        - if ``pwm_min_multiplier`` is not a float or an integer,
        - if ``pwm_min`` is defined and it is not a float or an integer.
    ValueError
        - If ``transmission.chain`` is an empty tuple,
        - if the ``transmission`` motor cannot compute ``electric_current`` property,
        - if ``pwm_min_multiplier`` is less than or equal to ``1``,
        - if ``pwm_min`` is defined and it is negative or null.

    See Also
    --------
    :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.pwm`
    """

    def __init__(self,
                 encoder: AbsoluteRotaryEncoder,
                 transmission: Transmission,
                 target_angular_position: AngularPosition,
                 pwm_min_multiplier: Union[float, int],
                 pwm_min: Optional[float] = None):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(f"Parameter 'encoder' must be an instance of {AbsoluteRotaryEncoder.__name__!r}.")

        if not isinstance(transmission, Transmission):
            raise TypeError(f"Parameter 'transmission' must be an instance of {Transmission.__name__!r}.")

        if not transmission.chain:
            raise ValueError("Parameter 'transmission.chain' cannot be an empty tuple.")

        if not isinstance(transmission.chain[0], MotorBase):
            raise TypeError(f"First element in 'transmission' must be an instance of {MotorBase.__name__!r}.")

        if not transmission.chain[0].electric_current_is_computable:
            raise ValueError("The motor in 'transmission' cannot compute 'electric_current' property.")

        if not all([isinstance(item, RotatingObject) for item in transmission.chain]):
            raise TypeError(f"All elements of 'transmission' must be instances of {RotatingObject.__name__!r}.")

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(f"Parameter 'target_angular_position' must be an instance of {AngularPosition.__name__!r}.")

        if not isinstance(pwm_min_multiplier, float) and not isinstance(pwm_min_multiplier, int):
            raise TypeError(f"Parameter 'pwm_min_multiplier' must be a float or an integer.")

        if pwm_min_multiplier <= 1:
            raise ValueError(f"Parameter 'pwm_min_multiplier' must be greater than 1.")

        if pwm_min is not None:
            if not isinstance(pwm_min, float) and not isinstance(pwm_min, int):
                raise TypeError(f"Parameter 'pwm_min' must be a float or an integer.")

            if pwm_min <= 0:
                raise ValueError(f"Parameter 'pwm_min' must be positive.")

        self.__encoder = encoder
        self.__transmission = transmission
        self.__target_angular_position = target_angular_position
        self.__pwm_min_multiplier = pwm_min_multiplier
        self.__pwm_min = pwm_min

    @property
    def encoder(self) -> AbsoluteRotaryEncoder:
        """Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
        ``target_angular_position``.

        Returns
        -------
        AbsoluteRotaryEncoder
            Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
            ``target_angular_position``.

        Notes
        -----
        This parameter serves as a remainder for the user about the need to use an encoder in the mechanism, otherwise
        this type of control cannot be applied.

        See Also
        --------
        :py:class:`gearpy.sensors.AbsoluteRotaryEncoder`
        """
        return self.__encoder

    @property
    def transmission(self) -> Transmission:
        """Transmission whose motor's ``pwm`` is controlled proportionally to the ``encoder``'s target
        ``angular_position``.

        Returns
        -------
        Transmission
            Transmission whose motor's ``pwm`` is controlled proportionally to the ``encoder``'s target
            ``angular_position``.

        See Also
        --------
        :py:class:`gearpy.transmission.Transmission`
        """
        return self.__transmission

    @property
    def target_angular_position(self) -> AngularPosition:
        """Angular position to be reached by the ``encoder``'s target. The rule is applied up until the ``encoder``'s
        target's ``angular_position`` equals the ``target_angular_position``.

        Returns
        -------
        AngularPosition
            Angular position to be reached by the ``encoder``'s target.

        See Also
        --------
        :py:class:`gearpy.units.units.AngularPosition`
        """
        return self.__target_angular_position

    @property
    def pwm_min_multiplier(self) -> Union[float, int]:
        """Multiplication factor of motor's minimum ``pwm``. \n
        The ``transmission``'s motor has a minimum ``pwm`` which, as is, cannot be used to control the motor, since at
        this value the motor will remain still. So, in order to properly control the motor motion, it is required to
        apply a ``pwm`` greater than the minimum ``pwm``, therefore the motor minimum ``pwm`` is multiplied by
        ``pwm_min_multiplier`` to get a starting ``pwm`` to be applied to the motor.

        Returns
        -------
        float or int
            Multiplication factor of motor's minimum ``pwm``.

        See Also
        --------
        :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.pwm`
        """
        return self.__pwm_min_multiplier

    @property
    def pwm_min(self) -> Union[None, float, int]:
        """Minimum ``pwm`` to be used in case the ``transmission``'s motor minimum ``pwm`` is null. \n
        If the motor's minimum ``pwm`` is null, then it is useless to multiply this value by ``pwm_min_multiplier`` in
        order to get a starting ``pwm``; therefore, only in this case, ``pwm_min`` is directly used as starting ``pwm``.

        Returns
        -------
        None or float or int
            Minimum ``pwm`` to be used in case the ``transmission``'s motor minimum ``pwm`` is null.

        See Also
        --------
        :py:attr:`pwm_min_multiplier`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.pwm`
        """
        return self.__pwm_min

    def apply(self) -> Union[None, float, int]:
        r"""Computes the ``pwm`` to apply to the ``transmission`` motor, proportional to the ``encoder``'s ``target``
        ``angular_position`` until it reaches the ``target_angular_position``.

        Returns
        -------
        float or int or None
            PWM value to apply to the motor, proportional to the ``encoder``'s ``target`` ``angular_position``.

        Notes
        -----
        It computes a *candidate* minimum applicable ``pwm`` as:

        .. math::
            D_{min}^c \left( T_l \right) = \frac{1}{\eta_t} \, \frac{T_l}{T_{max}} \, \frac{i_{max} - i_0}{i_{max}} +
            \frac{i_0}{i_{max}}

        where:

        - :math:`D_{min}^c` is the *candidate* minimum applicable ``pwm``,
        - :math:`T_l` is the load torque on the ``transmission`` DC motor,
        - :math:`T_{max}` is the maximum torque developed by the ``transmission`` DC motor,
        - :math:`i_{max}` is the maximum electric current absorbed by the ``transmission`` DC motor,
        - :math:`i_0` is the no load electric current absorbed by the ``transmission`` DC motor,
        - :math:`\eta_t` is the ``transmission`` overall efficiency, computed as:

        .. math::
            \eta_t = \prod_{i = 1}^N \eta_i

        where:

        - :math:`\eta_i` is the mechanical mating efficiency of the mating between two gears,
        - :math:`N` is the total number of gear matings in the ``transmission``.

        If both the load torque on the ``transmission`` DC motor :math:`T_l` and the motor no load electric current
        :math:`i_0` are null, then also the computed *candidate* minimum applicable ``pwm`` :math:`D_{min}^c` is null.
        Only in this case, the compuded *candidate* minimum applicable ``pwm`` is discarded and it is taken into account
        the ``pwm_min`` parameter, which must have been set (don't used otherwise):

        .. math::
            D_{min} = D_{min}^p

        where:

        - :math:`D_{min}` is the minimum applicable ``pwm``,
        - :math:`D_{min}^p` is the ``pwm_min`` parameter.

        Otherwise, the *candidate* :math:`D_{min}` is multiplied by the ``pwm_min_multiplier`` parameter:

        .. math::
            D_{min} = D_{min}^c \, g

        where :math:`g` is the ``pwm_min_multiplier`` parameter.

        Then it checks the applicability condition, defined as:

        .. math::
            \theta \le \theta_t

        where:

        - :math:`\theta` is the ``encoder``'s ``target`` ``angular_position``,
        - :math:`\theta_t` is the ``target_angular_position``.

        If the applicability condition is not met, then it returns ``None``, otherwise it computes the ``pwm`` as:

        .. math::
            D \left( \theta \right) = \left( 1 - D_{min} \right) \frac{\theta}{\theta_t} + D_{min}
        """
        angular_position = self.encoder.get_value()

        computed_pwm_min = self.pwm_min_multiplier*_compute_pwm_min(transmission = self.transmission)
        if computed_pwm_min != 0:
            pwm_min = computed_pwm_min
        else:
            if self.pwm_min is None:
                raise ValueError("Missing 'pwm_min' parameter.")
            pwm_min = self.pwm_min

        if angular_position <= self.target_angular_position:
            return (1 - pwm_min)*angular_position/self.target_angular_position + pwm_min


class StartLimitCurrent(RuleBase):
    """gearpy.motor_control.rules.StartLimitCurrent object. \n
    It can be used to make a gradual start of the transmission's motion and limit the ``motor`` absorbed electric
    current to be lower than or equal to a ``limit_electric_current`` value. It computes a ``pwm`` to apply to the
    ``motor`` up until the ``encoder``'s ``target``'s ``angular_position`` equals ``target_angular_position``. \n
    For an optimal ``pwm`` management, it is suggested to set the ``motor`` as the ``tachometer``'s ``target``.

    Attributes
    ----------
    :py:attr:`encoder` : AbsoluteRotaryEncoder
        Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
        ``target_angular_position``.
    :py:attr:`tachometer` : Tachometer
        Sensor used to measure the ``angular_speed`` of a ``RotatingObject``.
    :py:attr:`motor` : DCMotor
        Motor that has to be controlled through ``pwm`` value.
    :py:attr:`limit_electric_current` : Current
        Maximum allowable electric current to be absorbed by the ``motor``.
    :py:attr:`target_angular_position` : AngularPosition
        Angular position to be reached by the ``encoder``'s target.

    Methods
    -------
    :py:meth:`apply`
        Computes the ``pwm`` to apply to the ``motor`` in order to limit its absorbed electric current to be lower
        or equal to ``limit_electric_current``, until the ``encoder``'s ``target`` rotating object's
        ``angular_position`` equals the ``target_angular_position``.

    Raises
    ------
    TypeError
        - If ``encoder`` is not an instance of ``AbsoluteRotaryEncoder``,
        - If ``tachometer`` is not an instance of ``Tachometer``,
        - If ``motor`` is not an instance of ``DCMotor``,
        - if ``target_angular_position`` is not an instance of ``AngularPosition``,
        - if ``limit_electric_current`` is not an instance of ``Current``.
    ValueError
        - If the ``motor`` cannot compute ``electric_current`` property,
        - if ``limit_electric_current`` is negative or null.

    See Also
    --------
    :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.pwm`
    """

    def __init__(self,
                 encoder: AbsoluteRotaryEncoder,
                 tachometer: Tachometer,
                 motor: DCMotor,
                 target_angular_position: AngularPosition,
                 limit_electric_current: Current):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(f"Parameter 'encoder' must be an instance of {AbsoluteRotaryEncoder.__name__!r}.")

        if not isinstance(tachometer, Tachometer):
            raise TypeError(f"Parameter 'tachometer' must be an instance of {Tachometer.__name__!r}.")

        if not isinstance(motor, DCMotor):
            raise TypeError(f"Parameter 'motor' must be an instance of {DCMotor.__name__!r}.")

        if not motor.electric_current_is_computable:
            raise ValueError("Parameter 'motor' cannot compute 'electric_current' property.")

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(f"Parameter 'target_angular_position' must be an instance of {AngularPosition.__name__!r}.")

        if not isinstance(limit_electric_current, Current):
            raise TypeError(f"Parameter 'limit_electric_current' must be an instance of {Current.__name__!r}.")

        if limit_electric_current.value <= 0:
            raise ValueError("Parameter 'limit_electric_current' must be positive.")

        self.__encoder = encoder
        self.__tachometer = tachometer
        self.__motor = motor
        self.__limit_electric_current = limit_electric_current
        self.__target_angular_position = target_angular_position

    @property
    def encoder(self) -> AbsoluteRotaryEncoder:
        """Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
        ``target_angular_position``.

        Returns
        -------
        AbsoluteRotaryEncoder
            Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
            ``target_angular_position``.

        Notes
        -----
        This parameter serves as a remainder for the user about the need to use an encoder in the mechanism, otherwise
        this type of control cannot be applied.

        See Also
        --------
        :py:class:`gearpy.sensors.AbsoluteRotaryEncoder`
        """
        return self.__encoder

    @property
    def tachometer(self) -> Tachometer:
        """Sensor used to measure the ``angular_speed`` of a ``RotatingObject``.

        Returns
        -------
        Tachometer
            Sensor used to measure the ``angular_speed`` of a ``RotatingObject``.

        Notes
        -----
        This parameter serves as a remainder for the user about the need to use a tachometer in the mechanism,
        otherwise this type of control cannot be applied.

        See Also
        --------
        :py:class:`gearpy.sensors.Tachometer`
        """
        return self.__tachometer

    @property
    def motor(self) -> DCMotor:
        """Motor that has to be controlled through ``pwm`` value.

        Returns
        -------
        DCMotor
           Motor that has to be controlled through ``pwm`` value.

        See Also
        --------
        :py:class:`gearpy.mechanical_object.mechanical_objects.DCMotor`
        """
        return self.__motor

    @property
    def limit_electric_current(self) -> Current:
        """Maximum allowable electric current to be absorbed by the ``motor``. While the rule is applied, the absorbed
        electric current is equal to or lower than this value.

        Returns
        -------
        Current
            Maximum allowable electric current to be absorbed by the ``DCMotor``.

        See Also
        --------
        :py:class:`gearpy.units.units.Current`
        """
        return self.__limit_electric_current

    @property
    def target_angular_position(self) -> AngularPosition:
        """Angular position to be reached by the ``encoder``'s target. The rule is applied up until the ``encoder``'s
        target's ``angular_position`` equals the ``target_angular_position``.

        Returns
        -------
        AngularPosition
            Angular position to be reached by the ``encoder``'s target.

        See Also
        --------
        :py:class:`gearpy.units.units.AngularPosition`
        """
        return self.__target_angular_position

    def apply(self) -> Union[None, float, int]:
        r"""Computes the ``pwm`` to apply to the ``motor`` in order to limit its absorbed electric current to be lower
        or equal to ``limit_electric_current``, until the ``encoder``'s ``target`` rotating object's
        ``angular_position`` equals the ``target_angular_position``.

        Returns
        -------
        float or int or None
            PWM value to apply to the ``motor`` in order to limit its absorbed electric current to be lower or equal to
            ``limit_electric_current``

        Notes
        -----
        It checks the applicability condition, defined as:

        .. math::
            \theta \le \theta_t

        where:

        - :math:`\theta` is the ``encoder``'s ``target`` ``angular_position``,
        - :math:`\theta_t` is the ``target_angular_position``.

        If the applicability condition is not met, then it returns ``None``, otherwise it computes the ``pwm`` as:

        .. math::
            D \left( \dot{\theta} \right) = \frac{1}{2} \, \left( \frac{\dot{\theta}}{\dot{\theta}_0} +
            \frac{i_{lim}}{i_{max}} + \sqrt{ \left( \frac{\dot{\theta}}{\dot{\theta}_0} \right)^2 +
            \left( \frac{i_{lim}}{i_{max}} \right)^2 +
            2 \frac{\dot{\theta}}{\dot{\theta}_0} \frac{i_{lim} - 2 i_0}{i_{max}} } \right)

        where:

        - :math:`\dot{\theta}` is the ``tachometer``'s ``target``'s angular speed,
        - :math:`\dot{\theta}_0` is the ``motor`` no load angular speed (``no_load_speed``),
        - :math:`i_{lim}` is the ``limit_electric_current`` parameter,
        - :math:`i_{max}` is the ``motor`` maximum electric current (``maximum_electric_current``),
        - :math:`i_0` is the ``motor`` no load electric current (``no_load_electric_current``).
        """
        angular_position = self.encoder.get_value()
        angular_speed = self.tachometer.get_value()
        no_load_speed = self.motor.no_load_speed
        maximum_electric_current = self.motor.maximum_electric_current
        no_load_electric_current = self.motor.no_load_electric_current
        speed_ratio = angular_speed/no_load_speed
        electric_ratio = self.limit_electric_current/maximum_electric_current

        if angular_position <= self.target_angular_position:
            return 1/2*(speed_ratio + electric_ratio +
                        np.sqrt(speed_ratio**2 + electric_ratio**2 +
                                2*speed_ratio*((self.limit_electric_current - 2*no_load_electric_current)/
                                                maximum_electric_current)))


def _compute_static_error(braking_angle: Angle, transmission: Transmission) -> Union[Angle, AngularPosition]:
    maximum_torque = transmission.chain[0].maximum_torque
    load_torque = transmission.chain[0].load_torque

    transmission_efficiency = 1
    for element in transmission.chain:
        if isinstance(element, SpurGear):
            transmission_efficiency *= element.master_gear_efficiency

    if load_torque is not None:
        static_error = ((load_torque/maximum_torque)/transmission_efficiency)*braking_angle
    else:
        static_error = AngularPosition(0, 'rad')

    return static_error


def _compute_pwm_min(transmission: Transmission) -> Union[float, int]:
    maximum_torque = transmission.chain[0].maximum_torque
    if transmission.chain[0].time_variables['load torque']:
        load_torque = transmission.chain[0].time_variables['load torque'][0]
    else:
        load_torque = transmission.chain[0].load_torque
    no_load_electric_current = transmission.chain[0].no_load_electric_current
    maximum_electric_current = transmission.chain[0].maximum_electric_current

    transmission_efficiency = 1
    for element in transmission.chain:
        if isinstance(element, SpurGear):
            transmission_efficiency *= element.master_gear_efficiency

    return 1/transmission_efficiency*(load_torque/maximum_torque)*\
           ((maximum_electric_current - no_load_electric_current)/maximum_electric_current) + \
           no_load_electric_current/maximum_electric_current
