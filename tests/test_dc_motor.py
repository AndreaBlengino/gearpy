from gearpy import DCMotor
from hypothesis import given, settings
from hypothesis.strategies import text, floats
from pytest import mark, raises


@mark.dc_motor
class TestInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia = floats(min_value = 0, exclude_min = True),
           no_load_speed = floats(min_value = 0, exclude_min = True),
           maximum_torque = floats(min_value = 0, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, name, inertia, no_load_speed, maximum_torque):
        DCMotor(name = name, inertia = inertia, no_load_speed = no_load_speed, maximum_torque = maximum_torque)


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
