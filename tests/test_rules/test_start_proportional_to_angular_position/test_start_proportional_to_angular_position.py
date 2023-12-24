from gearpy.mechanical_object import DCMotor, SpurGear
from gearpy.motor_control import StartProportionalToAngularPosition
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.transmission import Transmission
from gearpy.units import AngularPosition, InertiaMoment, AngularSpeed, Torque, Current
from gearpy.utils import add_fixed_joint
from hypothesis import given, settings
from hypothesis.strategies import integers, floats, one_of, none
from pytest import mark, raises
from tests.conftest import transmissions
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_torque.conftest import torques


@mark.rules
class TestStartProportionalToAngularPositionInit:


    @mark.genuine
    @given(element_index = integers(min_value = 0),
           transmission = transmissions(),
           target_angular_position = angular_positions(),
           pwm_min_multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1, exclude_min = True, max_value = 1000),
           pwm_min = one_of(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1),
                            none()))
    @settings(max_examples = 100)
    def test_method(self, element_index, transmission, target_angular_position, pwm_min_multiplier, pwm_min):
        if transmission.chain[0].electric_current_is_computable:
            element_index %= len(transmission.chain)
            encoder = AbsoluteRotaryEncoder(target = transmission.chain[element_index])
            rule = StartProportionalToAngularPosition(encoder = encoder, transmission = transmission,
                                                      target_angular_position = target_angular_position,
                                                      pwm_min_multiplier = pwm_min_multiplier, pwm_min = pwm_min)

            assert rule.encoder == encoder
            assert rule.transmission == transmission
            assert rule.target_angular_position == target_angular_position
            assert rule.pwm_min_multiplier == pwm_min_multiplier
            assert rule.pwm_min == pwm_min


    @mark.error
    def test_raises_type_error(self, start_proportional_to_angular_position_init_type_error):
        with raises(TypeError):
            StartProportionalToAngularPosition(**start_proportional_to_angular_position_init_type_error)


    @mark.error
    def test_raises_value_error(self, start_proportional_to_angular_position_init_value_error):
        with raises(ValueError):
            StartProportionalToAngularPosition(**start_proportional_to_angular_position_init_value_error)


@mark.rules
class TestStartProportionalToAngularPositionApply:


    @mark.genuine
    @given(element_index = integers(min_value = 0),
           transmission = transmissions(),
           current_angular_position = floats(allow_nan = False, allow_infinity = False, min_value = 1, max_value = 1000),
           pwm_min_multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1, exclude_min = True, max_value = 1000),
           pwm_min = one_of(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1),
                            none()),
           target_angular_position_multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 2, max_value = 1000),
           load_torque = torques())
    @settings(max_examples = 100)
    def test_method(self, element_index, transmission, current_angular_position, pwm_min_multiplier, pwm_min,
                    target_angular_position_multiplier, load_torque):
        if transmission.chain[0].electric_current_is_computable:
            if transmission.chain[0].no_load_electric_current.value != 0:
                element_index %= len(transmission.chain)
                encoder = AbsoluteRotaryEncoder(target = transmission.chain[element_index])
                rule = StartProportionalToAngularPosition(encoder = encoder, transmission = transmission,
                                                          target_angular_position = AngularPosition(value = current_angular_position*target_angular_position_multiplier,
                                                                                                    unit = 'rad'),
                                                          pwm_min_multiplier = pwm_min_multiplier,
                                                          pwm_min = pwm_min)
                transmission.chain[element_index].angular_position = AngularPosition(value = current_angular_position, unit = 'rad')
                if transmission.chain[0].time_variables['load torque']:
                    transmission.chain[0].time_variables['load torque'][0] = load_torque
                else:
                    transmission.chain[0].load_torque = load_torque

                pwm = rule.apply()
                if pwm is not None:
                    assert isinstance(pwm, int) or isinstance(pwm, float)
        elif pwm_min is not None:
            motor = DCMotor(name = 'motor', inertia_moment = InertiaMoment(1, 'kgm^2'),
                            no_load_speed = AngularSpeed(1000, 'rad/s'), maximum_torque = Torque(1, 'Nm'),
                            no_load_electric_current = Current(0, 'A'), maximum_electric_current = Current(1, 'A'))
            gear = SpurGear(name = 'gear', n_teeth = 20, inertia_moment = InertiaMoment(1, 'kgm^2'))
            add_fixed_joint(master = motor, slave = gear)
            transmission = Transmission(motor = motor)
            encoder = AbsoluteRotaryEncoder(target = motor)
            rule = StartProportionalToAngularPosition(encoder = encoder, transmission = transmission,
                                                      target_angular_position = AngularPosition(value = current_angular_position*target_angular_position_multiplier,
                                                                                                unit = 'rad'),
                                                      pwm_min_multiplier = pwm_min_multiplier, pwm_min = pwm_min)
            motor.angular_position = AngularPosition(value = current_angular_position, unit = 'rad')
            if motor.time_variables['load torque']:
                motor.time_variables['load torque'][0] = Torque(0, 'Nm')
            else:
                motor.load_torque = Torque(0, 'Nm')

            pwm = rule.apply()
            if pwm is not None:
                assert isinstance(pwm, int) or isinstance(pwm, float)


    @mark.error
    def test_raises_value_error(self):
        motor = DCMotor(name = 'motor', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rad/s'), maximum_torque = Torque(1, 'Nm'),
                        no_load_electric_current = Current(0, 'A'), maximum_electric_current = Current(1, 'A'))
        gear = SpurGear(name = 'gear', n_teeth = 20, inertia_moment = InertiaMoment(1, 'kgm^2'))
        add_fixed_joint(master = motor, slave = gear)
        transmission = Transmission(motor = motor)
        encoder = AbsoluteRotaryEncoder(target = motor)
        rule = StartProportionalToAngularPosition(encoder = encoder, transmission = transmission,
                                                  target_angular_position = AngularPosition(1, 'rad'),
                                                  pwm_min_multiplier = 2)

        motor.angular_position = AngularPosition(0, 'rad')
        if motor.time_variables['load torque']:
            motor.time_variables['load torque'][0] = Torque(0, 'Nm')
        else:
            motor.load_torque = Torque(0, 'Nm')

        with raises(ValueError):
            rule.apply()
