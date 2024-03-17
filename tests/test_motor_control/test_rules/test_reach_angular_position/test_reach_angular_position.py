from gearpy.motor_control.rules import ReachAngularPosition
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.units import AngularPosition, Angle, Torque
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import integers, floats, booleans
from pytest import mark, raises
from tests.test_motor_control.test_rules.test_reach_angular_position.conftest import PowertrainFake
from tests.conftest import basic_encoder, powertrains
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angle.conftest import angles


@mark.rules
class TestReachAngularPositionInit:


    @mark.genuine
    @given(element_index = integers(min_value = 0),
           powertrain = powertrains(),
           target_angular_position = angular_positions(),
           braking_angle = angles())
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, element_index, powertrain, target_angular_position, braking_angle):
        element_index %= len(powertrain.elements)
        encoder = AbsoluteRotaryEncoder(target = powertrain.elements[element_index])
        rule = ReachAngularPosition(encoder = encoder, powertrain = powertrain,
                                    target_angular_position = target_angular_position, braking_angle = braking_angle)

        assert rule.encoder == encoder
        assert rule.powertrain == powertrain
        assert rule.target_angular_position == target_angular_position
        assert rule.braking_angle == braking_angle


    @mark.error
    def test_raises_type_error(self, reach_angular_position_init_type_error):
        with raises(TypeError):
            ReachAngularPosition(**reach_angular_position_init_type_error)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            ReachAngularPosition(encoder = basic_encoder, powertrain = PowertrainFake([]),
                                 target_angular_position = AngularPosition(1, 'rad'), braking_angle = Angle(1, 'rad'))


@mark.rules
class TestReachAngularPositionApply:


    @mark.genuine
    @given(element_index = integers(min_value = 0),
           powertrain = powertrains(),
           current_angular_position = floats(allow_nan = False, allow_infinity = False, min_value = 1, max_value = 1000),
           braking_angle_multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 2, max_value = 1000),
           target_angular_position_multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 3, max_value = 1000),
           available_load_torque = booleans())
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, element_index, powertrain, current_angular_position, braking_angle_multiplier,
                    target_angular_position_multiplier, available_load_torque):
        element_index %= len(powertrain.elements)
        encoder = AbsoluteRotaryEncoder(target = powertrain.elements[element_index])
        rule = ReachAngularPosition(encoder = encoder, powertrain = powertrain,
                                    target_angular_position = AngularPosition(value = current_angular_position*target_angular_position_multiplier,
                                                                              unit = 'rad'),
                                    braking_angle = Angle(value = current_angular_position*braking_angle_multiplier,
                                                          unit = 'rad'))
        powertrain.elements[element_index].angular_position = AngularPosition(value = current_angular_position, unit = 'rad')
        if available_load_torque:
            powertrain.elements[0].load_torque = Torque(0, 'Nm')
        pwm = rule.apply()

        if pwm is not None:
            assert isinstance(pwm, int) or isinstance(pwm, float)
