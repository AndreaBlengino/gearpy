from gearpy.mechanical_objects import HelicalGear, MatingMaster, MatingSlave
from gearpy.units import Angle, Force, InertiaMoment, Length, Stress, Torque
from gearpy.utils import add_gear_mating
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers, functions
from pytest import mark, raises
from tests.conftest import basic_helical_gear_1, basic_helical_gear_2
from tests.test_units.test_inertia_moment.conftest import inertia_moments
from tests.test_units.test_torque.conftest import torques
from tests.test_units.test_angle.conftest import angles


@mark.helical_gear
class TestHelicalGearInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           n_teeth = integers(min_value = 10, max_value = 1000),
           helix_angle = angles(min_value = 1e-1, max_value = 40, unit = 'deg'),
           inertia_moment = inertia_moments(),
           module_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 10),
           face_width_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 100),
           elastic_modulus_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 10))
    @settings(max_examples = 100)
    def test_method(self, name, n_teeth, helix_angle, inertia_moment, module_value, face_width_value, elastic_modulus_value):
        module = Length(module_value, 'mm')
        face_width = Length(face_width_value, 'mm')
        elastic_modulus = Stress(elastic_modulus_value, 'GPa')
        gear = HelicalGear(name = name, n_teeth = n_teeth, helix_angle = helix_angle, inertia_moment = inertia_moment,
                           module = module, face_width = face_width, elastic_modulus = elastic_modulus)

        assert gear.name == name
        assert gear.n_teeth == n_teeth
        assert gear.helix_angle == helix_angle
        assert gear.inertia_moment == inertia_moment
        assert gear.module == module
        assert gear.reference_diameter == n_teeth*module
        assert gear.face_width == face_width
        assert gear.elastic_modulus == elastic_modulus


    @mark.error
    def test_raises_type_error(self, helical_gear_init_type_error):
        with raises(TypeError):
            HelicalGear(**helical_gear_init_type_error)


    @mark.error
    def test_raises_value_error(self, helical_gear_init_value_error):
        with raises(ValueError):
            HelicalGear(**helical_gear_init_value_error)


@mark.helical_gear
class TestHelicalGearMatingRole:


    @mark.genuine
    def test_property(self):
        gear_1 = HelicalGear(name = 'gear 1', n_teeth = 10, helix_angle = Angle(30, 'deg'), inertia_moment = InertiaMoment(1, 'gm^2'))
        gear_2 = HelicalGear(name = 'gear 2', n_teeth = 10, helix_angle = Angle(30, 'deg'), inertia_moment = InertiaMoment(1, 'gm^2'))
        add_gear_mating(master = gear_1, slave = gear_2, efficiency = 1)

        assert gear_1.mating_role == MatingMaster
        assert gear_2.mating_role == MatingSlave


    @mark.error
    def test_raises_type_error(self, helical_gear_mating_role_type_error):
        with raises(TypeError):
            basic_helical_gear_1.mating_role = helical_gear_mating_role_type_error


@mark.helical_gear
class TestHelicalGearTangentialForce:


    @mark.genuine
    def test_property(self):
        tangential_force = Force(1, 'N')
        basic_helical_gear_1.tangential_force = tangential_force

        assert basic_helical_gear_1.tangential_force == tangential_force


    @mark.error
    def test_raises_type_error(self, helical_gear_tangential_force_type_error):
        with raises(TypeError):
            basic_helical_gear_1.tangential_force = helical_gear_tangential_force_type_error


