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

    Attributes
    ----------
    :py:attr:`timer` : Timer
        The timer which, when active, sets the control of ``powertrain`` motor ``pwm``.
    :py:attr:`powertrain` : Powertrain
        Powertrain whose motor's ``pwm`` is set to a constant value equal to ``target_pwm_value``.
    :py:attr:`target_pwm_min` : float or int
        Target value to set ``powertrain`` motor ``pwm`` when the ``timer`` is active.

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

    @property
    def timer(self) -> Timer:
        """Timer which, when active, sets the control of ``powertrain`` motor ``pwm``.

        Returns
        -------
        Timer
            The timer which, when active, sets the control of ``powertrain`` motor ``pwm``.

        Raises
        ------
        TypeError
            If ``timer`` is not an instance of ``Timer``.

        See Also
        --------
        :py:class:`gearpy.sensors.Timer`
        """
        return self.__timer

    @property
    def powertrain(self) -> Powertrain:
        """Powertrain whose motor's ``pwm`` is set to a constant value equal to ``target_pwm_value``.

        Returns
        -------
        Powertrain
            Powertrain whose motor's ``pwm`` is set to a constant value equal to ``target_pwm_value``.

        Raises
        ------
        TypeError
            If ``powertrain`` is not an instance of ``Powertrain``.

        See Also
        --------
        :py:class:`gearpy.powertrain.Powertrain`
        """
        return self.__powertrain

    @property
    def target_pwm_value(self) -> Union[float, int]:
        """Target value to set ``powertrain`` motor ``pwm`` when the ``timer`` is active.

        Returns
        -------
        float or int
            Target value to set ``powertrain`` motor ``pwm`` when the ``timer`` is active.

        Raises
        ------
        TypeError
            If ``target_pwm_value`` is not a float or an integer.
        ValueError
            If ``target_pwm_value`` is not within ``-1`` and ``1``.

        See Also
        --------
        :py:attr:`gearpy.mechanical_objects.dc_motor.DCMotor.pwm`
        """
        return self.__target_pwm_value

    def apply(self) -> Union[None, float, int]:
        r"""Checks if ``timer`` is active and, if so, it returns the ``pwm`` to apply to the ``powertrain`` motor,
        equal to ``target_pwm_value``.

        Returns
        -------
        float or int or None
            PWM value to apply to the motor, equal to ``target_pwm_value``.
        """
        if self.timer.is_active(current_time = self.powertrain.time[-1]):
            return self.target_pwm_value
