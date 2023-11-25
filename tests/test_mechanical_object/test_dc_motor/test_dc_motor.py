from gearpy.mechanical_object import DCMotor, SpurGear
from gearpy.units import Length, Torque, Current
from hypothesis import given, settings
from hypothesis.strategies import text
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
           no_load_speed = angular_speeds(),
           maximum_torque = torques(),
           speed = angular_speeds())
    @settings(max_examples = 100)
    def test_method(self, name, inertia_moment, no_load_speed, maximum_torque, speed):
        if no_load_speed.value > 1e-10 and maximum_torque.value > 1e-10:
            motor = DCMotor(name = name, inertia_moment = inertia_moment, no_load_speed = no_load_speed, maximum_torque = maximum_torque)
            motor.angular_speed = speed
            motor.compute_torque()

            assert isinstance(motor.driving_torque, Torque)


@mark.dc_motor
class TestDCMotorComputeElectricalCurrent:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia_moment = inertia_moments(),
           no_load_speed = angular_speeds(),
           maximum_torque = torques(),
           no_load_electrical_current = currents(),
           maximum_electrical_current = currents(),
           driving_torque = torques())
    @settings(max_examples = 100)
    def test_method(self, name, inertia_moment, no_load_speed, maximum_torque, no_load_electrical_current, maximum_electrical_current, driving_torque):
        if no_load_speed.value > 1e-10 and maximum_torque.value > 1e-10 \
                and no_load_electrical_current.value > 1e-10 and maximum_electrical_current.value > 1e-10:
            motor = DCMotor(name = name, inertia_moment = inertia_moment, no_load_speed = no_load_speed,
                            maximum_torque = maximum_torque, no_load_electrical_current =  no_load_electrical_current,
                            maximum_electrical_current = maximum_electrical_current)
            motor.driving_torque = driving_torque
            motor.compute_electrical_current()

            assert isinstance(motor.electrical_current, Current)


@mark.dc_motor
class TestDCMotorElectricalCurrent:

    @mark.genuine
    def test_property(self):
        electrical_current = Current(1, 'A')
        basic_dc_motor_1.electrical_current = electrical_current

        assert basic_dc_motor_1.electrical_current == electrical_current

    @mark.error
    def test_raises_type_error(self, dc_motor_electrical_current_type_error):
        with raises(TypeError):
            basic_dc_motor_1.electrical_current = dc_motor_electrical_current_type_error


@mark.dc_motor
class TestDCMotorComputeElectricalCurrent:

    @mark.genuine
    def test_method(self):
        basic_dc_motor_2.driving_torque = basic_dc_motor_2.maximum_torque/2
        basic_dc_motor_2.compute_electrical_current()

        assert basic_dc_motor_2.electrical_current is not None
        assert isinstance(basic_dc_motor_2.electrical_current, Current)


@mark.dc_motor
class TestDCMotorElectricalCurrentIsComputable:

    @mark.genuine
    def test_property(self):
        for motor in [basic_dc_motor_1, basic_dc_motor_2]:
            if (motor.no_load_electrical_current is None) or (motor.maximum_electrical_current is None):
                assert not motor.electrical_current_is_computable
            else:
                assert motor.electrical_current_is_computable
