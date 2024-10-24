from gearpy.mechanical_objects import HelicalGear
from gearpy.units import Length, Stress
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers
from pytest import mark, raises
from tests.test_units.test_inertia_moment.conftest import inertia_moments
from tests.test_units.test_angle.conftest import angles


@mark.helical_gear
class TestHelicalGearInit:

    @mark.genuine
    @given(
        name=text(min_size=1),
        n_teeth=integers(min_value=10, max_value=1000),
        helix_angle=angles(min_value=1e-1, max_value=40, unit='deg'),
        inertia_moment=inertia_moments(),
        module_value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0.1,
            max_value=10
        ),
        face_width_value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0.1,
            max_value=100
        ),
        elastic_modulus_value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0.1,
            max_value=10
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(
        self,
        name,
        n_teeth,
        helix_angle,
        inertia_moment,
        module_value,
        face_width_value,
        elastic_modulus_value
    ):
        module = Length(module_value, 'mm')
        face_width = Length(face_width_value, 'mm')
        elastic_modulus = Stress(elastic_modulus_value, 'GPa')
        gear = HelicalGear(
            name=name,
            n_teeth=n_teeth,
            helix_angle=helix_angle,
            inertia_moment=inertia_moment,
            module=module,
            face_width=face_width,
            elastic_modulus=elastic_modulus
        )

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
