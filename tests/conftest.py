from gearpy.mechanical_objects import (
    SpurGear,
    HelicalGear,
    DCMotor,
    Flywheel,
    MatingMaster,
    MatingSlave,
    WormGear,
    WormWheel
)
from gearpy.mechanical_objects.mechanical_object_base import (
    WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES,
    WORM_GEAR_AND_WHEEL_DATA
)
from gearpy.sensors import (
    AbsoluteRotaryEncoder,
    Amperometer,
    Tachometer,
    Timer
)
from gearpy.solver import Solver
from gearpy.powertrain import Powertrain
from gearpy.units import (
    AngularAcceleration,
    AngularPosition,
    AngularSpeed,
    Current,
    Force,
    InertiaMoment,
    Length,
    Stress,
    Surface,
    Time,
    TimeInterval,
    Torque,
    Angle
)
from gearpy.utils import add_fixed_joint, add_gear_mating, add_worm_gear_mating
from hypothesis.strategies import (
    composite,
    text,
    integers,
    floats,
    lists,
    sampled_from,
    shared,
    builds,
    characters,
    one_of
)
import numpy as np
import os
from random import shuffle


basic_dc_motor_1 = DCMotor(
    name='motor',
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    no_load_speed=AngularSpeed(1000, 'rpm'),
    maximum_torque=Torque(1, 'Nm')
)

basic_dc_motor_2 = DCMotor(
    name='motor',
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    no_load_speed=AngularSpeed(1000, 'rpm'),
    maximum_torque=Torque(1, 'Nm'),
    no_load_electric_current=Current(0.1, 'A'),
    maximum_electric_current=Current(1, 'A')
)

basic_flywheel = Flywheel(
    name='flywheel',
    inertia_moment=InertiaMoment(1, 'kgm^2')
)

basic_worm_gear_1 = WormGear(
    name='worm gear',
    n_starts=1,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    pressure_angle=Angle(20, 'deg'),
    helix_angle=Angle(10, 'deg')
)

basic_worm_gear_2 = WormGear(
    name='worm gear',
    n_starts=1,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    pressure_angle=Angle(20, 'deg'),
    helix_angle=Angle(10, 'deg'),
    reference_diameter=Length(10, 'mm')
)

basic_worm_wheel_1 = WormWheel(
    name='worm gear',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    pressure_angle=Angle(20, 'deg'),
    helix_angle=Angle(10, 'deg')
)

basic_worm_wheel_2 = WormWheel(
    name='worm gear',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    pressure_angle=Angle(20, 'deg'),
    helix_angle=Angle(10, 'deg'),
    module=Length(1, 'mm'),
    face_width=Length(10, 'mm')
)

basic_spur_gear_1 = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2')
)

basic_spur_gear_2 = SpurGear(
    name='gear 2',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)

basic_helical_gear_1 = HelicalGear(
    name='gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2')
)

basic_helical_gear_2 = HelicalGear(
    name='gear 2',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    module=Length(1, 'mm'),
    face_width=Length(5, 'mm'),
    elastic_modulus=Stress(100, 'GPa')
)


powertrain_dc_motor = DCMotor(
    name='motor',
    inertia_moment=InertiaMoment(1, 'kgm^2'),
    no_load_speed=AngularSpeed(1000, 'rpm'),
    maximum_torque=Torque(1, 'Nm'),
    no_load_electric_current=Current(100, 'mA'),
    maximum_electric_current=Current(2000, 'A')
)
powertrain_flywheel = Flywheel(
    name='flywheel',
    inertia_moment=InertiaMoment(1, 'kgm^2')
)
powertrain_spur_gear_1 = SpurGear(
    name='spur gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'kgm^2')
)
powertrain_spur_gear_2 = SpurGear(
    name='spur gear 2',
    n_teeth=40,
    inertia_moment=InertiaMoment(1, 'kgm^2')
)
powertrain_helical_gear_1 = HelicalGear(
    name='helical gear 1',
    n_teeth=10,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2')
)
powertrain_helical_gear_2 = HelicalGear(
    name='helical gear 2',
    n_teeth=40,
    helix_angle=Angle(30, 'deg'),
    inertia_moment=InertiaMoment(1, 'kgm^2')
)
add_fixed_joint(master=powertrain_dc_motor, slave=powertrain_flywheel)
add_fixed_joint(master=powertrain_flywheel, slave=powertrain_spur_gear_1)
add_gear_mating(
    master=powertrain_spur_gear_1,
    slave=powertrain_spur_gear_2,
    efficiency=0.9
)
add_fixed_joint(master=powertrain_spur_gear_2, slave=powertrain_helical_gear_1)
add_gear_mating(
    master=powertrain_helical_gear_1,
    slave=powertrain_helical_gear_2,
    efficiency=0.9
)
basic_powertrain = Powertrain(motor=powertrain_dc_motor)

