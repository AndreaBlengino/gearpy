from gearpy.mechanical_object import GearBase, MotorBase, Flywheel, DCMotor
from gearpy.units import Time
from pytest import fixture
from tests.conftest import types_to_check, basic_spur_gear_1, basic_transmission, basic_dc_motor_1


add_gear_mating_type_error_1 = [{'master': type_to_check, 'slave': basic_spur_gear_1, 'efficiency': 0.5}
                                for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]

add_gear_mating_type_error_2 = [{'master': basic_spur_gear_1, 'slave': type_to_check, 'efficiency': 0.5}
                                for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]

add_gear_mating_type_error_3 = [{'master': basic_spur_gear_1, 'slave': basic_spur_gear_1, 'efficiency': type_to_check}
                                for type_to_check in types_to_check if not isinstance(type_to_check, float)
                                and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]

@fixture(params = [*add_gear_mating_type_error_1,
                   *add_gear_mating_type_error_2,
                   *add_gear_mating_type_error_3])
def add_gear_mating_type_error(request):
    return request.param


@fixture(params = [-1, 2, 0.5])
def add_gear_mating_value_error(request):
    return request.param


add_fixed_joint_type_error_1 = [{'master': type_to_check, 'slave': basic_spur_gear_1} for type_to_check in types_to_check
                                if not isinstance(type_to_check, GearBase) and not isinstance(type_to_check, MotorBase)
                                and not isinstance(type_to_check, Flywheel)]

add_fixed_joint_type_error_2 = [{'master': basic_spur_gear_1, 'slave': type_to_check} for type_to_check in types_to_check
                                if not isinstance(type_to_check, GearBase) and not isinstance(type_to_check, Flywheel)]

@fixture(params = [*add_fixed_joint_type_error_1,
                   *add_fixed_joint_type_error_2])
def add_fixed_joint_type_error(request):
    return request.param


dc_motor_characteristics_animation_type_error_1 = [{'motor': type_to_check, 'time': basic_transmission.time}
                                                   for type_to_check in types_to_check
                                                   if not isinstance(type_to_check, DCMotor)]

dc_motor_characteristics_animation_type_error_2 = [{'motor': basic_transmission.chain[0], 'time': type_to_check}
                                                   for type_to_check in types_to_check
                                                   if not isinstance(type_to_check, list)]

dc_motor_characteristics_animation_type_error_3 = [{'motor': basic_transmission.chain[0], 'time': [type_to_check]}
                                                   for type_to_check in types_to_check
                                                   if not isinstance(type_to_check, Time)]

dc_motor_characteristics_animation_type_error_4 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                    'interval': type_to_check} for type_to_check in types_to_check
                                                   if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)
                                                   and not isinstance(type_to_check, bool)]

dc_motor_characteristics_animation_type_error_5 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                    'torque_speed_curve': type_to_check} for type_to_check in types_to_check
                                                   if not isinstance(type_to_check, bool) and not isinstance(type_to_check, int)]

dc_motor_characteristics_animation_type_error_6 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                    'torque_current_curve': type_to_check} for type_to_check in types_to_check
                                                   if not isinstance(type_to_check, bool) and not isinstance(type_to_check, int)]

dc_motor_characteristics_animation_type_error_7 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                    'angular_speed_unit': type_to_check} for type_to_check in types_to_check
                                                   if not isinstance(type_to_check, str)]

dc_motor_characteristics_animation_type_error_8 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                    'torque_unit': type_to_check} for type_to_check in types_to_check
                                                   if not isinstance(type_to_check, str)]

dc_motor_characteristics_animation_type_error_9 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                    'current_unit': type_to_check} for type_to_check in types_to_check
                                                   if not isinstance(type_to_check, str)]

dc_motor_characteristics_animation_type_error_10 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                     'figsize': type_to_check} for type_to_check in types_to_check
                                                     if not isinstance(type_to_check, tuple) and type_to_check is not None]

dc_motor_characteristics_animation_type_error_11 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                     'figsize': (type_to_check, type_to_check)} for type_to_check in types_to_check
                                                     if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)
                                                     and not isinstance(type_to_check, bool)]

dc_motor_characteristics_animation_type_error_12 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                     'line_color': type_to_check} for type_to_check in types_to_check
                                                    if not isinstance(type_to_check, str) and type_to_check is not None]

dc_motor_characteristics_animation_type_error_13 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                     'marker_color': type_to_check} for type_to_check in types_to_check
                                                    if not isinstance(type_to_check, str) and type_to_check is not None]

dc_motor_characteristics_animation_type_error_14 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                     'marker_size': type_to_check} for type_to_check in types_to_check
                                                     if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)
                                                     and not isinstance(type_to_check, bool) and type_to_check is not None]

dc_motor_characteristics_animation_type_error_15 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                     'padding': type_to_check} for type_to_check in types_to_check
                                                     if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)
                                                     and not isinstance(type_to_check, bool)]

dc_motor_characteristics_animation_type_error_16 = [{'motor': basic_transmission.chain[0], 'time': basic_transmission.time,
                                                     'show': type_to_check} for type_to_check in types_to_check
                                                     if not isinstance(type_to_check, bool) and not isinstance(type_to_check, int)]

@fixture(params = [*dc_motor_characteristics_animation_type_error_1,
                   *dc_motor_characteristics_animation_type_error_2,
                   *dc_motor_characteristics_animation_type_error_3,
                   *dc_motor_characteristics_animation_type_error_4,
                   *dc_motor_characteristics_animation_type_error_5,
                   *dc_motor_characteristics_animation_type_error_6,
                   *dc_motor_characteristics_animation_type_error_7,
                   *dc_motor_characteristics_animation_type_error_8,
                   *dc_motor_characteristics_animation_type_error_9,
                   *dc_motor_characteristics_animation_type_error_10,
                   *dc_motor_characteristics_animation_type_error_11,
                   *dc_motor_characteristics_animation_type_error_12,
                   *dc_motor_characteristics_animation_type_error_13,
                   *dc_motor_characteristics_animation_type_error_14,
                   *dc_motor_characteristics_animation_type_error_15,
                   *dc_motor_characteristics_animation_type_error_16])
def dc_motor_characteristics_animation_type_error(request):
    return request.param


@fixture(params = [{'motor': basic_transmission.chain[0], 'time': []},
                   {'motor': basic_transmission.chain[0], 'time': basic_transmission.time, 'torque_speed_curve': False, 'torque_current_curve': False},
                   {'motor': basic_dc_motor_1, 'time': basic_transmission.time, 'torque_current_curve': True},
                   {'motor': basic_transmission.chain[0], 'time': basic_transmission.time, 'figsize': (1, )},
                   {'motor': basic_transmission.chain[0], 'time': basic_transmission.time, 'figsize': (1, 2, 3)},
                   {'motor': basic_transmission.chain[0], 'time': basic_transmission.time, 'padding': -1}])
def dc_motor_characteristics_animation_value_error(request):
    return request.param
