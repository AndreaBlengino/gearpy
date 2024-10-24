from gearpy.sensors import Timer
from gearpy.powertrain import Powertrain
from gearpy.motor_control.rules.rules_base import RuleBase


class ConstantPWM(RuleBase):
    """:py:class:`ConstantPWM <gearpy.motor_control.rules.constant_pwm.ConstantPWM>`
    object. \n
    It can be used to make a gradual start of the ``powertrain``'s motion, in
    order to avoid a peak in the ``powertrain``'s DC motor absorbed electric
    current. \n
    It checks whether the ``timer`` is active and, if so, it sets the ``pwm``
    of ``powertrain`` motor to the constant ``target_pwm_value``.

    Methods
    -------
    :py:meth:`apply`
        It checks if ``timer`` is active and, if so, it returns the ``pwm`` to
        apply to the ``powertrain`` motor, equal to ``target_pwm_value``.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``timer`` is not an instance of
             :py:class:`Timer <gearpy.sensors.timer.Timer>`,
           - if ``powertrain`` is not an instance of
             :py:class:`Powertrain <gearpy.powertrain.Powertrain>`,
           - if ``target_pwm_value`` is not a :py:class:`float` or an
             :py:class:`int`.
       ``ValueError``
           If ``target_pwm_value`` is not within ``-1`` and ``1``.

    .. admonition:: See Also
       :class: seealso

       :py:attr:`DCMotor.pwm <gearpy.mechanical_objects.dc_motor.DCMotor.pwm>`
    """

    def __init__(
        self,
        timer: Timer,
        powertrain: Powertrain,
        target_pwm_value: float | int
    ):
        super().__init__()

        if not isinstance(timer, Timer):
            raise TypeError(
                f"Parameter 'timer' must be an instance of {Timer.__name__!r}."
            )

        if not isinstance(powertrain, Powertrain):
            raise TypeError(
                f"Parameter 'powertrain' must be an instance of "
                f"{Powertrain.__name__!r}."
            )

        if not isinstance(target_pwm_value, float | int):
            raise TypeError(
                "Parameter 'target_pwm_value' must be a float or an integer."
            )

        if (target_pwm_value < -1) or (target_pwm_value > 1):
            raise ValueError(
                "Parameter 'target_pwm_value' must be within -1 and 1."
            )

        self.__timer = timer
        self.__powertrain = powertrain
        self.__target_pwm_value = target_pwm_value

    def apply(self) -> None | float | int:
        r"""It checks if ``timer`` is active and, if so, it returns the ``pwm``
        to apply to the ``powertrain`` motor, equal to ``target_pwm_value``.

        Returns
        -------
        :py:class:`float` or :py:class:`int` or :py:obj:`None`
            PWM value to apply to the motor, equal to ``target_pwm_value``.
        """
        if self.__timer.is_active(current_time=self.__powertrain.time[-1]):
            return self.__target_pwm_value
