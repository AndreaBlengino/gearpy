from gearpy.mechanical_objects import RotatingObject, GearBase, MotorBase, DCMotor, SpurGear, HelicalGear, WormGear, \
                                      WormWheel
from gearpy.motor_control import PWMControl
from gearpy.motor_control.rules import ReachAngularPosition
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.solver import Solver
from gearpy.powertrain import Powertrain
from gearpy.units import (
    Angle,
    AngularPosition,
    AngularSpeed,
    Current,
    InertiaMoment,
    Length,
    Time,
    TimeInterval,
    Torque
)
from gearpy.utils import add_fixed_joint
from pytest import fixture
from tests.conftest import (
    types_to_check,
    basic_spur_gear_1,
    basic_powertrain,
    basic_dc_motor_1,
    basic_worm_gear_1,
    basic_worm_wheel_1
)


mate_gear = SpurGear(
    name='mate gear',
    n_teeth=20,
    inertia_moment=InertiaMoment(1, 'kgm^2')
)

add_gear_mating_type_error_1 = [
    {'master': type_to_check, 'slave': mate_gear, 'efficiency': 0.5}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, GearBase)
]

add_gear_mating_type_error_2 = [
    {'master': mate_gear, 'slave': type_to_check, 'efficiency': 0.5}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, GearBase)
]

add_gear_mating_type_error_3 = [
    {
        'master': basic_spur_gear_1,
        'slave': mate_gear,
        'efficiency': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float) and
    not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)
]


@fixture(
    params=[
        *add_gear_mating_type_error_1,
        *add_gear_mating_type_error_2,
        *add_gear_mating_type_error_3
    ]
)
def add_gear_mating_type_error(request):
    return request.param


