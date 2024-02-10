from gearpy.motor_control import ConstantPWM
from hypothesis import given, settings
from hypothesis.strategies import floats
from pytest import mark, raises
from tests.conftest import transmissions
from tests.test_units.test_time.conftest import times
from tests.test_sensors.test_timer.conftest import timers
import warnings


@mark.rules
class TestConstantPWMInit:


    @mark.genuine
    @given(timer = timers(),
           transmission = transmissions(),
           target_pwm_value = floats(allow_nan = False, allow_infinity = False, min_value = -1, max_value = 1))
    @settings(max_examples = 100)
    def test_method(self, timer, transmission, target_pwm_value):
        rule = ConstantPWM(timer = timer, transmission = transmission, target_pwm_value = target_pwm_value)

        assert rule.timer == timer
        assert rule.transmission == transmission
        assert rule.target_pwm_value == target_pwm_value


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


    @given(timer = timers(),
           transmission = transmissions(),
           target_pwm_value = floats(allow_nan = False, allow_infinity = False, min_value = -1, max_value = 1),
           current_time = times())
    def test_method(self, timer, transmission, target_pwm_value, current_time):
        warnings.filterwarnings('ignore', category = RuntimeWarning)
        rule = ConstantPWM(timer = timer, transmission = transmission, target_pwm_value = target_pwm_value)
        transmission.update_time(instant = current_time)

        pwm = rule.apply()
        if pwm is not None:
            assert isinstance(pwm, int) or isinstance(pwm, float)
            assert pwm == target_pwm_value
