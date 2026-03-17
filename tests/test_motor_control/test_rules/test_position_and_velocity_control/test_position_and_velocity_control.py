from gearpy.motor_control.rules import PositionAndVelocityControl
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from hypothesis import given, settings
from pytest import mark, raises
from tests.conftest import powertrains, solved_powertrains
from tests.test_motor_control.test_utils.test_s_curve_trajectory.conftest \
    import s_trajectories
from tests.test_motor_control.test_utils.test_pid_controller.conftest \
    import pid_controllers
import warnings


@mark.rules
class TestPositionAndVelocityControlInit:

    @mark.genuine
    @given(
        powertrain=powertrains(allow_motors_with_current=True),
        position_pid=pid_controllers(),
        velocity_pid=pid_controllers(),
        trajectory=s_trajectories()
    )
    @settings(max_examples=100, deadline=None)
    def test_method(
        self,
        powertrain,
        position_pid,
        velocity_pid,
        trajectory
    ):
        encoder = AbsoluteRotaryEncoder(target=powertrain.elements[0])
        tachometer = Tachometer(target=powertrain.elements[0])
        rule = PositionAndVelocityControl(
            encoder=encoder,
            tachometer=tachometer,
            powertrain=powertrain,
            position_PID=position_pid,
            velocity_PID=velocity_pid,
            trajectory=trajectory
        )

        assert rule._PositionAndVelocityControl__encoder == encoder
        assert rule._PositionAndVelocityControl__tachometer == tachometer
        assert rule._PositionAndVelocityControl__powertrain == powertrain
        assert rule._PositionAndVelocityControl__position_PID == position_pid
        assert rule._PositionAndVelocityControl__velocity_PID == velocity_pid
        assert rule._PositionAndVelocityControl__trajectory == trajectory

    @mark.error
    def test_raises_type_error(
        self,
        position_and_velocity_control_init_type_error
    ):
        with raises(TypeError):
            PositionAndVelocityControl(
                **position_and_velocity_control_init_type_error
            )


@mark.rules
class TestPositionAndVelocityControlApply:

    @mark.genuine
    @given(
        powertrain=solved_powertrains(),
        position_pid=pid_controllers(),
        velocity_pid=pid_controllers(),
        trajectory=s_trajectories()
    )
    @settings(max_examples=100, deadline=None)
    def test_method(
        self,
        powertrain,
        position_pid,
        velocity_pid,
        trajectory
    ):
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        encoder = AbsoluteRotaryEncoder(target=powertrain.elements[0])
        tachometer = Tachometer(target=powertrain.elements[0])
        rule = PositionAndVelocityControl(
            encoder=encoder,
            tachometer=tachometer,
            powertrain=powertrain,
            position_PID=position_pid,
            velocity_PID=velocity_pid,
            trajectory=trajectory
        )

        pwm = rule.apply()
        if pwm is not None:
            assert isinstance(pwm, float | int)
