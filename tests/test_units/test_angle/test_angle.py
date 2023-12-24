from gearpy.units import AngularPosition, Angle
from hypothesis.strategies import floats, sampled_from, one_of, booleans, integers
from hypothesis import given, settings
from tests.test_units.test_angle.conftest import basic_angle, angles
from pytest import mark, raises


units_list = list(Angle._AngularPosition__UNITS.keys())


@mark.units
class TestAngleInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angle = Angle(value = value, unit = unit)

        assert angle.value == value
        assert angle.unit == unit


    @mark.error
    def test_raises_type_error(self, angle_init_type_error):
        with raises(TypeError):
            Angle(**angle_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                Angle(value = 1, unit = fake_unit)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            Angle(value = -1, unit = 'rad')


@mark.units
class TestAngleRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angle = Angle(value = value, unit = unit)

        assert str(angle) == f'{value} {unit}'


@mark.units
class TestLengthFormat:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           total_digits = integers(min_value = 1, max_value = 10),
           decimal_digits = integers(min_value = 1, max_value = 10))
    @settings(max_examples = 100)
    def test_method(self, value, unit, total_digits, decimal_digits):
        angle = Angle(value = value, unit = unit)

        assert angle.__format__(f'{total_digits}.{decimal_digits}f') == f'{angle:{total_digits}.{decimal_digits}f}'


@mark.units
class TestAngleAbs:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angle = Angle(value = value, unit = unit)

        assert abs(angle) == Angle(value = abs(value), unit = unit)
        assert abs(angle).value >= 0


@mark.units
class TestAngleNeg:


    @mark.error
    def test_method(self):
        angle = Angle(value = 1, unit = 'rad')

        with raises(ValueError):
            assert -angle


@mark.units
class TestAngleAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = 0),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = 0),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        angle_1 = Angle(value = value_1, unit = unit_1)
        angle_2 = Angle(value = value_2, unit = unit_2)
        angular_position = AngularPosition(value = value_2, unit = unit_2)
        result_1 = angle_1 + angle_2
        result_2 = angle_1 + angular_position

        assert isinstance(result_1, Angle)
        assert result_1.value == angle_1.value + angle_2.to(unit_1).value
        assert result_1.unit == angle_1.unit
        assert isinstance(result_2, AngularPosition)
        assert result_2.value == angle_1.value + angular_position.to(unit_1).value
        assert result_2.unit == angle_1.unit


    @mark.error
    def test_raises_type_error(self, angle_add_type_error):
        with raises(TypeError):
            assert basic_angle + angle_add_type_error


@mark.units
class TestAngleSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = 0),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = 0),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        angle_1 = Angle(value = value_1, unit = unit_1)
        angle_2 = Angle(value = value_2, unit = unit_2)
        angular_position = AngularPosition(value = value_2, unit = unit_2)

        if angle_1 > angle_2:
            result_1 = angle_1 - angle_2

            assert isinstance(result_1, Angle)
            assert result_1.value == angle_1.value - angle_2.to(unit_1).value
            assert result_1.unit == angle_1.unit

        if angle_1 > angular_position:
            result_2 = angle_1 - angular_position

            assert isinstance(result_2, AngularPosition)
            assert result_2.value == angle_1.value + angular_position.to(unit_1).value
            assert result_2.unit == angle_1.unit


    @mark.error
    def test_raises_type_error(self, angle_sub_type_error):
        with raises(TypeError):
            assert basic_angle - angle_sub_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_angle - Angle(basic_angle.value + 1, basic_angle.unit)


@mark.units
class TestAngleMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        angle = Angle(value = value, unit = unit)
        result = angle*multiplier

        assert isinstance(result, Angle)
        assert result.value == angle.value*multiplier
        assert result.unit == angle.unit


    @mark.error
    def test_raises_type_error(self, angle_mul_type_error):
        with raises(TypeError):
            assert basic_angle*angle_mul_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_angle*(-1)


@mark.units
class TestAngleRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        angle = Angle(value = value, unit = unit)
        result = multiplier*angle

        assert isinstance(result, Angle)
        assert result.value == angle.value*multiplier
        assert result.unit == angle.unit


    @mark.error
    def test_raises_type_error(self, angle_rmul_type_error):
        with raises(TypeError):
            assert angle_rmul_type_error*basic_angle


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert -1*basic_angle


@mark.units
class TestAngleTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
                            angles()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        angle = Angle(value = value, unit = unit)

        if isinstance(divider, Angle):
            if abs(divider.value) >= 1e-300:
                result = angle/divider
                assert isinstance(result, float)
                assert result == angle.value/divider.to(unit).value
        else:
            if divider != 0:
                result = angle/divider
                assert isinstance(result, Angle)
                assert result.value == angle.value/divider
                assert result.unit == angle.unit


    @mark.error
    def test_raises_type_error(self, angle_truediv_type_error):
        with raises(TypeError):
            assert basic_angle/angle_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, angle_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_angle/angle_truediv_zero_division_error


@mark.units
class TestAngleEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angle_1 = Angle(value = value, unit = unit)
        angle_2 = Angle(value = value, unit = unit)

        for target_unit in units_list:
            assert angle_1 == angle_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angle_eq_type_error):
        with raises(TypeError):
            assert basic_angle == angle_eq_type_error


@mark.units
class TestAngleNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        angle_1 = Angle(value = value, unit = unit)
        angle_2 = Angle(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert angle_1 != angle_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angle_ne_type_error):
        with raises(TypeError):
            assert basic_angle != angle_ne_type_error


@mark.units
class TestAngleGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        angle_1 = Angle(value = value + gap, unit = unit)
        angle_2 = Angle(value = value, unit = unit)

        for target_unit in units_list:
            assert angle_1 > angle_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angle_gt_type_error):
        with raises(TypeError):
            assert basic_angle > angle_gt_type_error


@mark.units
class TestAngleGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        angle_1 = Angle(value = value + gap, unit = unit)
        angle_2 = Angle(value = value, unit = unit)

        for target_unit in units_list:
            assert angle_1 >= angle_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angle_ge_type_error):
        with raises(TypeError):
            assert basic_angle >= angle_ge_type_error


@mark.units
class TestAngleLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        if value != 0:
            angle_1 = Angle(value = value, unit = unit)
            angle_2 = Angle(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert angle_1 < angle_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angle_lt_type_error):
        with raises(TypeError):
            assert basic_angle < angle_lt_type_error


@mark.units
class TestAngleLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        if value != 0:
            angle_1 = Angle(value = value, unit = unit)
            angle_2 = Angle(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert angle_1 <= angle_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angle_le_type_error):
        with raises(TypeError):
            assert basic_angle <= angle_le_type_error


@mark.units
class TestAngleTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 0, max_value = 1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            angle = Angle(value = value, unit = unit)

            for target_unit in units_list:
                converted_angle = angle.to(target_unit = target_unit, inplace = inplace)

                assert converted_angle.unit == target_unit
                if Angle._AngularPosition__UNITS[target_unit] != Angle._AngularPosition__UNITS[unit]:
                    assert converted_angle.value != value
                    assert converted_angle.unit != unit

                    if inplace:
                        assert converted_angle.value == angle.value
                        assert converted_angle.unit == angle.unit
                    else:
                        assert converted_angle.value != angle.value
                        assert converted_angle.unit != angle.unit
                else:
                    assert converted_angle == angle


    @mark.error
    def test_raises_type_error(self, angle_to_type_error):
        with raises(TypeError):
            basic_angle.to(**angle_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_angle.to(fake_unit)
