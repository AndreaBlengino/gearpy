from gearpy.units import Surface
from hypothesis.strategies import floats, sampled_from, one_of, booleans, integers
from hypothesis import given, settings
from tests.test_units.test_surface.conftest import basic_surface, surfaces
from pytest import mark, raises


units_list = list(Surface._Surface__UNITS.keys())


@mark.units
class TestSurfaceInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        surface = Surface(value = value, unit = unit)

        assert surface.value == value
        assert surface.unit == unit


    @mark.error
    def test_raises_type_error(self, surface_init_type_error):
        with raises(TypeError):
            Surface(**surface_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                Surface(value = 1, unit = fake_unit)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            Surface(value = -1, unit = 'm^2')


@mark.units
class TestSurfaceRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        surface = Surface(value = value, unit = unit)

        assert str(surface) == f'{value} {unit}'


@mark.units
class TestSurfaceFormat:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           total_digits = integers(min_value = 1, max_value = 10),
           decimal_digits = integers(min_value = 1, max_value = 10))
    @settings(max_examples = 100)
    def test_method(self, value, unit, total_digits, decimal_digits):
        surface = Surface(value = value, unit = unit)

        assert surface.__format__(f'{total_digits}.{decimal_digits}f') == f'{surface:{total_digits}.{decimal_digits}f}'


@mark.units
class TestSurfaceAbs:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        surface = Surface(value = value, unit = unit)

        assert abs(surface) == Surface(value = abs(value), unit = unit)
        assert abs(surface).value >= 0


@mark.units
class TestSurfaceNeg:


    @mark.error
    def test_method(self):
        surface = Surface(value = 1, unit = 'm^2')

        with raises(ValueError):
            assert -surface


@mark.units
class TestSurfaceAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        surface_1 = Surface(value = value_1, unit = unit_1)
        surface_2 = Surface(value = value_2, unit = unit_2)
        result = surface_1 + surface_2

        assert isinstance(result, Surface)
        assert result.value == surface_1.value + surface_2.to(unit_1).value
        assert result.unit == surface_1.unit


    @mark.error
    def test_raises_type_error(self, surface_add_type_error):
        with raises(TypeError):
            assert basic_surface + surface_add_type_error


@mark.units
class TestSurfaceSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        surface_1 = Surface(value = value_1, unit = unit_1)
        surface_2 = Surface(value = value_2, unit = unit_2)
        if surface_1 > surface_2:
            result = surface_1 - surface_2

            assert isinstance(result, Surface)
            assert result.value == surface_1.value - surface_2.to(unit_1).value
            assert result.unit == surface_1.unit


    @mark.error
    def test_raises_type_error(self, surface_sub_type_error):
        with raises(TypeError):
            assert basic_surface - surface_sub_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_surface - Surface(basic_surface.value + 1, basic_surface.unit)


@mark.units
class TestSurfaceMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        surface = Surface(value = value, unit = unit)
        result = surface*multiplier

        assert isinstance(result, Surface)
        assert result.value == surface.value*multiplier
        assert result.unit == surface.unit


    @mark.error
    def test_raises_type_error(self, surface_mul_type_error):
        with raises(TypeError):
            assert basic_surface*surface_mul_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_surface*(-1)


@mark.units
class TestSurfaceRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        surface = Surface(value = value, unit = unit)
        result = multiplier*surface

        assert isinstance(result, Surface)
        assert result.value == surface.value*multiplier
        assert result.unit == surface.unit


    @mark.error
    def test_raises_type_error(self, surface_rmul_type_error):
        with raises(TypeError):
            assert surface_rmul_type_error*basic_surface


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert -1*basic_surface


@mark.units
class TestSurfaceTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
                            surfaces()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        surface = Surface(value = value, unit = unit)

        if isinstance(divider, Surface):
            if abs(divider.value) >= 1e-300:
                result = surface/divider
                assert isinstance(result, float)
                assert result == surface.value/divider.to(unit).value
        else:
            if divider != 0:
                result = surface/divider
                assert isinstance(result, Surface)
                assert result.value == surface.value/divider
                assert result.unit == surface.unit


    @mark.error
    def test_raises_type_error(self, surface_truediv_type_error):
        with raises(TypeError):
            assert basic_surface/surface_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, surface_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_surface/surface_truediv_zero_division_error


@mark.units
class TestSurfaceEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit):
        surface_1 = Surface(value = value, unit = unit)
        surface_2 = Surface(value = value, unit = unit)

        for target_unit in units_list:
            assert surface_1 == surface_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, surface_eq_type_error):
        with raises(TypeError):
            assert basic_surface == surface_eq_type_error


@mark.units
class TestSurfaceNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        surface_1 = Surface(value = value, unit = unit)
        surface_2 = Surface(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert surface_1 != surface_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, surface_ne_type_error):
        with raises(TypeError):
            assert basic_surface != surface_ne_type_error


@mark.units
class TestSurfaceGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        surface_1 = Surface(value = value + gap, unit = unit)
        surface_2 = Surface(value = value, unit = unit)

        for target_unit in units_list:
            assert surface_1 > surface_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, surface_gt_type_error):
        with raises(TypeError):
            assert basic_surface > surface_gt_type_error


@mark.units
class TestSurfaceGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        surface_1 = Surface(value = value + gap, unit = unit)
        surface_2 = Surface(value = value, unit = unit)

        for target_unit in units_list:
            assert surface_1 >= surface_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, surface_ge_type_error):
        with raises(TypeError):
            assert basic_surface >= surface_ge_type_error


@mark.units
class TestSurfaceLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        if value != 0:
            surface_1 = Surface(value = value, unit = unit)
            surface_2 = Surface(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert surface_1 < surface_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, surface_lt_type_error):
        with raises(TypeError):
            assert basic_surface < surface_lt_type_error


@mark.units
class TestSurfaceLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        if value != 0:
            surface_1 = Surface(value = value, unit = unit)
            surface_2 = Surface(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert surface_1 <= surface_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, surface_le_type_error):
        with raises(TypeError):
            assert basic_surface <= surface_le_type_error


@mark.units
class TestSurfaceTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            surface = Surface(value = value, unit = unit)

            for target_unit in units_list:
                converted_inertia = surface.to(target_unit = target_unit, inplace = inplace)

                assert converted_inertia.unit == target_unit
                if Surface._Surface__UNITS[target_unit] != Surface._Surface__UNITS[unit]:
                    assert converted_inertia.value != value
                    assert converted_inertia.unit != unit

                    if inplace:
                        assert converted_inertia.value == surface.value
                        assert converted_inertia.unit == surface.unit
                    else:
                        assert converted_inertia.value != surface.value
                        assert converted_inertia.unit != surface.unit
                else:
                    assert converted_inertia == surface


    @mark.error
    def test_raises_type_error(self, surface_to_type_error):
        with raises(TypeError):
            basic_surface.to(**surface_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_surface.to(fake_unit)
