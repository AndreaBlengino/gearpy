from gearpy import SpurGear, add_gear_mating, add_fixed_joint
from hypothesis import given, settings
from hypothesis.strategies import floats
from pytest import mark, raises
from tests.conftest import spur_gears


@mark.utils
class TestAddGearMating:


    @mark.genuine
    @given(gear_1 = spur_gears(),
           gear_2 = spur_gears(),
           efficiency = floats(allow_nan = False, allow_infinity = False,
                               min_value = 0, exclude_min = False, max_value = 1, exclude_max = False))
    @settings(max_examples = 100)
    def test_function(self, gear_1, gear_2, efficiency):
        add_gear_mating(master = gear_1, slave = gear_2, efficiency = efficiency)

        assert gear_1.drives == gear_2
        assert gear_2.driven_by == gear_1
        assert gear_2.master_gear_ratio == gear_2.n_teeth/gear_1.n_teeth
        assert gear_2.master_gear_efficiency == efficiency


    @mark.error
    def test_raises_type_error(self, add_gear_mating_type_error):
        with raises(TypeError):
            add_gear_mating(master = add_gear_mating_type_error['gear 1'],
                            slave = add_gear_mating_type_error['gear 2'],
                            efficiency = add_gear_mating_type_error['efficiency'])


    @mark.error
    def test_raises_value_error(self, add_gear_mating_value_error):
        gear_1 = SpurGear(name = 'gear 1', n_teeth = 10, inertia = 1)
        gear_2 = SpurGear(name = 'gear 2', n_teeth = 20, inertia = 1)
        with raises(ValueError):
            add_gear_mating(master = gear_1, slave = gear_2, efficiency = add_gear_mating_value_error)


@mark.utils
class TestAddFixedJoint:


    @mark.genuine
    @given(gear_1 = spur_gears(), gear_2 = spur_gears())
    @settings(max_examples = 100)
    def test_function(self, gear_1, gear_2):
        add_fixed_joint(master = gear_1, slave = gear_2)

        assert gear_1.drives == gear_2
        assert gear_2.driven_by == gear_1
        assert gear_2.master_gear_ratio == 1.0


    @mark.error
    def test_raises_type_error(self, add_fixed_joint_type_error):
        with raises(TypeError):
            add_fixed_joint(master = add_fixed_joint_type_error['master'],
                            slave = add_fixed_joint_type_error['slave'])
