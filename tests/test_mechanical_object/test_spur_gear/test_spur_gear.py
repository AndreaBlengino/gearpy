from gearpy.mechanical_object import DCMotor, SpurGear
from gearpy.units import AngularSpeed, Force, InertiaMoment, Length, Torque
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers, functions
from pytest import mark, raises
from tests.conftest import basic_spur_gear
from tests.test_units.test_inertia_moment.conftest import inertia_moments


@mark.spur_gear
class TestSpurGearInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           n_teeth = integers(min_value = 1),
           module_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 10),
           inertia_moment = inertia_moments())
    @settings(max_examples = 100)
    def test_method(self, name, n_teeth, module_value, inertia_moment):
        module = Length(module_value, 'mm')
        gear = SpurGear(name = name, n_teeth = n_teeth, module = module, inertia_moment = inertia_moment)

        assert gear.name == name
        assert gear.n_teeth == n_teeth
        assert gear.module == module
        assert gear.inertia_moment == inertia_moment
        assert gear.reference_diameter == n_teeth*module


    @mark.error
    def test_raises_type_error(self, spur_gear_init_type_error):
        with raises(TypeError):
            SpurGear(**spur_gear_init_type_error)


    @mark.error
    def test_raises_value_error(self, spur_gear_init_value_error):
        with raises(ValueError):
            SpurGear(**spur_gear_init_value_error)


@mark.spur_gear
class TestSpurGearDrivenBy:


    @mark.genuine
    def test_property(self):
        motor = DCMotor(name = 'motor', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
        gear = SpurGear(name = 'gear', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))

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
        gear = SpurGear(name = 'gear', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        basic_spur_gear.drives = gear

        assert basic_spur_gear.drives == gear


    @mark.error
    def test_raises_type_error(self, spur_gear_drives_type_error):
        with raises(TypeError):
            basic_spur_gear.drives = spur_gear_drives_type_error


@mark.spur_gear
class TestSpurGearTangentialForce:


    @mark.genuine
    def test_property(self):
        tangential_force = Force(1, 'N')
        basic_spur_gear.tangential_force = tangential_force

        assert basic_spur_gear.tangential_force == tangential_force


    @mark.error
    def test_raises_type_error(self, spur_gear_tangential_force_type_error):
        with raises(TypeError):
            basic_spur_gear.tangential_force = spur_gear_tangential_force_type_error


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
