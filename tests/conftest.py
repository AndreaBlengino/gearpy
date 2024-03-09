from gearpy.mechanical_objects import SpurGear, HelicalGear, DCMotor, Flywheel, MatingMaster, MatingSlave, WormGear, WormWheel
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer, Timer
from gearpy.solver import Solver
from gearpy.powertrain import Powertrain
from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, Current, Force, InertiaMoment, Length, \
    Stress, Surface, Time, TimeInterval, Torque, Angle
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
                           no_load_electric_current = Current(0.1, 'A'),
                           maximum_electric_current = Current(1, 'A'))

basic_flywheel = Flywheel(name = 'flywheel', inertia_moment = InertiaMoment(1, 'kgm^2'))

basic_worm_gear_1 = WormGear(name = 'worm gear', n_starts = 1, inertia_moment = InertiaMoment(1, 'kgm^2'),
                             helix_angle = Angle(10, 'deg'), pressure_angle = Angle(20, 'deg'))

basic_worm_gear_2 = WormGear(name = 'worm gear', n_starts = 1, inertia_moment = InertiaMoment(1, 'kgm^2'),
                             helix_angle = Angle(10, 'deg'), pressure_angle = Angle(20, 'deg'),
                             reference_diameter = Length(10, 'mm'))

basic_worm_wheel_1 = WormWheel(name = 'worm gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                               helix_angle = Angle(10, 'deg'), pressure_angle = Angle(20, 'deg'))

basic_worm_wheel_2 = WormWheel(name = 'worm gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                               helix_angle = Angle(10, 'deg'), pressure_angle = Angle(20, 'deg'),
                               module = Length(1, 'mm'), face_width = Length(10, 'mm'))

basic_spur_gear_1 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))

basic_spur_gear_2 = SpurGear(name = 'gear 2', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'),
                             module = Length(1, 'mm'), face_width = Length(5, 'mm'),
                             elastic_modulus = Stress(100, 'GPa'))

basic_helical_gear_1 = HelicalGear(name = 'gear 1', n_teeth = 10, helix_angle = Angle(30, 'deg'),
                                   inertia_moment = InertiaMoment(1, 'kgm^2'))

basic_helical_gear_2 = HelicalGear(name = 'gear 2', n_teeth = 10, helix_angle = Angle(30, 'deg'),
                                   inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'),
                                   face_width = Length(5, 'mm'), elastic_modulus = Stress(100, 'GPa'))


powertrain_dc_motor = DCMotor(name = 'motor',
                              inertia_moment = InertiaMoment(1, 'kgm^2'),
                              no_load_speed = AngularSpeed(1000, 'rpm'),
                              maximum_torque = Torque(1, 'Nm'),
                              no_load_electric_current = Current(100, 'mA'),
                              maximum_electric_current = Current(2000, 'A'))
