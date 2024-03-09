from gearpy.mechanical_objects import DCMotor, WormGear, WormWheel, MatingMaster, MatingSlave
from gearpy.units import AngularSpeed, Force, InertiaMoment, Length, Torque, Angle
from gearpy.utils import add_worm_gear_mating
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers, functions, sampled_from
from pytest import mark, raises
from tests.conftest import basic_worm_gear_1, basic_worm_gear_2, basic_flywheel
from tests.test_units.test_inertia_moment.conftest import inertia_moments
from tests.test_units.test_torque.conftest import torques
from gearpy.mechanical_objects.mechanical_object_base import WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES


@mark.worm_gear
class TestWormGearInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           n_starts = integers(min_value = 10, max_value = 1000),
           inertia_moment = inertia_moments(),
           pressure_angle = sampled_from(elements = WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES),
           helix_angle_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 15),
           reference_diameter_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 10))
    @settings(max_examples = 100)
    def test_method(self, name, n_starts, inertia_moment, pressure_angle, helix_angle_value, reference_diameter_value):
        helix_angle = Angle(helix_angle_value, 'deg')
        reference_diameter = Length(reference_diameter_value, 'mm')
        gear = WormGear(name = name, n_starts = n_starts, inertia_moment = inertia_moment,
                        pressure_angle = pressure_angle, helix_angle = helix_angle, reference_diameter = reference_diameter)

        assert gear.name == name
        assert gear.n_starts == n_starts
        assert gear.inertia_moment == inertia_moment
        assert gear.pressure_angle == pressure_angle
        assert gear.helix_angle == helix_angle
        assert gear.reference_diameter == reference_diameter


    @mark.error
    def test_raises_type_error(self, worm_gear_init_type_error):
        with raises(TypeError):
            WormGear(**worm_gear_init_type_error)


    @mark.error
    def test_raises_value_error(self, worm_gear_init_value_error):
        with raises(ValueError):
            WormGear(**worm_gear_init_value_error)


@mark.worm_gear
class TestWormGearSelfLocking:


    @mark.genuine
    def test_property(self):
        for self_locking in [True, False]:
            basic_worm_gear_1.self_locking = self_locking

            assert basic_worm_gear_1.self_locking == self_locking


    @mark.error
    def test_raises_type_error(self, worm_gear_self_locking_type_error):
        with raises(TypeError):
            basic_worm_gear_1.self_locking = worm_gear_self_locking_type_error


