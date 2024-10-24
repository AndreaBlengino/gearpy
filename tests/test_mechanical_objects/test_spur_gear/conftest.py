from gearpy.units import InertiaMoment, Length, Stress
from pytest import fixture
from tests.conftest import types_to_check


spur_gear_init_type_error_1 = [
    {
        'name': type_to_check,
        'n_teeth': 10,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': Length(1, 'mm'),
        'face_width': Length(5, 'mm'),
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

spur_gear_init_type_error_2 = [
    {
        'name': 'gear',
        'n_teeth': type_to_check,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': Length(1, 'mm'),
        'face_width': Length(5, 'mm'),
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, int | bool)
]

spur_gear_init_type_error_3 = [
    {
        'name': 'gear',
        'n_teeth': 10,
        'inertia_moment': type_to_check,
        'module': Length(1, 'mm'),
        'face_width': Length(5, 'mm'),
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, InertiaMoment)
]

spur_gear_init_type_error_4 = [
    {
        'name': 'gear',
        'n_teeth': 10,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': type_to_check,
        'face_width': Length(5, 'mm'),
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Length) and type_to_check is not None
]

spur_gear_init_type_error_5 = [
    {
        'name': 'gear',
        'n_teeth': 10,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': Length(1, 'mm'),
        'face_width': type_to_check,
        'elastic_modulus': Stress(100, 'GPa')
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Length) and type_to_check is not None
]

spur_gear_init_type_error_6 = [
    {
        'name': 'gear',
        'n_teeth': 10,
        'inertia_moment': InertiaMoment(1, 'kgm^2'),
        'module': Length(1, 'mm'),
        'face_width': Length(5, 'mm'),
        'elastic_modulus': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Stress) and type_to_check is not None
]


@fixture(
    params=[
        *spur_gear_init_type_error_1,
        *spur_gear_init_type_error_2,
        *spur_gear_init_type_error_3,
        *spur_gear_init_type_error_4,
        *spur_gear_init_type_error_5,
        *spur_gear_init_type_error_6
    ]
)
def spur_gear_init_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'name': '',
            'n_teeth': 10,
            'inertia_moment': InertiaMoment(1, 'kgm^2')
        },
        {
            'name': 'gear',
            'n_teeth': -1,
            'inertia_moment': InertiaMoment(1, 'kgm^2')
        },
        {
            'name': 'gear',
            'n_teeth': 10,
            'inertia_moment': InertiaMoment(1, 'kgm^2'),
            'elastic_modulus': Stress(-10, 'GPa')
        }
    ]
)
def spur_gear_init_value_error(request):
    return request.param
