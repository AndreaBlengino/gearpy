from copy import deepcopy
from gearpy.mechanical_objects import Role, SpurGear, HelicalGear
from gearpy.units import Force, Stress, Length, InertiaMoment, Angle, Torque
from gearpy.utils import add_gear_mating
from tests.conftest import (
    types_to_check,
    basic_spur_gear_1,
    basic_spur_gear_2,
    basic_helical_gear_1,
    basic_helical_gear_2,
    basic_worm_gear_1,
    basic_worm_gear_2,
    basic_worm_wheel_1,
    basic_worm_wheel_2
)
from pytest import fixture
from typing import Callable


basic_gears = [
    basic_spur_gear_1,
    basic_spur_gear_2,
    basic_helical_gear_1,
    basic_helical_gear_2,
    basic_worm_gear_1,
    basic_worm_gear_2,
    basic_worm_wheel_1,
    basic_worm_wheel_2
]

basic_structural_gears_1 = [
    basic_spur_gear_2,
    basic_helical_gear_2,
    basic_worm_gear_2,
    basic_worm_wheel_2
]
basic_structural_gears_2 = [
    deepcopy(basic_spur_gear_2),
    deepcopy(basic_helical_gear_2),
    deepcopy(basic_worm_wheel_2),
    deepcopy(basic_worm_gear_2)
]


class FakeRole(Role): ...


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not hasattr(type_to_check, '__name__') or
        not issubclass(type_to_check, Role)
    ]
)
def gear_mating_role_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Force)
    ]
)
def gear_tangential_force_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Stress)
    ]
)
def gear_bending_stress_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Stress)
    ]
)
def gear_contact_stress_type_error(request):
    return request.param


gear_compute_contact_stress_value_error_1 = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)

gear_compute_contact_stress_value_error_2 = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
gear_compute_contact_stress_value_error_2_mate = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
add_gear_mating(
    master=gear_compute_contact_stress_value_error_2,
    slave=gear_compute_contact_stress_value_error_2_mate,
    efficiency=1
)

gear_compute_contact_stress_value_error_3 = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
gear_compute_contact_stress_value_error_3_mate = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm')
)
add_gear_mating(
    master=gear_compute_contact_stress_value_error_3,
    slave=gear_compute_contact_stress_value_error_3_mate,
    efficiency=1
)

gear_compute_contact_stress_value_error_4 = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
gear_compute_contact_stress_value_error_4_mate = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
add_gear_mating(
    master=gear_compute_contact_stress_value_error_4_mate,
    slave=gear_compute_contact_stress_value_error_4,
    efficiency=1
)

gear_compute_contact_stress_value_error_5 = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
gear_compute_contact_stress_value_error_5_mate = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm')
)
add_gear_mating(
    master=gear_compute_contact_stress_value_error_5_mate,
    slave=gear_compute_contact_stress_value_error_5,
    efficiency=1
)

gear_compute_contact_stress_value_error_6 = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)

gear_compute_contact_stress_value_error_7 = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
gear_compute_contact_stress_value_error_7_mate = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
add_gear_mating(
    master=gear_compute_contact_stress_value_error_7,
    slave=gear_compute_contact_stress_value_error_7_mate,
    efficiency=1
)

gear_compute_contact_stress_value_error_8 = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
gear_compute_contact_stress_value_error_8_mate = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm')
)
add_gear_mating(
    master=gear_compute_contact_stress_value_error_8,
    slave=gear_compute_contact_stress_value_error_8_mate,
    efficiency=1
)

gear_compute_contact_stress_value_error_9 = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
gear_compute_contact_stress_value_error_9_mate = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
add_gear_mating(
    master=gear_compute_contact_stress_value_error_9_mate,
    slave=gear_compute_contact_stress_value_error_9,
    efficiency=1
)

gear_compute_contact_stress_value_error_10 = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)
gear_compute_contact_stress_value_error_10_mate = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm')
)
add_gear_mating(
    master=gear_compute_contact_stress_value_error_10_mate,
    slave=gear_compute_contact_stress_value_error_10,
    efficiency=1
)


@fixture(
    params=[
        gear_compute_contact_stress_value_error_1,
        gear_compute_contact_stress_value_error_2,
        gear_compute_contact_stress_value_error_3,
        gear_compute_contact_stress_value_error_4,
        gear_compute_contact_stress_value_error_5,
        gear_compute_contact_stress_value_error_6,
        gear_compute_contact_stress_value_error_7,
        gear_compute_contact_stress_value_error_8,
        gear_compute_contact_stress_value_error_9,
        gear_compute_contact_stress_value_error_10
    ]
)
def gear_compute_contact_stress_value_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Callable)
    ]
)
def gear_external_torque_type_error(request):
    return request.param


@fixture(
    params=[
        lambda angular_speed, time: Torque(1, 'Nm'),
        lambda angular_position, time: Torque(1, 'Nm'),
        lambda angular_position, angular_speed: Torque(1, 'Nm')
    ]
)
def gear_external_torque_key_error(request):
    return request.param
