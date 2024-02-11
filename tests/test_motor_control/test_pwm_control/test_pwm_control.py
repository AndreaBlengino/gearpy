from gearpy.mechanical_objects import DCMotor, SpurGear
from gearpy.motor_control import PWMControl
from gearpy.motor_control.rules import StartLimitCurrent, StartProportionalToAngularPosition, ReachAngularPosition
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from gearpy.powertrain import Powertrain
from gearpy.units import Angle, AngularSpeed, AngularPosition, Current, InertiaMoment, Torque
from gearpy.utils import add_fixed_joint
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import integers, floats, booleans
from pytest import mark, raises
from tests.conftest import powertrains, basic_powertrain
from tests.test_motor_control.test_pwm_control.conftest import PowertrainFake
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_units.test_angle.conftest import angles
from tests.test_units.test_current.conftest import currents


@mark.motor_control
class TestPWMControlInit:


    @mark.genuine
    @given(powertrain = powertrains())
    @settings(max_examples = 100, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, powertrain):
        motor_control = PWMControl(powertrain = powertrain)

        assert motor_control.powertrain == powertrain
        assert isinstance(motor_control.rules, list)
        assert not motor_control.rules


    @mark.error
    def test_raises_type_error(self, pwm_control_init_type_error):
        with raises(TypeError):
            PWMControl(**pwm_control_init_type_error)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            PWMControl(powertrain = PowertrainFake([]))


@mark.motor_control
class TestPWMControlAddRule:


    @mark.genuine
    @given(powertrain = powertrains(allow_simple_motors = False),
           start_target_angular_position = angular_positions(),
           reach_target_angular_position = angular_positions(),
           pwm_min_multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1 + 1e-10, exclude_min = True, max_value = 10),
           pwm_min = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 1),
           braking_angle = angles(),
           limit_electric_current = currents(min_value = 10, max_value = 15, unit = 'A'),
           element_index = integers(min_value = 0),
           use_limit_current_rule = booleans())
    @settings(max_examples = 100, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, powertrain, start_target_angular_position, reach_target_angular_position,
                    pwm_min_multiplier, pwm_min, braking_angle, limit_electric_current, element_index, use_limit_current_rule):
        element_index %= len(powertrain.elements)
        encoder = AbsoluteRotaryEncoder(target = powertrain.elements[element_index])

        if use_limit_current_rule:
            tachometer = Tachometer(target = powertrain.elements[element_index])
            start_rule = StartLimitCurrent(encoder = encoder, tachometer = tachometer, motor = powertrain.elements[0],
                                           target_angular_position = start_target_angular_position,
                                           limit_electric_current = limit_electric_current)
        else:
            start_rule = StartProportionalToAngularPosition(encoder = encoder, powertrain = powertrain,
                                                            target_angular_position = start_target_angular_position,
                                                            pwm_min_multiplier = pwm_min_multiplier, pwm_min = pwm_min)
        reach_rule = ReachAngularPosition(encoder = encoder, powertrain = powertrain,
                                          target_angular_position = reach_target_angular_position, braking_angle = braking_angle)
        motor_control = PWMControl(powertrain = powertrain)
        motor_control.add_rule(rule = start_rule)
        motor_control.add_rule(rule = reach_rule)

        assert start_rule in motor_control.rules
        assert reach_rule in motor_control.rules
        assert len(motor_control.rules) == 2


    @mark.error
    def test_raises_type_error(self, pwm_control_add_rule_type_error):
        motor_control = PWMControl(powertrain = basic_powertrain)
        with raises(TypeError):
            motor_control.add_rule(*pwm_control_add_rule_type_error)


