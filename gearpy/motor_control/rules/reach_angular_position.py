from gearpy.mechanical_objects import MotorBase, RotatingObject
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.powertrain import Powertrain
from gearpy.units import AngularPosition, Angle
from gearpy.motor_control.rules.rules_base import RuleBase
from typing import Union
from .utils import _compute_static_error


class ReachAngularPosition(RuleBase):
    """gearpy.motor_control.rules.reach_angular_position.ReachAngularPosition object. \n
    It can be used to make the ``encoder``'s ``target`` reach a ``target_angular_position`` within a ``braking_angle``.

    Attributes
    ----------
    :py:attr:`encoder` : AbsoluteRotaryEncoder
        Sensor used to measure the ``angular_position`` of a ``RotatingObject``, which is compared to
        ``target_angular_position``.
    :py:attr:`powertrain` : Powertrain
        Powertrain whose motor's ``pwm`` is controlled in order to reach a specific angular position.
    :py:attr:`target_angular_position` : AngularPosition
        Angular position to be reached by the ``encoder``'s target.
    :py:attr:`braking_angle` : Angle
        The angle within which the motor's ``pwm`` is controlled in order to brake and reach the
        ``target_angular_position``.

    Methods
    -------
    :py:meth:`apply`
        Computes the ``pwm`` to apply to the ``powertrain``'s motor in order to reach a ``target_angular_position`` by
        the ``target`` rotating object of the ``encoder``, within a specific ``braking_angle``.

    Raises
    ------
    TypeError
        - If ``encoder`` is not an instance of ``AbsoluteRotaryEncoder``,
        - if ``powertrain`` is not an instance of ``Powertrain``,
        - if the first element in ``powertrain`` is not an instance of ``MotorBase``,
        - if an element of ``powertrain`` is not an instance of ``RotatingObject``,
        - if ``target_angular_position`` is not an instance of ``AngularPosition``,
        - if ``braking_angle`` is not an instance of ``Angle``.
    ValueError
        If ``powertrain.elements`` is an empty tuple.

    See Also
    --------
    :py:attr:`gearpy.mechanical_objects.dc_motor.DCMotor.pwm`
    """

    def __init__(self,
                 encoder: AbsoluteRotaryEncoder,
                 powertrain: Powertrain,
                 target_angular_position: AngularPosition,
                 braking_angle: Angle):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(f"Parameter 'encoder' must be an instance of {AbsoluteRotaryEncoder.__name__!r}.")

        if not isinstance(powertrain, Powertrain):
            raise TypeError(f"Parameter 'powertrain' must be an instance of {Powertrain.__name__!r}.")

        if not powertrain.elements:
            raise ValueError("Parameter 'powertrain.elements' cannot be an empty tuple.")

        if not isinstance(powertrain.elements[0], MotorBase):
            raise TypeError(f"First element in 'powertrain' must be an instance of {MotorBase.__name__!r}.")

        if not all([isinstance(item, RotatingObject) for item in powertrain.elements]):
            raise TypeError(f"All elements of 'powertrain' must be instances of {RotatingObject.__name__!r}.")

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(f"Parameter 'target_angular_position' must be an instance of {AngularPosition.__name__!r}.")

        if not isinstance(braking_angle, Angle):
            raise TypeError(f"Parameter 'braking_angle' must be an instance of {Angle.__name__!r}.")

        self.__encoder = encoder
        self.__powertrain = powertrain
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
    def powertrain(self) -> Powertrain:
        """Powertrain whose motor's ``pwm`` is controlled in order to reach a specific angular position.

        Returns
        -------
        Powertrain
            Powertrain whose motor's ``pwm`` is controlled in order to reach a specific angular position.

        See Also
        --------
        :py:class:`gearpy.powertrain.Powertrain`
        """
        return self.__powertrain

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
            The angle within which the motor's ``pwm`` is controlled in order to brake and reach the
            ``target_angular_position``.

        See Also
        --------
        :py:class:`gearpy.units.units.Angle`
        """
        return self.__braking_angle

    def apply(self) -> Union[None, float, int]:
        r"""Computes the ``pwm`` to apply to the ``powertrain``'s DC motor in order to reach a
        ``target_angular_position`` by the ``target`` rotating object of the ``encoder``, within a specific
        ``braking_angle``.

        Returns
        -------
        float or int or None
            PWM value to apply to the motor in order to reach the target angular position.

        Notes
        -----
        It computes the ``powertrain``'s *static error* according to the following formula:

        .. math::
            \theta_{err} \left( T_l \right) = \frac{T_l}{T_{max}} \, \frac{\theta_b}{\eta_t}

        where:

        - :math:`\theta_{err}` is the ``powertrain`` static error,
        - :math:`T_l` is the load torque on the ``powertrain`` DC motor,
        - :math:`T_{max}` is the maximum torque developed by the ``powertrain`` DC motor,
        - :math:`\theta_b` is the ``braking_angle`` parameter,
        - :math:`\eta_t` is the ``powertrain`` overall efficiency, computed as:

        .. math::
            \eta_t = \prod_{i = 1}^N \eta_i

        where:

        - :math:`\eta_i` is the mechanical mating efficiency of the mating between two gears,
        - :math:`N` is the total number of gear matings in the ``powertrain``.

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
                                                              powertrain = self.powertrain)
        braking_starting_angle = self.target_angular_position - self.braking_angle + regime_angular_position_error

        if angular_position >= braking_starting_angle:
            return 1 - (angular_position - braking_starting_angle)/self.braking_angle
