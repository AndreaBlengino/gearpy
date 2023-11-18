from gearpy.units import Stress
from hypothesis.strategies import composite, floats, sampled_from
import numpy as np
from tests.conftest import types_to_check
from pytest import fixture


basic_stress = Stress(1, 'Pa')


@composite
def stresses(draw):
    value = draw(floats(allow_nan = False, allow_infinity = False, min_value = -1000, max_value = 1000))
    unit = draw(sampled_from(elements = list(Stress._Stress__UNITS.keys())))

    return Stress(value = value, unit = unit)


stress_init_type_error_1 = [{'value': type_to_check, 'unit': 'unit'} for type_to_check in types_to_check
                            if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)]

stress_init_type_error_2 = [{'value': 1, 'unit': types_to_check} for type_to_check in types_to_check
                            if not isinstance(type_to_check, str)]

@fixture(params = [*stress_init_type_error_1,
                   *stress_init_type_error_2])
def stress_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def stress_add_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def stress_sub_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check
                   if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)])
def stress_mul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, np.ndarray)])
def stress_rmul_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, Stress)])
def stress_truediv_type_error(request):
    return request.param


@fixture(params = [0, 0.0, Stress(0, 'Pa')])
def stress_truediv_zero_division_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def stress_eq_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def stress_ne_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def stress_gt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def stress_ge_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def stress_lt_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def stress_le_type_error(request):
    return request.param


stress_to_type_error_1 = [{'target_unit': type_to_check, 'inplace': True}
                          for type_to_check in types_to_check if not isinstance(type_to_check, str)]

stress_to_type_error_2 = [{'target_unit': 'target_unit', 'inplace': type_to_check} for type_to_check in types_to_check
                          if not isinstance(type_to_check, bool) and not isinstance(type_to_check, int)]

@fixture(params = [*stress_to_type_error_1,
                   *stress_to_type_error_2])
def stress_to_type_error(request):
    return request.param