@mark.helical_gear
class TestHelicalGearComputeTangentialForce:


    @mark.genuine
    def test_method(self):
        gear_1 = HelicalGear(name = 'gear 1', n_teeth = 10, helix_angle = Angle(30, 'deg'),
                             inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'))
        gear_2 = HelicalGear(name = 'gear 2', n_teeth = 20, helix_angle = Angle(30, 'deg'),
                             inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'))

        add_gear_mating(master = gear_1, slave = gear_2, efficiency = 0.9)
        gear_1.driving_torque = Torque(1, 'Nm')
        gear_2.driving_torque = Torque(1, 'Nm')
        gear_1.load_torque = Torque(1, 'Nm')
        gear_2.load_torque= Torque(1, 'Nm')
        gear_1.compute_tangential_force()
        gear_2.compute_tangential_force()

        assert gear_1.tangential_force is not None
        assert gear_2.tangential_force is not None
        assert isinstance(gear_1.tangential_force, Force)
        assert isinstance(gear_2.tangential_force, Force)


    @mark.error
    def test_raises_value_error(self):
        gear = HelicalGear(name = 'gear', n_teeth = 10, helix_angle = Angle(30, 'deg'),
                           inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'))
        with raises(ValueError):
            gear.compute_tangential_force()


@mark.helical_gear
class TestHelicalGearTangentialForceIsComputable:


    @mark.genuine
    def test_property(self):
        for gear in [basic_helical_gear_1, basic_helical_gear_2]:
            if gear.module is None:
                assert not gear.tangential_force_is_computable
            else:
                assert gear.tangential_force_is_computable


@mark.helical_gear
class TestHelicalGearBendingStress:

    @mark.genuine
    def test_property(self):
        bending_stress = Stress(1, 'MPa')
        basic_helical_gear_1.bending_stress = bending_stress

        assert basic_helical_gear_1.bending_stress == bending_stress

    @mark.error
    def test_raises_type_error(self, helical_gear_bending_stress_type_error):
        with raises(TypeError):
            basic_helical_gear_1.bending_stress = helical_gear_bending_stress_type_error


@mark.helical_gear
class TestHelicalGearComputeBendingStress:

    @mark.genuine
    def test_method(self):
        gear_1 = HelicalGear(name = 'gear 1', n_teeth = 10, helix_angle = Angle(30, 'deg'),
                             inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'),
                             face_width = Length(5, 'mm'))
        gear_2 = HelicalGear(name = 'gear 2', n_teeth = 20, helix_angle = Angle(30, 'deg'),
                             inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'),
                             face_width = Length(5, 'mm'))
        add_gear_mating(master = gear_1, slave = gear_2, efficiency = 0.9)
        gear_2.driving_torque = Torque(1, 'Nm')
        gear_2.compute_tangential_force()
        gear_2.compute_bending_stress()

        assert gear_2.bending_stress is not None
        assert isinstance(gear_2.bending_stress, Stress)


@mark.helical_gear
class TestHelicalGearBendingStressIsComputable:

    @mark.genuine
    def test_property(self):
        for gear in [basic_helical_gear_1, basic_helical_gear_2]:
            if (gear.module is None) or (gear.face_width is None):
                assert not gear.bending_stress_is_computable
            else:
                assert gear.bending_stress_is_computable


@mark.helical_gear
class TestHelicalGearContactStress:

    @mark.genuine
    def test_property(self):
        contact_stress = Stress(1, 'MPa')
        basic_helical_gear_1.contact_stress = contact_stress

        assert basic_helical_gear_1.contact_stress == contact_stress

    @mark.error
    def test_raises_type_error(self, helical_gear_contact_stress_type_error):
        with raises(TypeError):
            basic_helical_gear_1.contact_stress = helical_gear_contact_stress_type_error


@mark.helical_gear
class TestHelicalGearComputeContactStress:

    @mark.genuine
    def test_method(self):
        gear_1 = HelicalGear(name = 'gear 1', n_teeth = 10, helix_angle = Angle(30, 'deg'),
                             inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'),
                             face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))
        gear_2 = HelicalGear(name = 'gear 2', n_teeth = 20, helix_angle = Angle(30, 'deg'),
                             inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'),
                             face_width = Length(5, 'mm'), elastic_modulus = Stress(200, 'GPa'))
        add_gear_mating(master = gear_1, slave = gear_2, efficiency = 0.9)
        gear_1.master_gear_ratio = 1.0

        for gear in [gear_1, gear_2]:
            gear.driving_torque = Torque(1, 'Nm')
            gear.load_torque = Torque(1, 'Nm')
            gear.compute_tangential_force()
            gear.compute_contact_stress()

            assert gear.contact_stress is not None
            assert isinstance(gear.contact_stress, Stress)


    @mark.error
    def test_raises_value_error(self, helical_gear_compute_contact_stress_value_error):
        with raises(ValueError):
            helical_gear_compute_contact_stress_value_error.compute_contact_stress()


@mark.helical_gear
class TestHelicalGearContactStressIsComputable:

    @mark.genuine
    def test_property(self):
        for gear in [basic_helical_gear_1, basic_helical_gear_2]:
            if (gear.module is None) or (gear.face_width is None) or (gear.elastic_modulus is None):
                assert not gear.contact_stress_is_computable
            else:
                assert gear.contact_stress_is_computable


@mark.helical_gear
class TestHelicalGearExternalTorque:


    @mark.genuine
    @given(external_torque = functions(like = lambda angular_position, angular_speed, time: Torque(1, 'Nm'),
                                       returns = torques()))
    @settings(max_examples = 100)
    def test_property(self, external_torque):
        basic_helical_gear_1.external_torque = external_torque

        assert basic_helical_gear_1.external_torque == external_torque


    @mark.error
    def test_raises_type_error(self, helical_gear_external_torque_type_error):
        with raises(TypeError):
            basic_helical_gear_1.external_torque = helical_gear_external_torque_type_error


    @mark.error
    def test_raises_key_error(self, helical_gear_external_torque_key_error):
        with raises(KeyError):
            basic_helical_gear_1.external_torque = helical_gear_external_torque_key_error
