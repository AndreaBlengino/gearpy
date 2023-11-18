# Import required packages, classes and functions

from gearpy.mechanical_object import DCMotor, SpurGear, Flywheel
from gearpy.units import AngularSpeed, InertiaMoment, Length, Torque, AngularPosition, TimeInterval, Time, Stress
from gearpy.utils import add_gear_mating, add_fixed_joint
from gearpy.transmission import Transmission
from gearpy.solver import Solver
import numpy as np


# Model Set Up

motor = DCMotor(name = 'motor',
                no_load_speed = AngularSpeed(2000, 'rpm'),
                maximum_torque = Torque(200, 'mNm'),
                inertia_moment = InertiaMoment(5, 'gm^2'))
flywheel = Flywheel(name = 'flywheel',
                    inertia_moment = InertiaMoment(30, 'gm^2'))
gear_1 = SpurGear(name = 'gear 1',
                  n_teeth = 10,
                  inertia_moment = InertiaMoment(10, 'gm^2'),
                  module = Length(1, 'mm'),
                  face_width = Length(5, 'mm'),
                  elastic_modulus = Stress(210, 'GPa'))
gear_2 = SpurGear(name = 'gear 2',
                  n_teeth = 80,
                  inertia_moment = InertiaMoment(80, 'gm^2'),
                  module = Length(1, 'mm'),
                  face_width = Length(5, 'mm'),
                  elastic_modulus = Stress(210, 'GPa'))
gear_3 = SpurGear(name = 'gear 3',
                  n_teeth = 10,
                  inertia_moment = InertiaMoment(10, 'gm^2'),
                  module = Length(1, 'mm'),
                  face_width = Length(5, 'mm'),
                  elastic_modulus = Stress(210, 'GPa'))
gear_4 = SpurGear(name = 'gear 4',
                  n_teeth = 60,
                  inertia_moment = InertiaMoment(60, 'gm^2'),
                  module = Length(1, 'mm'),
                  face_width = Length(5, 'mm'),
                  elastic_modulus = Stress(210, 'GPa'))


add_fixed_joint(master = motor, slave = flywheel)
add_fixed_joint(master = flywheel, slave = gear_1)
add_gear_mating(master = gear_1, slave = gear_2, efficiency = 0.9)
add_fixed_joint(master = gear_2, slave = gear_3)
add_gear_mating(master = gear_3, slave = gear_4, efficiency = 0.9)


def ext_torque(time, angular_position, angular_speed):
    return Torque(value = 6 + 0.5*np.sin(2*np.pi/10*angular_position.to('rad').value),
                  unit = 'Nm')

gear_4.external_torque = ext_torque


transmission = Transmission(motor = motor)


# Simulation Set Up

gear_4.angular_position = AngularPosition(0, 'rad')
gear_4.angular_speed = AngularSpeed(0, 'rad/s')


solver = Solver(time_discretization = TimeInterval(0.1, 'sec'),
                simulation_time = TimeInterval(100, 'sec'),
                transmission = transmission)
solver.run()


# Result Analysis

transmission.snapshot(target_time = Time(50, 'sec'))


transmission.plot(figsize = (10, 12))

transmission.plot(elements = ['gear 1', 'gear 2', 'gear 3', 'gear 4'],
                  variables = ['angular position', 'torque', 'driving torque', 'load torque',
                               'tangential force', 'bending stress', 'contact stress'],
                  angular_position_unit = 'rot',
                  figsize = (8, 6))


# # Improved Model Set Up

motor = DCMotor(name = 'motor',
                no_load_speed = AngularSpeed(2000, 'rpm'),
                maximum_torque = Torque(200, 'mNm'),
                inertia_moment = InertiaMoment(5, 'gm^2'))
flywheel = Flywheel(name = 'flywheel',
                    inertia_moment = InertiaMoment(30, 'gm^2'))
gear_1 = SpurGear(name = 'gear 1',
                  n_teeth = 10,
                  inertia_moment = InertiaMoment(10, 'gm^2'),
                  module = Length(1.25, 'mm'),
                  face_width = Length(10, 'mm'),
                  elastic_modulus = Stress(210, 'GPa'))
gear_2 = SpurGear(name = 'gear 2',
                  n_teeth = 80,
                  inertia_moment = InertiaMoment(80, 'gm^2'),
                  module = Length(1.25, 'mm'),
                  face_width = Length(10, 'mm'),
                  elastic_modulus = Stress(210, 'GPa'))
gear_3 = SpurGear(name = 'gear 3',
                  n_teeth = 10,
                  inertia_moment = InertiaMoment(40, 'gm^2'),
                  module = Length(2.5, 'mm'),
                  face_width = Length(20, 'mm'),
                  elastic_modulus = Stress(210, 'GPa'))
gear_4 = SpurGear(name = 'gear 4',
                  n_teeth = 60,
                  inertia_moment = InertiaMoment(240, 'gm^2'),
                  module = Length(2.5, 'mm'),
                  face_width = Length(20, 'mm'),
                  elastic_modulus = Stress(210, 'GPa'))


add_fixed_joint(master = motor, slave = flywheel)
add_fixed_joint(master = flywheel, slave = gear_1)
add_gear_mating(master = gear_1, slave = gear_2, efficiency = 0.9)
add_fixed_joint(master = gear_2, slave = gear_3)
add_gear_mating(master = gear_3, slave = gear_4, efficiency = 0.9)


def ext_torque(time, angular_position, angular_speed):
    return Torque(value = 6 + 0.5*np.sin(2*np.pi/10*angular_position.to('rad').value),
                  unit = 'Nm')

gear_4.external_torque = ext_torque


transmission = Transmission(motor = motor)


# Simulation Set Up

gear_4.angular_position = AngularPosition(0, 'rad')
gear_4.angular_speed = AngularSpeed(0, 'rad/s')


solver = Solver(time_discretization = TimeInterval(0.1, 'sec'),
                simulation_time = TimeInterval(100, 'sec'),
                transmission = transmission)
solver.run()


# Improved Model Result Analysis

transmission.snapshot(target_time = Time(50, 'sec'))


transmission.plot(elements = ['gear 1', 'gear 2', 'gear 3', 'gear 4'],
                  variables = ['angular position', 'torque', 'driving torque', 'load torque',
                               'tangential force', 'bending stress', 'contact stress'],
                  angular_position_unit = 'rot',
                  figsize = (8, 6))
