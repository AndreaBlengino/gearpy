from gearpy.units import Surface
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_surface = Surface(1, 'm^2')


@composite
def surfaces(draw):
    value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = True, max_value = 1000))
    unit = draw(sampled_from(elements = list(Surface._Surface__UNITS.keys())))

    return Surface(value = value, unit = unit)


surface_init_type_error_1 = [{'value': type_to_check, 'unit': 'unit'} for type_to_check in types_to_check
                             if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)]

surface_init_type_error_2 = [{'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
                             if not isinstance(type_to_check, str)]

@fixture(params = [*surface_init_type_error_1,
                   *surface_init_type_error_2])
def surface_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Surface)])
def surface_add_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Surface)])
def surface_sub_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)])
def surface_mul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, np.ndarray)])
def surface_rmul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, Surface)])
def surface_truediv_type_error(request):
    return request.param


@fixture(params = [0, 0.0])
def surface_truediv_zero_division_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Surface)])
def surface_eq_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Surface)])
def surface_ne_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Surface)])
def surface_gt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Surface)])
def surface_ge_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Surface)])
def surface_lt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Surface)])
def surface_le_type_error(request):
    return request.param


surface_to_type_error_1 = [{'target_unit': type_to_check, 'inplace': True}
                           for type_to_check in types_to_check if not isinstance(type_to_check, str)]

surface_to_type_error_2 = [{'target_unit': 'target_unit', 'inplace': type_to_check}
                           for type_to_check in types_to_check if not isinstance(type_to_check, bool)
                           and not isinstance(type_to_check, int)]

@fixture(params = [*surface_to_type_error_1,
                   *surface_to_type_error_2])
def surface_to_type_error(request):
    return request.param