powertrain_flywheel = Flywheel(name = 'flywheel', inertia_moment = InertiaMoment(1, 'kgm^2'))
powertrain_spur_gear_1 = SpurGear(name = 'spur gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
powertrain_spur_gear_2 = SpurGear(name = 'spur gear 2', n_teeth = 40, inertia_moment = InertiaMoment(1, 'kgm^2'))
powertrain_helical_gear_1 = HelicalGear(name = 'helical gear 1', n_teeth = 10, helix_angle = Angle(30, 'deg'), inertia_moment = InertiaMoment(1, 'kgm^2'))
powertrain_helical_gear_2 = HelicalGear(name = 'helical gear 2', n_teeth = 40, helix_angle = Angle(30, 'deg'), inertia_moment = InertiaMoment(1, 'kgm^2'))
add_fixed_joint(master = powertrain_dc_motor, slave = powertrain_flywheel)
add_fixed_joint(master = powertrain_flywheel, slave = powertrain_spur_gear_1)
add_gear_mating(master = powertrain_spur_gear_1, slave = powertrain_spur_gear_2, efficiency = 0.9)
add_fixed_joint(master = powertrain_spur_gear_2, slave = powertrain_helical_gear_1)
add_gear_mating(master = powertrain_helical_gear_1, slave = powertrain_helical_gear_2, efficiency = 0.9)
basic_powertrain = Powertrain(motor = powertrain_dc_motor)

powertrain_helical_gear_2.external_torque = lambda time, angular_position, angular_speed: Torque(1, 'mNm')
powertrain_helical_gear_2.angular_position = AngularPosition(0, 'rad')
powertrain_helical_gear_2.angular_speed = AngularSpeed(0, 'rad/s')
basic_solver = Solver(powertrain = basic_powertrain)
basic_solver.run(time_discretization = TimeInterval(1, 'sec'), simulation_time = TimeInterval(100, 'sec'))

basic_encoder = AbsoluteRotaryEncoder(target = basic_spur_gear_1)
basic_tachometer = Tachometer(target = basic_spur_gear_1)
basic_timer = Timer(start_time = Time(0, 'sec'), duration = TimeInterval(5, 'sec'))


types_to_check = ['string', 2, 2.2, True, (0, 1), [0, 1], {0, 1}, {0: 1}, None, np.array([0]),
                  AngularPosition(1, 'rad'), AngularSpeed(1, 'rad/s'),
                  AngularAcceleration(1, 'rad/s^2'), Current(1, 'A'),
                  Force(1, 'N'), InertiaMoment(1, 'kgm^2'), Length(1, 'm'),
                  Stress(1, 'Pa'), Surface(1, 'm^2'), Time(1, 'sec'),
                  TimeInterval(1, 'sec'), Torque(1, 'Nm'), Angle(1, 'rad'),
                  basic_dc_motor_1, basic_spur_gear_1, basic_helical_gear_1, basic_helical_gear_2, basic_flywheel,
                  basic_solver, basic_powertrain, basic_encoder, basic_tachometer, basic_timer, basic_worm_gear_1,
                  basic_worm_gear_2, basic_worm_wheel_1, basic_worm_wheel_2, MatingMaster, MatingSlave, SpurGear]


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
def simple_helical_gears(draw):
    name = draw(names(text(min_size = 1, alphabet = characters(categories = ['L', 'N']))))
    n_teeth = draw(integers(min_value = 10, max_value = 100))
    helix_angle = Angle(30, 'deg')
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))

    return HelicalGear(name = name, n_teeth = n_teeth, helix_angle = helix_angle,
                       inertia_moment = InertiaMoment(inertia_moment_value, 'kgmm^2'))


@composite
def structural_helical_gears(draw):
    name = draw(names(text(min_size = 1, alphabet = characters(categories = ['L', 'N']))))
    n_teeth = draw(integers(min_value = 10, max_value = 100))
    helix_angle = Angle(30, 'deg')
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))
    module = Length(1, 'mm')
    face_width_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))
    face_width = Length(face_width_value, 'mm')
    elastic_modulus_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))
    elastic_modulus = Stress(elastic_modulus_value, 'GPa')

    return HelicalGear(name = name, n_teeth = n_teeth, helix_angle = helix_angle,
                       inertia_moment = InertiaMoment(inertia_moment_value, 'kgmm^2'), module = module,
                       face_width = face_width, elastic_modulus = elastic_modulus)


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
def electric_dc_motors(draw):
    name = draw(names(text(min_size = 1, alphabet = characters(categories = ['L', 'N']))))
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))
    no_load_speed_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 5000, max_value = 10000))
    maximum_torque_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1.5, max_value = 5))
    no_load_electric_current_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 0.01, max_value = 5))
    electric_current_multiplier = draw(floats(allow_nan = False, allow_infinity = False, min_value = 1.5, max_value = 10))
    maximum_electric_current_value = no_load_electric_current_value*electric_current_multiplier

    return DCMotor(name = name,
                   inertia_moment = InertiaMoment(inertia_moment_value, 'kgmm^2'),
                   no_load_speed = AngularSpeed(no_load_speed_value, 'rpm'),
                   maximum_torque = Torque(maximum_torque_value, 'mNm'),
                   no_load_electric_current = Current(no_load_electric_current_value, 'A'),
                   maximum_electric_current = Current(maximum_electric_current_value, 'A'))


@composite
def flywheels(draw):
    name = draw(names(text(min_size = 1, alphabet = characters(categories = ['L', 'N']))))
    inertia_moment_value = draw(floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 1000))

    return Flywheel(name = name, inertia_moment = InertiaMoment(inertia_moment_value, 'kgmm^2'))


