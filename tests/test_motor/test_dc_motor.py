from gearpy.gear import SpurGear
from gearpy.motor import DCMotor
from gearpy.units import Torque
from hypothesis import given, settings
from hypothesis.strategies import text
from pytest import mark, raises
from tests.test_motor.conftest import basic_dc_motor
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_units.test_inertia_moment.conftest import inertia_moments, basic_inertia_moment
from tests.test_units.test_torque.conftest import torques


@mark.dc_motor
class TestDCMotorInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia_moment = inertia_moments(),
           no_load_speed = angular_speeds(),
           maximum_torque = torques())
    @settings(max_examples = 100)
    def test_method(self, name, inertia_moment, no_load_speed, maximum_torque):
        if no_load_speed.value > 0 and maximum_torque.value > 0:
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
        gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = basic_inertia_moment)
        basic_dc_motor.drives = gear

        assert basic_dc_motor.drives == gear


    @mark.error
    def test_raises_type_error(self, dc_motor_drives_type_error):
        with raises(TypeError):
            basic_dc_motor.drives = dc_motor_drives_type_error


@mark.dc_motor
class TestDCMotorComputeTorque:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia_moment = inertia_moments(),
           no_load_speed = angular_speeds(),
           maximum_torque = torques(),
           speed = angular_speeds())
    @settings(max_examples = 100)
    def test_method(self, name, inertia_moment, no_load_speed, maximum_torque, speed):
        if no_load_speed.value > 1e-10 and maximum_torque.value > 1e-10:
            motor = DCMotor(name = name, inertia_moment = inertia_moment, no_load_speed = no_load_speed, maximum_torque = maximum_torque)
            motor.angular_speed = speed
            torque = motor.compute_torque()

            assert isinstance(torque, Torque)