gear = HelicalGear(
    name='master',
    n_teeth=10,
    helix_angle=Angle(20, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2')
)


@fixture(
    params=[
        {
            'master': SpurGear(
                name='master',
                n_teeth=10,
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'slave': SpurGear(
                name='slave',
                n_teeth=10,
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'efficiency': -1
        },
        {
            'master': SpurGear(
                name='master',
                n_teeth=10,
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'slave': SpurGear(
                name='slave',
                n_teeth=10,
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'efficiency': 2
        },
        {
            'master': SpurGear(
                name='master',
                n_teeth=10,
                module=Length(1, 'mm'),
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'slave': SpurGear(
                name='slave',
                n_teeth=10,
                module=Length(2, 'mm'),
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'efficiency': 0.9
        },
        {
            'master': SpurGear(
                name='master',
                n_teeth=10,
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'slave': HelicalGear(
                name='slave',
                n_teeth=10,
                helix_angle=Angle(30, 'deg'),
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'efficiency': 0.9
        },
        {
            'master': HelicalGear(
                name='master',
                n_teeth=10,
                helix_angle=Angle(30, 'deg'),
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'slave': SpurGear(
                name='slave',
                n_teeth=10,
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'efficiency': 0.9
        },
        {
            'master': HelicalGear(
                name='master',
                n_teeth=10,
                helix_angle=Angle(20, 'deg'),
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'slave': HelicalGear(
                name='slave',
                n_teeth=10,
                helix_angle=Angle(30, 'deg'),
                inertia_moment=InertiaMoment(1, 'kgm^2')
            ),
            'efficiency': 0.9
        },
        {'master': gear, 'slave': gear, 'efficiency': 0.9}
    ]
)
def add_gear_mating_value_error(request):
    return request.param


add_worm_gear_mating_type_error_1 = [
    {
        'master': type_to_check,
        'slave': basic_worm_wheel_1,
        'friction_coefficient': 0
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, WormGear) and
    not isinstance(type_to_check, WormWheel)
]

add_worm_gear_mating_type_error_2 = [
    {
        'master': basic_worm_gear_1,
        'slave': type_to_check,
        'friction_coefficient': 0
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, WormGear) and
    not isinstance(type_to_check, WormWheel)
]

add_worm_gear_mating_type_error_3 = [
    {
        'master': basic_worm_gear_1,
        'slave': basic_worm_gear_1,
        'friction_coefficient': 0
    }
]

add_worm_gear_mating_type_error_4 = [
    {
        'master': basic_worm_wheel_1,
        'slave': basic_worm_wheel_1,
        'friction_coefficient': 0
    }
]

add_worm_gear_mating_type_error_5 = [
    {
        'master': basic_worm_gear_1,
        'slave': basic_worm_wheel_1,
        'friction_coefficient': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float) and
    not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)
]


@fixture(
    params=[
        *add_worm_gear_mating_type_error_1,
        *add_worm_gear_mating_type_error_2,
        *add_worm_gear_mating_type_error_3,
        *add_worm_gear_mating_type_error_4,
        *add_worm_gear_mating_type_error_5
    ]
)
def add_worm_gear_mating_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'master': basic_worm_gear_1,
            'slave': basic_worm_wheel_1,
            'friction_coefficient': -1
        },
        {
            'master': basic_worm_gear_1,
            'slave': basic_worm_wheel_1,
            'friction_coefficient': 2
        },
        {
            'master': WormGear(
                name='worm gear',
                n_starts=1,
                inertia_moment=InertiaMoment(1, 'kgm^2'),
                pressure_angle=Angle(20, 'deg'),
                helix_angle=Angle(10, 'deg')
            ),
            'slave': WormWheel(
                name='worm gear',
                n_teeth=10,
                inertia_moment=InertiaMoment(1, 'kgm^2'),
                pressure_angle=Angle(25, 'deg'),
                helix_angle=Angle(10, 'deg')
            ),
            'friction_coefficient': 0
        }
    ]
)
def add_worm_gear_mating_value_error(request):
    return request.param


add_fixed_joint_type_error_1 = [
    {'master': type_to_check, 'slave': basic_spur_gear_1}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, RotatingObject)
]

add_fixed_joint_type_error_2 = [
    {'master': basic_spur_gear_1, 'slave': type_to_check}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, RotatingObject)
]

add_fixed_joint_type_error_3 = [
    {'master': basic_spur_gear_1, 'slave': type_to_check}
    for type_to_check in types_to_check if isinstance(type_to_check, MotorBase)
]


@fixture(
    params=[
        *add_fixed_joint_type_error_1,
        *add_fixed_joint_type_error_2,
        *add_fixed_joint_type_error_3
    ]
)
def add_fixed_joint_type_error(request):
    return request.param


motor_1 = DCMotor(
    name='motor',
    no_load_speed=AngularSpeed(1000, 'rad/s'),
    maximum_torque=Torque(1, 'Nm'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    no_load_electric_current=Current(1, 'A'),
    maximum_electric_current=Current(2, 'A')
)
gear = SpurGear(
    name='gear',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2')
)
add_fixed_joint(master=motor_1, slave=gear)
powertrain_1 = Powertrain(motor=motor_1)
encoder = AbsoluteRotaryEncoder(target=gear)
rule = ReachAngularPosition(
    encoder=encoder,
    powertrain=powertrain_1,
    target_angular_position=AngularPosition(200, 'rad'),
    braking_angle=Angle(150, 'rad')
)
motor_control = PWMControl(powertrain=powertrain_1)
motor_control.add_rule(rule=rule)
gear.external_torque = \
    lambda angular_position, angular_speed, time: Torque(0, 'Nm')
gear.angular_position = AngularPosition(0, 'rad')
gear.angular_speed = AngularSpeed(0, 'rad/s')
solver = Solver(powertrain=powertrain_1)
solver.run(
    time_discretization=TimeInterval(2, 'sec'),
    simulation_time=TimeInterval(60, 'sec'),
    motor_control=motor_control
)


motor_2 = DCMotor(
    name='motor',
    no_load_speed=AngularSpeed(1000, 'rad/s'),
    maximum_torque=Torque(1, 'Nm'),
    inertia_moment=InertiaMoment(1, 'kgm^2')
)
gear = SpurGear(
    name='gear',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2')
)
add_fixed_joint(master=motor_2, slave=gear)
powertrain_2 = Powertrain(motor=motor_2)
gear.external_torque = \
    lambda angular_position, angular_speed, time: Torque(0, 'Nm')
gear.angular_position = AngularPosition(0, 'rad')
gear.angular_speed = AngularSpeed(0, 'rad/s')
solver = Solver(powertrain=powertrain_2)
solver.run(
    time_discretization=TimeInterval(2, 'sec'),
    simulation_time=TimeInterval(20, 'sec')
)


dc_motor_characteristics_animation_type_error_1 = [
    {'motor': type_to_check, 'time': basic_powertrain.time}
    for type_to_check in types_to_check
    if not isinstance(type_to_check, DCMotor)
]

dc_motor_characteristics_animation_type_error_2 = [
    {'motor': basic_powertrain.elements[0], 'time': type_to_check}
    for type_to_check in types_to_check if not isinstance(type_to_check, list)
]

dc_motor_characteristics_animation_type_error_3 = [
    {'motor': basic_powertrain.elements[0], 'time': [type_to_check]}
    for type_to_check in types_to_check if not isinstance(type_to_check, Time)
]

dc_motor_characteristics_animation_type_error_4 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'interval': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float) and
    not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)
]

dc_motor_characteristics_animation_type_error_5 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'torque_speed_curve': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, bool) and
    not isinstance(type_to_check, int)
]

dc_motor_characteristics_animation_type_error_6 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'torque_current_curve': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, bool) and
    not isinstance(type_to_check, int)
]

