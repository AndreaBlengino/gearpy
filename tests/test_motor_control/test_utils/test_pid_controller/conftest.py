from gearpy.units import TimeInterval
from gearpy.motor_control.utils import PIDController
from hypothesis.strategies import composite, floats, booleans
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


@composite
def pid_controllers(draw):
    Kp = draw(floats(allow_nan=False, allow_infinity=False))
    Ki = draw(floats(allow_nan=False, allow_infinity=False))
    Kd = draw(floats(allow_nan=False, allow_infinity=False))
    clamping = draw(booleans())
    reference_min = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=-1000,
            max_value=1000
        )
    )
    reference_range = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1,
            max_value=1000
        )
    )
    return PIDController(
        Kp=Kp,
        Ki=Ki,
        Kd=Kd,
        clamping=clamping,
        reference_min=reference_min,
        reference_max=reference_min + reference_range
    )
