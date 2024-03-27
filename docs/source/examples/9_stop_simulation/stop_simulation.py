# Import required packages, classes and functions

from gearpy.mechanical_objects import DCMotor, SpurGear, Flywheel
from gearpy.motor_control import PWMControl
from gearpy.motor_control.rules import StartLimitCurrent
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer, Amperometer
from gearpy.units import AngularSpeed, InertiaMoment, Torque, AngularPosition, TimeInterval, Current
from gearpy.utils import add_gear_mating, add_fixed_joint, StopCondition
from gearpy.powertrain import Powertrain
from gearpy.solver import Solver
import numpy as np


# Model Set Up

motor = DCMotor(name = 'motor',
                no_load_speed = AngularSpeed(15000, 'rpm'),
                maximum_torque = Torque(10, 'mNm'),
                inertia_moment = InertiaMoment(3, 'gcm^2'),
                no_load_electric_current = Current(200, 'mA'),
                maximum_electric_current = Current(5, 'A'))
flywheel = Flywheel(name = 'flywheel',
                    inertia_moment = InertiaMoment(20000, 'gcm^2'))
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
    return Torque(value = 50 + np.exp(time.to('sec').value - 20),
                  unit = 'mNm')

gear_6.external_torque = ext_torque


powertrain = Powertrain(motor = motor)


encoder = AbsoluteRotaryEncoder(target = gear_6)
tachometer = Tachometer(target = motor)

start = StartLimitCurrent(encoder = encoder,
                          tachometer = tachometer,
                          motor = motor,
                          limit_electric_current = Current(2, 'A'),
                          target_angular_position = AngularPosition(10, 'rot'))

motor_control = PWMControl(powertrain = powertrain)
motor_control.add_rule(rule = start)

amperometer = Amperometer(target = motor)
stop_condition = StopCondition(sensor = amperometer,
                               threshold = Current(4, 'A'),
                               operator = StopCondition.greater_than_or_equal_to)


# Simulation Set Up

gear_6.angular_position = AngularPosition(0, 'rad')
gear_6.angular_speed = AngularSpeed(0, 'rad/s')

solver = Solver(powertrain = powertrain)
solver.run(time_discretization = TimeInterval(0.1, 'sec'),
           simulation_time = TimeInterval(100, 'sec'),
           motor_control = motor_control,
           stop_condition = stop_condition)


# Result Analysis

powertrain.plot(figsize = (10, 8),
                elements = ['motor', 'gear 6'],
                angular_position_unit = 'rot',
                torque_unit = 'mNm',
                variables = ['angular position', 'angular speed', 'angular acceleration',
                             'driving torque', 'load torque', 'torque', 'electric current', 'pwm'])
