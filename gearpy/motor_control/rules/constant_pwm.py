from gearpy.sensors import Timer
from gearpy.powertrain import Powertrain
from gearpy.motor_control.rules.rules_base import RuleBase
from typing import Union


class ConstantPWM(RuleBase):
    """gearpy.motor_control.rules.constant_pwm.ConstantPWM object. \n
    It can be used to make a gradual start of the ``powertrain``'s motion, in order to avoid a peak in the
    ``powertrain``'s DC motor absorbed electric current. \n
    It checks whether the ``timer`` is active and, if so, it sets the ``pwm`` of ``powertrain`` motor to the constant
    ``target_pwm_value``.

    Methods
    -------
    :py:meth:`apply`
        Checks if ``timer`` is active and, if so, it returns the ``pwm`` to apply to the ``powertrain`` motor,
        equal to ``target_pwm_value``.

    Raises
    ------
    TypeError
        - If ``timer`` is not an instance of ``Timer``,
        - if ``powertrain`` is not an instance of ``Powertrain``,
        - if ``target_pwm_value`` is not a float or an integer.
    ValueError
        If ``target_pwm_value`` is not within ``-1`` and ``1``.

    See Also
    --------
    :py:attr:`gearpy.mechanical_objects.dc_motor.DCMotor.pwm`
    :py:class:`gearpy.sensors.Timer`
    """

    def __init__(self,
                 timer: Timer,
                 powertrain: Powertrain,
                 target_pwm_value: Union[float, int]):
        super().__init__()

        if not isinstance(timer, Timer):
            raise TypeError(f"Parameter 'timer' must be an instance of {Timer.__name__!r}.")

        if not isinstance(powertrain, Powertrain):
            raise TypeError(f"Parameter 'powertrain' must be an instance of {Powertrain.__name__!r}.")

        if not isinstance(target_pwm_value, float) and not isinstance(target_pwm_value, int):
            raise TypeError(f"Parameter 'target_pwm_value' must be a float or an integer.")

        if (target_pwm_value < -1) or (target_pwm_value > 1):
            raise ValueError(f"Parameter 'target_pwm_value' must be within -1 and 1.")

        self.__timer = timer
        self.__powertrain = powertrain
        self.__target_pwm_value = target_pwm_value

    def apply(self) -> Union[None, float, int]:
        r"""Checks if ``timer`` is active and, if so, it returns the ``pwm`` to apply to the ``powertrain`` motor,
        equal to ``target_pwm_value``.

        Returns
        -------
        float or int or None
            PWM value to apply to the motor, equal to ``target_pwm_value``.
        """
        if self.__timer.is_active(current_time = self.__powertrain.time[-1]):
            return self.__target_pwm_value
