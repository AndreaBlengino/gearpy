from gearpy.units import AngularAcceleration, AngularSpeed, Time
from hypothesis.strategies import floats, sampled_from, one_of, booleans
from hypothesis import given, settings
from tests.test_units.test_angular_acceleration.conftest import basic_angular_acceleration, angular_accelerations, times
from pytest import mark, raises


units_list = list(AngularAcceleration._AngularAcceleration__UNITS.keys())


@mark.units
class TestAngularAccelerationInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_acceleration = AngularAcceleration(value = value, unit = unit)

        assert angular_acceleration.value == value
        assert angular_acceleration.unit == unit


    @mark.error
    def test_raises_type_error(self, angular_acceleration_init_type_error):
        with raises(TypeError):
            AngularAcceleration(**angular_acceleration_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                AngularAcceleration(value = 1, unit = fake_unit)


@mark.units
class TestAngularAccelerationRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_acceleration = AngularAcceleration(value = value, unit = unit)

        assert str(angular_acceleration) == f'{value} {unit}'


@mark.units
class TestAngularAccelerationAbs:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_acceleration = AngularAcceleration(value = value, unit = unit)

        assert abs(angular_acceleration) == AngularAcceleration(value = abs(value), unit = unit)
        assert abs(angular_acceleration).value >= 0


@mark.units
class TestAngularAccelerationAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        angular_acceleration_1 = AngularAcceleration(value = value_1, unit = unit_1)
        angular_acceleration_2 = AngularAcceleration(value = value_2, unit = unit_2)
        result = angular_acceleration_1 + angular_acceleration_2

        assert isinstance(result, AngularAcceleration)
        assert result.value == angular_acceleration_1.value + angular_acceleration_2.to(unit_1).value
        assert result.unit == angular_acceleration_1.unit


    @mark.error
    def test_raises_type_error(self, angular_acceleration_add_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration + angular_acceleration_add_type_error


@mark.units
class TestAngularAccelerationSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        angular_acceleration_1 = AngularAcceleration(value = value_1, unit = unit_1)
        angular_acceleration_2 = AngularAcceleration(value = value_2, unit = unit_2)
        result = angular_acceleration_1 - angular_acceleration_2

        assert isinstance(result, AngularAcceleration)
        assert result.value == angular_acceleration_1.value - angular_acceleration_2.to(unit_1).value
        assert result.unit == angular_acceleration_1.unit


    @mark.error
    def test_raises_type_error(self, angular_acceleration_sub_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration - angular_acceleration_sub_type_error


@mark.units
class TestAngularAccelerationMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                               times()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        angular_acceleration = AngularAcceleration(value = value, unit = unit)
        result = angular_acceleration*multiplier

        if isinstance(multiplier, Time):
            assert isinstance(result, AngularSpeed)
            assert result.value == angular_acceleration.to('rad/s^2').value*multiplier.to('sec').value
            assert result.unit == 'rad/s'
        else:
            assert isinstance(result, AngularAcceleration)
            assert result.value == angular_acceleration.value*multiplier
            assert result.unit == angular_acceleration.unit


    @mark.error
    def test_raises_type_error(self, angular_acceleration_mul_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration*angular_acceleration_mul_type_error


@mark.units
class TestAngularAccelerationRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                               times()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        angular_acceleration = AngularAcceleration(value = value, unit = unit)
        result = multiplier*angular_acceleration

        if isinstance(multiplier, Time):
            assert isinstance(result, AngularSpeed)
            assert result.value == angular_acceleration.to('rad/s^2').value*multiplier.to('sec').value
            assert result.unit == 'rad/s'
        else:
            assert isinstance(result, AngularAcceleration)
            assert result.value == angular_acceleration.value*multiplier
            assert result.unit == angular_acceleration.unit


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method_patch(self, value, unit):
        angular_acceleration = AngularAcceleration(value = value, unit = unit)

        class FakeTime(Time):

            def __mul__(self, other: AngularAcceleration): return NotImplemented

        fake_multiplier = FakeTime(1, 'sec')
        result = fake_multiplier*angular_acceleration

        assert isinstance(result, AngularSpeed)
        assert result.value == angular_acceleration.to('rad/s^2').value*fake_multiplier.to('sec').value
        assert result.unit == 'rad/s'


    @mark.error
    def test_raises_type_error(self, angular_acceleration_rmul_type_error):
        with raises(TypeError):
            assert angular_acceleration_rmul_type_error*basic_angular_acceleration


@mark.units
class TestAngularAccelerationTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                            angular_accelerations()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        angular_acceleration = AngularAcceleration(value = value, unit = unit)

        if isinstance(divider, AngularAcceleration):
            if abs(divider.value) >= 1e-300:
                result = angular_acceleration/divider
                assert isinstance(result, float)
                assert result == angular_acceleration.value/divider.to(unit).value
        else:
            if divider != 0:
                result = angular_acceleration/divider
                assert isinstance(result, AngularAcceleration)
                assert result.value == angular_acceleration.value/divider
                assert result.unit == angular_acceleration.unit


    @mark.error
    def test_raises_type_error(self, angular_acceleration_truediv_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration/angular_acceleration_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, angular_acceleration_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_angular_acceleration/angular_acceleration_truediv_zero_division_error


@mark.units
class TestAngularAccelerationEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        angular_acceleration_1 = AngularAcceleration(value = value, unit = unit)
        angular_acceleration_2 = AngularAcceleration(value = value, unit = unit)

        for target_unit in units_list:
            assert angular_acceleration_1 == angular_acceleration_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_acceleration_eq_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration == angular_acceleration_eq_type_error


@mark.units
class TestAngularAccelerationNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        angular_acceleration_1 = AngularAcceleration(value = value, unit = unit)
        angular_acceleration_2 = AngularAcceleration(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert angular_acceleration_1 != angular_acceleration_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_acceleration_ne_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration != angular_acceleration_ne_type_error


@mark.units
class TestAngularAccelerationGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        angular_acceleration_1 = AngularAcceleration(value = value + gap, unit = unit)
        angular_acceleration_2 = AngularAcceleration(value = value, unit = unit)

        for target_unit in units_list:
            assert angular_acceleration_1 > angular_acceleration_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_acceleration_gt_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration > angular_acceleration_gt_type_error


@mark.units
class TestAngularAccelerationGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        angular_acceleration_1 = AngularAcceleration(value = value + gap, unit = unit)
        angular_acceleration_2 = AngularAcceleration(value = value, unit = unit)

        for target_unit in units_list:
            assert angular_acceleration_1 >= angular_acceleration_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_acceleration_ge_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration >= angular_acceleration_ge_type_error


@mark.units
class TestAngularAccelerationLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            angular_acceleration_1 = AngularAcceleration(value = value, unit = unit)
            angular_acceleration_2 = AngularAcceleration(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert angular_acceleration_1 < angular_acceleration_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_acceleration_lt_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration < angular_acceleration_lt_type_error


@mark.units
class TestAngularAccelerationLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            angular_acceleration_1 = AngularAcceleration(value = value, unit = unit)
            angular_acceleration_2 = AngularAcceleration(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert angular_acceleration_1 <= angular_acceleration_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, angular_acceleration_le_type_error):
        with raises(TypeError):
            assert basic_angular_acceleration <= angular_acceleration_le_type_error


@mark.units
class TestAngularAccelerationTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            angular_acceleration = AngularAcceleration(value = value, unit = unit)

            for target_unit in units_list:
                converted_acceleration = angular_acceleration.to(target_unit = target_unit, inplace = inplace)

                assert converted_acceleration.unit == target_unit
                if AngularAcceleration._AngularAcceleration__UNITS[target_unit] != AngularAcceleration._AngularAcceleration__UNITS[unit]:
                    assert converted_acceleration.value != value
                    assert converted_acceleration.unit != unit

                    if inplace:
                        assert converted_acceleration.value == angular_acceleration.value
                        assert converted_acceleration.unit == angular_acceleration.unit
                    else:
                        assert converted_acceleration.value != angular_acceleration.value
                        assert converted_acceleration.unit != angular_acceleration.unit
                else:
                    assert converted_acceleration == angular_acceleration


    @mark.error
    def test_raises_type_error(self, angular_acceleration_to_type_error):
        with raises(TypeError):
            basic_angular_acceleration.to(**angular_acceleration_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_angular_acceleration.to(fake_unit)
