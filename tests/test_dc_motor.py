from gearpy import DCMotor, SpurGear
from hypothesis import given, settings
from hypothesis.strategies import text, floats
from pytest import mark, raises
from tests.conftest import basic_dc_motor


@mark.dc_motor
class TestDCMotorInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia = floats(min_value = 0, exclude_min = True),
           no_load_speed = floats(min_value = 0, exclude_min = True),
           maximum_torque = floats(min_value = 0, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, name, inertia, no_load_speed, maximum_torque):
        motor = DCMotor(name = name, inertia = inertia, no_load_speed = no_load_speed, maximum_torque = maximum_torque)

        assert motor.name == name
        assert motor.inertia == inertia
        assert motor.no_load_speed == no_load_speed
        assert motor.maximum_torque == maximum_torque


    @mark.error
    def test_raises_type_error(self, dc_motor_init_type_error):
        with raises(TypeError):
            DCMotor(name = dc_motor_init_type_error['name'],
                    inertia = dc_motor_init_type_error['inertia'],
                    no_load_speed = dc_motor_init_type_error['no_load_speed'],
                    maximum_torque = dc_motor_init_type_error['maximum_torque'])


    @mark.error
    def test_raises_value_error(self, dc_motor_init_value_error):
        with raises(ValueError):
            DCMotor(name = dc_motor_init_value_error['name'],
                    inertia = dc_motor_init_value_error['inertia'],
                    no_load_speed = dc_motor_init_value_error['no_load_speed'],
                    maximum_torque = dc_motor_init_value_error['maximum_torque'])


@mark.dc_motor
class TestDCMotorDrives:


    @mark.genuine
    def test_property(self):
        gear = SpurGear(name = 'gear', n_teeth = 10, inertia = 1)
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
           inertia = floats(min_value = 0, exclude_min = True),
           no_load_speed = floats(min_value = 0, exclude_min = True),
           maximum_torque = floats(min_value = 0, exclude_min = True),
           speed = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_method(self, name, inertia, no_load_speed, maximum_torque, speed):
        motor = DCMotor(name = name, inertia = inertia, no_load_speed = no_load_speed, maximum_torque = maximum_torque)
        motor.speed = speed
        torque = motor.compute_torque()

        assert isinstance(torque, float) or isinstance(torque, int)