@mark.motor_control
class TestPWMControlApplyRules:


    @mark.genuine
    @given(powertrain = powertrains(allow_simple_motors = False),
           start_target_angular_position = angular_positions(min_value = 100, max_value = 200, unit = 'rad'),
           reach_target_angular_position = angular_positions(min_value = 100_000, max_value = 200_000, unit = 'rad'),
           pwm_min_multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1 + 1e-10,
                                       exclude_min = True, max_value = 10),
           pwm_min = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 1),
           braking_angle = angles(min_value = 100, max_value = 1000, unit = 'rad'),
           limit_electric_current = currents(min_value = 10, max_value = 15, unit = 'A'),
           element_index = integers(min_value = 0),
           use_limit_current_rule = booleans(),
           current_angular_position = angular_positions(min_value = 0, max_value = 200_000, unit = 'rad'),
           current_angular_speed = angular_speeds())
    @settings(max_examples = 100, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, powertrain, start_target_angular_position, reach_target_angular_position,
                    pwm_min_multiplier, pwm_min, braking_angle, limit_electric_current, element_index,
                    use_limit_current_rule, current_angular_position, current_angular_speed):
        element_index %= len(powertrain.elements)
        encoder = AbsoluteRotaryEncoder(target = powertrain.elements[element_index])
        powertrain.elements[element_index].angular_position = current_angular_position

        if use_limit_current_rule:
            tachometer = Tachometer(target = powertrain.elements[element_index])
            powertrain.elements[element_index].angular_speed = current_angular_speed
            start_rule = StartLimitCurrent(encoder = encoder, tachometer = tachometer, motor = powertrain.elements[0],
                                           target_angular_position = start_target_angular_position,
                                           limit_electric_current = limit_electric_current)
        else:
            if powertrain.elements[0].time_variables['load torque']:
                powertrain.elements[0].time_variables['load torque'][0] = Torque(0, 'Nm')
            else:
                powertrain.elements[0].load_torque = Torque(0, 'Nm')
            start_rule = StartProportionalToAngularPosition(encoder = encoder, powertrain = powertrain,
                                                            target_angular_position = start_target_angular_position,
                                                            pwm_min_multiplier = pwm_min_multiplier, pwm_min = pwm_min)
        reach_rule = ReachAngularPosition(encoder = encoder, powertrain = powertrain,
                                          target_angular_position = reach_target_angular_position,
                                          braking_angle = braking_angle)
        motor_control = PWMControl(powertrain = powertrain)
        motor_control.add_rule(rule = start_rule)
        motor_control.add_rule(rule = reach_rule)
        motor_control.apply_rules()
        pwm = basic_powertrain.elements[0].pwm

        assert pwm is not None
        assert isinstance(pwm, float) or isinstance(pwm, int)
        assert (pwm <= 1) and (pwm >= -1)


    @mark.error
    def test_raises_value_error(self):
        motor = DCMotor(name = 'motor', no_load_speed = AngularSpeed(1000, 'rad/s'), maximum_torque = Torque(10, 'Nm'),
                        inertia_moment = InertiaMoment(1, 'kgm^2'), no_load_electric_current = Current(0.1, 'A'),
                        maximum_electric_current = Current(2, 'A'))
        gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
        add_fixed_joint(master = motor, slave = gear)
        powertrain = Powertrain(motor = motor)
        encoder = AbsoluteRotaryEncoder(target = motor)
        motor.angular_position = AngularPosition(10, 'rad')
        if powertrain.elements[0].time_variables['load torque']:
            powertrain.elements[0].time_variables['load torque'][0] = Torque(0, 'Nm')
        else:
            powertrain.elements[0].load_torque = Torque(0, 'Nm')

        start_rule = StartProportionalToAngularPosition(encoder = encoder, powertrain = powertrain,
                                                        target_angular_position = AngularPosition(1000, 'rad'),
                                                        pwm_min_multiplier = 1.1, pwm_min = 0.2)
        reach_rule = ReachAngularPosition(encoder = encoder, powertrain = powertrain,
                                          target_angular_position = AngularPosition(1, 'rad'),
                                          braking_angle = Angle(3, 'rad'))
        motor_control = PWMControl(powertrain = powertrain)
        motor_control.add_rule(rule = start_rule)
        motor_control.add_rule(rule = reach_rule)

        with raises(ValueError):
            motor_control.apply_rules()
