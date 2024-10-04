from gearpy.motor_control.rules import ConstantPWM
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import floats
from pytest import mark, raises
from tests.conftest import powertrains
from tests.test_units.test_time.conftest import times
from tests.test_sensors.test_timer.conftest import timers
import warnings


@mark.rules
class TestConstantPWMInit:

    @mark.genuine
    @given(
        timer=timers(),
        powertrain=powertrains(),
        target_pwm_value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1,
            max_value=1
        )
    )
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.too_slow]
    )
    def test_method(self, timer, powertrain, target_pwm_value):
        rule = ConstantPWM(
            timer=timer,
            powertrain=powertrain,
            target_pwm_value=target_pwm_value
        )

        assert rule._ConstantPWM__timer == timer
        assert rule._ConstantPWM__powertrain == powertrain
        assert rule._ConstantPWM__target_pwm_value == target_pwm_value

    @mark.error
    def test_raises_type_error(self, constant_pwm_init_type_error):
        with raises(TypeError):
            ConstantPWM(**constant_pwm_init_type_error)

    @mark.error
    def test_raises_value_error(self, constant_pwm_init_value_error):
        with raises(ValueError):
            ConstantPWM(**constant_pwm_init_value_error)


@mark.rules
class TestConstantPWMApply:

    @given(
        timer=timers(),
        powertrain=powertrains(),
        target_pwm_value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1,
            max_value=1
        ),
        current_time=times())
    @settings(
        max_examples=100,
        deadline=None,
        suppress_health_check=[HealthCheck.too_slow]
    )
    def test_method(self, timer, powertrain, target_pwm_value, current_time):
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        rule = ConstantPWM(
            timer=timer,
            powertrain=powertrain,
            target_pwm_value=target_pwm_value
        )
        powertrain.update_time(instant=current_time)

        pwm = rule.apply()
        if pwm is not None:
            assert isinstance(pwm, int) or isinstance(pwm, float)
            assert pwm == target_pwm_value
