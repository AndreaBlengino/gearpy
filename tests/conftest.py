from gearpy import DCMotor
from gearpy import SpurGear
from gearpy.mechanical_object.rotating_object import RotatingObject
import numpy as np
from pytest import fixture


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
