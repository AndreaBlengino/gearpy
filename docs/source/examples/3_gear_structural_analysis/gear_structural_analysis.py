# Import required packages, classes and functions

from gearpy.mechanical_objects import DCMotor, SpurGear, Flywheel
from gearpy.units import (
    AngularSpeed,
    InertiaMoment,
    Length,
    Torque,
    AngularPosition,
    TimeInterval,
    Time,
    Stress
)
from gearpy.utils import add_gear_mating, add_fixed_joint
from gearpy.powertrain import Powertrain
from gearpy.solver import Solver
import numpy as np


# Model Set Up

motor = DCMotor(
    name='motor',
    no_load_speed=AngularSpeed(15000, 'rpm'),
    maximum_torque=Torque(10, 'mNm'),
    inertia_moment=InertiaMoment(3, 'gcm^2')
)
flywheel = Flywheel(
    name='flywheel',
    inertia_moment=InertiaMoment(20000, 'gcm^2')
)
gear_1 = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(1, 'gcm^2'),
    module=Length(1, 'mm'),
    face_width=Length(10, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)
gear_2 = SpurGear(
    name='gear 2',
    n_teeth=80,
    inertia_moment=InertiaMoment(3100, 'gcm^2'),
    module=Length(1, 'mm'),
    face_width=Length(10, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)
gear_3 = SpurGear(
    name='gear 3',
    n_teeth=10,
    inertia_moment=InertiaMoment(4, 'gcm^2'),
    module=Length(1.5, 'mm'),
    face_width=Length(10, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)
gear_4 = SpurGear(
    name='gear 4',
    n_teeth=60,
    inertia_moment=InertiaMoment(5000, 'gcm^2'),
    module=Length(1.5, 'mm'),
    face_width=Length(10, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)
gear_5 = SpurGear(
    name='gear 5',
    n_teeth=10,
    inertia_moment=InertiaMoment(12, 'gcm^2'),
    module=Length(2, 'mm'),
    face_width=Length(10, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)
gear_6 = SpurGear(
    name='gear 6',
    n_teeth=50,
    inertia_moment=InertiaMoment(7600, 'gcm^2'),
    module=Length(2, 'mm'),
    face_width=Length(10, 'mm'),
    elastic_modulus=Stress(200, 'GPa')
)


add_fixed_joint(master=motor, slave=flywheel)
add_fixed_joint(master=flywheel, slave=gear_1)
add_gear_mating(master=gear_1, slave=gear_2, efficiency=0.9)
add_fixed_joint(master=gear_2, slave=gear_3)
add_gear_mating(master=gear_3, slave=gear_4, efficiency=0.9)
add_fixed_joint(master=gear_4, slave=gear_5)
add_gear_mating(master=gear_5, slave=gear_6, efficiency=0.9)


def ext_torque(time, angular_position, angular_speed):
    return Torque(
        value=200 +
        80*angular_position.sin(frequency=1/60) +
        2*angular_speed.to('rad/s').value**2 +
        20*np.sin(2*np.pi/3*time.to('sec').value),
        unit='mNm'
    )


gear_6.external_torque = ext_torque


powertrain = Powertrain(motor=motor)


# Simulation Set Up

gear_6.angular_position = AngularPosition(0, 'rad')
gear_6.angular_speed = AngularSpeed(0, 'rad/s')


solver = Solver(powertrain=powertrain)
solver.run(
    time_discretization=TimeInterval(0.5, 'sec'),
    simulation_time=TimeInterval(100, 'sec')
)


# Result Analysis

powertrain.snapshot(
    target_time=Time(10, 'sec'),
    torque_unit='mNm',
    driving_torque_unit='mNm',
    load_torque_unit='mNm'
)

powertrain.plot(
    figsize=(10, 10),
    elements=[gear_1, gear_2, gear_3, gear_4, gear_5, gear_6],
    angular_position_unit='rot',
    torque_unit='mNm',
    variables=[
        'driving torque',
        'load torque',
        'torque',
        'tangential force',
        'bending stress',
        'contact stress'
    ]
)

powertrain.plot(
    figsize=(8, 8),
    elements=[gear_5, gear_6],
    angular_position_unit='rot',
    torque_unit='mNm',
    variables=[
        'driving torque',
        'load torque',
        'torque',
        'tangential force',
        'bending stress',
        'contact stress'
    ]
)
