from gearpy.mechanical_objects import (
    MatingMaster,
    MatingSlave,
    WormGear,
    WormWheel
)
from gearpy.units import Force, Torque, Stress
from gearpy.utils import add_gear_mating, add_worm_gear_mating
from hypothesis import given, settings
from hypothesis.strategies import functions
from pytest import mark, raises
from tests.test_mechanical_objects.test_gear.conftest import (
    basic_gears,
    basic_structural_gears_1,
    basic_structural_gears_2,
    FakeRole
)
from tests.test_units.test_torque.conftest import torques


@mark.gear
class TestGearMatingRole:

    @mark.genuine
    def test_property(self):
        for gear in basic_gears:
            for role in [MatingMaster, MatingSlave]:
                gear.mating_role = role

                assert gear.mating_role == role

    @mark.error
    def test_raises_type_error(self, gear_mating_role_type_error):
        for gear in basic_gears:
            with raises(TypeError):
                gear.mating_role = gear_mating_role_type_error


@mark.gear
class TestGearTangentialForce:

    @mark.genuine
    def test_property(self):
        tangential_force = Force(1, 'N')
        for gear in basic_gears:
            gear.tangential_force = tangential_force

            assert gear.tangential_force == tangential_force

    @mark.error
    def test_raises_type_error(self, gear_tangential_force_type_error):
        for gear in basic_gears:
            with raises(TypeError):
                gear.tangential_force = gear_tangential_force_type_error


@mark.gear
class TestGearComputeTangentialForce:

    @mark.genuine
    def test_method(self):
        for master, slave in zip(
            basic_structural_gears_1,
            basic_structural_gears_2
        ):
            if isinstance(master, WormGear | WormWheel):
                add_worm_gear_mating(
                    master=master,
                    slave=slave,
                    friction_coefficient=0
                )
            else:
                add_gear_mating(master=master, slave=slave, efficiency=0.9)

            master.driving_torque = Torque(1, 'Nm')
            slave.driving_torque = Torque(1, 'Nm')
            master.load_torque = Torque(1, 'Nm')
            slave.load_torque = Torque(1, 'Nm')
            master.compute_tangential_force()
            slave.compute_tangential_force()

            assert master.tangential_force is not None
            assert slave.tangential_force is not None
            assert isinstance(master.tangential_force, Force)
            assert isinstance(slave.tangential_force, Force)

    @mark.error
    def test_raises_value_error(self):
        for gear in basic_structural_gears_1:
            gear.mating_role = FakeRole
            with raises(ValueError):
                gear.compute_tangential_force()


@mark.gear
class TestGearTangentialForceIsComputable:

    @mark.genuine
    def test_property(self):
        for gear in basic_gears:
            if not isinstance(gear, WormGear):
                if gear.module is None:
                    assert not gear.tangential_force_is_computable
                else:
                    assert gear.tangential_force_is_computable
            else:
                if gear.reference_diameter is None:
                    assert not gear.tangential_force_is_computable
                else:
                    assert gear.tangential_force_is_computable


@mark.gear
class TestGearBendingStress:

    @mark.genuine
    def test_property(self):
        bending_stress = Stress(1, 'MPa')
        for gear in basic_gears:
            if not isinstance(gear, WormGear):
                gear.bending_stress = bending_stress

                assert gear.bending_stress == bending_stress

    @mark.error
    def test_raises_type_error(self, gear_bending_stress_type_error):
        for gear in basic_gears:
            if not isinstance(gear, WormGear):
                with raises(TypeError):
                    gear.bending_stress = gear_bending_stress_type_error


