from gearpy import DCMotor, SpurGear
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers, functions
from pytest import mark, raises
from tests.conftest import basic_spur_gear


@mark.spur_gear
class TestSpurGearInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           n_teeth = integers(min_value = 1),
           inertia = floats(min_value = 0, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, name, n_teeth, inertia):
        gear = SpurGear(name = name, n_teeth = n_teeth, inertia = inertia)

        assert gear.name == name
        assert gear.n_teeth == n_teeth
        assert gear.inertia == inertia


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


@mark.spur_gear
class TestSpurGearDrivenBy:


    @mark.genuine
    def test_property(self):
        motor = DCMotor(name = 'motor', inertia = 1, no_load_speed = 1, maximum_torque = 1)
        gear = SpurGear(name = 'gear', n_teeth = 10, inertia = 1)

        for master in [motor, gear]:
            basic_spur_gear.driven_by = master

            assert basic_spur_gear.driven_by == master


    @mark.error
    def test_raises_type_error(self, spur_gear_driven_by_type_error):
        with raises(TypeError):
            basic_spur_gear.driven_by = spur_gear_driven_by_type_error


@mark.spur_gear
class TestSpurGearDrives:


    @mark.genuine
    def test_property(self):
        gear = SpurGear(name = 'gear', n_teeth = 10, inertia = 1)
        basic_spur_gear.drives = gear

        assert basic_spur_gear.drives == gear


    @mark.error
    def test_raises_type_error(self, spur_gear_drives_type_error):
        with raises(TypeError):
            basic_spur_gear.drives = spur_gear_drives_type_error


@mark.spur_gear
class TestSpurGearMasterGearRatio:


    @mark.genuine
    @given(master_gear_ratio = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = True))
    @settings(max_examples = 100)
    def test_property(self, master_gear_ratio):
        basic_spur_gear.master_gear_ratio = master_gear_ratio

        assert basic_spur_gear.master_gear_ratio == master_gear_ratio


    @mark.error
    def test_raises_type_error(self, spur_gear_master_gear_ratio_type_error):
        with raises(TypeError):
            basic_spur_gear.master_gear_ratio = spur_gear_master_gear_ratio_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            basic_spur_gear.master_gear_ratio = -1.0


@mark.spur_gear
class TestSpurGearMasterGearEfficiency:

    @mark.genuine
    @given(master_gear_efficiency = floats(allow_nan = False, allow_infinity = False,
                                           min_value = 0, exclude_min = False, max_value = 1, exclude_max = False))
    @settings(max_examples = 100)
    def test_property(self, master_gear_efficiency):
        basic_spur_gear.master_gear_efficiency = master_gear_efficiency

        assert basic_spur_gear.master_gear_efficiency == master_gear_efficiency

    @mark.error
    def test_raises_type_error(self, spur_gear_master_gear_efficiency_type_error):
        with raises(TypeError):
            basic_spur_gear.master_gear_efficiency = spur_gear_master_gear_efficiency_type_error


    @mark.error
    def test_raises_value_error(self, spur_gear_master_gear_efficiency_value_error):
        with raises(ValueError):
            basic_spur_gear.master_gear_efficiency = spur_gear_master_gear_efficiency_value_error


@mark.spur_gear
class TestSpurGearExternalTorque:

    @mark.genuine
    @given(external_torque = functions())
    @settings(max_examples = 100)
    def test_property(self, external_torque):
        basic_spur_gear.external_torque = external_torque

        assert basic_spur_gear.external_torque == external_torque

    @mark.error
    def test_raises_type_error(self, spur_gear_external_torque_type_error):
        with raises(TypeError):
            basic_spur_gear.external_torque = spur_gear_external_torque_type_error
