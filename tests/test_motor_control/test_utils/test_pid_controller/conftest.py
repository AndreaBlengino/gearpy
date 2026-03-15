from gearpy.units import TimeInterval
from pytest import fixture
from tests.conftest import types_to_check


pid_controller_init_type_error_1 = [
    {
        'Kp': type_to_check,
        'Ki': 1,
        'Kd': 1,
        'clamping': False,
        'reference_min': -1,
        'reference_max': 1
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]


pid_controller_init_type_error_2 = [
    {
        'Kp': 1,
        'Ki': type_to_check,
        'Kd': 1,
        'clamping': False,
        'reference_min': -1,
        'reference_max': 1
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]


pid_controller_init_type_error_3 = [
    {
        'Kp': 1,
        'Ki': 1,
        'Kd': type_to_check,
        'clamping': False,
        'reference_min': -1,
        'reference_max': 1
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]


pid_controller_init_type_error_4 = [
    {
        'Kp': 1,
        'Ki': 1,
        'Kd': 1,
        'clamping': type_to_check,
        'reference_min': -1,
        'reference_max': 1
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, bool)
]


pid_controller_init_type_error_5 = [
    {
        'Kp': 1,
        'Ki': 1,
        'Kd': 1,
        'clamping': False,
        'reference_min': type_to_check,
        'reference_max': 1
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int) and type_to_check is not None
]


pid_controller_init_type_error_6 = [
    {
        'Kp': 1,
        'Ki': 1,
        'Kd': 1,
        'clamping': False,
        'reference_min': -1,
        'reference_max': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int) and type_to_check is not None
]


@fixture(
    params=[
        *pid_controller_init_type_error_1,
        *pid_controller_init_type_error_2,
        *pid_controller_init_type_error_3,
        *pid_controller_init_type_error_4,
        *pid_controller_init_type_error_5,
        *pid_controller_init_type_error_6
    ]
)
def pid_controller_init_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'Kp': 1,
            'Ki': 1,
            'Kd': 1,
            'clamping': False,
            'reference_min': 1,
            'reference_max': -1,
        },
    ]
)
def pid_controller_init_value_error(request):
    return request.param


pid_controller_compute_type_error_1 = [
    {
        'error': type_to_check,
        'time_step': TimeInterval(1, 'sec'),
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float | int)
]


pid_controller_compute_type_error_2 = [
    {
        'error': 1,
        'time_step': type_to_check,
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, TimeInterval)
]


@fixture(
    params=[
        *pid_controller_compute_type_error_1,
        *pid_controller_compute_type_error_2,
    ]
)
def pid_controller_compute_type_error(request):
    return request.param
