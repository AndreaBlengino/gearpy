from gearpy.mechanical_objects import DCMotor
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from gearpy.units import AngularPosition, Current
import numpy as np
from gearpy.motor_control.rules.rules_base import RuleBase
from typing import Union


class StartLimitCurrent(RuleBase):
    """gearpy.motor_control.rules.start_limit_current.StartLimitCurrent object. \n
    It can be used to make a gradual start of the powertrain's motion and limit the ``motor`` absorbed electric
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
    :py:attr:`gearpy.mechanical_objects.dc_motor.DCMotor.pwm`
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
        :py:class:`gearpy.mechanical_objects.dc_motor.DCMotor`
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
