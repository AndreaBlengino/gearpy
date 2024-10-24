from gearpy.units import Current
from hypothesis.strategies import (
    floats,
    sampled_from,
    one_of,
    booleans,
    integers
)
from hypothesis import given, settings
from tests.test_units.test_current.conftest import basic_current, currents
from pytest import mark, raises


units_list = list(Current._Current__UNITS.keys())


@mark.units
class TestCurrentInit:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit):
        current = Current(value=value, unit=unit)

        assert current.value == value
        assert current.unit == unit

    @mark.error
    def test_raises_type_error(self, current_init_type_error):
        with raises(TypeError):
            Current(**current_init_type_error)

    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                Current(value=1, unit=fake_unit)


@mark.units
class TestCurrentRepr:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit):
        current = Current(value=value, unit=unit)

        assert str(current) == f'{value} {unit}'


@mark.units
class TestCurrentFormat:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list),
        total_digits=integers(min_value=1, max_value=10),
        decimal_digits=integers(min_value=1, max_value=10)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, total_digits, decimal_digits):
        current = Current(value=value, unit=unit)

        assert current.__format__(
            f'{total_digits}.{decimal_digits}f'
        ) == f'{current:{total_digits}.{decimal_digits}f}'


@mark.units
class TestCurrentAbs:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit):
        current = Current(value=value, unit=unit)

        assert abs(current) == Current(value=abs(value), unit=unit)
        assert abs(current).value >= 0


@mark.units
class TestCurrentNeg:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit):
        current = Current(value=value, unit=unit)

        assert -current == Current(value=-value, unit=unit)


@mark.units
class TestCurrentAdd:

    @mark.genuine
    @given(
        value_1=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit_1=sampled_from(elements=units_list),
        value_2=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit_2=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        current_1 = Current(value=value_1, unit=unit_1)
        current_2 = Current(value=value_2, unit=unit_2)
        result = current_1 + current_2

        assert isinstance(result, Current)
        assert result.value == current_1.value + current_2.to(unit_1).value
        assert result.unit == current_1.unit

    @mark.error
    def test_raises_type_error(self, current_add_type_error):
        with raises(TypeError):
            assert basic_current + current_add_type_error


@mark.units
class TestCurrentSub:

    @mark.genuine
    @given(
        value_1=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit_1=sampled_from(elements=units_list),
        value_2=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit_2=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        current_1 = Current(value=value_1, unit=unit_1)
        current_2 = Current(value=value_2, unit=unit_2)
        result = current_1 - current_2

        assert isinstance(result, Current)
        assert result.value == current_1.value - current_2.to(unit_1).value
        assert result.unit == current_1.unit

    @mark.error
    def test_raises_type_error(self, current_sub_type_error):
        with raises(TypeError):
            assert basic_current - current_sub_type_error


@mark.units
class TestCurrentMul:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list),
        multiplier=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, multiplier):
        current = Current(value=value, unit=unit)
        result = current*multiplier

        assert isinstance(result, Current)
        assert result.value == current.value*multiplier
        assert result.unit == current.unit

    @mark.error
    def test_raises_type_error(self, current_mul_type_error):
        with raises(TypeError):
            assert basic_current*current_mul_type_error


@mark.units
class TestCurrentRmul:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list),
        multiplier=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, multiplier):
        current = Current(value=value, unit=unit)
        result = multiplier*current

        assert isinstance(result, Current)
        assert result.value == current.value*multiplier
        assert result.unit == current.unit

    @mark.error
    def test_raises_type_error(self, current_rmul_type_error):
        with raises(TypeError):
            assert current_rmul_type_error*basic_current


@mark.units
class TestCurrentTruediv:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list),
        divider=one_of(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=-1000,
                max_value=1000
            ),
            currents()
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, divider):
        current = Current(value=value, unit=unit)

        if isinstance(divider, Current):
            if abs(divider.value) >= 1e-300:
                result = current/divider
                assert isinstance(result, float)
                assert result == current.value/divider.to(unit).value
        else:
            if divider != 0:
                result = current/divider
                assert isinstance(result, Current)
                assert result.value == current.value/divider
                assert result.unit == current.unit

    @mark.error
    def test_raises_type_error(self, current_truediv_type_error):
        with raises(TypeError):
            assert basic_current/current_truediv_type_error

    @mark.error
    def test_raises_zero_division_error(
        self,
        current_truediv_zero_division_error
    ):
        with raises(ZeroDivisionError):
            assert basic_current/current_truediv_zero_division_error


