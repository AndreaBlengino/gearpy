from gearpy.gear import GearBase, SpurGear
from gearpy.mechanical_object import RotatingObject
from gearpy.motor import MotorBase, DCMotor
from gearpy.transmission import Transmission
from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, InertiaMoment, Torque, Time, TimeInterval
from gearpy.utils import add_fixed_joint, add_gear_mating
from hypothesis.strategies import composite, text, integers, floats, lists, sampled_from
import numpy as np
from pytest import fixture


types_to_check = ['string', 2, 2.2, True, (0, 1), [0, 1], {0, 1}, {0: 1}, None, np.array([0]),
                  AngularPosition(1, 'rad'), AngularSpeed(1, 'rad/s'), AngularAcceleration(1, 'rad/s^2'),
                  InertiaMoment(1, 'kgm^2'), Torque(1, 'Nm'), Time(1, 'sec'), TimeInterval(1, 'sec')]


basic_spur_gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))

basic_dc_motor = DCMotor(name = 'name',
                         inertia_moment = InertiaMoment(1, 'kgm^2'),
                         no_load_speed = AngularSpeed(1000, 'rpm'),
                         maximum_torque = Torque(1, 'Nm'))


@composite
def spur_gears(draw):
    name = draw(text(min_size = 1))

    n_teeth = draw(integers(min_value = 1))

    inertia_moment_units_list = list(InertiaMoment._InertiaMoment__UNITS.keys())
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    inertia_moment_unit = draw(sampled_from(elements = inertia_moment_units_list))

    return SpurGear(name = name,
                    n_teeth = n_teeth,
                    inertia_moment = InertiaMoment(inertia_moment_value, inertia_moment_unit))


@composite
def dc_motors(draw):
    name = draw(text(min_size = 1))

    inertia_moment_units_list = list(InertiaMoment._InertiaMoment__UNITS.keys())
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    inertia_moment_unit = draw(sampled_from(elements = inertia_moment_units_list))

    no_load_speed_units_list = list(AngularSpeed._AngularSpeed__UNITS.keys())
    no_load_speed_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    no_load_speed_unit = draw(sampled_from(elements = no_load_speed_units_list))

    maximum_torque_units_list = list(Torque._Torque__UNITS.keys())
    maximum_torque_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    maximum_torque_unit = draw(sampled_from(elements = maximum_torque_units_list))

    return DCMotor(name = name,
                   inertia_moment = InertiaMoment(inertia_moment_value, inertia_moment_unit),
                   no_load_speed = AngularSpeed(no_load_speed_value, no_load_speed_unit),
                   maximum_torque = Torque(maximum_torque_value, maximum_torque_unit))


@composite
def transmissions(draw):
    motor = draw(dc_motors())
    gears = draw(lists(elements = spur_gears(), min_size = 1))

    add_fixed_joint(master = motor, slave = gears[0])

    for i in range(0, len(gears) - 1):
        if i%2 == 0:
            add_gear_mating(master = gears[i], slave = gears[i + 1], efficiency = 1)
        else:
            add_fixed_joint(master = gears[i], slave = gears[i + 1])

    return Transmission(motor = motor)


@composite
def time_intervals(draw):
    value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    unit = draw(sampled_from(elements = list(TimeInterval._Time__UNITS.keys())))

    return TimeInterval(value = value, unit = unit)


add_gear_mating_type_error_1 = [{'master': type_to_check, 'slave': basic_spur_gear, 'efficiency': 0.5}
                                for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]

add_gear_mating_type_error_2 = [{'master': basic_spur_gear, 'slave': type_to_check, 'efficiency': 0.5}
                                for type_to_check in types_to_check if not isinstance(type_to_check, GearBase)]

add_gear_mating_type_error_3 = [{'master': basic_spur_gear, 'slave': basic_spur_gear, 'efficiency': type_to_check}
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


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)])
def transmission_init_type_error(request):
    return request.param


motor_transmission_solver_init_type_error = DCMotor(name = 'name', inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                    no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
gear_transmission_solver_init_type_error = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
add_fixed_joint(master = motor_transmission_solver_init_type_error, slave = gear_transmission_solver_init_type_error)
transmission_solver_init_type_error = Transmission(motor = motor_transmission_solver_init_type_error)

class TransmissionFake(Transmission):

    def __init__(self, chain: list):
        self.__chain = chain

    @property
    def chain(self):
        return self.__chain

    @chain.setter
    def chain(self, chain):
        self.__chain = chain

solver_init_type_error_1 = [{'time_discretization': type_to_check, 'simulation_time': TimeInterval(5, 'sec'),
                             'transmission': transmission_solver_init_type_error} for type_to_check in types_to_check
                            if not isinstance(type_to_check, TimeInterval)]

solver_init_type_error_2 = [{'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': type_to_check,
                             'transmission': transmission_solver_init_type_error} for type_to_check in types_to_check
                            if not isinstance(type_to_check, TimeInterval)]

solver_init_type_error_3 = [{'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': TimeInterval(5, 'sec'),
                             'transmission': type_to_check} for type_to_check in types_to_check
                            if not isinstance(type_to_check, Transmission)]

solver_init_type_error_4 = [{'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': TimeInterval(5, 'sec'),
                             'transmission': TransmissionFake([type_to_check, basic_spur_gear])}
                            for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)]

solver_init_type_error_5 = [{'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': TimeInterval(5, 'sec'),
                             'transmission': TransmissionFake([basic_dc_motor, type_to_check])}
                            for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)]

@fixture(params = [*solver_init_type_error_1,
                   *solver_init_type_error_2,
                   *solver_init_type_error_3,
                   *solver_init_type_error_4,
                   *solver_init_type_error_5])
def solver_init_type_error(request):
    return request.param

motor_transmission_solver_init_value_error = DCMotor(name = 'name', inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                     no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
gear_transmission_solver_init_value_error = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
add_fixed_joint(master = motor_transmission_solver_init_value_error, slave = gear_transmission_solver_init_value_error)
transmission_solver_init_value_error = Transmission(motor = motor_transmission_solver_init_value_error)

@fixture(params = [{'time_discretization': TimeInterval(5, 'sec'), 'simulation_time': TimeInterval(1, 'sec'), 'transmission': transmission_solver_init_value_error},
                   {'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': TimeInterval(5, 'sec'), 'transmission': TransmissionFake([])}])
def solver_init_value_error(request):
    return request.param
