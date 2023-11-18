# Import required packages, classes and functions

from gearpy.mechanical_object import DCMotor, SpurGear, Flywheel
from gearpy.units import AngularSpeed, InertiaMoment, Torque, AngularPosition, TimeInterval, Time
from gearpy.utils import add_gear_mating, add_fixed_joint
from gearpy.transmission import Transmission
from gearpy.solver import Solver
import numpy as np


# Model Set Up

motor = DCMotor(name = 'motor',
                no_load_speed = AngularSpeed(1500, 'rad/s'),
                maximum_torque = Torque(10, 'mNm'),
                inertia_moment = InertiaMoment(0.5, 'gm^2'))
flywheel = Flywheel(name = 'flywheel',
                    inertia_moment = InertiaMoment(3, 'gm^2'))
gear_1 = SpurGear(name = 'gear 1',
                  n_teeth = 10,
                  inertia_moment = InertiaMoment(1, 'gm^2'))
gear_2 = SpurGear(name = 'gear 2',
                  n_teeth = 20,
                  inertia_moment = InertiaMoment(2, 'gm^2'))
gear_3 = SpurGear(name = 'gear 3',
                  n_teeth = 10,
                  inertia_moment = InertiaMoment(1, 'gm^2'))
gear_4 = SpurGear(name = 'gear 4',
                  n_teeth = 30,
                  inertia_moment = InertiaMoment(3, 'gm^2'))


add_fixed_joint(master = motor, slave = flywheel)
add_fixed_joint(master = flywheel, slave = gear_1)
add_gear_mating(master = gear_1, slave = gear_2, efficiency = 0.9)
add_fixed_joint(master = gear_2, slave = gear_3)
add_gear_mating(master = gear_3, slave = gear_4, efficiency = 0.9)


def ext_torque(time, angular_position, angular_speed):
    return Torque(30, 'mNm')

# def ext_torque(time, angular_position, angular_speed):
#     return Torque(value = 10 +
#                           2*np.sin(2*np.pi/10000*angular_position.to('rad').value) +
#                           0.001*angular_speed.to('rad/s').value**2 +
#                           1.5*np.sin(2*np.pi/200*time.to('sec').value),
#                   unit = 'mNm')

gear_4.external_torque = ext_torque


transmission = Transmission(motor = motor)


# Simulation Set Up

gear_4.angular_position = AngularPosition(0, 'rad')
gear_4.angular_speed = AngularSpeed(0, 'rad/s')


solver = Solver(time_discretization = TimeInterval(1, 'sec'),
                simulation_time = TimeInterval(2000, 'sec'),
                transmission = transmission)
solver.run()


# Result Analysis

transmission.snapshot(target_time = Time(1000, 'sec'))

transmission.snapshot(target_time = Time(1000, 'sec'),
                      torque_unit = 'mNm',
                      driving_torque_unit = 'mNm',
                      load_torque_unit = 'mNm')


transmission.plot(figsize = (12, 9))

transmission.plot(elements = ['gear 4', motor],
                  variables = ['torque', 'driving torque', 'angular speed', 'load torque'],
                  torque_unit = 'mNm',
                  figsize = (8, 6))
