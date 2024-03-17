from gearpy.units import Time, TimeInterval
from hypothesis.strategies import floats, sampled_from, one_of, booleans, integers
from hypothesis import given, settings
from tests.conftest import time_intervals
from tests.test_units.test_time_interval.conftest import basic_time_interval
from pytest import mark, raises


units_list = list(TimeInterval._Time__UNITS.keys())


@mark.units
class TestTimeIntervalInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit):
        time_interval = TimeInterval(value = value, unit = unit)

        assert time_interval.value == value
        assert time_interval.unit == unit


    @mark.error
    def test_raises_type_error(self, time_interval_init_type_error):
        with raises(TypeError):
            TimeInterval(**time_interval_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                TimeInterval(value = 1, unit = fake_unit)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            TimeInterval(value = -1, unit = 'sec')


@mark.units
class TestTimeIntervalRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit):
        time_interval = TimeInterval(value = value, unit = unit)

        assert str(time_interval) == f'{value} {unit}'


@mark.units
class TestTimeIntervalFormat:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           total_digits = integers(min_value = 1, max_value = 10),
           decimal_digits = integers(min_value = 1, max_value = 10))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, total_digits, decimal_digits):
        time_interval = TimeInterval(value = value, unit = unit)

        assert time_interval.__format__(f'{total_digits}.{decimal_digits}f') == f'{time_interval:{total_digits}.{decimal_digits}f}'


@mark.units
class TestTimeIntervalAbs:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit):
        time_interval = TimeInterval(value = value, unit = unit)

        assert abs(time_interval) == TimeInterval(value = abs(value), unit = unit)
        assert abs(time_interval).value >= 0


@mark.units
class TestTimeIntervalNeg:


    @mark.error
    def test_method(self):
        time_interval = TimeInterval(value = 1, unit = 'sec')

        with raises(ValueError):
            assert -time_interval


@mark.units
class TestTimeIntervalAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        time_interval_1 = TimeInterval(value = value_1, unit = unit_1)
        time_interval_2 = TimeInterval(value = value_2, unit = unit_2)
        time = Time(value = value_2, unit = unit_2)
        result_1 = time_interval_1 + time_interval_2
        result_2 = time_interval_1 + time

        assert isinstance(result_1, TimeInterval)
        assert result_1.value == time_interval_1.value + time_interval_2.to(unit_1).value
        assert result_1.unit == time_interval_1.unit
        assert isinstance(result_2, Time)
        assert result_2.value == time_interval_1.value + time.to(unit_1).value
        assert result_2.unit == time_interval_1.unit


    @mark.error
    def test_raises_type_error(self, time_interval_add_type_error):
        with raises(TypeError):
            assert basic_time_interval + time_interval_add_type_error


@mark.units
class TestTimeIntervalSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        time_interval_1 = TimeInterval(value = value_1, unit = unit_1)
        time_interval_2 = TimeInterval(value = value_2, unit = unit_2)
        time = Time(value = value_2, unit = unit_2)

        if time_interval_1 > time_interval_2:
            result_1 = time_interval_1 - time_interval_2

            assert isinstance(result_1, TimeInterval)
            assert result_1.value == time_interval_1.value - time_interval_2.to(unit_1).value
            assert result_1.unit == time_interval_1.unit

        if time_interval_1 > time:
            result_2 = time_interval_1 - time

            assert isinstance(result_2, Time)
            assert result_2.value == time_interval_1.value + time.to(unit_1).value
            assert result_2.unit == time_interval_1.unit


    @mark.error
    def test_raises_type_error(self, time_interval_sub_type_error):
        with raises(TypeError):
            assert basic_time_interval - time_interval_sub_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_time_interval - TimeInterval(basic_time_interval.value + 1, basic_time_interval.unit)


@mark.units
class TestTimeIntervalMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, multiplier):
        time_interval = TimeInterval(value = value, unit = unit)
        result = time_interval*multiplier

        assert isinstance(result, TimeInterval)
        assert result.value == time_interval.value*multiplier
        assert result.unit == time_interval.unit


    @mark.error
    def test_raises_type_error(self, time_interval_mul_type_error):
        with raises(TypeError):
            assert basic_time_interval*time_interval_mul_type_error


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_time_interval*(-1)


