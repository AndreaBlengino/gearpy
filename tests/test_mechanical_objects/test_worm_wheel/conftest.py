from gearpy.units import Angle, InertiaMoment, Length
from pytest import fixture
from tests.conftest import types_to_check


worm_wheel_init_type_error_1 = [
    {
        'name': type_to_check,
        'n_teeth': 10,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': Angle(10, 'deg'),
        'module': Length(1, 'mm'),
        'face_width': Length(10, 'mm')
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

worm_wheel_init_type_error_2 = [
    {
        'name': 'wheel',
        'n_teeth': type_to_check,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': Angle(10, 'deg'),
        'module': Length(1, 'mm'),
        'face_width': Length(10, 'mm')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, int | bool)
]

worm_wheel_init_type_error_3 = [
    {
        'name': 'wheel',
        'n_teeth': 10,
        'inertia_moment': type_to_check,
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': Angle(10, 'deg'),
        'module': Length(1, 'mm'),
        'face_width': Length(10, 'mm')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, InertiaMoment)
]

worm_wheel_init_type_error_4 = [
    {
        'name': 'wheel',
        'n_teeth': 10,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': type_to_check,
        'helix_angle': Angle(10, 'deg'),
        'module': Length(1, 'mm'),
        'face_width': Length(10, 'mm')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Angle)
]

worm_wheel_init_type_error_5 = [
    {
        'name': 'wheel',
        'n_teeth': 10,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': type_to_check,
        'module': Length(1, 'mm'),
        'face_width': Length(10, 'mm')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Angle)
]

worm_wheel_init_type_error_6 = [
    {
        'name': 'wheel',
        'n_teeth': 10,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': Angle(10, 'deg'),
        'module': type_to_check,
        'face_width': Length(10, 'mm')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Length) and type_to_check is not None
]

worm_wheel_init_type_error_7 = [
    {
        'name': 'wheel',
        'n_teeth': 10,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': Angle(10, 'deg'),
        'module': Length(1, 'mm'),
        'face_width': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Length) and type_to_check is not None]


@fixture(
    params=[
        *worm_wheel_init_type_error_1,
        *worm_wheel_init_type_error_2,
        *worm_wheel_init_type_error_3,
        *worm_wheel_init_type_error_4,
        *worm_wheel_init_type_error_5,
        *worm_wheel_init_type_error_6,
        *worm_wheel_init_type_error_7
    ]
)
def worm_wheel_init_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'name': '',
            'n_teeth': 10,
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'pressure_angle': Angle(20, 'deg'),
            'helix_angle': Angle(10, 'deg')
        },
        {
            'name': 'wheel',
            'n_teeth': -1,
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'pressure_angle': Angle(20, 'deg'),
            'helix_angle': Angle(10, 'deg')
        },
        {
            'name': 'wheel',
            'n_teeth': 10,
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'pressure_angle': Angle(0, 'deg'),
            'helix_angle': Angle(10, 'deg')
        },
        {
            'name': 'wheel',
            'n_teeth': 10,
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'pressure_angle': Angle(20, 'deg'),
            'helix_angle': Angle(80, 'deg')
        }
    ]
)
def worm_wheel_init_value_error(request):
    return request.param
