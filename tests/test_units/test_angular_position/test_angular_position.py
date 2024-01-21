from gearpy.units import AngularPosition
from hypothesis.strategies import floats, sampled_from, one_of, booleans, integers
from hypothesis import given, settings
from tests.test_units.test_angular_position.conftest import basic_angular_position, angular_positions
from pytest import mark, raises


units_list = list(AngularPosition._AngularPosition__UNITS.keys())


@mark.units
class TestAngularPositionInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_position = AngularPosition(value = value, unit = unit)

        assert angular_position.value == value
        assert angular_position.unit == unit


    @mark.error
    def test_raises_type_error(self, angular_position_init_type_error):
        with raises(TypeError):
            AngularPosition(**angular_position_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                AngularPosition(value = 1, unit = fake_unit)


@mark.units
class TestAngularPositionRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_position = AngularPosition(value = value, unit = unit)

        assert str(angular_position) == f'{value} {unit}'


@mark.units
class TestAngularPositionFormat:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           total_digits = integers(min_value = 1, max_value = 10),
           decimal_digits = integers(min_value = 1, max_value = 10))
    @settings(max_examples = 100)
    def test_method(self, value, unit, total_digits, decimal_digits):
        angular_position = AngularPosition(value = value, unit = unit)

        assert angular_position.__format__(f'{total_digits}.{decimal_digits}f') == f'{angular_position:{total_digits}.{decimal_digits}f}'


@mark.units
class TestAngularPositionAbs:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_position = AngularPosition(value = value, unit = unit)

        assert abs(angular_position) == AngularPosition(value = abs(value), unit = unit)
        assert abs(angular_position).value >= 0


@mark.units
class TestAngularPositionNeg:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_position = AngularPosition(value = value, unit = unit)

        assert -angular_position == AngularPosition(value = -value, unit = unit)


@mark.units
class TestAngularPositionAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        angular_position_1 = AngularPosition(value = value_1, unit = unit_1)
        angular_position_2 = AngularPosition(value = value_2, unit = unit_2)
        result = angular_position_1 + angular_position_2

        assert isinstance(result, AngularPosition)
        assert result.value == angular_position_1.value + angular_position_2.to(unit_1).value
        assert result.unit == angular_position_1.unit


    @mark.error
    def test_raises_type_error(self, angular_position_add_type_error):
        with raises(TypeError):
            assert basic_angular_position + angular_position_add_type_error


@mark.units
class TestAngularPositionSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        angular_position_1 = AngularPosition(value = value_1, unit = unit_1)
        angular_position_2 = AngularPosition(value = value_2, unit = unit_2)
        result = angular_position_1 - angular_position_2

        assert isinstance(result, AngularPosition)
        assert result.value == angular_position_1.value - angular_position_2.to(unit_1).value
        assert result.unit == angular_position_1.unit


    @mark.error
    def test_raises_type_error(self, angular_position_sub_type_error):
        with raises(TypeError):
            assert basic_angular_position - angular_position_sub_type_error


@mark.units
class TestAngularPositionMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        angular_position = AngularPosition(value = value, unit = unit)
        result = angular_position*multiplier

        assert isinstance(result, AngularPosition)
        assert result.value == angular_position.value*multiplier
        assert result.unit == angular_position.unit


    @mark.error
    def test_raises_type_error(self, angular_position_mul_type_error):
        with raises(TypeError):
            assert basic_angular_position*angular_position_mul_type_error


@mark.units
class TestAngularPositionRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        angular_position = AngularPosition(value = value, unit = unit)
        result = multiplier*angular_position

        assert isinstance(result, AngularPosition)
        assert result.value == angular_position.value*multiplier
        assert result.unit == angular_position.unit


    @mark.error
    def test_raises_type_error(self, angular_position_rmul_type_error):
        with raises(TypeError):
            assert angular_position_rmul_type_error*basic_angular_position


@mark.units
class TestAngularPositionTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                            angular_positions()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        angular_position = AngularPosition(value = value, unit = unit)

        if isinstance(divider, AngularPosition):
            if abs(divider.value) >= 1e-300:
                result = angular_position/divider
                assert isinstance(result, float)
                assert result == angular_position.value/divider.to(unit).value
        else:
            if divider != 0:
                result = angular_position/divider
                assert isinstance(result, AngularPosition)
                assert result.value == angular_position.value/divider
                assert result.unit == angular_position.unit


    @mark.error
    def test_raises_type_error(self, angular_position_truediv_type_error):
        with raises(TypeError):
            assert basic_angular_position/angular_position_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, angular_position_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_angular_position/angular_position_truediv_zero_division_error


@mark.units
class TestAngularPositionEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit):
        angular_position_1 = AngularPosition(value = value, unit = unit)
        angular_position_2 = AngularPosition(value = value, unit = unit)

        for target_unit in units_list:
            assert angular_position_1 == angular_position_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_position_eq_type_error):
        with raises(TypeError):
            assert basic_angular_position == angular_position_eq_type_error


@mark.units
class TestAngularPositionNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        angular_position_1 = AngularPosition(value = value, unit = unit)
        angular_position_2 = AngularPosition(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert angular_position_1 != angular_position_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_position_ne_type_error):
        with raises(TypeError):
            assert basic_angular_position != angular_position_ne_type_error


@mark.units
class TestAngularPositionGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        angular_position_1 = AngularPosition(value = value + gap, unit = unit)
        angular_position_2 = AngularPosition(value = value, unit = unit)

        for target_unit in units_list:
            assert angular_position_1 > angular_position_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_position_gt_type_error):
        with raises(TypeError):
            assert basic_angular_position > angular_position_gt_type_error


@mark.units
class TestAngularPositionGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        angular_position_1 = AngularPosition(value = value + gap, unit = unit)
        angular_position_2 = AngularPosition(value = value, unit = unit)

        for target_unit in units_list:
            assert angular_position_1 >= angular_position_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_position_ge_type_error):
        with raises(TypeError):
            assert basic_angular_position >= angular_position_ge_type_error


@mark.units
class TestAngularPositionLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        if value != 0:
            angular_position_1 = AngularPosition(value = value, unit = unit)
            angular_position_2 = AngularPosition(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert angular_position_1 < angular_position_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_position_lt_type_error):
        with raises(TypeError):
            assert basic_angular_position < angular_position_lt_type_error


@mark.units
class TestAngularPositionLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        if value != 0:
            angular_position_1 = AngularPosition(value = value, unit = unit)
            angular_position_2 = AngularPosition(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert angular_position_1 <= angular_position_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_position_le_type_error):
        with raises(TypeError):
            assert basic_angular_position <= angular_position_le_type_error


@mark.units
class TestAngularPositionTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            angular_position = AngularPosition(value = value, unit = unit)

            for target_unit in units_list:
                converted_position = angular_position.to(target_unit = target_unit, inplace = inplace)

                assert converted_position.unit == target_unit
                if AngularPosition._AngularPosition__UNITS[target_unit] != AngularPosition._AngularPosition__UNITS[unit]:
                    assert converted_position.value != value
                    assert converted_position.unit != unit

                    if inplace:
                        assert converted_position.value == angular_position.value
                        assert converted_position.unit == angular_position.unit
                    else:
                        assert converted_position.value != angular_position.value
                        assert converted_position.unit != angular_position.unit
                else:
                    assert converted_position == angular_position


    @mark.error
    def test_raises_type_error(self, angular_position_to_type_error):
        with raises(TypeError):
            basic_angular_position.to(**angular_position_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_angular_position.to(fake_unit)
