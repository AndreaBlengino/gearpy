import numpy as np
from pytest import fixture


types_to_check = ['string', 2, 2.2, True, (0, 1), [0, 1], {0, 1}, {0: 1}, None, np.array([0])]


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