@mark.units
class TestTimeIntervalRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, multiplier):
        time_interval = TimeInterval(value = value, unit = unit)
        result = multiplier*time_interval

        assert isinstance(result, TimeInterval)
        assert result.value == time_interval.value*multiplier
        assert result.unit == time_interval.unit


    @mark.error
    def test_raises_type_error(self, time_interval_rmul_type_error):
        with raises(TypeError):
            assert time_interval_rmul_type_error*basic_time_interval


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert -1*basic_time_interval


@mark.units
class TestTimeIntervalTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
                            time_intervals()))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, divider):
        time_interval = TimeInterval(value = value, unit = unit)

        if isinstance(divider, TimeInterval):
            if abs(divider.value) >= 1e-300:
                result = time_interval/divider
                assert isinstance(result, float)
                assert result == time_interval.value/divider.to(unit).value
        else:
            if divider != 0:
                result = time_interval/divider
                assert isinstance(result, TimeInterval)
                assert result.value == time_interval.value/divider
                assert result.unit == time_interval.unit


    @mark.error
    def test_raises_type_error(self, time_interval_truediv_type_error):
        with raises(TypeError):
            assert basic_time_interval/time_interval_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, time_interval_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_time_interval/time_interval_truediv_zero_division_error


@mark.units
class TestTimeIntervalEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit):
        time_interval_1 = TimeInterval(value = value, unit = unit)
        time_interval_2 = TimeInterval(value = value, unit = unit)

        for target_unit in units_list:
            assert time_interval_1 == time_interval_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_interval_eq_type_error):
        with raises(TypeError):
            assert basic_time_interval == time_interval_eq_type_error


@mark.units
class TestTimeIntervalNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        time_interval_1 = TimeInterval(value = value, unit = unit)
        time_interval_2 = TimeInterval(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert time_interval_1 != time_interval_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_interval_ne_type_error):
        with raises(TypeError):
            assert basic_time_interval != time_interval_ne_type_error


@mark.units
class TestTimeIntervalGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        time_interval_1 = TimeInterval(value = value + gap, unit = unit)
        time_interval_2 = TimeInterval(value = value, unit = unit)

        for target_unit in units_list:
            assert time_interval_1 > time_interval_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_interval_gt_type_error):
        with raises(TypeError):
            assert basic_time_interval > time_interval_gt_type_error


@mark.units
class TestTimeIntervalGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        time_interval_1 = TimeInterval(value = value + gap, unit = unit)
        time_interval_2 = TimeInterval(value = value, unit = unit)

        for target_unit in units_list:
            assert time_interval_1 >= time_interval_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_interval_ge_type_error):
        with raises(TypeError):
            assert basic_time_interval >= time_interval_ge_type_error


@mark.units
class TestTimeIntervalLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        if value != 0:
            time_interval_1 = TimeInterval(value = value, unit = unit)
            time_interval_2 = TimeInterval(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert time_interval_1 < time_interval_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_interval_lt_type_error):
        with raises(TypeError):
            assert basic_time_interval < time_interval_lt_type_error


@mark.units
class TestTimeIntervalLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, gap):
        if value != 0:
            time_interval_1 = TimeInterval(value = value, unit = unit)
            time_interval_2 = TimeInterval(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert time_interval_1 <= time_interval_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_interval_le_type_error):
        with raises(TypeError):
            assert basic_time_interval <= time_interval_le_type_error


@mark.units
class TestTimeIntervalTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            time_interval = TimeInterval(value = value, unit = unit)

            for target_unit in units_list:
                converted_time_interval = time_interval.to(target_unit = target_unit, inplace = inplace)

                assert converted_time_interval.unit == target_unit
                if TimeInterval._Time__UNITS[target_unit] != TimeInterval._Time__UNITS[unit]:
                    assert converted_time_interval.value != value
                    assert converted_time_interval.unit != unit

                    if inplace:
                        assert converted_time_interval.value == time_interval.value
                        assert converted_time_interval.unit == time_interval.unit
                    else:
                        assert converted_time_interval.value != time_interval.value
                        assert converted_time_interval.unit != time_interval.unit
                else:
                    assert converted_time_interval == time_interval


    @mark.error
    def test_raises_type_error(self, time_interval_to_type_error):
        with raises(TypeError):
            basic_time_interval.to(**time_interval_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_time_interval.to(fake_unit)
