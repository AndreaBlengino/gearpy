from gearpy.units import Length, Surface
from hypothesis.strategies import (
    floats,
    sampled_from,
    one_of,
    booleans,
    integers
)
from hypothesis import given, settings
from tests.test_units.test_length.conftest import basic_length, lengths
from pytest import mark, raises


units_list = list(Length._Length__UNITS.keys())


@mark.units
class TestLengthInit:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0,
            exclude_min=True,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit):
        length = Length(value=value, unit=unit)

        assert length.value == value
        assert length.unit == unit

    @mark.error
    def test_raises_type_error(self, length_init_type_error):
        with raises(TypeError):
            Length(**length_init_type_error)

    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                Length(value=1, unit=fake_unit)

    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            Length(value=-1, unit='m')


@mark.units
class TestLengthRepr:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0,
            exclude_min=True,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit):
        length = Length(value=value, unit=unit)

        assert str(length) == f'{value} {unit}'


@mark.units
class TestLengthFormat:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list),
        total_digits=integers(min_value=1, max_value=10),
        decimal_digits=integers(min_value=1, max_value=10)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, total_digits, decimal_digits):
        length = Length(value=value, unit=unit)

        assert length.__format__(
            f'{total_digits}.{decimal_digits}f'
        ) == f'{length:{total_digits}.{decimal_digits}f}'


@mark.units
class TestLengthAbs:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit):
        length = Length(value=value, unit=unit)

        assert abs(length) == Length(value=abs(value), unit=unit)
        assert abs(length).value >= 0


@mark.units
class TestLengthNeg:

    @mark.error
    def test_method(self):
        length = Length(value=1, unit='m')

        with raises(ValueError):
            assert -length


@mark.units
class TestLengthAdd:

    @mark.genuine
    @given(
        value_1=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit_1=sampled_from(elements=units_list),
        value_2=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit_2=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        length_1 = Length(value=value_1, unit=unit_1)
        length_2 = Length(value=value_2, unit=unit_2)
        result = length_1 + length_2

        assert isinstance(result, Length)
        assert result.value == length_1.value + length_2.to(unit_1).value
        assert result.unit == length_1.unit

    @mark.error
    def test_raises_type_error(self, length_add_type_error):
        with raises(TypeError):
            assert basic_length + length_add_type_error


@mark.units
class TestLengthSub:

    @mark.genuine
    @given(
        value_1=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit_1=sampled_from(elements=units_list),
        value_2=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit_2=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value_1, unit_1, value_2, unit_2):
        length_1 = Length(value=value_1, unit=unit_1)
        length_2 = Length(value=value_2, unit=unit_2)
        if length_1 > length_2:
            result = length_1 - length_2

            assert isinstance(result, Length)
            assert result.value == length_1.value - length_2.to(unit_1).value
            assert result.unit == length_1.unit

    @mark.error
    def test_raises_type_error(self, length_sub_type_error):
        with raises(TypeError):
            assert basic_length - length_sub_type_error

    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_length - \
                Length(basic_length.value + 1, basic_length.unit)


@mark.units
class TestLengthMul:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list),
        multiplier=one_of(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=1e-10,
                exclude_min=True,
                max_value=1000
            ),
            lengths()
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, multiplier):
        length = Length(value=value, unit=unit)
        result = length*multiplier

        if isinstance(multiplier, Length):
            assert isinstance(result, Surface)
            assert result.value == length.to('m').value * \
                multiplier.to('m').value
            assert result.unit == 'm^2'
        else:
            assert isinstance(result, Length)
            assert result.value == length.value*multiplier
            assert result.unit == length.unit

    @mark.error
    def test_raises_type_error(self, length_mul_type_error):
        with raises(TypeError):
            assert basic_length*length_mul_type_error

    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert basic_length*(-1)


@mark.units
class TestLengthRmul:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list),
        multiplier=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, multiplier):
        length = Length(value=value, unit=unit)
        result = multiplier*length

        assert isinstance(result, Length)
        assert result.value == length.value*multiplier
        assert result.unit == length.unit

    @mark.error
    def test_raises_type_error(self, length_rmul_type_error):
        with raises(TypeError):
            assert length_rmul_type_error*basic_length

    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            assert -1*basic_length