powertrain_helical_gear_2.external_torque = \
    lambda time, angular_position, angular_speed: Torque(1, 'mNm')
powertrain_helical_gear_2.angular_position = AngularPosition(0, 'rad')
powertrain_helical_gear_2.angular_speed = AngularSpeed(0, 'rad/s')
basic_solver = Solver(powertrain=basic_powertrain)
basic_solver.run(
    time_discretization=TimeInterval(1, 'sec'),
    simulation_time=TimeInterval(100, 'sec')
)

basic_encoder = AbsoluteRotaryEncoder(target=basic_spur_gear_1)
basic_tachometer = Tachometer(target=basic_spur_gear_1)
basic_amperometer = Amperometer(target=basic_dc_motor_2)
basic_timer = Timer(start_time=Time(0, 'sec'), duration=TimeInterval(5, 'sec'))


types_to_check = [
    'string',
    2,
    2.2,
    True,
    (0, 1),
    [0, 1],
    {0, 1},
    {0: 1},
    None,
    np.array([0]),
    AngularPosition(1, 'rad'),
    AngularSpeed(1, 'rad/s'),
    AngularAcceleration(1, 'rad/s^2'),
    Current(1, 'A'),
    Force(1, 'N'),
    InertiaMoment(1, 'kgm^2'),
    Length(1, 'm'),
    Stress(1, 'Pa'),
    Surface(1, 'm^2'),
    Time(1, 'sec'),
    TimeInterval(1, 'sec'),
    Torque(1, 'Nm'),
    Angle(1, 'rad'),
    basic_dc_motor_1,
    basic_spur_gear_1,
    basic_helical_gear_1,
    basic_helical_gear_2,
    basic_flywheel,
    basic_solver,
    basic_powertrain,
    basic_encoder,
    basic_amperometer,
    basic_tachometer,
    basic_timer,
    basic_worm_gear_1,
    basic_worm_gear_2,
    basic_worm_wheel_1,
    basic_worm_wheel_2,
    MatingMaster,
    MatingSlave,
    SpurGear
]


@composite
def names(draw, strategy):
    seen = draw(shared(builds(set), key="key-for-unique-elems"))
    return draw(
        strategy.filter(
            lambda x: x not in seen
        ).map(lambda x: seen.add(x) or x)
    )


@composite
def spur_gears(draw, structural=False):
    name = draw(
        names(text(min_size=1, alphabet=characters(categories=['L', 'N'])))
    )
    n_teeth = draw(integers(min_value=10, max_value=100))
    inertia_moment_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=10,
            max_value=1000
        )
    )
    if structural:
        module = Length(1, 'mm')
        face_width_value = draw(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=10,
                max_value=1000
            )
        )
        face_width = Length(face_width_value, 'mm')
        elastic_modulus_value = draw(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=10,
                max_value=1000
            )
        )
        elastic_modulus = Stress(elastic_modulus_value, 'GPa')

        return SpurGear(
            name=name,
            n_teeth=n_teeth,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgmm^2'),
            module=module,
            face_width=face_width,
            elastic_modulus=elastic_modulus
        )
    else:
        return SpurGear(
            name=name,
            n_teeth=n_teeth,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgmm^2')
        )


