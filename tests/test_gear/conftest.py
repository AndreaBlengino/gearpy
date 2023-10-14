from gearpy.mechanical_object import RotatingObject
from gearpy.units import InertiaMoment
from pytest import fixture
from tests.conftest import types_to_check
from typing import Callable


spur_gear_init_type_error_1 = [{'name': type_to_check, 'n_teeth': 10, 'inertia_moment': InertiaMoment(1, 'kgm^2')}
                               for type_to_check in types_to_check if not isinstance(type_to_check, str)]

spur_gear_init_type_error_2 = [{'name': 'gear', 'n_teeth': type_to_check, 'inertia_moment': InertiaMoment(1, 'kgm^2')}
                               for type_to_check in types_to_check if not isinstance(type_to_check, int)
                               and not isinstance(type_to_check, bool)]

spur_gear_init_type_error_3 = [{'name': 'gear', 'n_teeth': 10, 'inertia_moment': type_to_check}
                               for type_to_check in types_to_check if not isinstance(type_to_check, InertiaMoment)]

@fixture(params = [*spur_gear_init_type_error_1,
                   *spur_gear_init_type_error_2,
                   *spur_gear_init_type_error_3])
def spur_gear_init_type_error(request):
    return request.param


@fixture(params = [{'name': '', 'n_teeth': 1, 'inertia_moment': InertiaMoment(1, 'kgm^2')},
                   {'name': 'gear', 'n_teeth': -1, 'inertia_moment': InertiaMoment(1, 'kgm^2')}])
def spur_gear_init_value_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)])
def spur_gear_driven_by_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)])
def spur_gear_drives_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)])
def spur_gear_master_gear_ratio_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def spur_gear_master_gear_efficiency_type_error(request):
    return request.param


@fixture(params = [-1, 2])
def spur_gear_master_gear_efficiency_value_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Callable)])
def spur_gear_external_torque_type_error(request):
    return request.param
