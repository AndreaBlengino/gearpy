from gearpy.mechanical_object import SpurGear, MatingMaster, MatingSlave
from gearpy.units import InertiaMoment, Length
from gearpy.utils import add_gear_mating, add_fixed_joint
from hypothesis import given, settings
from hypothesis.strategies import floats, one_of
from pytest import mark, raises
from tests.conftest import dc_motors, simple_spur_gears, flywheels


@mark.utils
class TestAddGearMating:


    @mark.genuine
    @given(gear_1 = simple_spur_gears(),
           gear_2 = simple_spur_gears(),
           efficiency = floats(allow_nan = False, allow_infinity = False,
                               min_value = 0, exclude_min = False, max_value = 1, exclude_max = False))
    @settings(max_examples = 100)
    def test_function(self, gear_1, gear_2, efficiency):
        add_gear_mating(master = gear_1, slave = gear_2, efficiency = efficiency)

        assert gear_1.drives == gear_2
        assert gear_1.mating_role == MatingMaster
        assert gear_2.driven_by == gear_1
        assert gear_2.mating_role == MatingSlave
        assert gear_2.master_gear_ratio == gear_2.n_teeth/gear_1.n_teeth
        assert gear_2.master_gear_efficiency == efficiency


    @mark.error
    def test_raises_type_error(self, add_gear_mating_type_error):
        with raises(TypeError):
            add_gear_mating(**add_gear_mating_type_error)


    @mark.error
    def test_raises_value_error(self, add_gear_mating_value_error):
        gear_1 = SpurGear(name = 'gear 1', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        gear_2 = SpurGear(name = 'gear 2', n_teeth = 20, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        gear_3 = SpurGear(name = 'gear 3', n_teeth = 20, module = Length(2, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        if add_gear_mating_value_error < 0 or add_gear_mating_value_error > 1:
            with raises(ValueError):
                add_gear_mating(master = gear_1, slave = gear_2, efficiency = add_gear_mating_value_error)
        else:
            with raises(ValueError):
                add_gear_mating(master = gear_1, slave = gear_3, efficiency = add_gear_mating_value_error)


@mark.utils
class TestAddFixedJoint:


    @mark.genuine
    @given(master = one_of(dc_motors(), simple_spur_gears(), flywheels()),
           slave = one_of(simple_spur_gears(), flywheels()))
    @settings(max_examples = 100)
    def test_function(self, master, slave):
        add_fixed_joint(master = master, slave = slave)

        assert master.drives == slave
        assert slave.driven_by == master
        assert slave.master_gear_ratio == 1.0


    @mark.error
    def test_raises_type_error(self, add_fixed_joint_type_error):
        with raises(TypeError):
            add_fixed_joint(**add_fixed_joint_type_error)
