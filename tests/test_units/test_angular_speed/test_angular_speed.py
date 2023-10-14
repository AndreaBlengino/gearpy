from gearpy.units import AngularPosition, AngularSpeed, Time
from hypothesis.strategies import floats, sampled_from, one_of, booleans
from hypothesis import given, settings
from tests.test_units.test_angular_speed.conftest import basic_angular_speed, angular_speeds, times
from pytest import mark, raises


units_list = list(AngularSpeed._AngularSpeed__UNITS.keys())


@mark.units
class TestAngularSpeedInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_speed = AngularSpeed(value = value, unit = unit)

        assert angular_speed.value == value
        assert angular_speed.unit == unit


    @mark.error
    def test_raises_type_error(self, angular_speed_init_type_error):
        with raises(TypeError):
            AngularSpeed(**angular_speed_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                AngularSpeed(value = 1, unit = fake_unit)


@mark.units
class TestAngularSpeedRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_speed = AngularSpeed(value = value, unit = unit)

        assert str(angular_speed) == f'{value} {unit}'



@mark.units
class TestAngularSpeedAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        angular_speed_1 = AngularSpeed(value = value_1, unit = unit_1)
        angular_speed_2 = AngularSpeed(value = value_2, unit = unit_2)
        result = angular_speed_1 + angular_speed_2

        assert isinstance(result, AngularSpeed)
        assert result.value == angular_speed_1.value + angular_speed_2.to(unit_1).value
        assert result.unit == angular_speed_1.unit


    @mark.error
    def test_raises_type_error(self, angular_speed_add_type_error):
        with raises(TypeError):
            assert basic_angular_speed + angular_speed_add_type_error


@mark.units
class TestAngularSpeedSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        angular_speed_1 = AngularSpeed(value = value_1, unit = unit_1)
        angular_speed_2 = AngularSpeed(value = value_2, unit = unit_2)
        result = angular_speed_1 - angular_speed_2

        assert isinstance(result, AngularSpeed)
        assert result.value == angular_speed_1.value - angular_speed_2.to(unit_1).value
        assert result.unit == angular_speed_1.unit


    @mark.error
    def test_raises_type_error(self, angular_speed_sub_type_error):
        with raises(TypeError):
            assert basic_angular_speed - angular_speed_sub_type_error


@mark.units
class TestAngularSpeedMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                               times()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        angular_speed = AngularSpeed(value = value, unit = unit)
        result = angular_speed*multiplier

        if isinstance(multiplier, Time):
            assert isinstance(result, AngularPosition)
            assert result.value == angular_speed.to('rad/s').value*multiplier.to('sec').value
            assert result.unit == 'rad'
        else:
            assert isinstance(result, AngularSpeed)
            assert result.value == angular_speed.value*multiplier
            assert result.unit == angular_speed.unit


    @mark.error
    def test_raises_type_error(self, angular_speed_mul_type_error):
        with raises(TypeError):
            assert basic_angular_speed*angular_speed_mul_type_error


@mark.units
class TestAngularSpeedRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                               times()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        angular_speed = AngularSpeed(value = value, unit = unit)
        result = multiplier*angular_speed

        if isinstance(multiplier, Time):
            assert isinstance(result, AngularPosition)
            assert result.value == angular_speed.to('rad/s').value*multiplier.to('sec').value
            assert result.unit == 'rad'
        else:
            assert isinstance(result, AngularSpeed)
            assert result.value == angular_speed.value*multiplier
            assert result.unit == angular_speed.unit


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method_patch(self, value, unit):
        angular_speed = AngularSpeed(value = value, unit = unit)

        class FakeTime(Time):

            def __mul__(self, other: AngularSpeed): return NotImplemented

        fake_multiplier = FakeTime(1, 'sec')
        result = fake_multiplier*angular_speed

        assert isinstance(result, AngularPosition)
        assert result.value == angular_speed.to('rad/s').value*fake_multiplier.to('sec').value
        assert result.unit == 'rad'


    @mark.error
    def test_raises_type_error(self, angular_speed_rmul_type_error):
        with raises(TypeError):
            assert angular_speed_rmul_type_error*basic_angular_speed


@mark.units
class TestAngularSpeedTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                            angular_speeds()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        angular_speed = AngularSpeed(value = value, unit = unit)

        if isinstance(divider, AngularSpeed):
            if abs(divider.value) >= 1e-300:
                result = angular_speed/divider
                assert isinstance(result, float)
                assert result == angular_speed.value/divider.to(unit).value
        else:
            if divider != 0:
                result = angular_speed/divider
                assert isinstance(result, AngularSpeed)
                assert result.value == angular_speed.value/divider
                assert result.unit == angular_speed.unit


    @mark.error
    def test_raises_type_error(self, angular_speed_truediv_type_error):
        with raises(TypeError):
            assert basic_angular_speed/angular_speed_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, angular_speed_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_angular_speed/angular_speed_truediv_zero_division_error


@mark.units
class TestAngularSpeedEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_speed_1 = AngularSpeed(value = value, unit = unit)
        angular_speed_2 = AngularSpeed(value = value, unit = unit)

        for target_unit in units_list:
            assert angular_speed_1 == angular_speed_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_speed_eq_type_error):
        with raises(TypeError):
            assert basic_angular_speed == angular_speed_eq_type_error


