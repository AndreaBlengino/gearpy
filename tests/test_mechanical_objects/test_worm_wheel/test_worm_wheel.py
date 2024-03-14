from gearpy.mechanical_objects import WormGear, WormWheel, MatingMaster, MatingSlave
from gearpy.units import Angle, Force, InertiaMoment, Length, Stress, Torque
from gearpy.utils import add_worm_gear_mating
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers, functions, sampled_from
from pytest import mark, raises
from tests.conftest import basic_worm_gear_1, basic_worm_gear_2, basic_worm_wheel_1, basic_worm_wheel_2
from tests.test_units.test_inertia_moment.conftest import inertia_moments
from tests.test_units.test_torque.conftest import torques
from gearpy.mechanical_objects.mechanical_object_base import WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES


@mark.worm_wheel
class TestWormWheelInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           n_teeth = integers(min_value = 10, max_value = 1000),
           inertia_moment = inertia_moments(),
           pressure_angle = sampled_from(elements = WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES),
           helix_angle_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 15),
           module_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 10),
           face_width_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 100))
    @settings(max_examples = 100)
    def test_method(self, name, n_teeth, inertia_moment, pressure_angle, helix_angle_value, module_value, face_width_value):
        helix_angle = Angle(helix_angle_value, 'deg')
        module = Length(module_value, 'mm')
        face_width = Length(face_width_value, 'mm')
        gear = WormWheel(name = name, n_teeth = n_teeth, inertia_moment = inertia_moment,
                         pressure_angle = pressure_angle, helix_angle = helix_angle, module = module, face_width = face_width)

        assert gear.name == name
        assert gear.n_teeth == n_teeth
        assert gear.inertia_moment == inertia_moment
        assert gear.pressure_angle == pressure_angle
        assert gear.helix_angle == helix_angle
        assert gear.module == module
        assert gear.face_width == face_width
        assert gear.reference_diameter == n_teeth*module


    @mark.error
    def test_raises_type_error(self, worm_wheel_init_type_error):
        with raises(TypeError):
            WormWheel(**worm_wheel_init_type_error)


    @mark.error
    def test_raises_value_error(self, worm_wheel_init_value_error):
        with raises(ValueError):
            WormWheel(**worm_wheel_init_value_error)


@mark.worm_wheel
class TestWormWheelMatingRole:


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
    def test_raises_type_error(self, worm_wheel_mating_role_type_error):
        with raises(TypeError):
            basic_worm_wheel_1.mating_role = worm_wheel_mating_role_type_error


@mark.worm_wheel
class TestWormWheelTangentialForce:


    @mark.genuine
    def test_property(self):
        tangential_force = Force(1, 'N')
        basic_worm_wheel_1.tangential_force = tangential_force

        assert basic_worm_wheel_1.tangential_force == tangential_force


    @mark.error
    def test_raises_type_error(self, worm_wheel_tangential_force_type_error):
        with raises(TypeError):
            basic_worm_wheel_1.tangential_force = worm_wheel_tangential_force_type_error


@mark.worm_wheel
class TestWormWheelComputeTangentialForce:


    @mark.genuine
    def test_method(self):
        worm_gear = WormGear(name = 'worm gear', n_starts = 1, inertia_moment = InertiaMoment(1, 'gm^2'),
                             pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'),
                             reference_diameter = Length(10, 'mm'))
        worm_wheel = WormWheel(name = 'worm wheel', n_teeth = 10, inertia_moment = InertiaMoment(1, 'gm^2'),
                               pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'),
                               module = Length(1, 'mm'), face_width = Length(10, 'mm'))

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
        wheel = WormWheel(name = 'wheel', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                          pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'),
                          module = Length(1, 'mm'))
        with raises(ValueError):
            wheel.compute_tangential_force()


@mark.worm_wheel
class TestWormWheelTangentialForceIsComputable:


    @mark.genuine
    def test_property(self):
        for gear in [basic_worm_wheel_1, basic_worm_wheel_2]:
            if gear.module is None:
                assert not gear.tangential_force_is_computable
            else:
                assert gear.tangential_force_is_computable


