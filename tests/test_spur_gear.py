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


@mark.spur_gear
class TestSpurGearDrivenBy:


    @mark.genuine
    def test_property(self):
        motor = DCMotor(name = 'motor', inertia = 1, no_load_speed = 1, maximum_torque = 1)
        gear = SpurGear(name = 'gear', n_teeth = 10, inertia = 1)

        for master in [motor, gear]:
            basic_spur_gear.driven_by = master

            assert master == basic_spur_gear.driven_by


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

        assert gear == basic_spur_gear.drives


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

        assert master_gear_ratio == basic_spur_gear.master_gear_ratio


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

        assert master_gear_efficiency == basic_spur_gear.master_gear_efficiency

    @mark.error
    def test_raises_type_error(self, spur_gear_master_gear_efficiency_type_error):
        with raises(TypeError):
            basic_spur_gear.master_gear_efficiency = spur_gear_master_gear_efficiency_type_error


    @mark.error
    def test_raises_value_error(self, spur_gear_master_gear_efficiency_value_error):
        with raises(ValueError):
            basic_spur_gear.master_gear_efficiency = spur_gear_master_gear_efficiency_value_error


@mark.spur_gear
class TestSpurGearAngle:


    @mark.genuine
    @given(angle = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, angle):
        basic_spur_gear.angle = angle

        assert angle == basic_spur_gear.angle


    @mark.error
    def test_raises_type_error(self, spur_gear_angle_type_error):
        with raises(TypeError):
            basic_spur_gear.angle = spur_gear_angle_type_error


@mark.spur_gear
class TestSpurGearSpeed:


    @mark.genuine
    @given(speed = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, speed):
        basic_spur_gear.speed = speed

        assert speed == basic_spur_gear.speed


    @mark.error
    def test_raises_type_error(self, spur_gear_speed_type_error):
        with raises(TypeError):
            basic_spur_gear.speed = spur_gear_speed_type_error


@mark.spur_gear
class TestSpurGearAcceleration:


    @mark.genuine
    @given(acceleration = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, acceleration):
        basic_spur_gear.acceleration = acceleration

        assert acceleration == basic_spur_gear.acceleration


    @mark.error
    def test_raises_type_error(self, spur_gear_acceleration_type_error):
        with raises(TypeError):
            basic_spur_gear.acceleration = spur_gear_acceleration_type_error


@mark.spur_gear
class TestSpurGearTorque:


    @mark.genuine
    @given(torque = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, torque):
        basic_spur_gear.torque = torque

        assert torque == basic_spur_gear.torque


    @mark.error
    def test_raises_type_error(self, spur_gear_torque_type_error):
        with raises(TypeError):
            basic_spur_gear.torque = spur_gear_torque_type_error


@mark.spur_gear
class TestSpurGearDrivingTorque:


    @mark.genuine
    @given(driving_torque = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, driving_torque):
        basic_spur_gear.driving_torque = driving_torque

        assert driving_torque == basic_spur_gear.driving_torque


    @mark.error
    def test_raises_type_error(self, spur_gear_driving_torque_type_error):
        with raises(TypeError):
            basic_spur_gear.driving_torque = spur_gear_driving_torque_type_error


@mark.spur_gear
class TestSpurGearLoadTorque:


    @mark.genuine
    @given(load_torque = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100)
    def test_property(self, load_torque):
        basic_spur_gear.load_torque = load_torque

        assert load_torque == basic_spur_gear.load_torque


    @mark.error
    def test_raises_type_error(self, spur_gear_load_torque_type_error):
        with raises(TypeError):
            basic_spur_gear.load_torque = spur_gear_load_torque_type_error


@mark.spur_gear
class TestSpurGearExternalTorque:

    @mark.genuine
    @given(external_torque = functions())
    @settings(max_examples = 100)
    def test_property(self, external_torque):
        basic_spur_gear.external_torque = external_torque

        assert external_torque == basic_spur_gear.external_torque

    @mark.error
    def test_raises_type_error(self, spur_gear_external_torque_type_error):
        with raises(TypeError):
            basic_spur_gear.external_torque = spur_gear_external_torque_type_error


@mark.spur_gear
class TestSpurGearTimeVariables:


    @mark.genuine
    def test_property(self):
        time_variables = basic_spur_gear.time_variables

        assert isinstance(time_variables, dict)
        assert ['angle', 'speed', 'acceleration', 'torque', 'driving torque', 'load torque'] == list(time_variables.keys())
        assert all([value == [] for value in time_variables.values()])


@mark.spur_gear
class TestSpurGearUpdateTimeVariables:


    @mark.genuine
    @given(angle = floats(allow_nan = False, allow_infinity = False),
           speed = floats(allow_nan = False, allow_infinity = False),
           acceleration = floats(allow_nan = False, allow_infinity = False),
           torque = floats(allow_nan = False, allow_infinity = False),
           driving_torque = floats(allow_nan = False, allow_infinity = False),
           load_torque = floats(allow_nan = False, allow_infinity = False))
    def test_method(self, angle, speed, acceleration, torque, driving_torque, load_torque):
        gear = SpurGear(name = 'name', n_teeth = 10, inertia = 1)
        gear.angle = angle
        gear.speed = speed
        gear.acceleration = acceleration
        gear.torque = torque
        gear.driving_torque = driving_torque
        gear.load_torque = load_torque

        gear.update_time_variables()
        time_variables = gear.time_variables

        assert isinstance(time_variables, dict)
        assert ['angle', 'speed', 'acceleration', 'torque', 'driving torque', 'load torque'] == list(time_variables.keys())
        assert time_variables['angle'][-1] == angle
        assert time_variables['speed'][-1] == speed
        assert time_variables['acceleration'][-1] == acceleration
        assert time_variables['torque'][-1] == torque
        assert time_variables['driving torque'][-1] == driving_torque
        assert time_variables['load torque'][-1] == load_torque
