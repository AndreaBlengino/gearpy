from gearpy.motor_control.rules.rules_base import RuleBase
from gearpy.motor_control.utils import PIDController
from gearpy.motor_control.utils import SCurveTrajectory
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from gearpy.powertrain import Powertrain
from gearpy.units import TimeInterval, AngularSpeed


class PositionAndVelocityControl(RuleBase):
    """:py:class:`PositionAndVelocityControl <gearpy.motor_control.rules.position_and_velocity_control.PositionAndVelocityControl>`
    object. \n
    It can be used to force the angular position of a rotating object, tracked
    by the ``encoder``, to follow an S curve trajectory from a starting to a
    stopping position.

    Methods
    -------
    :py:meth:`apply`
        It computes the ``pwm`` to apply to the ``powertrain``'s motor in order
        to stick to position and velocity set by the ``trajectory`` through the
        two nested ``position_PID`` and ``velocity_PID``.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``encoder`` is not an instance of
             :py:class:`AbsoluteRotaryEncoder <gearpy.sensors.absolute_rotary_encoder.AbsoluteRotaryEncoder>`,
           - if ``tachometer`` is not an instance of
             :py:class:`Tachometer <gearpy.sensors.tachometer.Tachometer>`,
           - if ``powertrain`` is not an instance of
             :py:class:`DCMotor <gearpy.powertrain.Powertrain>`,
           - if ``position_PID`` is not an instance of
             :py:class:`PIDController <gearpy.motor_control.utils.pid_controller.PIDController>`,
           - if ``velocity_PID`` is not an instance of
             :py:class:`PIDController <gearpy.motor_control.utils.pid_controller.PIDController>`,
           - if ``trajectory`` is not an instance of
             :py:class:`SCurveTrajectory <gearpy.motor_control.utils.s_curve_trajectory.SCurveTrajectory>`.

    .. admonition:: See Also
       :class: seealso

       :py:attr:`DCMotor.pwm <gearpy.mechanical_objects.dc_motor.DCMotor.pwm>` \n
       :py:class:`PIDController <gearpy.motor_control.utils.pid_controller.PIDController>` \n
       :py:class:`SCurveTrajectory <gearpy.motor_control.utils.s_curve_trajectory.SCurveTrajectory>`
    """

    def __init__(
        self,
        encoder: AbsoluteRotaryEncoder,
        tachometer: Tachometer,
        powertrain: Powertrain,
        position_PID: PIDController,
        velocity_PID: PIDController,
        trajectory: SCurveTrajectory,
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

        if not isinstance(powertrain, Powertrain):
            raise TypeError(
                f"Parameter 'powertrain' must be an instance of "
                f"{Powertrain.__name__!r}."
            )

        if not isinstance(position_PID, PIDController):
            raise TypeError(
                f"Parameter 'position_PID' must be an instance of "
                f"{PIDController.__name__!r}."
            )

        if not isinstance(velocity_PID, PIDController):
            raise TypeError(
                f"Parameter 'velocity_PID' must be an instance of "
                f"{PIDController.__name__!r}."
            )

        if not isinstance(trajectory, SCurveTrajectory):
            raise TypeError(
                f"Parameter 'trajectory' must be an instance of "
                f"{SCurveTrajectory.__name__!r}."
            )

        self.__encoder = encoder
        self.__tachometer = tachometer
        self.__powertrain = powertrain
        self.__position_PID = position_PID
        self.__velocity_PID = velocity_PID
        self.__trajectory = trajectory

    def apply(self) -> None | float | int:
        r"""It computes the ``pwm`` to apply to the ``powertrain``'s motor in
        order to stick to position and velocity set by the ``trajectory``
        through the two nested ``position_PID`` and ``velocity_PID``.

        Returns
        -------
        :py:class:`float` or :py:class:`int` or :py:obj:`None`
            PWM value to apply to the ``powertrain``'s motor in order to stick
            to the S curve trajectory.

        .. admonition:: Notes
           :class: tip

           It computes a velocity reference through the ``position_PID`` as:

           .. math::
               \dot{\theta}_{ref} = PID_{pos}(\theta - \theta_{ref})

           where:

           - :math:`\dot{\theta}_{ref}` is the velocity reference,
           - :math:`\theta` is the current angular position, tracked by the
             ``encoder``,
           - :math:`\theta_{ref}` is the reference angular position, get by the
             S curve ``trajectory``.
           
           Then, it computes a PWM through the ``velocity_PID`` as:
           
           .. math::
              PWM_{ref} = PID_{vel}(\dot{\theta} - \dot{\theta}_{ref})

           where:

           - :math:`PWM_{ref}` is the reference PWM,
           - :math:`\dot{\theta}` is the current angular speed, tracked by the
             ``tachometer``.
        """
        current_angular_position = self.__encoder.get_value(unit="rad")
        set_angular_position = self.__trajectory.compute(
            self.__powertrain.time[-1].to("sec")
        ).to("rad").value

        angular_position_error = set_angular_position - \
            current_angular_position

        set_angular_speed = AngularSpeed(
            value=self.__position_PID.compute(
                angular_position_error,
                TimeInterval(value=1, unit="ms")
            ),
            unit="rad/s"
        )
        current_angular_speed = self.__tachometer.get_value()
        angular_speed_error = (
            set_angular_speed - current_angular_speed
        ).to("rad/s").value

        return self.__velocity_PID.compute(
            angular_speed_error,
            TimeInterval(value=1, unit="ms")
        )
