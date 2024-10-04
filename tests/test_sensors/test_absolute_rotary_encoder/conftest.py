from gearpy.mechanical_objects import RotatingObject
from pytest import fixture
from tests.conftest import types_to_check


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, RotatingObject)
    ]
)
def absolute_rotary_encoder_init_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, str)
    ]
)
def absolute_rotary_encoder_get_value_type_error(request):
    return request.param
