from gearpy.mechanical_object import RotatingObject
from gearpy.units import InertiaMoment
from pytest import fixture
from tests.conftest import types_to_check


flywheel_init_type_error_1 = [{'name': type_to_check, 'inertia_moment': InertiaMoment(1, 'kgm^2')}
                              for type_to_check in types_to_check if not isinstance(type_to_check, str)]

flywheel_init_type_error_2 = [{'name': 'flywheel', 'inertia_moment': type_to_check}
                              for type_to_check in types_to_check if not isinstance(type_to_check, InertiaMoment)]

@fixture(params = [*flywheel_init_type_error_1,
                   *flywheel_init_type_error_2])
def flywheel_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)])
def flywheel_driven_by_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)])
def flywheel_drives_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)])
def flywheel_master_gear_ratio_type_error(request):
    return request.param