@mark.units
class TestLengthTruediv:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list),
        divider=one_of(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=1e-10,
                exclude_min=True,
                max_value=1000
            ),
            lengths()
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, divider):
        length = Length(value=value, unit=unit)

        if isinstance(divider, Length):
            if abs(divider.value) >= 1e-300:
                result = length/divider
                assert isinstance(result, float)
                assert result == length.value/divider.to(unit).value
        else:
            if divider != 0:
                result = length/divider
                assert isinstance(result, Length)
                assert result.value == length.value/divider
                assert result.unit == length.unit

    @mark.error
    def test_raises_type_error(self, length_truediv_type_error):
        with raises(TypeError):
            assert basic_length/length_truediv_type_error

    @mark.error
    def test_raises_zero_division_error(
        self,
        length_truediv_zero_division_error
    ):
        with raises(ZeroDivisionError):
            assert basic_length/length_truediv_zero_division_error


@mark.units
class TestLengthEq:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list)
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit):
        length_1 = Length(value=value, unit=unit)
        length_2 = Length(value=value, unit=unit)

        for target_unit in units_list:
            assert length_1 == length_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, length_eq_type_error):
        with raises(TypeError):
            assert basic_length == length_eq_type_error


@mark.units
class TestLengthNe:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
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
        length_1 = Length(value=value, unit=unit)
        length_2 = Length(value=value + gap, unit=unit)

        for target_unit in units_list:
            assert length_1 != length_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, length_ne_type_error):
        with raises(TypeError):
            assert basic_length != length_ne_type_error


@mark.units
class TestLengthGt:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
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
        length_1 = Length(value=value + gap, unit=unit)
        length_2 = Length(value=value, unit=unit)

        for target_unit in units_list:
            assert length_1 > length_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, length_gt_type_error):
        with raises(TypeError):
            assert basic_length > length_gt_type_error


@mark.units
class TestLengthGe:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
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
        length_1 = Length(value=value + gap, unit=unit)
        length_2 = Length(value=value, unit=unit)

        for target_unit in units_list:
            assert length_1 >= length_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, length_ge_type_error):
        with raises(TypeError):
            assert basic_length >= length_ge_type_error


@mark.units
class TestLengthLt:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
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
            length_1 = Length(value=value, unit=unit)
            length_2 = Length(value=value + gap, unit=unit)

            for target_unit in units_list:
                assert length_1 < length_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, length_lt_type_error):
        with raises(TypeError):
            assert basic_length < length_lt_type_error


@mark.units
class TestLengthLe:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
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
            length_1 = Length(value=value, unit=unit)
            length_2 = Length(value=value + gap, unit=unit)

            for target_unit in units_list:
                assert length_1 <= length_2.to(target_unit)

    @mark.error
    def test_raises_type_error(self, length_le_type_error):
        with raises(TypeError):
            assert basic_length <= length_le_type_error


@mark.units
class TestLengthTo:

    @mark.genuine
    @given(
        value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1e-10,
            exclude_min=True,
            max_value=1000
        ),
        unit=sampled_from(elements=units_list),
        inplace=booleans()
    )
    @settings(max_examples=100, deadline=None)
    def test_method(self, value, unit, inplace):
        if abs(value) >= 1e-10:
            length = Length(value=value, unit=unit)

            for target_unit in units_list:
                converted_inertia = length.to(
                    target_unit=target_unit,
                    inplace=inplace
                )

                assert converted_inertia.unit == target_unit
                if Length._Length__UNITS[target_unit] != \
                        Length._Length__UNITS[unit]:
                    assert converted_inertia.value != value
                    assert converted_inertia.unit != unit

                    if inplace:
                        assert converted_inertia.value == length.value
                        assert converted_inertia.unit == length.unit
                    else:
                        assert converted_inertia.value != length.value
                        assert converted_inertia.unit != length.unit
                else:
                    assert converted_inertia == length

    @mark.error
    def test_raises_type_error(self, length_to_type_error):
        with raises(TypeError):
            basic_length.to(**length_to_type_error)

    @mark.error
    def test_raises_key_error(self):
        fake_units = [f'fake {unit}' for unit in units_list]
        for fake_unit in fake_units:
            with raises(KeyError):
                basic_length.to(fake_unit)
