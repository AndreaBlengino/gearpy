from gearpy.mechanical_objects import DCMotor
from gearpy.sensors import Amperometer
from gearpy.units import AngularSpeed, Current, InertiaMoment, Torque
from hypothesis import given, settings
from hypothesis.strategies import sampled_from, one_of, none
from pytest import mark, raises
from tests.conftest import dc_motors, basic_amperometer
from tests.test_units.test_current.conftest import currents


units_list = list(Current._Current__UNITS.keys())


@mark.sensors
class TestAmperometerInit:


    @mark.genuine
    @given(motor = dc_motors(current = True))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, motor):
        amperometer = Amperometer(target = motor)

        assert isinstance(amperometer, Amperometer)
        assert amperometer.target == motor


    @mark.error
    def test_raises_type_error(self, amperometer_init_type_error):
        with raises(TypeError):
            Amperometer(*amperometer_init_type_error)

    @mark.error
    def test_raises_value_error(self):
        motor = DCMotor(name = 'gear', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(10, 'Nm'))
        with raises(ValueError):
            Amperometer(target = motor)


@mark.sensors
class TestAmperometerGetValue:


    @mark.genuine
    @given(electric_current = currents(),
           unit = one_of(sampled_from(elements = units_list),
                         none()))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, electric_current, unit):
        motor = DCMotor(name = 'gear', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(10, 'Nm'),
                        no_load_electric_current = Current(0, 'A'), maximum_electric_current = Current(1, 'A'))
        motor.electric_current = electric_current
        amperometer = Amperometer(target = motor)
        measured_electric_current = amperometer.get_value(unit = unit)

        if unit is None:
            assert isinstance(measured_electric_current, Current)
            assert measured_electric_current == electric_current
        else:
            assert isinstance(measured_electric_current, float) or isinstance(measured_electric_current, int)
            assert measured_electric_current == electric_current.to(unit).value


    @mark.error
    def test_raises_type_error(self, amperometer_get_value_type_error):
        with raises(TypeError):
            basic_amperometer.get_value(*amperometer_get_value_type_error)
