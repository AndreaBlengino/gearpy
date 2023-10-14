# from gearpy.gear import GearBase, SpurGear
# from gearpy.mechanical_object import RotatingObject
# from gearpy.motor import MotorBase, DCMotor
# from gearpy.transmission import Transmission
from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, InertiaMoment, Torque, Time, TimeInterval
# from gearpy.utils import add_fixed_joint, add_gear_mating
# from hypothesis.strategies import composite, text, integers, floats, lists
import numpy as np
# from pytest import fixture
# from typing import Callable
#
#
# basic_dc_motor = DCMotor(name = 'name', inertia_moment = 1, no_load_speed = 1, maximum_torque = 1)
# basic_spur_gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = 1)
# basic_rotating_objects = [basic_dc_motor, basic_spur_gear]
#


types_to_check = ['string', 2, 2.2, True, (0, 1), [0, 1], {0, 1}, {0: 1}, None, np.array([0]),
                  AngularPosition(1, 'rad'), AngularSpeed(1, 'rad/s'), AngularAcceleration(1, 'rad/s^2'),
                  InertiaMoment(1, 'kgm^2'), Torque(1, 'Nm'), Time(1, 'sec'), TimeInterval(1, 'sec')]


#
# @composite
# def dc_motors(draw):
#     name = draw(text(min_size = 1))
#     inertia = draw(floats(min_value = 0, exclude_min = True, allow_nan = False, allow_infinity = False))
#     no_load_speed = draw(floats(min_value = 0, exclude_min = True, allow_nan = False, allow_infinity = False))
#     maximum_torque = draw(floats(min_value = 0, exclude_min = True, allow_nan = False, allow_infinity = False))
#
#     return DCMotor(name = name, inertia_moment = inertia, no_load_speed = no_load_speed, maximum_torque = maximum_torque)
#
#
# @composite
# def spur_gears(draw):
#     name = draw(text(min_size = 1))
#     n_teeth = draw(integers(min_value = 1))
#     inertia = draw(floats(min_value = 0, exclude_min = True, allow_nan = False, allow_infinity = False))
#
#     return SpurGear(name = name, n_teeth = n_teeth, inertia_moment = inertia)
#
#
# @composite
# def transmissions(draw):
#     motor = draw(dc_motors())
#     gears = draw(lists(elements = spur_gears(), min_size = 1))
#
#     add_fixed_joint(master = motor, slave = gears[0])
#
#     for i in range(0, len(gears) - 1):
#         if i%2 == 0:
#             add_gear_mating(master = gears[i], slave = gears[i + 1], efficiency = 1)
#         else:
#             add_fixed_joint(master = gears[i], slave = gears[i + 1])
#
#     return Transmission(motor = motor)
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                    and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
# def rotating_object_angle_type_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                    and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
# def rotating_object_speed_type_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                    and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
# def rotating_object_acceleration_type_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                    and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
# def rotating_object_torque_type_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                    and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
# def rotating_object_driving_torque_type_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                    and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
# def rotating_object_load_torque_type_error(request):
#     return request.param
#
#
# dc_motor_init_type_error_1 = [{'name': type_to_check, 'inertia_moment': 1, 'no_load_speed': 1, 'maximum_torque': 1}
#                               for type_to_check in types_to_check if not isinstance(type_to_check, str)]
#
# dc_motor_init_type_error_2 = [{'name': 'motor', 'inertia_moment': type_to_check, 'no_load_speed': 1, 'maximum_torque': 1}
#                               for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                               and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]
#
# dc_motor_init_type_error_3 = [{'name': 'motor', 'inertia_moment': 1, 'no_load_speed': type_to_check, 'maximum_torque': 1}
#                               for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                               and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]
#
# dc_motor_init_type_error_4 = [{'name': 'motor', 'inertia_moment': 1, 'no_load_speed': 1, 'maximum_torque': type_to_check}
#                               for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                               and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]
#
# @fixture(params = [*dc_motor_init_type_error_1,
#                    *dc_motor_init_type_error_2,
#                    *dc_motor_init_type_error_3,
#                    *dc_motor_init_type_error_4])
# def dc_motor_init_type_error(request):
#     return request.param
#
#
# @fixture(params = [{'name': '', 'inertia_moment': 1, 'no_load_speed': 1, 'maximum_torque': 1},
#                    {'name': 'motor', 'inertia_moment': -1, 'no_load_speed': 1, 'maximum_torque': 1},
#                    {'name': 'motor', 'inertia_moment': 1, 'no_load_speed': -1, 'maximum_torque': 1},
#                    {'name': 'motor', 'inertia_moment': 1, 'no_load_speed': 1, 'maximum_torque': -1}])
# def dc_motor_init_value_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)])
# def dc_motor_drives_type_error(request):
#     return request.param
#
#
# @fixture(params = [{'name': 'gear', 'n_teeth': type_to_check, 'inertia_moment': 1} for type_to_check in types_to_check
#                    if not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
# def spur_gear_init_type_error(request):
#     return request.param
#
#
# @fixture(params = [{'name': '', 'n_teeth': 1, 'inertia_moment': 1},
#                    {'name': 'gear', 'n_teeth': -1, 'inertia_moment': 1},
#                    {'name': 'gear', 'n_teeth': 1, 'inertia_moment': -1}])
# def spur_gear_init_value_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)])
# def spur_gear_driven_by_type_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)])
# def spur_gear_drives_type_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)])
# def spur_gear_master_gear_ratio_type_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                    and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)])
# def spur_gear_master_gear_efficiency_type_error(request):
#     return request.param
#
#
# @fixture(params = [-1, 2])
# def spur_gear_master_gear_efficiency_value_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, Callable)])
# def spur_gear_external_torque_type_error(request):
#     return request.param
#
#
# add_gear_mating_type_error_1 = [{'gear 1': type_to_check, 'gear 2': basic_spur_gear, 'efficiency': 0.5}
#                                 for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]
#
# add_gear_mating_type_error_2 = [{'gear 1': basic_spur_gear, 'gear 2': type_to_check, 'efficiency': 0.5}
#                                 for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]
#
# add_gear_mating_type_error_3 = [{'gear 1': basic_spur_gear, 'gear 2': basic_spur_gear, 'efficiency': type_to_check}
#                                 for type_to_check in types_to_check if not isinstance(type_to_check, float)
#                                 and not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]
#
# @fixture(params = [*add_gear_mating_type_error_1,
#                    *add_gear_mating_type_error_2,
#                    *add_gear_mating_type_error_3])
# def add_gear_mating_type_error(request):
#     return request.param
#
#
# @fixture(params = [-1, 2])
# def add_gear_mating_value_error(request):
#     return request.param
#
#
# add_fixed_joint_type_error_1 = [{'master': type_to_check, 'slave': basic_spur_gear} for type_to_check in types_to_check
#                                 if not isinstance(type_to_check, GearBase) and not isinstance(type_to_check, MotorBase)]
#
# add_fixed_joint_type_error_2 = [{'master': basic_spur_gear, 'slave': type_to_check}
#                                 for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]
#
# @fixture(params = [*add_fixed_joint_type_error_1,
#                    *add_fixed_joint_type_error_2])
# def add_fixed_joint_type_error(request):
#     return request.param
#
#
# @fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)])
# def transmission_init_type_error(request):
#     return request.param
#
#
# motor_transmission_solver_init_type_error = DCMotor(name = 'name', inertia_moment = 1, no_load_speed = 1, maximum_torque = 1)
# gear_transmission_solver_init_type_error = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = 1)
# add_fixed_joint(master = motor_transmission_solver_init_type_error, slave = gear_transmission_solver_init_type_error)
# transmission_solver_init_type_error = Transmission(motor = motor_transmission_solver_init_type_error)
#
# class TransmissionFake(Transmission):
#
#     def __init__(self, chain: list):
#         self.__chain = chain
#
#     @property
#     def chain(self):
#         return self.__chain
#
#     @chain.setter
#     def chain(self, chain):
#         self.__chain = chain
#
# solver_init_type_error_1 = [{'time_discretization': type_to_check, 'simulation_time': 1,
#                              'transmission': transmission_solver_init_type_error} for type_to_check in types_to_check
#                             if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)
#                             and not isinstance(type_to_check, bool)]
#
# solver_init_type_error_2 = [{'time_discretization': 1, 'simulation_time': type_to_check,
#                              'transmission': transmission_solver_init_type_error} for type_to_check in types_to_check
#                             if not isinstance(type_to_check, float) and not isinstance(type_to_check, int)
#                             and not isinstance(type_to_check, bool)]
#
# solver_init_type_error_3 = [{'time_discretization': 1, 'simulation_time': 5,
#                              'transmission': type_to_check} for type_to_check in types_to_check
#                             if not isinstance(type_to_check, Transmission)]
#
# solver_init_type_error_4 = [{'time_discretization': 1, 'simulation_time': 5,
#                              'transmission': TransmissionFake([type_to_check, basic_spur_gear])}
#                             for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)]
#
# solver_init_type_error_5 = [{'time_discretization': 1, 'simulation_time': 5,
#                              'transmission': TransmissionFake([basic_dc_motor, type_to_check])}
#                             for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)]
#
# @fixture(params = [*solver_init_type_error_1,
#                    *solver_init_type_error_2,
#                    *solver_init_type_error_3,
#                    *solver_init_type_error_4,
#                    *solver_init_type_error_5])
# def solver_init_type_error(request):
#     return request.param
#
# motor_transmission_solver_init_value_error = DCMotor(name = 'name', inertia_moment = 1,
#                                                      no_load_speed = 1, maximum_torque = 1)
# gear_transmission_solver_init_value_error = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = 1)
# add_fixed_joint(master = motor_transmission_solver_init_value_error, slave = gear_transmission_solver_init_value_error)
# transmission_solver_init_value_error = Transmission(motor = motor_transmission_solver_init_value_error)
#
# @fixture(params = [{'time_discretization': -1, 'simulation_time': 5, 'transmission': transmission_solver_init_value_error},
#                    {'time_discretization': 1, 'simulation_time': -1, 'transmission': transmission_solver_init_value_error},
#                    {'time_discretization': 6, 'simulation_time': 5, 'transmission': transmission_solver_init_value_error},
#                    {'time_discretization': 1, 'simulation_time': 5, 'transmission': TransmissionFake([])}])
# def solver_init_value_error(request):
#     return request.param
