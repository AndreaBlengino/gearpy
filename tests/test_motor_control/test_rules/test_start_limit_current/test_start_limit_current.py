from gearpy.motor_control.rules import StartLimitCurrent
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import floats
from pytest import mark, raises
from tests.conftest import dc_motors
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_units.test_current.conftest import currents
import warnings


@mark.rules
class TestStartLimitCurrentInit:

    @mark.genuine
    @given(
        motor=dc_motors(current=True),
        target_angular_position=angular_positions(),
        limit_electric_current=currents(min_value=1, max_value=10)
    )
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.too_slow]
    )
    def test_method(
        self,
        motor,
        target_angular_position,
        limit_electric_current
    ):
        encoder = AbsoluteRotaryEncoder(target=motor)
        tachometer = Tachometer(target=motor)
        rule = StartLimitCurrent(
            encoder=encoder,
            tachometer=tachometer,
            motor=motor,
            target_angular_position=target_angular_position,
            limit_electric_current=limit_electric_current
        )

        assert rule._StartLimitCurrent__encoder == encoder
        assert rule._StartLimitCurrent__tachometer == tachometer
        assert rule._StartLimitCurrent__motor == motor
        assert rule._StartLimitCurrent__limit_electric_current == \
            limit_electric_current
        assert rule._StartLimitCurrent__target_angular_position == \
            target_angular_position

    @mark.error
    def test_raises_type_error(self, start_limit_current_init_type_error):
        with raises(TypeError):
            StartLimitCurrent(**start_limit_current_init_type_error)

    @mark.error
    def test_raises_value_error(self, start_limit_current_init_value_error):
        with raises(ValueError):
            StartLimitCurrent(**start_limit_current_init_value_error)


@mark.rules
class TestStartLimitCurrentApply:

    @given(
        motor=dc_motors(current=True),
        current_angular_position=angular_positions(),
        limit_electric_current=currents(min_value=1, max_value=10),
        target_angular_position_multiplier=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=2,
            max_value=1000
        ),
        current_angular_speed=angular_speeds()
    )
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.too_slow]
    )
    def test_method(
        self,
        motor,
        current_angular_position,
        limit_electric_current,
        target_angular_position_multiplier,
        current_angular_speed
    ):
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        encoder = AbsoluteRotaryEncoder(target=motor)
        tachometer = Tachometer(target=motor)
        rule = StartLimitCurrent(
            encoder=encoder,
            tachometer=tachometer,
            motor=motor,
            target_angular_position=current_angular_position *
            target_angular_position_multiplier,
            limit_electric_current=limit_electric_current)
        motor.angular_position = current_angular_position
        motor.angular_speed = current_angular_speed

        pwm = rule.apply()
        if pwm is not None:
            assert isinstance(pwm, int) or isinstance(pwm, float)
