from gearpy.mechanical_objects import MotorBase, RotatingObject
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.powertrain import Powertrain
from gearpy.units import AngularPosition, Angle
from gearpy.motor_control.rules.rules_base import RuleBase
from .utils import _compute_static_error


class ReachAngularPosition(RuleBase):
    """:py:class:`ReachAngularPosition <gearpy.motor_control.rules.reach_angular_position.ReachAngularPosition>`
    object. \n
    It can be used to make the ``encoder``'s ``target`` reach a
    ``target_angular_position`` within a ``braking_angle``.

    Methods
    -------
    :py:meth:`apply`
        It computes the ``pwm`` to apply to the ``powertrain``'s motor in order
        to reach a ``target_angular_position`` by the ``target`` rotating
        object of the ``encoder``, within a specific ``braking_angle``.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``encoder`` is not an instance of
             :py:class:`AbsoluteRotaryEncoder <gearpy.sensors.absolute_rotary_encoder.AbsoluteRotaryEncoder>`,
           - if ``powertrain`` is not an instance of
             :py:class:`Powertrain <gearpy.powertrain.Powertrain>`,
           - if the first element in ``powertrain`` is not an instance of
             :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`,
           - if an element of ``powertrain`` is not an instance of
             :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`,
           - if ``target_angular_position`` is not an instance of
             :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`,
           - if ``braking_angle`` is not an instance of
             :py:class:`Angle <gearpy.units.units.Angle>`.
       ``ValueError``
           If ``powertrain.elements`` is an empty :py:class:`tuple`.

    .. admonition:: See Also
       :class: seealso

       :py:attr:`DCMotor.pwm <gearpy.mechanical_objects.dc_motor.DCMotor.pwm>`
    """

    def __init__(
        self,
        encoder: AbsoluteRotaryEncoder,
        powertrain: Powertrain,
        target_angular_position: AngularPosition,
        braking_angle: Angle
    ):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(
                f"Parameter 'encoder' must be an instance of "
                f"{AbsoluteRotaryEncoder.__name__!r}."
            )

        if not isinstance(powertrain, Powertrain):
            raise TypeError(
                f"Parameter 'powertrain' must be an instance of "
                f"{Powertrain.__name__!r}."
            )

        if not powertrain.elements:
            raise ValueError(
                "Parameter 'powertrain.elements' cannot be an empty tuple."
            )

        if not isinstance(powertrain.elements[0], MotorBase):
            raise TypeError(
                f"First element in 'powertrain' must be an instance of "
                f"{MotorBase.__name__!r}."
            )

        if not all(
            [isinstance(item, RotatingObject) for item in powertrain.elements]
        ):
            raise TypeError(
                f"All elements of 'powertrain' must be instances of "
                f"{RotatingObject.__name__!r}."
            )

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(
                f"Parameter 'target_angular_position' must be an instance of "
                f"{AngularPosition.__name__!r}."
            )

        if not isinstance(braking_angle, Angle):
            raise TypeError(
                f"Parameter 'braking_angle' must be an instance of "
                f"{Angle.__name__!r}."
            )

        self.__encoder = encoder
        self.__powertrain = powertrain
        self.__target_angular_position = target_angular_position
        self.__braking_angle = braking_angle

    def apply(self) -> None | float | int:
        """It computes the ``pwm`` to apply to the ``powertrain``'s DC motor in
        order to reach a ``target_angular_position`` by the ``target``
        rotating object of the ``encoder``, within a specific
        ``braking_angle``.

        Returns
        -------
        :py:class:`float` or :py:class:`int` or :py:obj:`None`
            PWM value to apply to the motor in order to reach the target
            angular position.

        .. admonition:: Notes
           :class: tip

           The braking angle is the angle within which the motor's ``pwm`` is
           controlled in order to brake and reach the
           ``target_angular_position``. \n
           The rule is applied only if the difference between
           ``target_angular_position`` and the ``encoder``'s target
           ``angular_position`` is lower than or equal to the
           ``braking_angle``. \n
           The lower the ``braking_angle`` the higher the deceleration of the
           system, thus the higher the vibrations produced. \n
           First of all, the rule computes the ``powertrain``'s *static error*
           according to the following formula:
        """\
        r"""
           .. math::
               \theta_{err} \left( T_l \right) = \frac{T_l}{T_{max}} \,
               \frac{\theta_b}{\eta_t}

           where:

           - :math:`\theta_{err}` is the ``powertrain`` static error,
           - :math:`T_l` is the load torque on the ``powertrain`` DC motor
             (:py:attr:`DCMotor.load_torque <gearpy.mechanical_objects.dc_motor.DCMotor.load_torque>`),
           - :math:`T_{max}` is the maximum torque developed by the
             ``powertrain`` DC motor
             (:py:attr:`DCMotor.maximum_torque <gearpy.mechanical_objects.dc_motor.DCMotor.maximum_torque>`),
           - :math:`\theta_b` is the ``braking_angle`` parameter,
           - :math:`\eta_t` is the ``powertrain`` overall efficiency, computed
             as:

           .. math::
               \eta_t = \prod_{i = 1}^N \eta_i

           where:

           - :math:`\eta_i` is the mechanical mating efficiency of the mating
             between two gears
             (:py:attr:`SpurGear.master_gear_efficiency <gearpy.mechanical_objects.spur_gear.SpurGear.master_gear_efficiency>`
             or
             :py:attr:`HelicalGear.master_gear_efficiency <gearpy.mechanical_objects.helical_gear.HelicalGear.master_gear_efficiency>`
             or
             :py:attr:`WormGear.master_gear_efficiency <gearpy.mechanical_objects.worm_gear.WormGear.master_gear_efficiency>`
             or
             :py:attr:`WormWheel.master_gear_efficiency <gearpy.mechanical_objects.worm_wheel.WormWheel.master_gear_efficiency>`),
           - :math:`N` is the total number of gear matings in the
             ``powertrain``.

           Then it checks the applicability condition, defined as:

           .. math::
               \theta \ge \theta_s = \theta_t - \theta_b + \theta_{err}

           where:

           - :math:`\theta` is the ``encoder``'s ``target``
             ``angular_position``,
           - :math:`\theta_s` is the braking starting angle,
           - :math:`\theta_t` is the ``target_angular_position`` parameter.

           If the applicability condition is not met, then it returns
           :py:obj:`None`, otherwise it computes the ``pwm`` as:

           .. math::
               D \left( \theta \right) = 1 - \frac{\theta - \theta_s}{\theta_b}

           where :math:`D` is the supply voltage PWM duty cycle ``pwm`` to
           apply to the DC motor in order to reach the
           ``target_angular_position`` by the ``encoder``'s ``target``
           rotating object.
        """
        angular_position = self.__encoder.get_value()

        regime_angular_position_error = _compute_static_error(
            braking_angle=self.__braking_angle,
            powertrain=self.__powertrain
        )
        braking_starting_angle = \
            self.__target_angular_position - \
            self.__braking_angle + regime_angular_position_error

        if angular_position >= braking_starting_angle:
            return 1 - (angular_position - braking_starting_angle) / \
                self.__braking_angle
