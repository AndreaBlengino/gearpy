from gearpy.mechanical_object import MotorBase, RotatingObject, DCMotor
from gearpy.units import Time
from pytest import fixture
from tests.conftest import types_to_check, basic_transmission


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)])
def transmission_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Time)])
def transmission_update_time_type_error(request):
    return request.param


transmission_snapshot_type_error_1 = [{'target_time': type_to_check, 'angular_position_unit': 'rad',
                                       'angular_speed_unit': 'rad/s', 'angular_acceleration_unit': 'rad/s^2',
                                       'torque_unit': 'Nm', 'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, Time)]

transmission_snapshot_type_error_2 = [{'target_time': Time(1, 'sec'), 'angular_position_unit': type_to_check,
                                       'angular_speed_unit': 'rad/s', 'angular_acceleration_unit': 'rad/s^2',
                                       'torque_unit': 'Nm', 'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_3 = [{'target_time': Time(1, 'sec'), 'angular_position_unit': 'rad',
                                       'angular_speed_unit': type_to_check, 'angular_acceleration_unit': 'rad/s^2',
                                       'torque_unit': 'Nm', 'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_4 = [{'target_time': Time(1, 'sec'), 'angular_position_unit': 'rad',
                                       'angular_speed_unit': 'rad/s', 'angular_acceleration_unit': type_to_check,
                                       'torque_unit': 'Nm', 'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_5 = [{'target_time': Time(1, 'sec'), 'angular_position_unit': 'rad',
                                       'angular_speed_unit': 'rad/s', 'angular_acceleration_unit': 'rad/s^2',
                                       'torque_unit': type_to_check, 'driving_torque_unit': 'Nm',
                                       'load_torque_unit': 'Nm', 'print_data': False}
                                      for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_6 = [{'target_time': Time(1, 'sec'), 'angular_position_unit': 'rad',
                                       'angular_speed_unit': 'rad/s', 'angular_acceleration_unit': 'rad/s^2',
                                       'torque_unit': 'Nm', 'driving_torque_unit': type_to_check,
                                       'load_torque_unit': 'Nm', 'print_data': False}
                                      for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_7 = [{'target_time': Time(1, 'sec'), 'angular_position_unit': 'rad',
                                       'angular_speed_unit': 'rad/s', 'angular_acceleration_unit': 'rad/s^2',
                                       'torque_unit': 'Nm', 'driving_torque_unit': 'Nm',
                                       'load_torque_unit': type_to_check, 'print_data': False}
                                      for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_8 = [{'target_time': Time(1, 'sec'), 'angular_position_unit': 'rad',
                                        'angular_speed_unit': 'rad/s', 'angular_acceleration_unit': 'rad/s^2',
                                        'torque_unit': 'Nm', 'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                        'print_data': type_to_check} for type_to_check in types_to_check
                                       if not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]

transmission_snapshot_type_error_9 = [{}]

@fixture(params = [*transmission_snapshot_type_error_1,
                   *transmission_snapshot_type_error_2,
                   *transmission_snapshot_type_error_3,
                   *transmission_snapshot_type_error_4,
                   *transmission_snapshot_type_error_5,
                   *transmission_snapshot_type_error_6,
                   *transmission_snapshot_type_error_7,
                   *transmission_snapshot_type_error_8,
                   *transmission_snapshot_type_error_9])
def transmission_snapshot_type_error(request):
    return request.param


elements = [basic_transmission.chain[0]]
variables = list(basic_transmission.chain[0].time_variables.keys())

transmission_plot_type_error_1 = [{'elements': type_to_check, 'variables': variables,
                                   'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check
                                  if not isinstance(type_to_check, list) and type_to_check is not None]

transmission_plot_type_error_2 = [{'elements': [type_to_check], 'variables': variables,
                                   'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check
                                  if not isinstance(type_to_check, RotatingObject) and not isinstance(type_to_check, str)]

transmission_plot_type_error_3 = [{'elements': elements, 'variables': type_to_check,
                                   'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check
                                  if not isinstance(type_to_check, list) and type_to_check is not None]

transmission_plot_type_error_4 = [{'elements': elements, 'variables': [type_to_check],
                                   'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_plot_type_error_5 = [{'elements': elements, 'variables': variables,
                                   'angular_position_unit': type_to_check, 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_plot_type_error_6 = [{'elements': elements, 'variables': variables,
                                   'angular_position_unit': 'rad', 'angular_speed_unit': type_to_check,
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_plot_type_error_7 = [{'elements': elements, 'variables': variables,
                                   'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': type_to_check, 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_plot_type_error_8 = [{'elements': elements, 'variables': variables,
                                   'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': type_to_check,
                                   'time_unit': 'sec'} for type_to_check in types_to_check
                                  if not isinstance(type_to_check, str)]

transmission_plot_type_error_9 = [{'elements': elements, 'variables': variables,
                                   'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm',
                                   'time_unit': type_to_check} for type_to_check in types_to_check
                                  if not isinstance(type_to_check, str)]

@fixture(params = [*transmission_plot_type_error_1,
                   *transmission_plot_type_error_2,
                   *transmission_plot_type_error_3,
                   *transmission_plot_type_error_4,
                   *transmission_plot_type_error_5,
                   *transmission_plot_type_error_6,
                   *transmission_plot_type_error_7,
                   *transmission_plot_type_error_8,
                   *transmission_plot_type_error_9])
def transmission_plot_type_error(request):
    return request.param


motor_not_in_basic_transmission = DCMotor(name = basic_transmission.chain[0].name + ' ',
                                          inertia_moment = basic_transmission.chain[0].inertia_moment,
                                          maximum_torque = basic_transmission.chain[0].maximum_torque,
                                          no_load_speed = basic_transmission.chain[0].no_load_speed)

@fixture(params = [{'elements': []},
                   {'elements': [motor_not_in_basic_transmission]},
                   {'elements': [motor_not_in_basic_transmission.name]},
                   {'variables': []},
                   {'variables': [f"not a {variables[0]}"]}])
def transmission_plot_value_error(request):
    return request.param
