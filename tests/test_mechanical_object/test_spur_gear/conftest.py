from gearpy.mechanical_object import RotatingObject, Role, SpurGear
from gearpy.units import Force, InertiaMoment, Length, Stress
from gearpy.utils import add_gear_mating
from pytest import fixture
from tests.conftest import types_to_check
from typing import Callable


spur_gear_init_type_error_1 = [{'name': type_to_check, 'n_teeth': 10, 'inertia_moment': InertiaMoment(1, 'kgm^2'),
                                'module': Length(1, 'mm'), 'face_width': Length(5, 'mm'),
                                'elastic_modulus': Stress(100, 'GPa')}
                               for type_to_check in types_to_check if not isinstance(type_to_check, str)]

spur_gear_init_type_error_2 = [{'name': 'gear', 'n_teeth': type_to_check, 'inertia_moment': InertiaMoment(1, 'kgm^2'),
                                'module': Length(1, 'mm'), 'face_width': Length(5, 'mm'),
                                'elastic_modulus': Stress(100, 'GPa')}
                               for type_to_check in types_to_check if not isinstance(type_to_check, int)
                               and not isinstance(type_to_check, bool)]

spur_gear_init_type_error_3 = [{'name': 'gear', 'n_teeth': 10, 'inertia_moment': type_to_check,
                                'module': Length(1, 'mm'), 'face_width': Length(5, 'mm'),
                                'elastic_modulus': Stress(100, 'GPa')}
                               for type_to_check in types_to_check if not isinstance(type_to_check, InertiaMoment)]

spur_gear_init_type_error_4 = [{'name': 'gear', 'n_teeth': 10, 'inertia_moment': InertiaMoment(1, 'kgm^2'),
                                'module': type_to_check, 'face_width': Length(5, 'mm'),
                                'elastic_modulus': Stress(100, 'GPa')}
                               for type_to_check in types_to_check if not isinstance(type_to_check, Length)
                               and type_to_check is not None]

spur_gear_init_type_error_5 = [{'name': 'gear', 'n_teeth': 10, 'inertia_moment': InertiaMoment(1, 'kgm^2'),
                                'module': Length(1, 'mm'), 'face_width': type_to_check,
                                'elastic_modulus': Stress(100, 'GPa')}
                               for type_to_check in types_to_check if not isinstance(type_to_check, Length)
                               and type_to_check is not None]

spur_gear_init_type_error_6 = [{'name': 'gear', 'n_teeth': 10, 'inertia_moment': InertiaMoment(1, 'kgm^2'),
                                'module': Length(1, 'mm'), 'face_width': Length(5, 'mm'),
                                'elastic_modulus': type_to_check}
                               for type_to_check in types_to_check if not isinstance(type_to_check, Stress)
                               and type_to_check is not None]

@fixture(params = [*spur_gear_init_type_error_1,
                   *spur_gear_init_type_error_2,
                   *spur_gear_init_type_error_3,
                   *spur_gear_init_type_error_4,
                   *spur_gear_init_type_error_5,
                   *spur_gear_init_type_error_6])
def spur_gear_init_type_error(request):
    return request.param


@fixture(params = [{'name': '', 'n_teeth': 10, 'inertia_moment': InertiaMoment(1, 'kgm^2')},
                   {'name': 'gear', 'n_teeth': -1, 'inertia_moment': InertiaMoment(1, 'kgm^2')},
                   {'name': 'gear', 'n_teeth': 10, 'inertia_moment': InertiaMoment(1, 'kgm^2'), 'elastic_modulus': Stress(-10, 'GPa')}])
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


@fixture(params = [type_to_check for type_to_check in types_to_check if not hasattr(type_to_check, '__name__') or not issubclass(type_to_check, Role)])
def spur_gear_mating_role_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Force)])
def spur_gear_tangential_force_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def spur_gear_bending_stress_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Stress)])
def spur_gear_contact_stress_type_error(request):
    return request.param


spur_gear_compute_contact_stress_value_error_1 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                          module = Length(1, 'mm'), face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))

spur_gear_compute_contact_stress_value_error_2 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                          module = Length(1, 'mm'), face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))
spur_gear_compute_contact_stress_value_error_2_mate = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                               face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))
add_gear_mating(master = spur_gear_compute_contact_stress_value_error_2, slave = spur_gear_compute_contact_stress_value_error_2_mate, efficiency = 1)

spur_gear_compute_contact_stress_value_error_3 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                          module = Length(1, 'mm'), face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))
spur_gear_compute_contact_stress_value_error_3_mate = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                               module = Length(1, 'mm'), face_width = Length(5, 'mm'))
add_gear_mating(master = spur_gear_compute_contact_stress_value_error_3, slave = spur_gear_compute_contact_stress_value_error_3_mate, efficiency = 1)

spur_gear_compute_contact_stress_value_error_4 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                          module = Length(1, 'mm'), face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))
spur_gear_compute_contact_stress_value_error_4_mate = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                               face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))
add_gear_mating(master = spur_gear_compute_contact_stress_value_error_4_mate, slave = spur_gear_compute_contact_stress_value_error_4, efficiency = 1)

spur_gear_compute_contact_stress_value_error_5 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                          module = Length(1, 'mm'), face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))
spur_gear_compute_contact_stress_value_error_5_mate = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                               module = Length(1, 'mm'), face_width = Length(5, 'mm'))
add_gear_mating(master = spur_gear_compute_contact_stress_value_error_5_mate, slave = spur_gear_compute_contact_stress_value_error_5, efficiency = 1)

@fixture(params = [spur_gear_compute_contact_stress_value_error_1,
                   spur_gear_compute_contact_stress_value_error_2,
                   spur_gear_compute_contact_stress_value_error_3,
                   spur_gear_compute_contact_stress_value_error_4,
                   spur_gear_compute_contact_stress_value_error_5])
def spur_gear_compute_contact_stress_value_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Callable)])
def spur_gear_external_torque_type_error(request):
    return request.param
