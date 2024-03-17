from gearpy.mechanical_objects import DCMotor, SpurGear
from gearpy.units import Length, Torque, Current
from hypothesis import given, settings
from hypothesis.strategies import text, floats, booleans
from pytest import mark, raises
from tests.conftest import basic_dc_motor_1, basic_dc_motor_2
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_units.test_inertia_moment.conftest import inertia_moments, basic_inertia_moment
from tests.test_units.test_torque.conftest import torques
from tests.test_units.test_current.conftest import currents


@mark.dc_motor
class TestDCMotorInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia_moment = inertia_moments(),
           no_load_speed = angular_speeds(min_value = 1, max_value = 1000),
           maximum_torque = torques(min_value = 1, max_value = 10))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, name, inertia_moment, no_load_speed, maximum_torque):
        motor = DCMotor(name = name, inertia_moment = inertia_moment, no_load_speed = no_load_speed, maximum_torque = maximum_torque)

        assert motor.name == name
        assert motor.inertia_moment == inertia_moment
        assert motor.no_load_speed == no_load_speed
        assert motor.maximum_torque == maximum_torque


    @mark.error
    def test_raises_type_error(self, dc_motor_init_type_error):
        with raises(TypeError):
            DCMotor(**dc_motor_init_type_error)


    @mark.error
    def test_raises_value_error(self, dc_motor_init_value_error):
        with raises(ValueError):
            DCMotor(**dc_motor_init_value_error)


@mark.dc_motor
class TestDCMotorDrives:


    @mark.genuine
    def test_property(self):
        gear = SpurGear(name = 'gear', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = basic_inertia_moment)
        basic_dc_motor_1.drives = gear

        assert basic_dc_motor_1.drives == gear


    @mark.error
    def test_raises_type_error(self, dc_motor_drives_type_error):
        with raises(TypeError):
            basic_dc_motor_1.drives = dc_motor_drives_type_error


@mark.dc_motor
class TestDCMotorComputeTorque:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia_moment = inertia_moments(),
           no_load_speed = angular_speeds(min_value = 1e-10, max_value = 1000),
           maximum_torque = torques(min_value = 1e-10, max_value = 10),
           no_load_electric_current = currents(min_value = 1, max_value = 2, unit = 'A'),
           maximum_electric_current = currents(min_value = 5, max_value = 10, unit = 'A'),
           speed = angular_speeds(),
           electric_motor = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_method(self, name, inertia_moment, no_load_speed, maximum_torque, no_load_electric_current,
                    maximum_electric_current, speed, electric_motor):
        if electric_motor:
            motor = DCMotor(name = name, inertia_moment = inertia_moment, no_load_speed = no_load_speed,
                            maximum_torque = maximum_torque, no_load_electric_current = no_load_electric_current,
                            maximum_electric_current = maximum_electric_current)
        else:
            motor = DCMotor(name = name, inertia_moment = inertia_moment, no_load_speed = no_load_speed,
                            maximum_torque = maximum_torque)
        motor.angular_speed = speed
        for pwm in [-1, 0, 1]:
            motor.pwm = pwm
            motor.compute_torque()

            assert isinstance(motor.driving_torque, Torque)


@mark.dc_motor
class TestDCMotorComputeElectricCurrent:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia_moment = inertia_moments(),
           no_load_speed = angular_speeds(min_value = 1e-10, max_value = 1000),
           maximum_torque = torques(min_value = 1e-10, max_value = 10),
           no_load_electric_current = currents(min_value = 0, max_value = 0.1, unit = 'A'),
           maximum_electric_current = currents(min_value = 0.2, max_value = 10, unit = 'A'),
           driving_torque = torques())
    @settings(max_examples = 100, deadline = None)
    def test_method(self, name, inertia_moment, no_load_speed, maximum_torque, no_load_electric_current,
                    maximum_electric_current, driving_torque):
        motor = DCMotor(name = name, inertia_moment = inertia_moment, no_load_speed = no_load_speed,
                        maximum_torque = maximum_torque, no_load_electric_current =  no_load_electric_current,
                        maximum_electric_current = maximum_electric_current)
        motor.driving_torque = driving_torque
        for pwm in [-1, 0, 1]:
            motor.pwm = pwm
            motor.compute_electric_current()

            assert isinstance(motor.electric_current, Current)


@mark.dc_motor
class TestDCMotorElectricCurrent:


    @mark.genuine
    def test_property(self):
        electric_current = Current(1, 'A')
        basic_dc_motor_1.electric_current = electric_current

        assert basic_dc_motor_1.electric_current == electric_current


    @mark.error
    def test_raises_type_error(self, dc_motor_electric_current_type_error):
        with raises(TypeError):
            basic_dc_motor_1.electric_current = dc_motor_electric_current_type_error


@mark.dc_motor
class TestDCMotorElectricCurrentIsComputable:


    @mark.genuine
    def test_property(self):
        for motor in [basic_dc_motor_1, basic_dc_motor_2]:
            if (motor.no_load_electric_current is None) or (motor.maximum_electric_current is None):
                assert not motor.electric_current_is_computable
            else:
                assert motor.electric_current_is_computable


@mark.dc_motor
class TestDCMotorPWM:


    @mark.genuine
    @given(pwm = floats(allow_nan = False, allow_infinity = False, min_value = -1, max_value = 1))
    @settings(max_examples = 100, deadline = None)
    def test_property(self, pwm):
        basic_dc_motor_1.pwm = pwm

        assert basic_dc_motor_1.pwm == pwm


    @mark.error
    def test_raises_type_error(self, dc_motor_pwm_type_error):
        with raises(TypeError):
            basic_dc_motor_1.pwm = dc_motor_pwm_type_error


    @mark.error
    def test_raises_value_error(self, dc_motor_pwm_value_error):
        with raises(ValueError):
            basic_dc_motor_1.pwm = dc_motor_pwm_value_error