dc_motor_characteristics_animation_type_error_7 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'angular_speed_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

dc_motor_characteristics_animation_type_error_8 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'torque_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

dc_motor_characteristics_animation_type_error_9 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'current_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

dc_motor_characteristics_animation_type_error_10 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'figsize': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, tuple) and type_to_check is not None
]

dc_motor_characteristics_animation_type_error_11 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'figsize': (type_to_check, type_to_check)
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float) and
    not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)
]

dc_motor_characteristics_animation_type_error_12 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'line_color': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, str) and type_to_check is not None
]

dc_motor_characteristics_animation_type_error_13 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'marker_color': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, str) and type_to_check is not None
]

dc_motor_characteristics_animation_type_error_14 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'marker_size': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float) and
    not isinstance(type_to_check, int) and
    not isinstance(type_to_check, bool) and type_to_check is not None
]

dc_motor_characteristics_animation_type_error_15 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'padding': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, float) and
    not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)
]

dc_motor_characteristics_animation_type_error_16 = [
    {
        'motor': basic_powertrain.elements[0],
        'time': basic_powertrain.time,
        'show': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, bool) and
    not isinstance(type_to_check, int)
]


@fixture(
    params=[
        *dc_motor_characteristics_animation_type_error_1,
        dc_motor_characteristics_animation_type_error_2,
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
        *dc_motor_characteristics_animation_type_error_16
    ]
)
def dc_motor_characteristics_animation_type_error(request):
    return request.param


@fixture(
    params=[
        {'motor': basic_powertrain.elements[0], 'time': []},
        {
            'motor': basic_powertrain.elements[0],
            'time': basic_powertrain.time,
            'torque_speed_curve': False,
            'torque_current_curve': False
        },
        {
            'motor': basic_dc_motor_1,
            'time': basic_powertrain.time,
            'torque_current_curve': True
        },
        {
            'motor': basic_powertrain.elements[0],
            'time': basic_powertrain.time,
            'figsize': (1, )
        },
        {
            'motor': basic_powertrain.elements[0],
            'time': basic_powertrain.time,
            'figsize': (1, 2, 3)
        },
        {
            'motor': basic_powertrain.elements[0],
            'time': basic_powertrain.time,
            'padding': -1
        }
    ]
)
def dc_motor_characteristics_animation_value_error(request):
    return request.param


export_time_variables_type_error_1 = [
    {
        'rotating_object': type_to_check,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')]
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, RotatingObject)
]

export_time_variables_type_error_2 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': type_to_check,
        'time_array': [Time(1, 'sec')]
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_3 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': type_to_check
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, list)
]

export_time_variables_type_error_4 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [type_to_check]
    } for type_to_check in types_to_check
    if not isinstance(type_to_check, Time)
]

export_time_variables_type_error_5 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'time_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_6 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'angular_position_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_7 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'angular_speed_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_8 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'angular_acceleration_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_9 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'torque_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_10 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'driving_torque_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_11 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'load_torque_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_12 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'force_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_13 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'stress_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]

export_time_variables_type_error_14 = [
    {
        'rotating_object': basic_dc_motor_1,
        'file_path': './test_data',
        'time_array': [Time(1, 'sec')],
        'current_unit': type_to_check
    } for type_to_check in types_to_check if not isinstance(type_to_check, str)
]


@fixture(
    params=[
        *export_time_variables_type_error_1,
        *export_time_variables_type_error_2,
        *export_time_variables_type_error_3,
        *export_time_variables_type_error_4,
        *export_time_variables_type_error_5,
        *export_time_variables_type_error_6,
        *export_time_variables_type_error_7,
        *export_time_variables_type_error_8,
        *export_time_variables_type_error_9,
        *export_time_variables_type_error_10,
        *export_time_variables_type_error_11,
        *export_time_variables_type_error_12,
        *export_time_variables_type_error_13,
        *export_time_variables_type_error_14
    ]
)
def export_time_variables_type_error(request):
    return request.param


@fixture(
    params=[
        {
            'rotating_object': basic_dc_motor_1,
            'file_path': '',
            'time_array': [Time(1, 'sec')]
        },
        {
            'rotating_object': basic_dc_motor_1,
            'file_path': './test_data',
            'time_array': []
        }
    ]
)
def export_time_variables_value_error(request):
    return request.param