@composite
def rotating_objects(draw):
    return draw(one_of(simple_spur_gears(), structural_spur_gears(), simple_helical_gears(), structural_helical_gears(),
                       simple_dc_motors(), electric_dc_motors(), flywheels()))


@composite
def powertrains(draw, allow_simple_motors = True, allow_electric_motors = True):
    if allow_simple_motors and allow_electric_motors:
        motor = draw(one_of(simple_dc_motors(), electric_dc_motors()))
    elif allow_simple_motors and not allow_electric_motors:
        motor = draw(simple_dc_motors())
    elif not allow_simple_motors and allow_electric_motors:
        motor = draw(electric_dc_motors())
    else:
        raise ValueError("At least one of 'allow_simple_motors' and 'allow_electric_motors' must be True.")
    spur_gears = draw(lists(elements = structural_spur_gears(), min_size = 2))
    helical_gears = draw(lists(elements = structural_helical_gears(), min_size = 2))

    if len(spur_gears)%2 == 1:
        spur_gears = spur_gears[:-1]

    if len(helical_gears)%2 == 1:
        helical_gears = helical_gears[:-1]

    gears = [*spur_gears, *helical_gears]

    add_fixed_joint(master = motor, slave = gears[0])

    for i in range(0, len(gears) - 1):
        if i%2 == 0:
            add_gear_mating(master = gears[i], slave = gears[i + 1], efficiency = 1)
        else:
            add_fixed_joint(master = gears[i], slave = gears[i + 1])

    return Powertrain(motor = motor)


@composite
def solved_powertrains(draw):
    motor = draw(one_of(simple_dc_motors(), electric_dc_motors()))
    flywheel = draw(flywheels())
    gear_1 = SpurGear(name = 'gear 1', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'))
    gear_2 = SpurGear(name = 'gear 2', n_teeth = 20, inertia_moment = InertiaMoment(1, 'kgm^2'), module = Length(1, 'mm'))
    simple_spur_gear_set = draw(lists(elements = simple_spur_gears(), min_size = 2, max_size = 4))
    structural_spur_gear_set = draw(lists(elements = structural_spur_gears(), min_size = 2, max_size = 4))
    simple_helical_gear_set = draw(lists(elements = simple_helical_gears(), min_size = 2, max_size = 4))
    structural_helical_gear_set = draw(lists(elements = structural_helical_gears(), min_size = 2, max_size = 4))

    if len(simple_spur_gear_set)%2 == 1:
        simple_spur_gear_set = simple_spur_gear_set[:-1]

    if len(structural_spur_gear_set)%2 == 1:
        structural_spur_gear_set = structural_spur_gear_set[:-1]

    if len(simple_helical_gear_set)%2 == 1:
        simple_helical_gear_set = simple_helical_gear_set[:-1]

    if len(structural_helical_gear_set)%2 == 1:
        structural_helical_gear_set = structural_helical_gear_set[:-1]

    simple_spur_gear_set = list(zip(*(iter(simple_spur_gear_set),)*2))
    structural_spur_gear_set = list(zip(*(iter(structural_spur_gear_set),)*2))
    simple_helical_gear_set = list(zip(*(iter(simple_helical_gear_set),)*2))
    structural_helical_gear_set = list(zip(*(iter(structural_helical_gear_set),)*2))

    gears = []
    gears.extend(simple_spur_gear_set)
    gears.extend(structural_spur_gear_set)
    gears.extend(simple_helical_gear_set)
    gears.extend(structural_helical_gear_set)
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

    powertrain = Powertrain(motor = motor)

    gears[-1].external_torque = lambda time, angular_position, angular_speed: Torque(1, 'mNm')
    gears[-1].angular_position = AngularPosition(0, 'rad')
    gears[-1].angular_speed = AngularSpeed(0, 'rad/s')
    simulation_time = time_discretization*simulation_steps
    solver = Solver(powertrain = powertrain)
    solver.run(time_discretization = time_discretization, simulation_time = simulation_time)

    return powertrain


@composite
def time_intervals(draw):
    value = draw(integers(min_value = 1, max_value = 10))
    unit = draw(sampled_from(elements = list(TimeInterval._Time__UNITS.keys())))

    return TimeInterval(value = value, unit = unit)
