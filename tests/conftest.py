from gearpy import DCMotor, SpurGear
from gearpy.gear.gear import GearBase
from gearpy.motor.motor import MotorBase
from gearpy.mechanical_object.rotating_object import RotatingObject
from hypothesis.strategies import composite, text, integers, floats
import numpy as np
from pytest import fixture
from typing import Callable


types_to_check = ['string', 2, 2.2, True, (0, 1), [0, 1], {0, 1}, {0: 1}, None, np.array([0])]


basic_dc_motor = DCMotor(name = 'name', inertia = 1, no_load_speed = 1, maximum_torque = 1)
basic_spur_gear = SpurGear(name = 'gear', n_teeth = 10, inertia = 1)
basic_rotating_objects = [basic_dc_motor, basic_spur_gear]


@composite
def dc_motors(draw):
    name = draw(text(min_size = 1))
    inertia = draw(floats(min_value = 0, exclude_min = True))
    no_load_speed = draw(floats(min_value = 0, exclude_min = True))
    maximum_torque = draw(floats(min_value = 0, exclude_min = True))

    return DCMotor(name = name, inertia = inertia, no_load_speed = no_load_speed, maximum_torque = maximum_torque)


@composite
def spur_gears(draw):
    name = draw(text(min_size = 1))
    n_teeth = draw(integers(min_value = 1))
    inertia = draw(floats(min_value = 0, exclude_min = True))

    return SpurGear(name = name, n_teeth = n_teeth, inertia = inertia)


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def rotating_object_angle_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def rotating_object_speed_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def rotating_object_acceleration_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def rotating_object_torque_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def rotating_object_driving_torque_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def rotating_object_load_torque_type_error(request):
    return request.param


dc_motor_init_type_error_1 = [{'name': type_to_check, 'inertia': 1, 'no_load_speed': 1, 'maximum_torque': 1}
                              for type_to_check in types_to_check if not isinstance(type_to_check, str)]

dc_motor_init_type_error_2 = [{'name': 'motor', 'inertia': type_to_check, 'no_load_speed': 1, 'maximum_torque': 1}
                              for type_to_check in types_to_check if not isinstance(type_to_check, float)
                              and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]

dc_motor_init_type_error_3 = [{'name': 'motor', 'inertia': 1, 'no_load_speed': type_to_check, 'maximum_torque': 1}
                              for type_to_check in types_to_check if not isinstance(type_to_check, float)
                              and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]

dc_motor_init_type_error_4 = [{'name': 'motor', 'inertia': 1, 'no_load_speed': 1, 'maximum_torque': type_to_check}
                              for type_to_check in types_to_check if not isinstance(type_to_check, float)
                              and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]

@fixture(params = [*dc_motor_init_type_error_1,
                   *dc_motor_init_type_error_2,
                   *dc_motor_init_type_error_3,
                   *dc_motor_init_type_error_4])
def dc_motor_init_type_error(request):
    return request.param


@fixture(params = [{'name': '', 'inertia': 1, 'no_load_speed': 1, 'maximum_torque': 1},
                   {'name': 'motor', 'inertia': -1, 'no_load_speed': 1, 'maximum_torque': 1},
                   {'name': 'motor', 'inertia': 1, 'no_load_speed': -1, 'maximum_torque': 1},
                   {'name': 'motor', 'inertia': 1, 'no_load_speed': 1, 'maximum_torque': -1}])
def dc_motor_init_value_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)])
def dc_motor_drives_type_error(request):
    return request.param


@fixture(params = [{'name': 'gear', 'n_teeth': type_to_check, 'inertia': 1} for type_to_check in types_to_check
                   if not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def spur_gear_init_type_error(request):
    return request.param


@fixture(params = [{'name': '', 'n_teeth': 1, 'inertia': 1},
                   {'name': 'gear', 'n_teeth': -1, 'inertia': 1},
                   {'name': 'gear', 'n_teeth': 1, 'inertia': -1}])
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


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Callable)])
def spur_gear_external_torque_type_error(request):
    return request.param


add_gear_mating_type_error_1 = [{'gear 1': type_to_check, 'gear 2': basic_spur_gear, 'efficiency': 0.5}
                                for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]

add_gear_mating_type_error_2 = [{'gear 1': basic_spur_gear, 'gear 2': type_to_check, 'efficiency': 0.5}
                                for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]

add_gear_mating_type_error_3 = [{'gear 1': basic_spur_gear, 'gear 2': basic_spur_gear, 'efficiency': type_to_check}
                                for type_to_check in types_to_check if not isinstance(type_to_check, float)
                                and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]

@fixture(params = [*add_gear_mating_type_error_1,
                   *add_gear_mating_type_error_2,
                   *add_gear_mating_type_error_3])
def add_gear_mating_type_error(request):
    return request.param


@fixture(params = [-1, 2])
def add_gear_mating_value_error(request):
    return request.param


add_fixed_joint_type_error_1 = [{'master': type_to_check, 'slave': basic_spur_gear} for type_to_check in types_to_check
                                if not isinstance(type_to_check, GearBase) and not isinstance(type_to_check, MotorBase)]

add_fixed_joint_type_error_2 = [{'master': basic_spur_gear, 'slave': type_to_check}
                                for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]

@fixture(params = [*add_fixed_joint_type_error_1,
                   *add_fixed_joint_type_error_2])
def add_fixed_joint_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)])
def transmission_init_type_error(request):
    return request.param