@composite
def helical_gears(draw, structural=False):
    name = draw(
        names(text(min_size=1, alphabet=characters(categories=['L', 'N'])))
    )
    n_teeth = draw(integers(min_value=10, max_value=100))
    helix_angle = Angle(30, 'deg')
    inertia_moment_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=10,
            max_value=1000
        )
    )
    if structural:
        module = Length(1, 'mm')
        face_width_value = draw(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=10,
                max_value=1000
            )
        )
        face_width = Length(face_width_value, 'mm')
        elastic_modulus_value = draw(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=10,
                max_value=1000
            )
        )
        elastic_modulus = Stress(elastic_modulus_value, 'GPa')

        return HelicalGear(
            name=name,
            n_teeth=n_teeth,
            helix_angle=helix_angle,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgmm^2'),
            module=module,
            face_width=face_width,
            elastic_modulus=elastic_modulus
        )
    else:
        return HelicalGear(
            name=name,
            n_teeth=n_teeth,
            helix_angle=helix_angle,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgmm^2')
        )


@composite
def worm_gears(draw, structural=False, pressure_angle=None):
    name = draw(
        names(text(min_size=1, alphabet=characters(categories=['L', 'N'])))
    )
    n_starts = draw(integers(min_value=1, max_value=4))
    inertia_moment_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=10,
            max_value=1000
        )
    )
    if pressure_angle is None:
        pressure_angle = draw(
            sampled_from(
                elements=WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES
            )
        )
    helix_angle_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0.1,
            max_value=15
        )
    )
    if structural:
        reference_diameter_value = draw(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=2,
                max_value=100
            )
        )

        return WormGear(
            name=name,
            n_starts=n_starts,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgmm^2'),
            pressure_angle=pressure_angle,
            helix_angle=Angle(helix_angle_value, 'deg'),
            reference_diameter=Length(reference_diameter_value, 'mm')
        )
    else:
        return WormGear(
            name=name,
            n_starts=n_starts,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgmm^2'),
            pressure_angle=pressure_angle,
            helix_angle=Angle(helix_angle_value, 'deg')
        )


@composite
def worm_wheels(draw, structural=False, pressure_angle=None):
    name = draw(
        names(text(min_size=1, alphabet=characters(categories=['L', 'N'])))
    )
    n_teeth = draw(integers(min_value=10, max_value=200))
    inertia_moment_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=10,
            max_value=1000
        )
    )
    maximum_helix_angle = 15
    if pressure_angle is None:
        pressure_angle = draw(
            sampled_from(
                elements=WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES
            )
        )
        maximum_helix_angle = WORM_GEAR_AND_WHEEL_DATA.set_index(
            'Pressure Angle'
        ).loc[pressure_angle.value, 'Maximum Helix Angle']
    helix_angle_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0.1,
            max_value=maximum_helix_angle
        )
    )
    if structural:
        module_value = draw(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=0.1,
                max_value=5
            )
        )
        face_width_value = draw(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=10,
                max_value=1000
            )
        )

        return WormWheel(
            name=name,
            n_teeth=n_teeth,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgm^2'),
            pressure_angle=pressure_angle,
            helix_angle=Angle(helix_angle_value, 'deg'),
            module=Length(module_value, 'mm'),
            face_width=Length(face_width_value, 'mm')
        )
    else:
        return WormWheel(
            name=name,
            n_teeth=n_teeth,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgm^2'),
            pressure_angle=pressure_angle,
            helix_angle=Angle(helix_angle_value, 'deg')
        )


@composite
def dc_motors(draw, current=False):
    name = draw(
        names(
            text(min_size=1, alphabet=characters(categories=['L', 'N']))
        )
    )
    inertia_moment_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=10,
            max_value=1000
        )
    )
    no_load_speed_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=5000,
            max_value=10000
        )
    )
    maximum_torque_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=1.5,
            max_value=5
        )
    )
    if current:
        no_load_electric_current_value = draw(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=0.01,
                max_value=5
            )
        )
        electric_current_multiplier = draw(
            floats(
                allow_nan=False,
                allow_infinity=False,
                min_value=1.5,
                max_value=10
            )
        )
        maximum_electric_current_value = no_load_electric_current_value * \
            electric_current_multiplier

        return DCMotor(
            name=name,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgmm^2'),
            no_load_speed=AngularSpeed(no_load_speed_value, 'rpm'),
            maximum_torque=Torque(maximum_torque_value, 'mNm'),
            no_load_electric_current=Current(
                no_load_electric_current_value,
                'A'
            ),
            maximum_electric_current=Current(
                maximum_electric_current_value,
                'A'
            )
        )
    else:
        return DCMotor(
            name=name,
            inertia_moment=InertiaMoment(inertia_moment_value, 'kgmm^2'),
            no_load_speed=AngularSpeed(no_load_speed_value, 'rpm'),
            maximum_torque=Torque(maximum_torque_value, 'mNm')
        )


