from gearpy.mechanical_objects import WormGear
from gearpy.units import Length, Angle
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers, sampled_from
from pytest import mark, raises
from tests.conftest import basic_worm_gear_1
from tests.test_units.test_inertia_moment.conftest import inertia_moments
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
    @settings(max_examples = 100, deadline = None)
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
