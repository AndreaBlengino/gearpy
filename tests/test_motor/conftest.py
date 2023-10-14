from gearpy.mechanical_object import RotatingObject
from gearpy.units import AngularSpeed, InertiaMoment, Torque
from tests.conftest import types_to_check
from pytest import fixture


dc_motor_init_type_error_1 = [{'name': type_to_check, 'inertia_moment': InertiaMoment(1, 'kgm^2'),
                               'no_load_speed': AngularSpeed(1000, 'rpm'), 'maximum_torque': Torque(1, 'Nm')}
                              for type_to_check in types_to_check if not isinstance(type_to_check, str)]

dc_motor_init_type_error_2 = [{'name': 'motor', 'inertia_moment': type_to_check,
                               'no_load_speed': AngularSpeed(1000, 'rpm'), 'maximum_torque': Torque(1, 'Nm')}
                              for type_to_check in types_to_check if not isinstance(type_to_check, InertiaMoment)]

dc_motor_init_type_error_3 = [{'name': 'motor', 'inertia_moment': InertiaMoment(1, 'kgm^2'),
                               'no_load_speed': type_to_check, 'maximum_torque': Torque(1, 'Nm')}
                              for type_to_check in types_to_check if not isinstance(type_to_check, AngularSpeed)]

dc_motor_init_type_error_4 = [{'name': 'motor', 'inertia_moment': InertiaMoment(1, 'kgm^2'),
                               'no_load_speed': AngularSpeed(1000, 'rpm'), 'maximum_torque': type_to_check}
                              for type_to_check in types_to_check if not isinstance(type_to_check, Torque)]

@fixture(params = [*dc_motor_init_type_error_1,
                   *dc_motor_init_type_error_2,
                   *dc_motor_init_type_error_3,
                   *dc_motor_init_type_error_4])
def dc_motor_init_type_error(request):
    return request.param


@fixture(params = [{'name': '', 'inertia_moment': InertiaMoment(1, 'kgm^2'), 'no_load_speed': AngularSpeed(1000, 'rpm'), 'maximum_torque': Torque(1, 'Nm')},
                   {'name': 'motor', 'inertia_moment': InertiaMoment(1, 'kgm^2'), 'no_load_speed': AngularSpeed(-1000, 'rpm'), 'maximum_torque': Torque(1, 'Nm')},
                   {'name': 'motor', 'inertia_moment': InertiaMoment(1, 'kgm^2'), 'no_load_speed': AngularSpeed(1000, 'rpm'), 'maximum_torque': Torque(-1, 'Nm')}])
def dc_motor_init_value_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)])
def dc_motor_drives_type_error(request):
    return request.param
