from gearpy.mechanical_objects import MotorBase
from pytest import fixture
from tests.conftest import types_to_check


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)])
def amperometer_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, str)])
def amperometer_get_value_type_error(request):
    return request.param
