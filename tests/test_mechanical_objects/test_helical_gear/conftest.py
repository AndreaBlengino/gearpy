from gearpy.units import Angle, InertiaMoment, Length, Stress
from pytest import fixture
from tests.conftest import types_to_check


helical_gear_init_type_error_1 = [
    {
        'name': type_to_check,
        'n_teeth': 10,
        'helix_angle': Angle(30, 'deg'),
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': Length(1, 'mm'),
        'face_width': Length(5, 'mm'),
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, str)
]

helical_gear_init_type_error_2 = [
    {
        'name': 'gear',
        'n_teeth': type_to_check,
        'helix_angle': Angle(30, 'deg'),
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': Length(1, 'mm'),
        'face_width': Length(5, 'mm'),
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, int) and
    not isinstance(type_to_check, bool)
]

helical_gear_init_type_error_3 = [
    {
        'name': 'gear',
        'n_teeth': 10,
        'helix_angle': type_to_check,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': Length(1, 'mm'),
        'face_width': Length(5, 'mm'),
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Angle)
]

helical_gear_init_type_error_4 = [
    {
        'name': 'gear',
        'n_teeth': 10,
        'helix_angle': Angle(30, 'deg'),
        'inertia_moment': type_to_check,
        'module': Length(1, 'mm'),
        'face_width': Length(5, 'mm'),
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, InertiaMoment)
]

helical_gear_init_type_error_5 = [
    {
        'name': 'gear',
        'n_teeth': 10,
        'helix_angle': Angle(30, 'deg'),
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': type_to_check,
        'face_width': Length(5, 'mm'),
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Length) and type_to_check is not None
]

helical_gear_init_type_error_6 = [
    {
        'name': 'gear',
        'n_teeth': 10,
        'helix_angle': Angle(30, 'deg'),
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': Length(1, 'mm'),
        'face_width': type_to_check,
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Length) and type_to_check is not None
]

helical_gear_init_type_error_7 = [
    {
        'name': 'gear',
        'n_teeth': 10,
        'helix_angle': Angle(30, 'deg'),
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': Length(1, 'mm'),
        'face_width': Length(5, 'mm'),
        'elastic_modulus': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Stress) and type_to_check is not None
]


@fixture(
    params=[
        *helical_gear_init_type_error_1,
        *helical_gear_init_type_error_2,
        *helical_gear_init_type_error_3,
        *helical_gear_init_type_error_4,
        *helical_gear_init_type_error_5,
        *helical_gear_init_type_error_6,
        *helical_gear_init_type_error_7
    ]
)
def helical_gear_init_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'name': '',
            'n_teeth': 10,
            'helix_angle': Angle(30, 'deg'),
            'inertia_moment': InertiaMoment(1, 'kgm^2')
        },
        {
            'name': 'gear',
            'n_teeth': -1,
            'helix_angle': Angle(30, 'deg'),
            'inertia_moment': InertiaMoment(1, 'kgm^2')
        },
        {
            'name': 'gear',
            'n_teeth': 10,
            'helix_angle': Angle(91, 'deg'),
            'inertia_moment': InertiaMoment(1, 'kgm^2')
        },
        {
            'name': 'gear',
            'n_teeth': 10, 'helix_angle': Angle(30, 'deg'),
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'elastic_modulus': Stress(-10, 'GPa')
        }
    ]
)
def helical_gear_init_value_error(request):
    return request.param
