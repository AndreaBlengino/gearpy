from gearpy.mechanical_objects import DCMotor
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from gearpy.units import AngularPosition, Current
import numpy as np
from gearpy.motor_control.rules.rules_base import RuleBase


class StartLimitCurrent(RuleBase):
    """:py:class:`StartLimitCurrent <gearpy.motor_control.rules.start_limit_current.StartLimitCurrent>`
    object. \n
    It can be used to make a gradual start of the powertrain's motion and limit
    the ``motor`` absorbed electric current to be lower than or equal to a
    ``limit_electric_current`` value. It computes a ``pwm`` to apply to the
    ``motor`` up until the ``encoder``'s ``target``'s ``angular_position``
    equals ``target_angular_position``. \n
    For an optimal ``pwm`` management, it is suggested to set the ``motor`` as
    the ``tachometer``'s ``target``.

    Methods
    -------
    :py:meth:`apply`
        It computes the ``pwm`` to apply to the ``motor`` in order to limit its
        absorbed electric current to be lower or equal to
        ``limit_electric_current``, until the ``encoder``'s ``target`` rotating
        object's ``angular_position`` equals the ``target_angular_position``.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``encoder`` is not an instance of
             :py:class:`AbsoluteRotaryEncoder <gearpy.sensors.absolute_rotary_encoder.AbsoluteRotaryEncoder>`,
           - If ``tachometer`` is not an instance of
             :py:class:`Tachometer <gearpy.sensors.tachometer.Tachometer>`,
           - If ``motor`` is not an instance of
             :py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>`,
           - if ``target_angular_position`` is not an instance of
             :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`,
           - if ``limit_electric_current`` is not an instance of
             :py:class:`Current <gearpy.units.units.Current>`.
       ``ValueError``
           - If the ``motor`` cannot compute ``electric_current`` property
             (:py:attr:`DCMotor.electric_current <gearpy.mechanical_objects.dc_motor.DCMotor.electric_current>`),
           - if ``limit_electric_current`` is negative or null.

    .. admonition:: See Also
       :class: seealso

       :py:attr:`DCMotor.pwm <gearpy.mechanical_objects.dc_motor.DCMotor.pwm>`
    """

    def __init__(
        self,
        encoder: AbsoluteRotaryEncoder,
        tachometer: Tachometer,
        motor: DCMotor,
        target_angular_position: AngularPosition,
        limit_electric_current: Current
    ):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(
                f"Parameter 'encoder' must be an instance of "
                f"{AbsoluteRotaryEncoder.__name__!r}."
            )

        if not isinstance(tachometer, Tachometer):
            raise TypeError(
                f"Parameter 'tachometer' must be an instance of "
                f"{Tachometer.__name__!r}."
            )

        if not isinstance(motor, DCMotor):
            raise TypeError(
                f"Parameter 'motor' must be an instance of "
                f"{DCMotor.__name__!r}."
            )

        if not motor.electric_current_is_computable:
            raise ValueError(
                "Parameter 'motor' cannot compute 'electric_current' property."
            )

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(
                f"Parameter 'target_angular_position' must be an instance of "
                f"{AngularPosition.__name__!r}."
            )

        if not isinstance(limit_electric_current, Current):
            raise TypeError(
                f"Parameter 'limit_electric_current' must be an instance of "
                f"{Current.__name__!r}."
            )

        if limit_electric_current.value <= 0:
            raise ValueError(
                "Parameter 'limit_electric_current' must be positive."
            )

        self.__encoder = encoder
        self.__tachometer = tachometer
        self.__motor = motor
        self.__limit_electric_current = limit_electric_current
        self.__target_angular_position = target_angular_position

    def apply(self) -> None | float | int:
        r"""It computes the ``pwm`` to apply to the ``motor`` in order to limit
        its absorbed electric current to be lower or equal to
        ``limit_electric_current``, until the ``encoder``'s ``target`` rotating
        object's ``angular_position`` equals the ``target_angular_position``.

        Returns
        -------
        :py:class:`float` or :py:class:`int` or :py:obj:`None`
            PWM value to apply to the ``motor`` in order to limit its absorbed
            electric current to be lower or equal to ``limit_electric_current``

        .. admonition:: Notes
           :class: tip

           It checks the applicability condition, defined as:

           .. math::
               \theta \le \theta_t

           where:

           - :math:`\theta` is the ``encoder``'s ``target``
             ``angular_position``,
           - :math:`\theta_t` is the ``target_angular_position``.

           If the applicability condition is not met, then it returns
           :py:obj:`None`, otherwise it computes the ``pwm`` as:

           .. math::
               D \left( \dot{\theta} \right) = \frac{1}{2} \, \left(
               \frac{\dot{\theta}}{\dot{\theta}_0} + \frac{i_{lim}}{i_{max}} +
               \sqrt{ \left( \frac{\dot{\theta}}{\dot{\theta}_0} \right)^2 +
               \left( \frac{i_{lim}}{i_{max}} \right)^2 +
               2 \frac{\dot{\theta}}{\dot{\theta}_0}
               \frac{i_{lim} - 2 i_0}{i_{max}} } \right)

           where:

           - :math:`\dot{\theta}` is the ``tachometer``'s ``target``'s angular
             speed,
           - :math:`\dot{\theta}_0` is the ``motor`` no load angular speed
             (:py:attr:`DCMotor.no_load_speed <gearpy.mechanical_objects.dc_motor.DCMotor.no_load_speed>`),
           - :math:`i_{lim}` is the ``limit_electric_current`` parameter,
           - :math:`i_{max}` is the ``motor`` maximum electric current
             (:py:attr:`DCMotor.maximum_electric_current <gearpy.mechanical_objects.dc_motor.DCMotor.maximum_electric_current>`),
           - :math:`i_0` is the ``motor`` no load electric current
             (:py:attr:`DCMotor.no_load_electric_current <gearpy.mechanical_objects.dc_motor.DCMotor.no_load_electric_current>`).
        """
        angular_position = self.__encoder.get_value()
        angular_speed = self.__tachometer.get_value()
        no_load_speed = self.__motor.no_load_speed
        maximum_electric_current = self.__motor.maximum_electric_current
        no_load_electric_current = self.__motor.no_load_electric_current
        speed_ratio = angular_speed/no_load_speed
        electric_ratio = self.__limit_electric_current/maximum_electric_current

        if angular_position <= self.__target_angular_position:
            return 1/2*(
                speed_ratio + electric_ratio + np.sqrt(
                    speed_ratio**2 + electric_ratio**2 + 2*speed_ratio*(
                        (
                            self.__limit_electric_current -
                            2*no_load_electric_current
                        )/maximum_electric_current
                    )
                )
            )
