from tests.conftest import basic_rotating_objects
from hypothesis import given, settings
from hypothesis.strategies import floats
from pytest import mark, raises


@mark.rotating_object
class TestRotatingObjectAngle:


    @mark.genuine
    @given(angle = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, angle):
        for rotating_object in basic_rotating_objects:
            rotating_object.angle = angle

            assert angle == rotating_object.angle


    @mark.error
    def test_raises_type_error(self, rotating_object_angle_type_error):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.angle = rotating_object_angle_type_error


@mark.rotating_object
class TestRotatingObjectSpeed:


    @mark.genuine
    @given(speed = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, speed):
        for rotating_object in basic_rotating_objects:
            rotating_object.speed = speed

            assert speed == rotating_object.speed


    @mark.error
    def test_raises_type_error(self, rotating_object_speed_type_error):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.speed = rotating_object_speed_type_error


@mark.rotating_object
class TestRotatingObjectAcceleration:


    @mark.genuine
    @given(acceleration = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, acceleration):
        for rotating_object in basic_rotating_objects:
            rotating_object.acceleration = acceleration

            assert acceleration == rotating_object.acceleration


    @mark.error
    def test_raises_type_error(self, rotating_object_acceleration_type_error):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.acceleration = rotating_object_acceleration_type_error


@mark.rotating_object
class TestRotatingObjectTorque:


    @mark.genuine
    @given(torque = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, torque):
        for rotating_object in basic_rotating_objects:
            rotating_object.torque = torque

            assert torque == rotating_object.torque


    @mark.error
    def test_raises_type_error(self, rotating_object_torque_type_error):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.torque = rotating_object_torque_type_error


@mark.rotating_object
class TestRotatingObjectDrivingTorque:


    @mark.genuine
    @given(driving_torque = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, driving_torque):
        for rotating_object in basic_rotating_objects:
            rotating_object.driving_torque = driving_torque

            assert driving_torque == rotating_object.driving_torque


    @mark.error
    def test_raises_type_error(self, rotating_object_driving_torque_type_error):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.driving_torque = rotating_object_driving_torque_type_error


@mark.rotating_object
class TestRotatingObjectLoadTorque:


    @mark.genuine
    @given(load_torque = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, load_torque):
        for rotating_object in basic_rotating_objects:
            rotating_object.load_torque = load_torque

            assert load_torque == rotating_object.load_torque


    @mark.error
    def test_raises_type_error(self, rotating_object_load_torque_type_error):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.load_torque = rotating_object_load_torque_type_error


@mark.rotating_object
class TestRotatingObjectTimeVariables:


    @mark.genuine
    def test_property(self):
        for rotating_object in basic_rotating_objects:
            time_variables = rotating_object.time_variables

            assert isinstance(time_variables, dict)
            assert ['angle', 'speed', 'acceleration',
                    'torque', 'driving torque', 'load torque'] == list(time_variables.keys())
            assert all([value == [] for value in time_variables.values()])


@mark.rotating_object
class TestRotatingObjectUpdateTimeVariables:


    @mark.genuine
    @given(angle = floats(allow_nan = False, allow_infinity = False),
           speed = floats(allow_nan = False, allow_infinity = False),
           acceleration = floats(allow_nan = False, allow_infinity = False),
           torque = floats(allow_nan = False, allow_infinity = False),
           driving_torque = floats(allow_nan = False, allow_infinity = False),
           load_torque = floats(allow_nan = False, allow_infinity = False))
    def test_method(self, angle, speed, acceleration, torque, driving_torque, load_torque):
        for rotating_object in basic_rotating_objects:
            rotating_object.angle = angle
            rotating_object.speed = speed
            rotating_object.acceleration = acceleration
            rotating_object.torque = torque
            rotating_object.driving_torque = driving_torque
            rotating_object.load_torque = load_torque

            rotating_object.update_time_variables()
            time_variables = rotating_object.time_variables

            assert isinstance(time_variables, dict)
            assert ['angle', 'speed', 'acceleration',
                    'torque', 'driving torque', 'load torque'] == list(time_variables.keys())
            assert time_variables['angle'][-1] == angle
            assert time_variables['speed'][-1] == speed
            assert time_variables['acceleration'][-1] == acceleration
            assert time_variables['torque'][-1] == torque
            assert time_variables['driving torque'][-1] == driving_torque
            assert time_variables['load torque'][-1] == load_torque