@mark.gear
class TestGearComputeBendingStress:

    @mark.genuine
    def test_method(self):
        for master, slave in zip(
            basic_structural_gears_1,
            basic_structural_gears_2
        ):
            if isinstance(master, WormGear | WormWheel):
                add_worm_gear_mating(
                    master=master,
                    slave=slave,
                    friction_coefficient=0
                )
            else:
                add_gear_mating(master=master, slave=slave, efficiency=0.9)

            if not isinstance(master, WormGear):
                master.driving_torque = Torque(1, 'Nm')
                master.load_torque = Torque(1, 'Nm')
                master.compute_tangential_force()
                master.compute_bending_stress()

                assert master.bending_stress is not None
                assert isinstance(master.bending_stress, Stress)

            if not isinstance(slave, WormGear):
                slave.driving_torque = Torque(1, 'Nm')
                slave.load_torque = Torque(1, 'Nm')
                slave.compute_tangential_force()
                slave.compute_bending_stress()

                assert slave.bending_stress is not None
                assert isinstance(slave.bending_stress, Stress)

    @mark.error
    def test_raises_value_error(self):
        for gear in basic_structural_gears_1:
            if isinstance(gear, WormWheel):
                gear.mating_role = FakeRole
                with raises(ValueError):
                    gear.compute_bending_stress()


@mark.gear
class TestGearBendingStressIsComputable:

    @mark.genuine
    def test_property(self):
        for gear in basic_gears:
            if not isinstance(gear, WormGear | WormWheel):
                if (gear.module is None) or (gear.face_width is None):
                    assert not gear.bending_stress_is_computable
                else:
                    assert gear.bending_stress_is_computable


@mark.gear
class TestGearContactStress:

    @mark.genuine
    def test_property(self):
        contact_stress = Stress(1, 'MPa')
        for gear in basic_gears:
            if not isinstance(gear, WormGear | WormWheel):
                gear.contact_stress = contact_stress

                assert gear.contact_stress == contact_stress

    @mark.error
    def test_raises_type_error(self, gear_contact_stress_type_error):
        for gear in basic_gears:
            if not isinstance(gear, WormGear | WormWheel):
                with raises(TypeError):
                    gear.contact_stress = gear_contact_stress_type_error


@mark.gear
class TestGearComputeContactStress:

    @mark.genuine
    def test_method(self):
        for master, slave in zip(
            basic_structural_gears_1,
            basic_structural_gears_2
        ):
            if not isinstance(master, WormGear | WormWheel):
                add_gear_mating(master=master, slave=slave, efficiency=0.9)

                for gear in [master, slave]:
                    gear.driving_torque = Torque(1, 'Nm')
                    gear.load_torque = Torque(1, 'Nm')
                    gear.compute_tangential_force()
                    gear.compute_contact_stress()

                    assert gear.contact_stress is not None
                    assert isinstance(gear.contact_stress, Stress)

    @mark.error
    def test_raises_value_error(self, gear_compute_contact_stress_value_error):
        with raises(ValueError):
            gear_compute_contact_stress_value_error.compute_contact_stress()


@mark.gear
class TestGearContactStressIsComputable:

    @mark.genuine
    def test_property(self):
        for gear in basic_gears:
            if not isinstance(gear, WormGear | WormWheel):
                if (gear.module is None) or (gear.face_width is None) \
                        or (gear.elastic_modulus is None):
                    assert not gear.contact_stress_is_computable
                else:
                    assert gear.contact_stress_is_computable


@mark.gear
class TestSpurExternalTorque:

    @mark.genuine
    @given(
        external_torque=functions(
            like=lambda angular_position, angular_speed, time: Torque(1, 'Nm'),
            returns=torques()
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_property(self, external_torque):
        for gear in basic_gears:
            gear.external_torque = external_torque

            assert gear.external_torque == external_torque

    @mark.error
    def test_raises_type_error(self, gear_external_torque_type_error):
        for gear in basic_gears:
            with raises(TypeError):
                gear.external_torque = gear_external_torque_type_error

    @mark.error
    def test_raises_key_error(self, gear_external_torque_key_error):
        for gear in basic_gears:
            with raises(KeyError):
                gear.external_torque = gear_external_torque_key_error
