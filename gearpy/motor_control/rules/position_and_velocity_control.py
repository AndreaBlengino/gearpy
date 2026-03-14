from gearpy.motor_control.rules.rules_base import RuleBase
from gearpy.motor_control.utils import PIDController
from gearpy.motor_control.utils import SCurveTrajectory
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from gearpy.powertrain import Powertrain
from gearpy.units import TimeInterval, AngularSpeed


class PositionAndVelocityControl(RuleBase):

    def __init__(
        self,
        encoder: AbsoluteRotaryEncoder,
        tachometer: Tachometer,
        powertrain: Powertrain,
        position_PID: PIDController,
        velocity_PID: PIDController,
        trajecotry: SCurveTrajectory,
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

        if not isinstance(trajecotry, SCurveTrajectory):
            raise TypeError(
                f"Parameter 'trajecotry' must be an instance of "
                f"{SCurveTrajectory.__name__!r}."
            )

        self.__encoder = encoder
        self.__tachometer = tachometer
        self.__powertrain = powertrain
        self.__position_PID = position_PID
        self.__velocity_PID = velocity_PID
        self.__trajectory = trajecotry

    def apply(self) -> None | float | int:
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
