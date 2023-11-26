from gearpy.mechanical_object import SpurGear, DCMotor, Flywheel, MatingMaster, MatingSlave
from gearpy.solver import Solver
from gearpy.transmission import Transmission
from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, Current, Force, InertiaMoment, Length, \
    Stress, Surface, Time, TimeInterval, Torque
from gearpy.utils import add_fixed_joint, add_gear_mating
from hypothesis.strategies import composite, text, integers, floats, lists, sampled_from, shared, builds, characters, one_of
import numpy as np
from random import shuffle


basic_dc_motor_1 = DCMotor(name = 'motor',
                           inertia_moment = InertiaMoment(1, 'kgm^2'),
                           no_load_speed = AngularSpeed(1000, 'rpm'),
                           maximum_torque = Torque(1, 'Nm'))

basic_dc_motor_2 = DCMotor(name = 'motor',
                           inertia_moment = InertiaMoment(1, 'kgm^2'),
                           no_load_speed = AngularSpeed(1000, 'rpm'),
                           maximum_torque = Torque(1, 'Nm'),
                           no_load_electrical_current = Current(0.1, 'A'),
                           maximum_electrical_current = Current(1, 'A'))

basic_flywheel = Flywheel(name = 'flywheel', inertia_moment = InertiaMoment(1, 'kgm^2'))

basic_spur_gear_1 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))

basic_spur_gear_2 = SpurGear(name = 'gear 2', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                           module = Length(1, 'mm'), face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))


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
basic_solver = Solver(transmission = basic_transmission)
basic_solver.run(time_discretization = TimeInterval(1, 'sec'), simulation_time = TimeInterval(2000, 'sec'))


types_to_check = ['string', 2, 2.2, True, (0, 1), [0, 1], {0, 1}, {0: 1}, None, np.array([0]),
                  AngularPosition(1, 'rad'), AngularSpeed(1, 'rad/s'), AngularAcceleration(1, 'rad/s^2'),
                  Current(1, 'A'), Force(1, 'N'), InertiaMoment(1, 'kgm^2'), Length(1, 'm'), Stress(1, 'Pa'),
                  Surface(1, 'm^2'), Time(1, 'sec'), TimeInterval(1, 'sec'), Torque(1, 'Nm'), basic_dc_motor_1,
                  basic_spur_gear_1, basic_flywheel, MatingMaster, MatingSlave, SpurGear]


@composite
def names(draw, strategy):
    seen = draw(shared(builds(set), key = "key-for-unique-elems"))
    return draw(strategy.filter(lambda x: x not in seen).map(lambda x: seen.add(x) or x))


@composite
def simple_spur_gears(draw):
    name = draw(names(text(min_size = 1, alphabet = characters(categories = ['L', 'N']))))
    n_teeth = draw(integers(min_value = 10, max_value = 100))
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))

    return SpurGear(name = name, n_teeth = n_teeth, inertia_moment = InertiaMoment(inertia_moment_value, 'kgmm^2'))


@composite
def structural_spur_gears(draw):
    name = draw(names(text(min_size = 1, alphabet = characters(categories = ['L', 'N']))))
    n_teeth = draw(integers(min_value = 10, max_value = 100))
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))
    module = Length(1, 'mm')
    face_width_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))
    face_width = Length(face_width_value, 'mm')
    elastic_modulus_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))
    elastic_modulus = Stress(elastic_modulus_value, 'GPa')

    return SpurGear(name = name, n_teeth = n_teeth, inertia_moment = InertiaMoment(inertia_moment_value, 'kgmm^2'),
                    module = module, face_width = face_width, elastic_modulus = elastic_modulus)


@composite
def simple_dc_motors(draw):
    name = draw(names(text(min_size = 1, alphabet = characters(categories = ['L', 'N']))))
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))
    no_load_speed_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 5000, max_value = 10000))
    maximum_torque_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1.5, max_value = 5))

    return DCMotor(name = name,
                   inertia_moment = InertiaMoment(inertia_moment_value, 'kgmm^2'),
                   no_load_speed = AngularSpeed(no_load_speed_value, 'rpm'),
                   maximum_torque = Torque(maximum_torque_value, 'mNm'))


