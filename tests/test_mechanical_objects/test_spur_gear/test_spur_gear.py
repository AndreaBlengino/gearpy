from gearpy.mechanical_objects import SpurGear
from gearpy.units import Length, Stress
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers
from pytest import mark, raises
from tests.test_units.test_inertia_moment.conftest import inertia_moments


@mark.spur_gear
class TestSpurGearInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           n_teeth = integers(min_value = 10, max_value = 1000),
           inertia_moment = inertia_moments(),
           module_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 10),
           face_width_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 100),
           elastic_modulus_value = floats(allow_nan = False, allow_infinity = False, min_value = 0.1, max_value = 10))
    @settings(max_examples = 100)
    def test_method(self, name, n_teeth, inertia_moment, module_value, face_width_value, elastic_modulus_value):
        module = Length(module_value, 'mm')
        face_width = Length(face_width_value, 'mm')
        elastic_modulus = Stress(elastic_modulus_value, 'GPa')
        gear = SpurGear(name = name, n_teeth = n_teeth, inertia_moment = inertia_moment,
                        module = module, face_width = face_width, elastic_modulus = elastic_modulus)

        assert gear.name == name
        assert gear.n_teeth == n_teeth
        assert gear.inertia_moment == inertia_moment
        assert gear.module == module
        assert gear.reference_diameter == n_teeth*module
        assert gear.face_width == face_width
        assert gear.elastic_modulus == elastic_modulus


    @mark.error
    def test_raises_type_error(self, spur_gear_init_type_error):
        with raises(TypeError):
            SpurGear(**spur_gear_init_type_error)


    @mark.error
    def test_raises_value_error(self, spur_gear_init_value_error):
        with raises(ValueError):
            SpurGear(**spur_gear_init_value_error)