@composite
def flywheels(draw):
    name = draw(
        names(
            text(min_size=1, alphabet=characters(categories=['L', 'N']))
        )
    )
    inertia_moment_value = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=10,
            max_value=1000
        )
    )

    return Flywheel(
        name=name,
        inertia_moment=InertiaMoment(inertia_moment_value, 'kgmm^2')
    )


@composite
def rotating_objects(draw):
    return draw(
        one_of(
            spur_gears(),
            spur_gears(structural=True),
            helical_gears(),
            helical_gears(structural=True),
            dc_motors(),
            dc_motors(current=True),
            flywheels()
        )
    )


@composite
def powertrains(
    draw,
    allow_motors_without_current=True,
    allow_motors_with_current=True
):
    if allow_motors_without_current and allow_motors_with_current:
        motor = draw(one_of(dc_motors(), dc_motors(current=True)))
    elif allow_motors_without_current and not allow_motors_with_current:
        motor = draw(dc_motors())
    elif not allow_motors_without_current and allow_motors_with_current:
        motor = draw(dc_motors(current=True))
    else:
        raise ValueError(
            "At least one of 'allow_motors_without_current' and "
            "'allow_motors_with_current' must be True."
        )
    worm_pressure_angle = draw(
        sampled_from(elements=WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES)
    )
    worm_gear = draw(
        worm_gears(structural=True, pressure_angle=worm_pressure_angle)
    )
    worm_wheel = draw(
        worm_wheels(structural=True, pressure_angle=worm_pressure_angle)
    )
    worm_friction_coefficient = draw(
        floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0,
            max_value=0.99,
            exclude_min=False,
            exclude_max=True
        )
    )
    spur_gear_set = draw(
        lists(elements=spur_gears(structural=True), min_size=2)
    )
    helical_gear_set = draw(
        lists(elements=helical_gears(structural=True), min_size=2)
    )

    if len(spur_gear_set) % 2 == 1:
        spur_gear_set = spur_gear_set[:-1]

    if len(helical_gear_set) % 2 == 1:
        helical_gear_set = helical_gear_set[:-1]

    gears = [*spur_gear_set, *helical_gear_set]

    add_fixed_joint(master=motor, slave=worm_gear)
    add_worm_gear_mating(
        master=worm_gear,
        slave=worm_wheel,
        friction_coefficient=worm_friction_coefficient
    )
    add_fixed_joint(master=worm_wheel, slave=gears[0])

    for i in range(0, len(gears) - 1):
        if i % 2 == 0:
            add_gear_mating(
                master=gears[i],
                slave=gears[i + 1],
                efficiency=1
            )
        else:
            add_fixed_joint(master=gears[i], slave=gears[i + 1])

    return Powertrain(motor=motor)