@mark.worm_wheel
class TestWormWheelBendingStress:

    @mark.genuine
    def test_property(self):
        bending_stress = Stress(1, 'MPa')
        basic_worm_wheel_1.bending_stress = bending_stress

        assert basic_worm_wheel_1.bending_stress == bending_stress

    @mark.error
    def test_raises_type_error(self, worm_wheel_bending_stress_type_error):
        with raises(TypeError):
            basic_worm_wheel_1.bending_stress = worm_wheel_bending_stress_type_error


@mark.worm_wheel
class TestWormWheelComputeBendingStress:

    @mark.genuine
    def test_method(self):
        worm_gear = WormGear(name = 'worm gear', n_starts = 1, inertia_moment = InertiaMoment(1, 'gm^2'),
                             pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'),
                             reference_diameter = Length(10, 'mm'))
        worm_wheel = WormWheel(name = 'worm wheel', n_teeth = 10, inertia_moment = InertiaMoment(1, 'gm^2'),
                               pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'),
                               module = Length(1, 'mm'), face_width = Length(10, 'mm'))

        for master, slave in zip([worm_gear, worm_wheel], [worm_wheel, worm_gear]):
            add_worm_gear_mating(master = master, slave = slave, friction_coefficient = 0)
            master.driving_torque = Torque(1, 'Nm')
            slave.driving_torque = Torque(1, 'Nm')
            master.load_torque = Torque(1, 'Nm')
            slave.load_torque= Torque(1, 'Nm')
            master.compute_tangential_force()
            slave.compute_tangential_force()
            if not isinstance(master, WormGear):
                master.compute_bending_stress()
            if not isinstance(slave, WormGear):
                slave.compute_bending_stress()

            assert worm_wheel.bending_stress is not None
            assert isinstance(worm_wheel.bending_stress, Stress)


    @mark.error
    def test_raises_value_error(self):
        wheel = WormWheel(name = 'wheel', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                          pressure_angle = Angle(20, 'deg'), helix_angle = Angle(10, 'deg'),
                          module = Length(1, 'mm'))
        with raises(ValueError):
            wheel.compute_bending_stress()


@mark.worm_wheel
class TestWormWheelBendingStressIsComputable:

    @mark.genuine
    def test_property(self):
        masters = [basic_worm_gear_1, basic_worm_gear_2, basic_worm_wheel_1, basic_worm_wheel_2]
        slaves = [basic_worm_wheel_1, basic_worm_wheel_2, basic_worm_gear_1, basic_worm_gear_2]

        for master, slave in zip(masters, slaves):
            add_worm_gear_mating(master = master, slave = slave, friction_coefficient = 0)
            if isinstance(master, WormGear):
                worm_gear = master
                worm_wheel = slave
            else:
                worm_gear = slave
                worm_wheel = master
            if (worm_wheel.module is None) or (worm_wheel.face_width is None) or (worm_gear.reference_diameter is None):
                assert not worm_wheel.bending_stress_is_computable
            else:
                assert worm_wheel.bending_stress_is_computable


@mark.worm_wheel
class TestWormWheelExternalTorque:


    @mark.genuine
    @given(external_torque = functions(like = lambda angular_position, angular_speed, time: Torque(1, 'Nm'),
                                       returns = torques()))
    @settings(max_examples = 100)
    def test_property(self, external_torque):
        basic_worm_wheel_1.external_torque = external_torque

        assert basic_worm_wheel_1.external_torque == external_torque


    @mark.error
    def test_raises_type_error(self, worm_wheel_external_torque_type_error):
        with raises(TypeError):
            basic_worm_wheel_1.external_torque = worm_wheel_external_torque_type_error


    @mark.error
    def test_raises_key_error(self, worm_wheel_external_torque_key_error):
        with raises(KeyError):
            basic_worm_wheel_1.external_torque = worm_wheel_external_torque_key_error
