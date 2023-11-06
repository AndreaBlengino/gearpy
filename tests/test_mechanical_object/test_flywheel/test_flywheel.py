from gearpy.mechanical_object import DCMotor, SpurGear, Flywheel
from gearpy.units import AngularSpeed, InertiaMoment, Length, Torque
from hypothesis import given, settings
from hypothesis.strategies import text, floats
from pytest import mark, raises
from tests.conftest import basic_flywheel
from tests.test_units.test_inertia_moment.conftest import inertia_moments


@mark.flywheel
class TestFlywheelInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia_moment = inertia_moments())
    @settings(max_examples = 100)
    def test_method(self, name, inertia_moment):
        flywheel = Flywheel(name = name, inertia_moment = inertia_moment)

        assert flywheel.name == name
        assert flywheel.inertia_moment == inertia_moment


    @mark.error
    def test_raises_type_error(self, flywheel_init_type_error):
        with raises(TypeError):
            Flywheel(**flywheel_init_type_error)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            Flywheel(name = '', inertia_moment = InertiaMoment(1, 'kgm^2'))


@mark.flywheel
class TestFlywheelDrivenBy:


    @mark.genuine
    def test_property(self):
        motor = DCMotor(name = 'motor', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
        flywheel = Flywheel(name = 'flywheel', inertia_moment = InertiaMoment(1, 'kgm^2'))
        gear = SpurGear(name = 'gear', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))

        for master in [motor, flywheel, gear]:
            basic_flywheel.driven_by = master

            assert basic_flywheel.driven_by == master


    @mark.error
    def test_raises_type_error(self, flywheel_driven_by_type_error):
        with raises(TypeError):
            basic_flywheel.driven_by = flywheel_driven_by_type_error


@mark.flywheel
class TestFlywheelDrives:


    @mark.genuine
    def test_property(self):
        gear = SpurGear(name = 'gear', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        flywheel = Flywheel(name = 'flywheel', inertia_moment = InertiaMoment(1, 'kgm^2'))

        for slave in [gear, flywheel]:
            basic_flywheel.drives = slave

            assert basic_flywheel.drives == slave


    @mark.error
    def test_raises_type_error(self, flywheel_drives_type_error):
        with raises(TypeError):
            basic_flywheel.drives = flywheel_drives_type_error


@mark.flywheel
class TestFlywheelMasterGearRatio:


    @mark.genuine
    @given(master_gear_ratio = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = True))
    @settings(max_examples = 100)
    def test_property(self, master_gear_ratio):
        basic_flywheel.master_gear_ratio = master_gear_ratio

        assert basic_flywheel.master_gear_ratio == master_gear_ratio


    @mark.error
    def test_raises_type_error(self, flywheel_master_gear_ratio_type_error):
        with raises(TypeError):
            basic_flywheel.master_gear_ratio = flywheel_master_gear_ratio_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            basic_flywheel.master_gear_ratio = -1.0


@mark.flywheel
class TestFlywheelMasterGearEfficiency:


    @mark.genuine
    def test_property(self):
        assert basic_flywheel.master_gear_efficiency == 1