@mark.worm_gear
class TestWormGearDrivenBy:


    @mark.genuine
    def test_property(self):
        motor = DCMotor(name = 'motor', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
        worm_gear = WormGear(name = 'gear', n_starts = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                             pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'))

        for master in [motor, worm_gear]:
            basic_worm_gear_1.driven_by = master

            assert basic_worm_gear_1.driven_by == master


    @mark.error
    def test_raises_type_error(self, worm_gear_driven_by_type_error):
        with raises(TypeError):
            basic_worm_gear_1.driven_by = worm_gear_driven_by_type_error


@mark.worm_gear
class TestWormGearDrives:


    @mark.genuine
    def test_property(self):
        worm_gear = WormGear(name = 'gear', n_starts = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                             pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'))
        worm_gear.drives = basic_flywheel

        assert worm_gear.drives == basic_flywheel


    @mark.error
    def test_raises_type_error(self, worm_gear_drives_type_error):
        with raises(TypeError):
            basic_worm_gear_1.drives = worm_gear_drives_type_error


@mark.worm_gear
class TestWormGearMasterGearRatio:


    @mark.genuine
    @given(master_gear_ratio = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = True))
    @settings(max_examples = 100)
    def test_property(self, master_gear_ratio):
        basic_worm_gear_1.master_gear_ratio = master_gear_ratio

        assert basic_worm_gear_1.master_gear_ratio == master_gear_ratio


    @mark.error
    def test_raises_type_error(self, worm_gear_master_gear_ratio_type_error):
        with raises(TypeError):
            basic_worm_gear_1.master_gear_ratio = worm_gear_master_gear_ratio_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            basic_worm_gear_1.master_gear_ratio = -1.0


@mark.worm_gear
class TestWormGearMasterGearEfficiency:


    @mark.genuine
    @given(master_gear_efficiency = floats(allow_nan = False, allow_infinity = False,
                                           min_value = 0, exclude_min = False, max_value = 1, exclude_max = False))
    @settings(max_examples = 100)
    def test_property(self, master_gear_efficiency):
        basic_worm_gear_1.master_gear_efficiency = master_gear_efficiency

        assert basic_worm_gear_1.master_gear_efficiency == master_gear_efficiency


    @mark.error
    def test_raises_type_error(self, worm_gear_master_gear_efficiency_type_error):
        with raises(TypeError):
            basic_worm_gear_1.master_gear_efficiency = worm_gear_master_gear_efficiency_type_error


    @mark.error
    def test_raises_value_error(self, worm_gear_master_gear_efficiency_value_error):
        with raises(ValueError):
            basic_worm_gear_1.master_gear_efficiency = worm_gear_master_gear_efficiency_value_error


@mark.worm_gear
class TestWormGearMatingRole:


    @mark.genuine
    def test_property(self):
        worm_gear = WormGear(name = 'worm gear', n_starts = 1, inertia_moment = InertiaMoment(1, 'gm^2'),
                             pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'))
        worm_wheel = WormWheel(name = 'worm wheel', n_teeth = 10, inertia_moment = InertiaMoment(1, 'gm^2'),
                               pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'))

        for master, slave in zip([worm_gear, worm_wheel], [worm_wheel, worm_gear]):
            add_worm_gear_mating(master = master, slave = slave, friction_coefficient = 0)

            assert master.mating_role == MatingMaster
            assert slave.mating_role == MatingSlave


    @mark.error
    def test_raises_type_error(self, worm_gear_mating_role_type_error):
        with raises(TypeError):
            basic_worm_gear_1.mating_role = worm_gear_mating_role_type_error


@mark.worm_gear
class TestWormGearTangentialForce:


    @mark.genuine
    def test_property(self):
        tangential_force = Force(1, 'N')
        basic_worm_gear_1.tangential_force = tangential_force

        assert basic_worm_gear_1.tangential_force == tangential_force


    @mark.error
    def test_raises_type_error(self, worm_gear_tangential_force_type_error):
        with raises(TypeError):
            basic_worm_gear_1.tangential_force = worm_gear_tangential_force_type_error


@mark.worm_gear
class TestWormGearComputeTangentialForce:


    @mark.genuine
    def test_method(self):
        worm_gear = WormGear(name = 'worm gear', n_starts = 1, inertia_moment = InertiaMoment(1, 'gm^2'),
                             pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'),
                             reference_diameter = Length(10, 'mm'))
        worm_wheel = WormWheel(name = 'worm wheel', n_teeth = 10, inertia_moment = InertiaMoment(1, 'gm^2'),
                               pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'),
                               module = Length(1, 'mm'))

        for master, slave in zip([worm_gear, worm_wheel], [worm_wheel, worm_gear]):
            add_worm_gear_mating(master = master, slave = slave, friction_coefficient = 0)

            master.driving_torque = Torque(1, 'Nm')
            slave.driving_torque = Torque(1, 'Nm')
            master.load_torque = Torque(1, 'Nm')
            slave.load_torque= Torque(1, 'Nm')
            master.compute_tangential_force()
            slave.compute_tangential_force()

            assert master.tangential_force is not None
            assert slave.tangential_force is not None
            assert isinstance(master.tangential_force, Force)
            assert isinstance(slave.tangential_force, Force)


    @mark.error
    def test_raises_value_error(self):
        gear = WormGear(name = 'gear 1', n_starts = 1, inertia_moment = InertiaMoment(1, 'kgm^2'),
                        pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'),
                        reference_diameter = Length(10, 'mm'))
        with raises(ValueError):
            gear.compute_tangential_force()


@mark.worm_gear
class TestWormGearTangentialForceIsComputable:


    @mark.genuine
    def test_property(self):
        for gear in [basic_worm_gear_1, basic_worm_gear_2]:
            if gear.reference_diameter is None:
                assert not gear.tangential_force_is_computable
            else:
                assert gear.tangential_force_is_computable


@mark.worm_gear
class TestWormGearExternalTorque:


    @mark.genuine
    @given(external_torque = functions(like = lambda angular_position, angular_speed, time: Torque(1, 'Nm'),
                                       returns = torques()))
    @settings(max_examples = 100)
    def test_property(self, external_torque):
        basic_worm_gear_1.external_torque = external_torque

        assert basic_worm_gear_1.external_torque == external_torque


    @mark.error
    def test_raises_type_error(self, worm_gear_external_torque_type_error):
        with raises(TypeError):
            basic_worm_gear_1.external_torque = worm_gear_external_torque_type_error


    @mark.error
    def test_raises_key_error(self, worm_gear_external_torque_key_error):
        with raises(KeyError):
            basic_worm_gear_1.external_torque = worm_gear_external_torque_key_error