@composite
def solved_powertrains(draw):
    motor = draw(one_of(dc_motors(), dc_motors(current=True)))
    flywheel = draw(flywheels())
    worm_gear = WormGear(
        name='worm gear',
        n_starts=1,
        inertia_moment=InertiaMoment(1, 'kgm^2'),
        helix_angle=Angle(10, 'deg'),
        pressure_angle=Angle(20, 'deg'),
        reference_diameter=Length(10, 'mm')
    )
    worm_wheel = WormWheel(
        name='worm wheel',
        n_teeth=10,
        inertia_moment=InertiaMoment(1, 'kgm^2'),
        helix_angle=Angle(10, 'deg'),
        pressure_angle=Angle(20, 'deg'),
        module=Length(1, 'mm'),
        face_width=Length(10, 'mm')
    )
    gear_1 = SpurGear(
        name='gear 1',
        n_teeth=10,
        inertia_moment=InertiaMoment(1, 'kgm^2'),
        module=Length(1, 'mm'),
        face_width=Length(10, 'mm')
    )
    gear_2 = SpurGear(
        name='gear 2',
        n_teeth=20,
        inertia_moment=InertiaMoment(1, 'kgm^2'),
        module=Length(1, 'mm')
    )
    non_structural_spur_gear_set = draw(
        lists(elements=spur_gears(), min_size=2, max_size=4)
    )
    structural_spur_gear_set = draw(
        lists(elements=spur_gears(structural=True), min_size=2, max_size=4)
    )
    non_structural_helical_gear_set = draw(
        lists(elements=helical_gears(), min_size=2, max_size=4)
    )
    structural_helical_gear_set = draw(
        lists(elements=helical_gears(structural=True), min_size=2, max_size=4)
    )

    if len(non_structural_spur_gear_set) % 2 == 1:
        non_structural_spur_gear_set = non_structural_spur_gear_set[:-1]

    if len(structural_spur_gear_set) % 2 == 1:
        structural_spur_gear_set = structural_spur_gear_set[:-1]

    if len(non_structural_helical_gear_set) % 2 == 1:
        non_structural_helical_gear_set = non_structural_helical_gear_set[:-1]

    if len(structural_helical_gear_set) % 2 == 1:
        structural_helical_gear_set = structural_helical_gear_set[:-1]

    non_structural_spur_gear_set = list(
        zip(*(iter(non_structural_spur_gear_set),)*2)
    )
    structural_spur_gear_set = list(zip(*(iter(structural_spur_gear_set),)*2))
    non_structural_helical_gear_set = list(
        zip(*(iter(non_structural_helical_gear_set),)*2)
    )
    structural_helical_gear_set = list(
        zip(*(iter(structural_helical_gear_set),)*2)
    )

    gears = []
    gears.extend(non_structural_spur_gear_set)
    gears.extend(structural_spur_gear_set)
    gears.extend(non_structural_helical_gear_set)
    gears.extend(structural_helical_gear_set)
    shuffle(gears)

    gears = [element for pair in gears for element in pair]
    gears.append(gear_1)
    gears.append(gear_2)

    time_discretization_value = draw(
        floats(
            min_value=1e-3,
            max_value=1,
            allow_nan=False,
            allow_infinity=False
        )
    )
    time_discretization = TimeInterval(
        value=time_discretization_value,
        unit='sec'
    )
    simulation_steps = draw(
        floats(
            min_value=5,
            max_value=50,
            allow_nan=False,
            allow_infinity=False
        )
    )

    add_fixed_joint(master=motor, slave=flywheel)
    add_fixed_joint(master=flywheel, slave=worm_gear)
    add_worm_gear_mating(
        master=worm_gear,
        slave=worm_wheel,
        friction_coefficient=0.4
    )
    add_fixed_joint(master=worm_wheel, slave=gears[0])

    for i in range(0, len(gears) - 1):
        if i % 2 == 0:
            add_gear_mating(master=gears[i], slave=gears[i + 1], efficiency=1)
        else:
            add_fixed_joint(master=gears[i], slave=gears[i + 1])

    powertrain = Powertrain(motor=motor)

    gears[-1].external_torque = \
        lambda time, angular_position, angular_speed: Torque(1, 'mNm')
    gears[-1].angular_position = AngularPosition(0, 'rad')
    gears[-1].angular_speed = AngularSpeed(0, 'rad/s')
    simulation_time = time_discretization*simulation_steps
    solver = Solver(powertrain=powertrain)
    solver.run(
        time_discretization=time_discretization,
        simulation_time=simulation_time
    )

    return powertrain


@composite
def time_intervals(draw):
    value = draw(integers(min_value=1, max_value=10))
    unit = draw(sampled_from(elements=list(TimeInterval._Time__UNITS.keys())))

    return TimeInterval(value=value, unit=unit)


@composite
def paths(draw):
    folder_list = draw(
        lists(
            elements=text(
                min_size=5,
                max_size=10,
                alphabet=characters(min_codepoint=97, max_codepoint=122)
            ),
            min_size=2,
            max_size=5
        )
    )
    folder_list.insert(0, os.path.join('.', 'test_data'))

    return os.path.join(*folder_list)
