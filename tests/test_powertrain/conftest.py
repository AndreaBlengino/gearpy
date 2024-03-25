from gearpy.mechanical_objects import MotorBase, RotatingObject, DCMotor
from gearpy.units import Time
from pytest import fixture
from tests.conftest import types_to_check, basic_powertrain


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)])
def powertrain_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Time)])
def powertrain_update_time_type_error(request):
    return request.param


powertrain_snapshot_type_error_1 = [{'target_time': type_to_check}
                                    for type_to_check in types_to_check if not isinstance(type_to_check, Time)]

powertrain_snapshot_type_error_2 = [{'target_time': Time(1, 'sec'), 'variables': type_to_check}
                                    for type_to_check in types_to_check if not isinstance(type_to_check, list)
                                    and type_to_check is not None]

powertrain_snapshot_type_error_3 = [{'target_time': Time(1, 'sec'), 'variables': [type_to_check]}
                                    for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_4 = [{'target_time': Time(1, 'sec'), 'angular_position_unit': type_to_check}
                                    for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_5 = [{'target_time': Time(1, 'sec'), 'angular_speed_unit': type_to_check}
                                    for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_6 = [{'target_time': Time(1, 'sec'), 'angular_acceleration_unit': type_to_check}
                                    for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_7 = [{'target_time': Time(1, 'sec'), 'torque_unit': type_to_check}
                                    for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_8 = [{'target_time': Time(1, 'sec'), 'driving_torque_unit': type_to_check}
                                    for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_9 = [{'target_time': Time(1, 'sec'), 'load_torque_unit': type_to_check}
                                    for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_10 = [{'target_time': Time(1, 'sec'), 'force_unit': type_to_check}
                                     for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_11 = [{'target_time': Time(1, 'sec'), 'stress_unit': type_to_check}
                                     for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_12 = [{'target_time': Time(1, 'sec'), 'current_unit': type_to_check}
                                     for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_snapshot_type_error_13 = [{'target_time': Time(1, 'sec'), 'print_data': type_to_check}
                                     for type_to_check in types_to_check
                                     if not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]

powertrain_snapshot_type_error_14 = [{}]

@fixture(params = [*powertrain_snapshot_type_error_1,
                   *powertrain_snapshot_type_error_2,
                   *powertrain_snapshot_type_error_3,
                   *powertrain_snapshot_type_error_4,
                   *powertrain_snapshot_type_error_5,
                   *powertrain_snapshot_type_error_6,
                   *powertrain_snapshot_type_error_7,
                   *powertrain_snapshot_type_error_8,
                   *powertrain_snapshot_type_error_9,
                   *powertrain_snapshot_type_error_10,
                   *powertrain_snapshot_type_error_11,
                   *powertrain_snapshot_type_error_12,
                   *powertrain_snapshot_type_error_13,
                   *powertrain_snapshot_type_error_14])
def powertrain_snapshot_type_error(request):
    return request.param


powertrain_snapshot_value_error_1 = [{'target_time': max(basic_powertrain.time) + Time(1, 'sec')}]

powertrain_snapshot_value_error_2 = [{'target_time': min(basic_powertrain.time) - Time(1, 'sec')}]

powertrain_snapshot_value_error_3 = [{'target_time': max(basic_powertrain.time), 'variables': []}]

powertrain_snapshot_value_error_4 = [{'target_time': max(basic_powertrain.time), 'variables': ['not a valid time variable']}]

powertrain_snapshot_value_error_5 = [{}]

@fixture(params = [*powertrain_snapshot_value_error_1,
                   *powertrain_snapshot_value_error_2,
                   *powertrain_snapshot_value_error_3,
                   *powertrain_snapshot_value_error_4,
                   *powertrain_snapshot_value_error_5])
def powertrain_snapshot_value_error(request):
    return request.param


elements = [basic_powertrain.elements[0]]
variables = list(basic_powertrain.elements[0].time_variables.keys())

powertrain_plot_type_error_1 = [{'elements': type_to_check}
                                for type_to_check in types_to_check
                                if not isinstance(type_to_check, list) and type_to_check is not None]

powertrain_plot_type_error_2 = [{'elements': [type_to_check]}
                                for type_to_check in types_to_check
                                if not isinstance(type_to_check, RotatingObject) and not isinstance(type_to_check, str)]

powertrain_plot_type_error_3 = [{'variables': type_to_check}
                                for type_to_check in types_to_check
                                if not isinstance(type_to_check, list) and type_to_check is not None]

powertrain_plot_type_error_4 = [{'variables': [type_to_check]}
                                for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_plot_type_error_5 = [{'angular_position_unit': type_to_check}
                                for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_plot_type_error_6 = [{'angular_speed_unit': type_to_check}
                                for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_plot_type_error_7 = [{'angular_acceleration_unit': type_to_check}
                                for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_plot_type_error_8 = [{'torque_unit': type_to_check}
                                for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_plot_type_error_9 = [{'force_unit': type_to_check}
                                for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_plot_type_error_10 = [{'stress_unit': type_to_check}
                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_plot_type_error_11 = [{'current_unit': type_to_check}
                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_plot_type_error_12 = [{'time_unit': type_to_check}
                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_plot_type_error_13 = [{'figsize': type_to_check}
                                 for type_to_check in types_to_check
                                 if not isinstance(type_to_check, tuple) and type_to_check is not None]

powertrain_plot_type_error_14 = [{'figsize': (type_to_check, type_to_check)}
                                 for type_to_check in types_to_check
                                 if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)]

@fixture(params = [*powertrain_plot_type_error_1,
                   *powertrain_plot_type_error_2,
                   *powertrain_plot_type_error_3,
                   *powertrain_plot_type_error_4,
                   *powertrain_plot_type_error_5,
                   *powertrain_plot_type_error_6,
                   *powertrain_plot_type_error_7,
                   *powertrain_plot_type_error_8,
                   *powertrain_plot_type_error_9,
                   *powertrain_plot_type_error_10,
                   *powertrain_plot_type_error_11,
                   *powertrain_plot_type_error_12,
                   *powertrain_plot_type_error_13,
                   *powertrain_plot_type_error_14])
def powertrain_plot_type_error(request):
    return request.param


motor_not_in_basic_powertrain = DCMotor(name = basic_powertrain.elements[0].name + ' ',
                                        inertia_moment = basic_powertrain.elements[0].inertia_moment,
                                        maximum_torque = basic_powertrain.elements[0].maximum_torque,
                                        no_load_speed = basic_powertrain.elements[0].no_load_speed)

@fixture(params = [{'elements': []},
                   {'elements': [motor_not_in_basic_powertrain]},
                   {'elements': [motor_not_in_basic_powertrain.name]},
                   {'variables': []},
                   {'variables': [f"not a {variables[0]}"]},
                   {'figsize': (1, 1, 1)}])
def powertrain_plot_value_error(request):
    return request.param


powertrain_export_time_variables_type_error_1 = [{'folder_path': type_to_check} for type_to_check in types_to_check
                                                 if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_2 = [{'folder_path': './test_data', 'time_unit': type_to_check}
                                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_3 = [{'folder_path': './test_data', 'angular_position_unit': type_to_check}
                                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_4 = [{'folder_path': './test_data', 'angular_speed_unit': type_to_check}
                                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_5 = [{'folder_path': './test_data', 'angular_acceleration_unit': type_to_check}
                                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_6 = [{'folder_path': './test_data', 'torque_unit': type_to_check}
                                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_7 = [{'folder_path': './test_data', 'driving_torque_unit': type_to_check}
                                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_8 = [{'folder_path': './test_data', 'load_torque_unit': type_to_check}
                                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_9 = [{'folder_path': './test_data', 'force_unit': type_to_check}
                                                 for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_10 = [{'folder_path': './test_data', 'stress_unit': type_to_check}
                                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

powertrain_export_time_variables_type_error_11 = [{'folder_path': './test_data', 'current_unit': type_to_check}
                                                  for type_to_check in types_to_check if not isinstance(type_to_check, str)]

@fixture(params = [*powertrain_export_time_variables_type_error_1,
                   *powertrain_export_time_variables_type_error_2,
                   *powertrain_export_time_variables_type_error_3,
                   *powertrain_export_time_variables_type_error_4,
                   *powertrain_export_time_variables_type_error_5,
                   *powertrain_export_time_variables_type_error_6,
                   *powertrain_export_time_variables_type_error_7,
                   *powertrain_export_time_variables_type_error_8,
                   *powertrain_export_time_variables_type_error_9,
                   *powertrain_export_time_variables_type_error_10,
                   *powertrain_export_time_variables_type_error_11])
def powertrain_export_time_variables_type_error(request):
    return request.param
