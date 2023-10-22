from gearpy.mechanical_object import RotatingObject, GearBase, MotorBase, SpurGear, DCMotor, Flywheel
from gearpy.solver import Solver
from gearpy.transmission import Transmission
from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, InertiaMoment, Torque, Time, TimeInterval
from gearpy.utils import add_fixed_joint, add_gear_mating
from hypothesis.strategies import composite, text, integers, floats, lists, sampled_from
import numpy as np
from pytest import fixture


basic_dc_motor = DCMotor(name = 'motor',
                         inertia_moment = InertiaMoment(1, 'kgm^2'),
                         no_load_speed = AngularSpeed(1000, 'rpm'),
                         maximum_torque = Torque(1, 'Nm'))

basic_flywheel = Flywheel(name = 'flywheel', inertia_moment = InertiaMoment(1, 'kgm^2'))

basic_spur_gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))


transmission_dc_motor = DCMotor(name = 'motor',
                                inertia_moment = InertiaMoment(1, 'kgm^2'),
                                no_load_speed = AngularSpeed(1000, 'rpm'),
                                maximum_torque = Torque(1, 'Nm'))
transmission_flywheel = Flywheel(name = 'flywheel', inertia_moment = InertiaMoment(1, 'kgm^2'))
transmission_spur_gear_1 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
transmission_spur_gear_2 = SpurGear(name = 'gear 2', n_teeth = 40, inertia_moment = InertiaMoment(1, 'kgm^2'))
add_fixed_joint(master = transmission_dc_motor, slave = transmission_flywheel)
add_fixed_joint(master = transmission_flywheel, slave = transmission_spur_gear_1)
add_gear_mating(master = transmission_spur_gear_1, slave = transmission_spur_gear_2, efficiency = 0.9)
basic_transmission = Transmission(motor = transmission_dc_motor)

transmission_spur_gear_2.external_torque = lambda time, angular_position, angular_speed: Torque(1, 'mNm')
transmission_spur_gear_2.angular_position = AngularPosition(0, 'rad')
transmission_spur_gear_2.angular_speed = AngularSpeed(0, 'rad/s')
basic_solver = Solver(time_discretization = TimeInterval(1, 'sec'),
                      simulation_time = TimeInterval(2000, 'sec'),
                      transmission = basic_transmission)
basic_solver.run()


types_to_check = ['string', 2, 2.2, True, (0, 1), [0, 1], {0, 1}, {0: 1}, None, np.array([0]),
                  AngularPosition(1, 'rad'), AngularSpeed(1, 'rad/s'), AngularAcceleration(1, 'rad/s^2'),
                  InertiaMoment(1, 'kgm^2'), Torque(1, 'Nm'), Time(1, 'sec'), TimeInterval(1, 'sec'),
                  basic_dc_motor, basic_spur_gear, basic_flywheel]


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
def flywheels(draw):
    name = draw(text(min_size = 1))

    inertia_moment_units_list = list(InertiaMoment._InertiaMoment__UNITS.keys())
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1e-10, exclude_min = True, max_value = 1000))
    inertia_moment_unit = draw(sampled_from(elements = inertia_moment_units_list))

    return Flywheel(name = name, inertia_moment = InertiaMoment(inertia_moment_value, inertia_moment_unit))


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
                                if not isinstance(type_to_check, GearBase) and not isinstance(type_to_check, MotorBase)
                                and not isinstance(type_to_check, Flywheel)]

add_fixed_joint_type_error_2 = [{'master': basic_spur_gear, 'slave': type_to_check} for type_to_check in types_to_check
                                if not isinstance(type_to_check, GearBase) and not isinstance(type_to_check, Flywheel)]

@fixture(params = [*add_fixed_joint_type_error_1,
                   *add_fixed_joint_type_error_2])
def add_fixed_joint_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)])
def transmission_init_type_error(request):
    return request.param


transmission_snapshot_type_error_1 = [{'time': type_to_check, 'target_time': Time(1, 'sec'),
                                       'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                       'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm',
                                       'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, list)]

transmission_snapshot_type_error_2 = [{'time': [type_to_check], 'target_time': Time(1, 'sec'),
                                       'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                       'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm',
                                       'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, Time)]

transmission_snapshot_type_error_3 = [{'time': basic_solver.time, 'target_time': type_to_check,
                                       'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                       'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm',
                                       'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, Time)]

transmission_snapshot_type_error_4 = [{'time': basic_solver.time, 'target_time': Time(1, 'sec'),
                                       'angular_position_unit': type_to_check, 'angular_speed_unit': 'rad/s',
                                       'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm',
                                       'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_5 = [{'time': basic_solver.time, 'target_time': Time(1, 'sec'),
                                       'angular_position_unit': 'rad', 'angular_speed_unit': type_to_check,
                                       'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm',
                                       'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_6 = [{'time': basic_solver.time, 'target_time': Time(1, 'sec'),
                                       'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                       'angular_acceleration_unit': type_to_check, 'torque_unit': 'Nm',
                                       'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_7 = [{'time': basic_solver.time, 'target_time': Time(1, 'sec'),
                                       'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                       'angular_acceleration_unit': 'rad/s^2', 'torque_unit': type_to_check,
                                       'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_8 = [{'time': basic_solver.time, 'target_time': Time(1, 'sec'),
                                       'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                       'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm',
                                       'driving_torque_unit': type_to_check, 'load_torque_unit': 'Nm',
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_9 = [{'time': basic_solver.time, 'target_time': Time(1, 'sec'),
                                       'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                       'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm',
                                       'driving_torque_unit': 'Nm', 'load_torque_unit': type_to_check,
                                       'print_data': False} for type_to_check in types_to_check
                                      if not isinstance(type_to_check, str)]

transmission_snapshot_type_error_10 = [{'time': basic_solver.time, 'target_time': Time(1, 'sec'),
                                        'angular_position_unit': 'rad', 'angular_speed_unit': 'rad/s',
                                        'angular_acceleration_unit': 'rad/s^2', 'torque_unit': 'Nm',
                                        'driving_torque_unit': 'Nm', 'load_torque_unit': 'Nm',
                                        'print_data': type_to_check} for type_to_check in types_to_check
                                       if not isinstance(type_to_check, int) and not isinstance(type_to_check, bool)]

@fixture(params = [*transmission_snapshot_type_error_1,
                   *transmission_snapshot_type_error_2,
                   *transmission_snapshot_type_error_3,
                   *transmission_snapshot_type_error_4,
                   *transmission_snapshot_type_error_5,
                   *transmission_snapshot_type_error_6,
                   *transmission_snapshot_type_error_7,
                   *transmission_snapshot_type_error_8,
                   *transmission_snapshot_type_error_9,
                   *transmission_snapshot_type_error_10])
def transmission_snapshot_type_error(request):
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
