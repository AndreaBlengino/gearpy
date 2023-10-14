from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, Time
from hypothesis.strategies import floats, sampled_from, one_of, booleans
from hypothesis import given, settings
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_units.test_angular_acceleration.conftest import angular_accelerations
from tests.test_units.test_time.conftest import basic_time, times
from pytest import mark, raises


units_list = list(Time._Time__UNITS.keys())


@mark.units
class TestTimeInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        time = Time(value = value, unit = unit)

        assert time.value == value
        assert time.unit == unit


    @mark.error
    def test_raises_type_error(self, time_init_type_error):
        with raises(TypeError):
            Time(**time_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                Time(value = 1, unit = fake_unit)


@mark.units
class TestTimeRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        time = Time(value = value, unit = unit)

        assert str(time) == f'{value} {unit}'



@mark.units
class TestTimeAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        time_1 = Time(value = value_1, unit = unit_1)
        time_2 = Time(value = value_2, unit = unit_2)
        result = time_1 + time_2

        assert isinstance(result, Time)
        assert result.value == time_1.value + time_2.to(unit_1).value
        assert result.unit == time_1.unit


    @mark.error
    def test_raises_type_error(self, time_add_type_error):
        with raises(TypeError):
            assert basic_time + time_add_type_error


@mark.units
class TestTimeSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        time_1 = Time(value = value_1, unit = unit_1)
        time_2 = Time(value = value_2, unit = unit_2)
        result = time_1 - time_2

        assert isinstance(result, Time)
        assert result.value == time_1.value - time_2.to(unit_1).value
        assert result.unit == time_1.unit


    @mark.error
    def test_raises_type_error(self, time_sub_type_error):
        with raises(TypeError):
            assert basic_time - time_sub_type_error


@mark.units
class TestTimeMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                               angular_speeds(),
                               angular_accelerations()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        time = Time(value = value, unit = unit)
        result = time*multiplier

        if isinstance(multiplier, AngularAcceleration):
            assert isinstance(result, AngularSpeed)
            assert result.value == time.to('sec').value*multiplier.to('rad/s^2').value
            assert result.unit == 'rad/s'
        elif isinstance(multiplier, AngularSpeed):
            assert isinstance(result, AngularPosition)
            assert result.value == time.to('sec').value*multiplier.to('rad/s').value
            assert result.unit == 'rad'
        else:
            assert isinstance(result, Time)
            assert result.value == time.value*multiplier
            assert result.unit == time.unit


    @mark.error
    def test_raises_type_error(self, time_mul_type_error):
        with raises(TypeError):
            assert basic_time*time_mul_type_error


@mark.units
class TestTimeRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                               angular_speeds(),
                               angular_accelerations()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        time = Time(value = value, unit = unit)
        result = multiplier*time

        if isinstance(multiplier, AngularAcceleration):
            assert isinstance(result, AngularSpeed)
            assert result.value == time.to('sec').value*multiplier.to('rad/s^2').value
            assert result.unit == 'rad/s'
        elif isinstance(multiplier, AngularSpeed):
            assert isinstance(result, AngularPosition)
            assert result.value == time.to('sec').value*multiplier.to('rad/s').value
            assert result.unit == 'rad'
        else:
            assert isinstance(result, Time)
            assert result.value == time.value*multiplier
            assert result.unit == time.unit


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method_patch_1(self, value, unit):
        time = Time(value = value, unit = unit)

        class FakeAngularAcceleration(AngularAcceleration):

            def __mul__(self, other: Time): return NotImplemented

        fake_multiplier = FakeAngularAcceleration(1, 'rad/s^2')
        result = fake_multiplier*time

        assert isinstance(result, AngularSpeed)
        assert result.value == time.to('sec').value*fake_multiplier.to('rad/s^2').value
        assert result.unit == 'rad/s'


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method_patch_2(self, value, unit):
        time = Time(value = value, unit = unit)

        class FakeAngularSpeed(AngularSpeed):

            def __mul__(self, other: Time): return NotImplemented

        fake_multiplier = FakeAngularSpeed(1, 'rad/s')
        result = fake_multiplier*time

        assert isinstance(result, AngularPosition)
        assert result.value == time.to('sec').value*fake_multiplier.to('rad/s').value
        assert result.unit == 'rad'


    @mark.error
    def test_raises_type_error(self, time_rmul_type_error):
        with raises(TypeError):
            assert time_rmul_type_error*basic_time


@mark.units
class TestTimeTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                            times()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        time = Time(value = value, unit = unit)

        if isinstance(divider, Time):
            if abs(divider.value) >= 1e-300:
                result = time/divider
                assert isinstance(result, float)
                assert result == time.value/divider.to(unit).value
        else:
            if divider != 0:
                result = time/divider
                assert isinstance(result, Time)
                assert result.value == time.value/divider
                assert result.unit == time.unit


    @mark.error
    def test_raises_type_error(self, time_truediv_type_error):
        with raises(TypeError):
            assert basic_time/time_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, time_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_time/time_truediv_zero_division_error


@mark.units
class TestTimeEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        time_1 = Time(value = value, unit = unit)
        time_2 = Time(value = value, unit = unit)

        for target_unit in units_list:
            assert time_1 == time_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_eq_type_error):
        with raises(TypeError):
            assert basic_time == time_eq_type_error


@mark.units
class TestTimeNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        time_1 = Time(value = value, unit = unit)
        time_2 = Time(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert time_1 != time_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_ne_type_error):
        with raises(TypeError):
            assert basic_time != time_ne_type_error


@mark.units
class TestTimeGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        time_1 = Time(value = value + gap, unit = unit)
        time_2 = Time(value = value, unit = unit)

        for target_unit in units_list:
            assert time_1 > time_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_gt_type_error):
        with raises(TypeError):
            assert basic_time > time_gt_type_error


@mark.units
class TestTimeGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        time_1 = Time(value = value + gap, unit = unit)
        time_2 = Time(value = value, unit = unit)

        for target_unit in units_list:
            assert time_1 >= time_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_ge_type_error):
        with raises(TypeError):
            assert basic_time >= time_ge_type_error


@mark.units
class TestTimeLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            time_1 = Time(value = value, unit = unit)
            time_2 = Time(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert time_1 < time_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_lt_type_error):
        with raises(TypeError):
            assert basic_time < time_lt_type_error


@mark.units
class TestTimeLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            time_1 = Time(value = value, unit = unit)
            time_2 = Time(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert time_1 <= time_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, time_le_type_error):
        with raises(TypeError):
            assert basic_time <= time_le_type_error


@mark.units
class TestTimeTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if value != 0:
            time = Time(value = value, unit = unit)

            for target_unit in units_list:
                converted_time = time.to(target_unit = target_unit, inplace = inplace)

                assert converted_time.unit == target_unit
                if target_unit != unit:
                    assert converted_time.value != value
                    assert converted_time.unit != unit

                    if inplace:
                        assert converted_time.value == time.value
                        assert converted_time.unit == time.unit
                    else:
                        assert converted_time.value != time.value
                        assert converted_time.unit != time.unit
                else:
                    assert converted_time == time


    @mark.error
    def test_raises_type_error(self, time_to_type_error):
        with raises(TypeError):
            basic_time.to(**time_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_time.to(fake_unit)
