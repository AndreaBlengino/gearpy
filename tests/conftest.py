from gearpy import DCMotor, SpurGear
from gearpy.gear.gear import GearBase
from gearpy.motor.motor import MotorBase
from gearpy.mechanical_object.rotating_object import RotatingObject
import numpy as np
from pytest import fixture
from typing import Callable


types_to_check = ['string', 2, 2.2, True, (0, 1), [0, 1], {0, 1}, {0: 1}, None, np.array([0])]


basic_dc_motor = DCMotor(name = 'name', inertia = 1, no_load_speed = 1, maximum_torque = 1)
basic_spur_gear = SpurGear(name = 'gear', n_teeth = 10, inertia = 1)


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


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def dc_motor_angle_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def dc_motor_speed_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def dc_motor_acceleration_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def dc_motor_torque_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def dc_motor_driving_torque_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def dc_motor_load_torque_type_error(request):
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


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def spur_gear_angle_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def spur_gear_speed_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def spur_gear_acceleration_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def spur_gear_torque_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def spur_gear_driving_torque_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
                   and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
def spur_gear_load_torque_type_error(request):
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
