from gearpy.units import InertiaMoment, Length, Angle
from pytest import fixture
from tests.conftest import types_to_check


worm_gear_init_type_error_1 = [
    {
        'name': type_to_check,
        'n_starts': 1,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': Angle(10, 'deg'),
        'reference_diameter': Length(10, 'mm')
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

worm_gear_init_type_error_2 = [
    {
        'name': 'gear',
        'n_starts': type_to_check,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': Angle(10, 'deg'),
        'reference_diameter': Length(10, 'mm')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, int) and
    not isinstance(type_to_check, bool)
]

worm_gear_init_type_error_3 = [
    {
        'name': 'gear',
        'n_starts': 1,
        'inertia_moment': type_to_check,
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': Angle(10, 'deg'),
        'reference_diameter': Length(10, 'mm')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, InertiaMoment)
]

worm_gear_init_type_error_4 = [
    {
        'name': 'gear',
        'n_starts': 1,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': type_to_check,
        'helix_angle': Angle(10, 'deg'),
        'reference_diameter': Length(10, 'mm')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Angle)
]

worm_gear_init_type_error_5 = [
    {
        'name': 'gear',
        'n_starts': 1,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': type_to_check,
        'reference_diameter': Length(10, 'mm')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Angle)
]

worm_gear_init_type_error_6 = [
    {
        'name': 'gear',
        'n_starts': 1,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'pressure_angle': Angle(20, 'deg'),
        'helix_angle': Angle(10, 'deg'),
        'reference_diameter': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Length) and type_to_check is not None
]


@fixture(
    params=[
        *worm_gear_init_type_error_1,
        *worm_gear_init_type_error_2,
        *worm_gear_init_type_error_3,
        *worm_gear_init_type_error_4,
        *worm_gear_init_type_error_5,
        *worm_gear_init_type_error_6
    ]
)
def worm_gear_init_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'name': '',
            'n_starts': 1,
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'pressure_angle': Angle(20, 'deg'),
            'helix_angle': Angle(10, 'deg')
        },
        {
            'name': 'gear',
            'n_starts': -1,
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'pressure_angle': Angle(20, 'deg'),
            'helix_angle': Angle(10, 'deg')
        },
        {
            'name': 'gear',
            'n_starts': 1,
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'pressure_angle': Angle(0, 'deg'),
            'helix_angle': Angle(10, 'deg')
        },
        {
            'name': 'gear',
            'n_starts': 1,
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'pressure_angle': Angle(20, 'deg'),
            'helix_angle': Angle(80, 'deg')
        }
    ]
)
def worm_gear_init_value_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, bool)
    ]
)
def worm_gear_self_locking_type_error(request):
    return request.param
