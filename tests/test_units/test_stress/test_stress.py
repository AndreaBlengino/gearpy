from gearpy.units import Stress
from hypothesis.strategies import floats, sampled_from, one_of, booleans, integers
from hypothesis import given, settings
from tests.test_units.test_stress.conftest import basic_stress, stresses
from pytest import mark, raises


units_list = list(Stress._Stress__UNITS.keys())


@mark.units
class TestStressInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        stress = Stress(value = value, unit = unit)

        assert stress.value == value
        assert stress.unit == unit


    @mark.error
    def test_raises_type_error(self, stress_init_type_error):
        with raises(TypeError):
            Stress(**stress_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                Stress(value = 1, unit = fake_unit)


@mark.units
class TestStressRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        stress = Stress(value = value, unit = unit)

        assert str(stress) == f'{value} {unit}'


@mark.units
class TestStressFormat:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           total_digits = integers(min_value = 1, max_value = 10),
           decimal_digits = integers(min_value = 1, max_value = 10))
    @settings(max_examples = 100)
    def test_method(self, value, unit, total_digits, decimal_digits):
        stress = Stress(value = value, unit = unit)

        assert stress.__format__(f'{total_digits}.{decimal_digits}f') == f'{stress:{total_digits}.{decimal_digits}f}'


@mark.units
class TestStressAbs:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        stress = Stress(value = value, unit = unit)

        assert abs(stress) == Stress(value = abs(value), unit = unit)
        assert abs(stress).value >= 0


@mark.units
class TestStressNeg:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        stress = Stress(value = value, unit = unit)

        assert -stress == Stress(value = -value, unit = unit)


@mark.units
class TestStressAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        stress_1 = Stress(value = value_1, unit = unit_1)
        stress_2 = Stress(value = value_2, unit = unit_2)
        result = stress_1 + stress_2

        assert isinstance(result, Stress)
        assert result.value == stress_1.value + stress_2.to(unit_1).value
        assert result.unit == stress_1.unit


    @mark.error
    def test_raises_type_error(self, stress_add_type_error):
        with raises(TypeError):
            assert basic_stress + stress_add_type_error


@mark.units
class TestStressSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        stress_1 = Stress(value = value_1, unit = unit_1)
        stress_2 = Stress(value = value_2, unit = unit_2)
        result = stress_1 - stress_2

        assert isinstance(result, Stress)
        assert result.value == stress_1.value - stress_2.to(unit_1).value
        assert result.unit == stress_1.unit


    @mark.error
    def test_raises_type_error(self, stress_sub_type_error):
        with raises(TypeError):
            assert basic_stress - stress_sub_type_error


@mark.units
class TestStressMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        stress = Stress(value = value, unit = unit)
        result = stress*multiplier

        assert isinstance(result, Stress)
        assert result.value == stress.value*multiplier
        assert result.unit == stress.unit


    @mark.error
    def test_raises_type_error(self, stress_mul_type_error):
        with raises(TypeError):
            assert basic_stress*stress_mul_type_error


@mark.units
class TestStressRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        stress = Stress(value = value, unit = unit)
        result = multiplier*stress

        assert isinstance(result, Stress)
        assert result.value == stress.value*multiplier
        assert result.unit == stress.unit


    @mark.error
    def test_raises_type_error(self, stress_rmul_type_error):
        with raises(TypeError):
            assert stress_rmul_type_error*basic_stress


@mark.units
class TestStressTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                            stresses()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        stress = Stress(value = value, unit = unit)

        if isinstance(divider, Stress):
            if abs(divider.value) >= 1e-300:
                result = stress/divider
                assert isinstance(result, float)
                assert result == stress.value/divider.to(unit).value
        else:
            if divider != 0:
                result = stress/divider
                assert isinstance(result, Stress)
                assert result.value == stress.value/divider
                assert result.unit == stress.unit


    @mark.error
    def test_raises_type_error(self, stress_truediv_type_error):
        with raises(TypeError):
            assert basic_stress/stress_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, stress_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_stress/stress_truediv_zero_division_error


@mark.units
class TestStressEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        stress_1 = Stress(value = value, unit = unit)
        stress_2 = Stress(value = value, unit = unit)

        for target_unit in units_list:
            assert stress_1 == stress_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, stress_eq_type_error):
        with raises(TypeError):
            assert basic_stress == stress_eq_type_error


@mark.units
class TestStressNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        stress_1 = Stress(value = value, unit = unit)
        stress_2 = Stress(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert stress_1 != stress_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, stress_ne_type_error):
        with raises(TypeError):
            assert basic_stress != stress_ne_type_error


@mark.units
class TestStressGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        stress_1 = Stress(value = value + gap, unit = unit)
        stress_2 = Stress(value = value, unit = unit)

        for target_unit in units_list:
            assert stress_1 > stress_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, stress_gt_type_error):
        with raises(TypeError):
            assert basic_stress > stress_gt_type_error


@mark.units
class TestStressGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        stress_1 = Stress(value = value + gap, unit = unit)
        stress_2 = Stress(value = value, unit = unit)

        for target_unit in units_list:
            assert stress_1 >= stress_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, stress_ge_type_error):
        with raises(TypeError):
            assert basic_stress >= stress_ge_type_error


@mark.units
class TestStressLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            stress_1 = Stress(value = value, unit = unit)
            stress_2 = Stress(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert stress_1 < stress_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, stress_lt_type_error):
        with raises(TypeError):
            assert basic_stress < stress_lt_type_error


@mark.units
class TestStressLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            stress_1 = Stress(value = value, unit = unit)
            stress_2 = Stress(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert stress_1 <= stress_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, stress_le_type_error):
        with raises(TypeError):
            assert basic_stress <= stress_le_type_error


@mark.units
class TestStressTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            stress = Stress(value = value, unit = unit)

            for target_unit in units_list:
                converted_stress = stress.to(target_unit = target_unit, inplace = inplace)

                assert converted_stress.unit == target_unit
                if Stress._Stress__UNITS[target_unit] != Stress._Stress__UNITS[unit]:
                    assert converted_stress.value != value
                    assert converted_stress.unit != unit

                    if inplace:
                        assert converted_stress.value == stress.value
                        assert converted_stress.unit == stress.unit
                    else:
                        assert converted_stress.value != stress.value
                        assert converted_stress.unit != stress.unit
                else:
                    assert converted_stress == stress


    @mark.error
    def test_raises_type_error(self, stress_to_type_error):
        with raises(TypeError):
            basic_stress.to(**stress_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_stress.to(fake_unit)
