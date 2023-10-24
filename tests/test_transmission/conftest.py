from gearpy.mechanical_object import MotorBase
from gearpy.units import Time
from pytest import fixture
from tests.conftest import types_to_check


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


transmission_plot_type_error_1 = [{'angular_position_unit': type_to_check, 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_plot_type_error_2 = [{'angular_position_unit': 'rad', 'angular_speed_unit': type_to_check,
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_plot_type_error_3 = [{'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': type_to_check, 'torque_unit': 'Nm', 'time_unit': 'sec'}
                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_plot_type_error_4 = [{'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': type_to_check, 'time_unit': 'sec'}
                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

transmission_plot_type_error_5 = [{'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                   'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm', 'time_unit': type_to_check}
                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

@fixture(params = [*transmission_plot_type_error_1,
                   *transmission_plot_type_error_2,
                   *transmission_plot_type_error_3,
                   *transmission_plot_type_error_4,
                   *transmission_plot_type_error_5])
def transmission_plot_type_error(request):
    return request.param
