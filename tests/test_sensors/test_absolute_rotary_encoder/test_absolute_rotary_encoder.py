from gearpy.mechanical_objects import SpurGear
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.units import AngularPosition, InertiaMoment
from hypothesis import given, settings
from hypothesis.strategies import sampled_from, one_of, none
from pytest import mark, raises
from tests.conftest import rotating_objects, basic_encoder
from tests.test_units.test_angular_position.conftest import angular_positions


units_list = list(AngularPosition._AngularPosition__UNITS.keys())


@mark.sensors
class TestAbsoluteRotaryEncoderInit:


    @mark.genuine
    @given(rotating_object = rotating_objects())
    @settings(max_examples = 100)
    def test_method(self, rotating_object):
        encoder = AbsoluteRotaryEncoder(target = rotating_object)

        assert isinstance(encoder, AbsoluteRotaryEncoder)


    @mark.error
    def test_raises_type_error(self, absolute_rotary_encoder_init_type_error):
        with raises(TypeError):
            AbsoluteRotaryEncoder(*absolute_rotary_encoder_init_type_error)


@mark.sensors
class TestAbsoluteRotaryEncoderTarget:


    @mark.genuine
    @given(rotating_object = rotating_objects())
    @settings(max_examples = 100)
    def test_property(self, rotating_object):
        encoder = AbsoluteRotaryEncoder(target = rotating_object)

        assert encoder.target == rotating_object


@mark.sensors
class TestAbsoluteRotaryEncoderGetValue:


    @mark.genuine
    @given(angular_position = angular_positions(),
           unit = one_of(sampled_from(elements = units_list),
                         none()))
    @settings(max_examples = 100)
    def test_method(self, angular_position, unit):
        gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
        gear.angular_position = angular_position
        encoder = AbsoluteRotaryEncoder(target = gear)
        measured_angular_position = encoder.get_value(unit = unit)

        if unit is None:
            assert isinstance(measured_angular_position, AngularPosition)
            assert measured_angular_position == angular_position
        else:
            assert isinstance(measured_angular_position, float) or isinstance(measured_angular_position, int)
            assert measured_angular_position == angular_position.to(unit).value


    @mark.error
    def test_raises_type_error(self, absolute_rotary_encoder_get_value_type_error):
        with raises(TypeError):
            basic_encoder.get_value(*absolute_rotary_encoder_get_value_type_error)