@mark.units
class TestAngularSpeedNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        angular_speed_1 = AngularSpeed(value = value, unit = unit)
        angular_speed_2 = AngularSpeed(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert angular_speed_1 != angular_speed_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_speed_ne_type_error):
        with raises(TypeError):
            assert basic_angular_speed != angular_speed_ne_type_error


@mark.units
class TestAngularSpeedGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        angular_speed_1 = AngularSpeed(value = value + gap, unit = unit)
        angular_speed_2 = AngularSpeed(value = value, unit = unit)

        for target_unit in units_list:
            assert angular_speed_1 > angular_speed_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_speed_gt_type_error):
        with raises(TypeError):
            assert basic_angular_speed > angular_speed_gt_type_error


@mark.units
class TestAngularSpeedGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        angular_speed_1 = AngularSpeed(value = value + gap, unit = unit)
        angular_speed_2 = AngularSpeed(value = value, unit = unit)

        for target_unit in units_list:
            assert angular_speed_1 >= angular_speed_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_speed_ge_type_error):
        with raises(TypeError):
            assert basic_angular_speed >= angular_speed_ge_type_error


@mark.units
class TestAngularSpeedLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            angular_speed_1 = AngularSpeed(value = value, unit = unit)
            angular_speed_2 = AngularSpeed(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert angular_speed_1 < angular_speed_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_speed_lt_type_error):
        with raises(TypeError):
            assert basic_angular_speed < angular_speed_lt_type_error


@mark.units
class TestAngularSpeedLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            angular_speed_1 = AngularSpeed(value = value, unit = unit)
            angular_speed_2 = AngularSpeed(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert angular_speed_1 <= angular_speed_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_speed_le_type_error):
        with raises(TypeError):
            assert basic_angular_speed <= angular_speed_le_type_error


@mark.units
class TestAngularSpeedTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if value != 0:
            angular_speed = AngularSpeed(value = value, unit = unit)

            for target_unit in units_list:
                converted_speed = angular_speed.to(target_unit = target_unit, inplace = inplace)

                assert converted_speed.unit == target_unit
                if target_unit != unit:
                    assert converted_speed.value != value
                    assert converted_speed.unit != unit

                    if inplace:
                        assert converted_speed.value == angular_speed.value
                        assert converted_speed.unit == angular_speed.unit
                    else:
                        assert converted_speed.value != angular_speed.value
                        assert converted_speed.unit != angular_speed.unit
                else:
                    assert converted_speed == angular_speed


    @mark.error
    def test_raises_type_error(self, angular_speed_to_type_error):
        with raises(TypeError):
            basic_angular_speed.to(**angular_speed_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_angular_speed.to(fake_unit)
