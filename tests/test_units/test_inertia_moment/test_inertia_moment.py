from gearpy.units import InertiaMoment
from hypothesis.strategies import floats, sampled_from, one_of, booleans
from hypothesis import given, settings
from tests.test_units.test_inertia_moment.conftest import basic_inertia_moment, inertia_moments
from pytest import mark, raises


units_list = list(InertiaMoment._InertiaMoment__UNITS.keys())


@mark.units
class TestInertiaMomentInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        inertia_moment = InertiaMoment(value = value, unit = unit)

        assert inertia_moment.value == value
        assert inertia_moment.unit == unit


    @mark.error
    def test_raises_type_error(self, inertia_moment_init_type_error):
        with raises(TypeError):
            InertiaMoment(**inertia_moment_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                InertiaMoment(value = 1, unit = fake_unit)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            InertiaMoment(value = -1, unit = 'kgm^2')


@mark.units
class TestInertiaMomentRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        inertia_moment = InertiaMoment(value = value, unit = unit)

        assert str(inertia_moment) == f'{value} {unit}'


@mark.units
class TestInertiaMomentAbs:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        inertia_moment = InertiaMoment(value = value, unit = unit)

        assert abs(inertia_moment) == InertiaMoment(value = abs(value), unit = unit)
        assert abs(inertia_moment).value >= 0


@mark.units
class TestInertiaMomentAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        inertia_moment_1 = InertiaMoment(value = value_1, unit = unit_1)
        inertia_moment_2 = InertiaMoment(value = value_2, unit = unit_2)
        result = inertia_moment_1 + inertia_moment_2

        assert isinstance(result, InertiaMoment)
        assert result.value == inertia_moment_1.value + inertia_moment_2.to(unit_1).value
        assert result.unit == inertia_moment_1.unit


    @mark.error
    def test_raises_type_error(self, inertia_moment_add_type_error):
        with raises(TypeError):
            assert basic_inertia_moment + inertia_moment_add_type_error


@mark.units
class TestInertiaMomentSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        inertia_moment_1 = InertiaMoment(value = value_1, unit = unit_1)
        inertia_moment_2 = InertiaMoment(value = value_2, unit = unit_2)
        if inertia_moment_1 > inertia_moment_2:
            result = inertia_moment_1 - inertia_moment_2

            assert isinstance(result, InertiaMoment)
            assert result.value == inertia_moment_1.value - inertia_moment_2.to(unit_1).value
            assert result.unit == inertia_moment_1.unit


    @mark.error
    def test_raises_type_error(self, inertia_moment_sub_type_error):
        with raises(TypeError):
            assert basic_inertia_moment - inertia_moment_sub_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_inertia_moment - InertiaMoment(basic_inertia_moment.value + 1, basic_inertia_moment.unit)


@mark.units
class TestInertiaMomentMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        inertia_moment = InertiaMoment(value = value, unit = unit)
        result = inertia_moment*multiplier

        assert isinstance(result, InertiaMoment)
        assert result.value == inertia_moment.value*multiplier
        assert result.unit == inertia_moment.unit


    @mark.error
    def test_raises_type_error(self, inertia_moment_mul_type_error):
        with raises(TypeError):
            assert basic_inertia_moment*inertia_moment_mul_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_inertia_moment*(-1)


@mark.units
class TestInertiaMomentRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        inertia_moment = InertiaMoment(value = value, unit = unit)
        result = multiplier*inertia_moment

        assert isinstance(result, InertiaMoment)
        assert result.value == inertia_moment.value*multiplier
        assert result.unit == inertia_moment.unit


    @mark.error
    def test_raises_type_error(self, inertia_moment_rmul_type_error):
        with raises(TypeError):
            assert inertia_moment_rmul_type_error*basic_inertia_moment


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert -1*basic_inertia_moment


@mark.units
class TestInertiaMomentTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
                            inertia_moments()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        inertia_moment = InertiaMoment(value = value, unit = unit)

        if isinstance(divider, InertiaMoment):
            if abs(divider.value) >= 1e-300:
                result = inertia_moment/divider
                assert isinstance(result, float)
                assert result == inertia_moment.value/divider.to(unit).value
        else:
            if divider != 0:
                result = inertia_moment/divider
                assert isinstance(result, InertiaMoment)
                assert result.value == inertia_moment.value/divider
                assert result.unit == inertia_moment.unit


    @mark.error
    def test_raises_type_error(self, inertia_moment_truediv_type_error):
        with raises(TypeError):
            assert basic_inertia_moment/inertia_moment_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, inertia_moment_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_inertia_moment/inertia_moment_truediv_zero_division_error


@mark.units
class TestInertiaMomentEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        inertia_moment_1 = InertiaMoment(value = value, unit = unit)
        inertia_moment_2 = InertiaMoment(value = value, unit = unit)

        for target_unit in units_list:
            assert inertia_moment_1 == inertia_moment_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, inertia_moment_eq_type_error):
        with raises(TypeError):
            assert basic_inertia_moment == inertia_moment_eq_type_error


