# Import required packages, classes and functions

from gearpy.mechanical_objects import (
    DCMotor,
    Flywheel,
    HelicalGear,
    WormGear,
    WormWheel
)
from gearpy.units import (
    Angle,
    AngularPosition,
    AngularSpeed,
    InertiaMoment,
    Length,
    Stress,
    Torque,
    TimeInterval,
    Time
)
from gearpy.utils import add_fixed_joint, add_gear_mating, add_worm_gear_mating
from gearpy.powertrain import Powertrain
from gearpy.solver import Solver


# Model Set Up

motor = DCMotor(
    name='motor',
    no_load_speed=AngularSpeed(15000, 'rpm'),
    maximum_torque=Torque(10, 'mNm'),
    inertia_moment=InertiaMoment(3, 'gcm^2')
)
flywheel = Flywheel(
    name='flywheel',
    inertia_moment=InertiaMoment(20, 'kgcm^2')
)
worm_gear = WormGear(
    name='worm gear',
    n_starts=1,
    inertia_moment=InertiaMoment(3, 'gcm^2'),
    pressure_angle=Angle(20, 'deg'),
    helix_angle=Angle(10, 'deg'),
    reference_diameter=Length(10, 'mm')
)
worm_wheel = WormWheel(
    name='worm wheel',
    n_teeth=50,
    inertia_moment=InertiaMoment(500, 'gcm^2'),
    pressure_angle=Angle(20, 'deg'),
    helix_angle=Angle(10, 'deg'),
    module=Length(1, 'mm'),
    face_width=Length(10, 'mm')
)
gear_1 = HelicalGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(2, 'gcm^2'),
    helix_angle=Angle(20, 'deg'),
    module=Length(1, 'mm'),
    face_width=Length(15, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)
gear_2 = HelicalGear(
    name='gear 2',
    n_teeth=50,
    inertia_moment=InertiaMoment(750, 'gcm^2'),
    helix_angle=Angle(20, 'deg'),
    module=Length(1, 'mm'),
    face_width=Length(15, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)
gear_3 = HelicalGear(
    name='gear 3',
    n_teeth=10,
    inertia_moment=InertiaMoment(8, 'gcm^2'),
    helix_angle=Angle(20, 'deg'),
    module=Length(1.5, 'mm'),
    face_width=Length(20, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)
gear_4 = HelicalGear(
    name='gear 4',
    n_teeth=40,
    inertia_moment=InertiaMoment(2000, 'gcm^2'),
    helix_angle=Angle(20, 'deg'),
    module=Length(1.5, 'mm'),
    face_width=Length(20, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)


add_fixed_joint(master=motor, slave=flywheel)
add_fixed_joint(master=flywheel, slave=worm_gear)
add_worm_gear_mating(
    master=worm_gear,
    slave=worm_wheel,
    friction_coefficient=0.4
)
add_fixed_joint(master=worm_wheel, slave=gear_1)
add_gear_mating(master=gear_1, slave=gear_2, efficiency=0.9)
add_fixed_joint(master=gear_2, slave=gear_3)
add_gear_mating(master=gear_3, slave=gear_4, efficiency=0.9)


def ext_torque(time, angular_position, angular_speed):
    return Torque(500, 'mNm')


gear_4.external_torque = ext_torque


powertrain = Powertrain(motor=motor)


# Simulation Set Up

gear_4.angular_position = AngularPosition(0, 'rad')
gear_4.angular_speed = AngularSpeed(0, 'rad/s')


solver = Solver(powertrain=powertrain)
solver.run(
    time_discretization=TimeInterval(0.5, 'sec'),
    simulation_time=TimeInterval(20, 'sec')
)


# Result Analysis

powertrain.snapshot(
    target_time=Time(10, 'sec'),
    angular_position_unit='rot',
    torque_unit='mNm',
    driving_torque_unit='mNm',
    load_torque_unit='mNm'
)

powertrain.plot(
    figsize=(8, 8),
    elements=[motor, worm_gear, worm_wheel, gear_4],
    variables=[
        'angular position',
        'angular speed',
        'torque',
        'driving torque',
        'load torque',
        'bending stress',
        'contact stress'
    ],
    torque_unit='mNm'
)
