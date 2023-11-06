from gearpy.units import Force
from hypothesis.strategies import floats, sampled_from, one_of, booleans
from hypothesis import given, settings
from tests.test_units.test_force.conftest import basic_force, forces
from pytest import mark, raises


units_list = list(Force._Force__UNITS.keys())


@mark.units
class TestForceInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        force = Force(value = value, unit = unit)

        assert force.value == value
        assert force.unit == unit


    @mark.error
    def test_raises_type_error(self, force_init_type_error):
        with raises(TypeError):
            Force(**force_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                Force(value = 1, unit = fake_unit)


@mark.units
class TestForceRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        force = Force(value = value, unit = unit)

        assert str(force) == f'{value} {unit}'


@mark.units
class TestForceAbs:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        force = Force(value = value, unit = unit)

        assert abs(force) == Force(value = abs(value), unit = unit)
        assert abs(force).value >= 0


@mark.units
class TestForceAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        force_1 = Force(value = value_1, unit = unit_1)
        force_2 = Force(value = value_2, unit = unit_2)
        result = force_1 + force_2

        assert isinstance(result, Force)
        assert result.value == force_1.value + force_2.to(unit_1).value
        assert result.unit == force_1.unit


    @mark.error
    def test_raises_type_error(self, force_add_type_error):
        with raises(TypeError):
            assert basic_force + force_add_type_error


@mark.units
class TestForceSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        force_1 = Force(value = value_1, unit = unit_1)
        force_2 = Force(value = value_2, unit = unit_2)
        result = force_1 - force_2

        assert isinstance(result, Force)
        assert result.value == force_1.value - force_2.to(unit_1).value
        assert result.unit == force_1.unit


    @mark.error
    def test_raises_type_error(self, force_sub_type_error):
        with raises(TypeError):
            assert basic_force - force_sub_type_error


@mark.units
class TestForceMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        force = Force(value = value, unit = unit)
        result = force*multiplier

        assert isinstance(result, Force)
        assert result.value == force.value*multiplier
        assert result.unit == force.unit


    @mark.error
    def test_raises_type_error(self, force_mul_type_error):
        with raises(TypeError):
            assert basic_force*force_mul_type_error


@mark.units
class TestForceRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        force = Force(value = value, unit = unit)
        result = multiplier*force

        assert isinstance(result, Force)
        assert result.value == force.value*multiplier
        assert result.unit == force.unit


    @mark.error
    def test_raises_type_error(self, force_rmul_type_error):
        with raises(TypeError):
            assert force_rmul_type_error*basic_force


@mark.units
class TestForceTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                            forces()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        torque = Force(value = value, unit = unit)

        if isinstance(divider, Force):
            if abs(divider.value) >= 1e-300:
                result = torque/divider
                assert isinstance(result, float)
                assert result == torque.value/divider.to(unit).value
        else:
            if divider != 0:
                result = torque/divider
                assert isinstance(result, Force)
                assert result.value == torque.value/divider
                assert result.unit == torque.unit


    @mark.error
    def test_raises_type_error(self, force_truediv_type_error):
        with raises(TypeError):
            assert basic_force/force_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, force_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_force/force_truediv_zero_division_error


@mark.units
class TestForceEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        force_1 = Force(value = value, unit = unit)
        force_2 = Force(value = value, unit = unit)

        for target_unit in units_list:
            assert force_1 == force_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, force_eq_type_error):
        with raises(TypeError):
            assert basic_force == force_eq_type_error


@mark.units
class TestForceNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        force_1 = Force(value = value, unit = unit)
        force_2 = Force(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert force_1 != force_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, force_ne_type_error):
        with raises(TypeError):
            assert basic_force != force_ne_type_error


@mark.units
class TestForceGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        force_1 = Force(value = value + gap, unit = unit)
        force_2 = Force(value = value, unit = unit)

        for target_unit in units_list:
            assert force_1 > force_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, force_gt_type_error):
        with raises(TypeError):
            assert basic_force > force_gt_type_error


@mark.units
class TestForceGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        force_1 = Force(value = value + gap, unit = unit)
        force_2 = Force(value = value, unit = unit)

        for target_unit in units_list:
            assert force_1 >= force_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, force_ge_type_error):
        with raises(TypeError):
            assert basic_force >= force_ge_type_error


@mark.units
class TestForceLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            force_1 = Force(value = value, unit = unit)
            force_2 = Force(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert force_1 < force_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, force_lt_type_error):
        with raises(TypeError):
            assert basic_force < force_lt_type_error


@mark.units
class TestForceLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            force_1 = Force(value = value, unit = unit)
            force_2 = Force(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert force_1 <= force_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, force_le_type_error):
        with raises(TypeError):
            assert basic_force <= force_le_type_error


@mark.units
class TestForceTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            force = Force(value = value, unit = unit)

            for target_unit in units_list:
                converted_force = force.to(target_unit = target_unit, inplace = inplace)

                assert converted_force.unit == target_unit
                if Force._Force__UNITS[target_unit] != Force._Force__UNITS[unit]:
                    assert converted_force.value != value
                    assert converted_force.unit != unit

                    if inplace:
                        assert converted_force.value == force.value
                        assert converted_force.unit == force.unit
                    else:
                        assert converted_force.value != force.value
                        assert converted_force.unit != force.unit
                else:
                    assert converted_force == force


    @mark.error
    def test_raises_type_error(self, force_to_type_error):
        with raises(TypeError):
            basic_force.to(**force_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_force.to(fake_unit)