@mark.units
class TestInertiaMomentNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        inertia_moment_1 = InertiaMoment(value = value, unit = unit)
        inertia_moment_2 = InertiaMoment(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert inertia_moment_1 != inertia_moment_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, inertia_moment_ne_type_error):
        with raises(TypeError):
            assert basic_inertia_moment != inertia_moment_ne_type_error


@mark.units
class TestInertiaMomentGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        inertia_moment_1 = InertiaMoment(value = value + gap, unit = unit)
        inertia_moment_2 = InertiaMoment(value = value, unit = unit)

        for target_unit in units_list:
            assert inertia_moment_1 > inertia_moment_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, inertia_moment_gt_type_error):
        with raises(TypeError):
            assert basic_inertia_moment > inertia_moment_gt_type_error


@mark.units
class TestInertiaMomentGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        inertia_moment_1 = InertiaMoment(value = value + gap, unit = unit)
        inertia_moment_2 = InertiaMoment(value = value, unit = unit)

        for target_unit in units_list:
            assert inertia_moment_1 >= inertia_moment_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, inertia_moment_ge_type_error):
        with raises(TypeError):
            assert basic_inertia_moment >= inertia_moment_ge_type_error


@mark.units
class TestInertiaMomentLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            inertia_moment_1 = InertiaMoment(value = value, unit = unit)
            inertia_moment_2 = InertiaMoment(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert inertia_moment_1 < inertia_moment_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, inertia_moment_lt_type_error):
        with raises(TypeError):
            assert basic_inertia_moment < inertia_moment_lt_type_error


@mark.units
class TestInertiaMomentLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            inertia_moment_1 = InertiaMoment(value = value, unit = unit)
            inertia_moment_2 = InertiaMoment(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert inertia_moment_1 <= inertia_moment_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, inertia_moment_le_type_error):
        with raises(TypeError):
            assert basic_inertia_moment <= inertia_moment_le_type_error


@mark.units
class TestInertiaMomentTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            inertia_moment = InertiaMoment(value = value, unit = unit)

            for target_unit in units_list:
                converted_inertia = inertia_moment.to(target_unit = target_unit, inplace = inplace)

                assert converted_inertia.unit == target_unit
                if InertiaMoment._InertiaMoment__UNITS[target_unit] != InertiaMoment._InertiaMoment__UNITS[unit]:
                    assert converted_inertia.value != value
                    assert converted_inertia.unit != unit

                    if inplace:
                        assert converted_inertia.value == inertia_moment.value
                        assert converted_inertia.unit == inertia_moment.unit
                    else:
                        assert converted_inertia.value != inertia_moment.value
                        assert converted_inertia.unit != inertia_moment.unit
                else:
                    assert converted_inertia == inertia_moment


    @mark.error
    def test_raises_type_error(self, inertia_moment_to_type_error):
        with raises(TypeError):
            basic_inertia_moment.to(**inertia_moment_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_inertia_moment.to(fake_unit)
