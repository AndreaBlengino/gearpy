from gearpy.mechanical_objects import SpurGear
from gearpy.sensors import Tachometer
from gearpy.units import AngularSpeed, InertiaMoment
from hypothesis import given, settings
from hypothesis.strategies import sampled_from, one_of, none
from pytest import mark, raises
from tests.conftest import rotating_objects, basic_tachometer
from tests.test_units.test_angular_speed.conftest import angular_speeds


units_list = list(AngularSpeed._AngularSpeed__UNITS.keys())


@mark.sensors
class TestTachometerInit:

    @mark.genuine
    @given(rotating_object=rotating_objects())
    @settings(max_examples=100, deadline=None)
    def test_method(self, rotating_object):
        tachometer = Tachometer(target=rotating_object)

        assert isinstance(tachometer, Tachometer)
        assert tachometer.target == rotating_object

    @mark.error
    def test_raises_type_error(self, tachometer_init_type_error):
        with raises(TypeError):
            Tachometer(*tachometer_init_type_error)


@mark.sensors
class TestTachometerGetValue:

    @mark.genuine
    @given(
        angular_speed=angular_speeds(),
        unit=one_of(
            sampled_from(elements=units_list),
            none()
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, angular_speed, unit):
        gear = SpurGear(
            name='gear',
            n_teeth=10,
            inertia_moment=InertiaMoment(1, 'kgm^2')
        )
        gear.angular_speed = angular_speed
        tachometer = Tachometer(target=gear)
        measured_angular_speed = tachometer.get_value(unit=unit)

        if unit is None:
            assert isinstance(measured_angular_speed, AngularSpeed)
            assert measured_angular_speed == angular_speed
        else:
            assert isinstance(measured_angular_speed, float | int)
            assert measured_angular_speed == angular_speed.to(unit).value

    @mark.error
    def test_raises_type_error(self, tachometer_get_value_type_error):
        with raises(TypeError):
            basic_tachometer.get_value(*tachometer_get_value_type_error)
