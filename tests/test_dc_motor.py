from gearpy import DCMotor
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

        assert name == motor.name
        assert inertia == motor.inertia
        assert no_load_speed == motor.no_load_speed
        assert maximum_torque == motor.maximum_torque


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
class TestDCMotorAngle:


    @mark.genuine
    @given(angle = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, angle):
        basic_dc_motor.angle = angle

        assert angle == basic_dc_motor.angle


    @mark.error
    def test_raises_type_error(self, dc_motor_angle_type_error):
        with raises(TypeError):
            basic_dc_motor.angle = dc_motor_angle_type_error


@mark.dc_motor
class TestDCMotorSpeed:


    @mark.genuine
    @given(speed = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, speed):
        basic_dc_motor.speed = speed

        assert speed == basic_dc_motor.speed


    @mark.error
    def test_raises_type_error(self, dc_motor_speed_type_error):
        with raises(TypeError):
            basic_dc_motor.speed = dc_motor_speed_type_error


@mark.dc_motor
class TestDCMotorAcceleration:


    @mark.genuine
    @given(acceleration = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, acceleration):
        basic_dc_motor.acceleration = acceleration

        assert acceleration == basic_dc_motor.acceleration


    @mark.error
    def test_raises_type_error(self, dc_motor_acceleration_type_error):
        with raises(TypeError):
            basic_dc_motor.acceleration = dc_motor_acceleration_type_error


@mark.dc_motor
class TestDCMotorTorque:


    @mark.genuine
    @given(torque = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, torque):
        basic_dc_motor.torque = torque

        assert torque == basic_dc_motor.torque


    @mark.error
    def test_raises_type_error(self, dc_motor_torque_type_error):
        with raises(TypeError):
            basic_dc_motor.torque = dc_motor_torque_type_error


@mark.dc_motor
class TestDCMotorDrivingTorque:


    @mark.genuine
    @given(driving_torque = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, driving_torque):
        basic_dc_motor.driving_torque = driving_torque

        assert driving_torque == basic_dc_motor.driving_torque


    @mark.error
    def test_raises_type_error(self, dc_motor_driving_torque_type_error):
        with raises(TypeError):
            basic_dc_motor.driving_torque = dc_motor_driving_torque_type_error


@mark.dc_motor
class TestDCMotorLoadTorque:


    @mark.genuine
    @given(load_torque = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, load_torque):
        basic_dc_motor.load_torque = load_torque

        assert load_torque == basic_dc_motor.load_torque


    @mark.error
    def test_raises_type_error(self, dc_motor_load_torque_type_error):
        with raises(TypeError):
            basic_dc_motor.load_torque = dc_motor_load_torque_type_error
