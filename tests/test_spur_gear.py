from gearpy import SpurGear
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers
from pytest import mark, raises


@mark.spur_gear
class TestSpurGearInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           n_teeth = integers(min_value = 1),
           inertia = floats(min_value = 0, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, name, n_teeth, inertia):
        gear = SpurGear(name = name, n_teeth = n_teeth, inertia = inertia)

        assert name == gear.name
        assert n_teeth == gear.n_teeth
        assert inertia == gear.inertia


    @mark.error
    def test_raises_type_error(self, spur_gear_init_type_error):
        with raises(TypeError):
            SpurGear(name = spur_gear_init_type_error['name'],
                     n_teeth = spur_gear_init_type_error['n_teeth'],
                     inertia = spur_gear_init_type_error['inertia'])


    @mark.error
    def test_raises_value_error(self, spur_gear_init_value_error):
        with raises(ValueError):
            SpurGear(name = spur_gear_init_value_error['name'],
                     n_teeth = spur_gear_init_value_error['n_teeth'],
                     inertia = spur_gear_init_value_error['inertia'])