@mark.units
class TestCurrentEq:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            max_value=1000,
            min_value=-1000
        ),
        unit=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit):
        current_1 = Current(value=value, unit=unit)
        current_2 = Current(value=value, unit=unit)

        for target_unit in units_list:
            assert current_1 == current_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, current_eq_type_error):
        with raises(TypeError):
            assert basic_current == current_eq_type_error


@mark.units
class TestCurrentNe:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            max_value=1000,
            min_value=-1000
        ),
        unit=sampled_from(elements=units_list),
        gap=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, gap):
        current_1 = Current(value=value, unit=unit)
        current_2 = Current(value=value + gap, unit=unit)

        for target_unit in units_list:
            assert current_1 != current_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, current_ne_type_error):
        with raises(TypeError):
            assert basic_current != current_ne_type_error


@mark.units
class TestCurrentGt:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            max_value=1000,
            min_value=-1000
        ),
        unit=sampled_from(elements=units_list),
        gap=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, gap):
        current_1 = Current(value=value + gap, unit=unit)
        current_2 = Current(value=value, unit=unit)

        for target_unit in units_list:
            assert current_1 > current_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, current_gt_type_error):
        with raises(TypeError):
            assert basic_current > current_gt_type_error


@mark.units
class TestCurrentGe:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            max_value=1000,
            min_value=-1000
        ),
        unit=sampled_from(elements=units_list),
        gap=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0,
            exclude_min=False,
            max_value=1000
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, gap):
        current_1 = Current(value=value + gap, unit=unit)
        current_2 = Current(value=value, unit=unit)

        for target_unit in units_list:
            assert current_1 >= current_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, current_ge_type_error):
        with raises(TypeError):
            assert basic_current >= current_ge_type_error


@mark.units
class TestCurrentLt:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            max_value=1000,
            min_value=-1000
        ),
        unit=sampled_from(elements=units_list),
        gap=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, gap):
        if value != 0:
            current_1 = Current(value=value, unit=unit)
            current_2 = Current(value=value + gap, unit=unit)

            for target_unit in units_list:
                assert current_1 < current_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, current_lt_type_error):
        with raises(TypeError):
            assert basic_current < current_lt_type_error


@mark.units
class TestCurrentLe:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            max_value=1000,
            min_value=-1000
        ),
        unit=sampled_from(elements=units_list),
        gap=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0,
            exclude_min=False,
            max_value=1000
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, gap):
        if value != 0:
            current_1 = Current(value=value, unit=unit)
            current_2 = Current(value=value + gap, unit=unit)

            for target_unit in units_list:
                assert current_1 <= current_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, current_le_type_error):
        with raises(TypeError):
            assert basic_current <= current_le_type_error


@mark.units
class TestCurrentTo:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            max_value=1000,
            min_value=-1000
        ),
        unit=sampled_from(elements=units_list),
        inplace=booleans()
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            current = Current(value=value, unit=unit)

            for target_unit in units_list:
                converted_current = current.to(
                    target_unit=target_unit,
                    inplace=inplace
                )

                assert converted_current.unit == target_unit
                if Current._Current__UNITS[target_unit] != \
                        Current._Current__UNITS[unit]:
                    assert converted_current.value != value
                    assert converted_current.unit != unit

                    if inplace:
                        assert converted_current.value == current.value
                        assert converted_current.unit == current.unit
                    else:
                        assert converted_current.value != current.value
                        assert converted_current.unit != current.unit
                else:
                    assert converted_current == current

    @mark.error
    def test_raises_type_error(self, current_to_type_error):
        with raises(TypeError):
            basic_current.to(**current_to_type_error)

    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_current.to(fake_unit)
