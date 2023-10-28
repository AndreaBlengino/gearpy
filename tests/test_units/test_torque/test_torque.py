from gearpy.units import AngularAcceleration, InertiaMoment, Torque
from hypothesis.strategies import floats, sampled_from, one_of, booleans
from hypothesis import given, settings
from tests.test_units.test_inertia_moment.conftest import inertia_moments
from tests.test_units.test_torque.conftest import basic_torque, torques
from pytest import mark, raises


units_list = list(Torque._Torque__UNITS.keys())


@mark.units
class TestTorqueInit:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        torque = Torque(value = value, unit = unit)

        assert torque.value == value
        assert torque.unit == unit


    @mark.error
    def test_raises_type_error(self, torque_init_type_error):
        with raises(TypeError):
            Torque(**torque_init_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                Torque(value = 1, unit = fake_unit)


@mark.units
class TestTorqueRepr:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        torque = Torque(value = value, unit = unit)

        assert str(torque) == f'{value} {unit}'



@mark.units
class TestTorqueAdd:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        torque_1 = Torque(value = value_1, unit = unit_1)
        torque_2 = Torque(value = value_2, unit = unit_2)
        result = torque_1 + torque_2

        assert isinstance(result, Torque)
        assert result.value == torque_1.value + torque_2.to(unit_1).value
        assert result.unit == torque_1.unit


    @mark.error
    def test_raises_type_error(self, torque_add_type_error):
        with raises(TypeError):
            assert basic_torque + torque_add_type_error


@mark.units
class TestTorqueSub:


    @mark.genuine
    @given(value_1 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_1 = sampled_from(elements = units_list),
           value_2 = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit_2 = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        torque_1 = Torque(value = value_1, unit = unit_1)
        torque_2 = Torque(value = value_2, unit = unit_2)
        result = torque_1 - torque_2

        assert isinstance(result, Torque)
        assert result.value == torque_1.value - torque_2.to(unit_1).value
        assert result.unit == torque_1.unit


    @mark.error
    def test_raises_type_error(self, torque_sub_type_error):
        with raises(TypeError):
            assert basic_torque - torque_sub_type_error


@mark.units
class TestTorqueMul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        torque = Torque(value = value, unit = unit)
        result = torque*multiplier

        assert isinstance(result, Torque)
        assert result.value == torque.value*multiplier
        assert result.unit == torque.unit


    @mark.error
    def test_raises_type_error(self, torque_mul_type_error):
        with raises(TypeError):
            assert basic_torque*torque_mul_type_error


@mark.units
class TestTorqueRmul:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           multiplier = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, multiplier):
        torque = Torque(value = value, unit = unit)
        result = multiplier*torque

        assert isinstance(result, Torque)
        assert result.value == torque.value*multiplier
        assert result.unit == torque.unit


    @mark.error
    def test_raises_type_error(self, torque_rmul_type_error):
        with raises(TypeError):
            assert torque_rmul_type_error*basic_torque


@mark.units
class TestTorqueTruediv:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
           unit = sampled_from(elements = units_list),
           divider = one_of(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000),
                            torques(),
                            inertia_moments()))
    @settings(max_examples = 100)
    def test_method(self, value, unit, divider):
        torque = Torque(value = value, unit = unit)

        if isinstance(divider, Torque):
            if abs(divider.value) >= 1e-300:
                result = torque/divider
                assert isinstance(result, float)
                assert result == torque.value/divider.to(unit).value
        elif isinstance(divider, InertiaMoment):
            if abs(divider.value) >= 1e-300:
                result = torque/divider
                assert isinstance(result, AngularAcceleration)
                assert result.value == torque.to('Nm').value/divider.to('kgm^2').value
                assert result.unit == 'rad/s^2'
        else:
            if divider != 0:
                result = torque/divider
                assert isinstance(result, Torque)
                assert result.value == torque.value/divider
                assert result.unit == torque.unit


    @mark.error
    def test_raises_type_error(self, torque_truediv_type_error):
        with raises(TypeError):
            assert basic_torque/torque_truediv_type_error


    @mark.error
    def test_raises_zero_division_error(self, torque_truediv_zero_division_error):
        with raises(ZeroDivisionError):
            assert basic_torque/torque_truediv_zero_division_error


@mark.units
class TestTorqueEq:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list))
    @settings(max_examples = 100)
    def test_method(self, value, unit):
        torque_1 = Torque(value = value, unit = unit)
        torque_2 = Torque(value = value, unit = unit)

        for target_unit in units_list:
            assert torque_1 == torque_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, torque_eq_type_error):
        with raises(TypeError):
            assert basic_torque == torque_eq_type_error


@mark.units
class TestTorqueNe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        torque_1 = Torque(value = value, unit = unit)
        torque_2 = Torque(value = value + gap, unit = unit)

        for target_unit in units_list:
            assert torque_1 != torque_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, torque_ne_type_error):
        with raises(TypeError):
            assert basic_torque != torque_ne_type_error


@mark.units
class TestTorqueGt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        torque_1 = Torque(value = value + gap, unit = unit)
        torque_2 = Torque(value = value, unit = unit)

        for target_unit in units_list:
            assert torque_1 > torque_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, torque_gt_type_error):
        with raises(TypeError):
            assert basic_torque > torque_gt_type_error


@mark.units
class TestTorqueGe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        torque_1 = Torque(value = value + gap, unit = unit)
        torque_2 = Torque(value = value, unit = unit)

        for target_unit in units_list:
            assert torque_1 >= torque_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, torque_ge_type_error):
        with raises(TypeError):
            assert basic_torque >= torque_ge_type_error


@mark.units
class TestTorqueLt:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            torque_1 = Torque(value = value, unit = unit)
            torque_2 = Torque(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert torque_1 < torque_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, torque_lt_type_error):
        with raises(TypeError):
            assert basic_torque < torque_lt_type_error


@mark.units
class TestTorqueLe:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           gap = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = False, max_value = 1000))
    @settings(max_examples = 100)
    def test_method(self, value, unit, gap):
        if value != 0:
            torque_1 = Torque(value = value, unit = unit)
            torque_2 = Torque(value = value + gap, unit = unit)

            for target_unit in units_list:
                assert torque_1 <= torque_2.to(target_unit)


    @mark.error
    def test_raises_type_error(self, torque_le_type_error):
        with raises(TypeError):
            assert basic_torque <= torque_le_type_error


@mark.units
class TestTorqueTo:


    @mark.genuine
    @given(value = floats(allow_nan = False, allow_infinity = False, max_value = 1000, min_value = -1000),
           unit = sampled_from(elements = units_list),
           inplace = booleans())
    @settings(max_examples = 100)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            torque = Torque(value = value, unit = unit)

            for target_unit in units_list:
                converted_torque = torque.to(target_unit = target_unit, inplace = inplace)

                assert converted_torque.unit == target_unit
                if Torque._Torque__UNITS[target_unit] != Torque._Torque__UNITS[unit]:
                    assert converted_torque.value != value
                    assert converted_torque.unit != unit

                    if inplace:
                        assert converted_torque.value == torque.value
                        assert converted_torque.unit == torque.unit
                    else:
                        assert converted_torque.value != torque.value
                        assert converted_torque.unit != torque.unit
                else:
                    assert converted_torque == torque


    @mark.error
    def test_raises_type_error(self, torque_to_type_error):
        with raises(TypeError):
            basic_torque.to(**torque_to_type_error)


    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_torque.to(fake_unit)