@composite
def electrical_dc_motors(draw):
    name = draw(names(text(min_size = 1, alphabet = characters(categories = ['L', 'N']))))
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))
    no_load_speed_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 5000, max_value = 10000))
    maximum_torque_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1.5, max_value = 5))
    no_load_electrical_current_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 0.01, max_value = 5))
    electrical_current_multiplier = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1.5, max_value = 10))
    maximum_electrical_current_value = no_load_electrical_current_value*electrical_current_multiplier

    return DCMotor(name = name,
                   inertia_moment = InertiaMoment(inertia_moment_value, 'kgmm^2'),
                   no_load_speed = AngularSpeed(no_load_speed_value, 'rpm'),
                   maximum_torque = Torque(maximum_torque_value, 'mNm'),
                   no_load_electrical_current = Current(no_load_electrical_current_value, 'A'),
                   maximum_electrical_current = Current(maximum_electrical_current_value, 'A'))


@composite
def flywheels(draw):
    name = draw(names(text(min_size = 1, alphabet = characters(categories = ['L', 'N']))))
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))

    return Flywheel(name = name, inertia_moment = InertiaMoment(inertia_moment_value, 'kgmm^2'))


@composite
def transmissions(draw):
    motor = draw(one_of(simple_dc_motors(), electrical_dc_motors()))
    gears = draw(lists(elements = structural_spur_gears(), min_size = 2))

    if len(gears)%2 == 1:
        gears = gears[:-1]

    add_fixed_joint(master = motor, slave = gears[0])

    for i in range(0, len(gears) - 1):
        if i%2 == 0:
            add_gear_mating(master = gears[i], slave = gears[i + 1], efficiency = 1)
        else:
            add_fixed_joint(master = gears[i], slave = gears[i + 1])

    return Transmission(motor = motor)


@composite
def solved_transmissions(draw):
    motor = draw(one_of(simple_dc_motors(), electrical_dc_motors()))
    flywheel = draw(flywheels())
    gear_1 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'))
    gear_2 = SpurGear(name = 'gear 2', n_teeth = 20, inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'))
    simple_gears = draw(lists(elements = simple_spur_gears(), min_size = 2, max_size = 4))
    structural_gears = draw(lists(elements = structural_spur_gears(), min_size = 2, max_size = 4))

    if len(simple_gears)%2 == 1:
        simple_gears = simple_gears[:-1]

    if len(structural_gears)%2 == 1:
        structural_gears = structural_gears[:-1]

    simple_gears = list(zip(*(iter(simple_gears),)*2))
    structural_gears = list(zip(*(iter(structural_gears),)*2))

    gears = []
    gears.extend(simple_gears)
    gears.extend(structural_gears)
    shuffle(gears)

    gears = [element for pair in gears for element in pair]
    gears.append(gear_1)
    gears.append(gear_2)

    time_discretization_value = draw(floats(min_value = 1e-3, max_value = 1, allow_nan = False, allow_infinity = False))
    time_discretization = TimeInterval(value = time_discretization_value, unit = 'sec')
    simulation_steps = draw(floats(min_value = 5, max_value = 50, allow_nan = False, allow_infinity = False))

    add_fixed_joint(master = motor, slave = flywheel)
    add_fixed_joint(master = flywheel, slave = gears[0])

    for i in range(0, len(gears) - 1):
        if i%2 == 0:
            add_gear_mating(master = gears[i], slave = gears[i + 1], efficiency = 1)
        else:
            add_fixed_joint(master = gears[i], slave = gears[i + 1])

    transmission = Transmission(motor = motor)

    gears[-1].external_torque = lambda time, angular_position, angular_speed: Torque(1, 'mNm')
    gears[-1].angular_position = AngularPosition(0, 'rad')
    gears[-1].angular_speed = AngularSpeed(0, 'rad/s')
    simulation_time = time_discretization*simulation_steps
    solver = Solver(transmission = transmission)
    solver.run(time_discretization = time_discretization, simulation_time = simulation_time)

    return transmission


@composite
def time_intervals(draw):
    value = draw(integers(min_value = 1, max_value = 10))
    unit = draw(sampled_from(elements = list(TimeInterval._Time__UNITS.keys())))

    return TimeInterval(value = value, unit = unit)
