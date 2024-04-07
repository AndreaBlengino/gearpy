# Import required packages, classes and functions

from gearpy.mechanical_objects import DCMotor, Flywheel, SpurGear
from gearpy.units import AngularSpeed, InertiaMoment, Torque, AngularPosition, TimeInterval
from gearpy.utils import add_fixed_joint, add_gear_mating
from gearpy.powertrain import Powertrain
from gearpy.solver import Solver
import os
import pandas as pd


# Model Set Up

motor = DCMotor(name = 'motor',
                no_load_speed = AngularSpeed(15000, 'rpm'),
                maximum_torque = Torque(10, 'mNm'),
                inertia_moment = InertiaMoment(3, 'gcm^2'))
flywheel = Flywheel(name = 'flywheel',
                    inertia_moment = InertiaMoment(20, 'kgcm^2'))
gear_1 = SpurGear(name = 'gear 1',
                  n_teeth = 10,
                  inertia_moment = InertiaMoment(1, 'gcm^2'))
gear_2 = SpurGear(name = 'gear 2',
                  n_teeth = 80,
                  inertia_moment = InertiaMoment(3100, 'gcm^2'))
gear_3 = SpurGear(name = 'gear 3',
                  n_teeth = 10,
                  inertia_moment = InertiaMoment(4, 'gcm^2'))
gear_4 = SpurGear(name = 'gear 4',
                  n_teeth = 60,
                  inertia_moment = InertiaMoment(5000, 'gcm^2'))
gear_5 = SpurGear(name = 'gear 5',
                  n_teeth = 10,
                  inertia_moment = InertiaMoment(12, 'gcm^2'))
gear_6 = SpurGear(name = 'gear 6',
                  n_teeth = 50,
                  inertia_moment = InertiaMoment(7600, 'gcm^2'))


add_fixed_joint(master = motor, slave = flywheel)
add_fixed_joint(master = flywheel, slave = gear_1)
add_gear_mating(master = gear_1, slave = gear_2, efficiency = 0.9)
add_fixed_joint(master = gear_2, slave = gear_3)
add_gear_mating(master = gear_3, slave = gear_4, efficiency = 0.9)
add_fixed_joint(master = gear_4, slave = gear_5)
add_gear_mating(master = gear_5, slave = gear_6, efficiency = 0.9)


def ext_torque(time, angular_position, angular_speed):
    return Torque(500, 'mNm')

gear_6.external_torque = ext_torque


powertrain = Powertrain(motor = motor)


# Simulation Set Up

gear_6.angular_position = AngularPosition(0, 'rad')
gear_6.angular_speed = AngularSpeed(0, 'rad/s')


solver = Solver(powertrain = powertrain)
solver.run(time_discretization = TimeInterval(0.5, 'sec'),
           simulation_time = TimeInterval(20, 'sec'))


# Time Variables Export

powertrain.export_time_variables(folder_path = 'data')

motor_data = pd.read_csv(os.path.join('data', 'motor.csv'))

print(motor_data.head(11).to_string())
