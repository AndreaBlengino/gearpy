# Import required packages, classes and functions

from gearpy.mechanical_objects import DCMotor, WormGear, WormWheel, SpurGear
from gearpy.motor_control import PWMControl
from gearpy.motor_control.rules import PositionAndVelocityControl, ConstantPWM
from gearpy.motor_control.utils import SCurveTrajectory, PIDController
from gearpy.powertrain import Powertrain
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer, Timer
from gearpy.solver import Solver
from gearpy.units import (
    AngularSpeed,
    InertiaMoment,
    Torque,
    Current,
    Angle,
    AngularPosition,
    AngularAcceleration,
    TimeInterval
)
from gearpy.utils import add_fixed_joint, add_worm_gear_mating, add_gear_mating
from gearpy.utils import StopCondition


# Model Set Up

motor = DCMotor(
    name='motor',
    no_load_speed=AngularSpeed(value=3000, unit='rpm'),
    maximum_torque=Torque(value=2000, unit='gfcm'),
    inertia_moment=InertiaMoment(value=50, unit='gcm^2'),
    no_load_electric_current=Current(value=0, unit='mA'),
    maximum_electric_current=Current(value=5, unit='A')
)
worm_gear = WormGear(
    name='worm gear',
    n_starts=1,
    inertia_moment=InertiaMoment(value=1, unit='gcm^2'),
    pressure_angle=Angle(value=20, unit='deg'),
    helix_angle=Angle(value=10, unit='deg')
)
worm_wheel = WormWheel(
    name='worm wheel',
    n_teeth=50,
    inertia_moment=InertiaMoment(value=40, unit='gcm^2'),
    pressure_angle=Angle(value=20, unit='deg'),
    helix_angle=Angle(value=10, unit='deg')
)
gear_1 = SpurGear(
    name='gear 1',
    n_teeth=10,
    inertia_moment=InertiaMoment(value=2, unit='gcm^2')
)
gear_2 = SpurGear(
    name='gear 2',
    n_teeth=40,
    inertia_moment=InertiaMoment(value=100, unit='gcm^2')
)


add_fixed_joint(master=motor, slave=worm_gear)
add_worm_gear_mating(
    master=worm_gear,
    slave=worm_wheel,
    friction_coefficient=0.2
)
add_fixed_joint(master=worm_wheel, slave=gear_1)
add_gear_mating(master=gear_1, slave=gear_2, efficiency=0.9)


def ext_torque(time, angular_position, angular_speed):
    return Torque(
        value=3*(1-angular_position.cos(frequency=2)),
        unit='Nm'
    )

gear_2.external_torque = ext_torque


start_position = AngularPosition(value=0, unit='rad')
intermediate_position = AngularPosition(value=1.5, unit='rad')
final_position = AngularPosition(value=1, unit='rad')


total_reduction_ratio = gear_2.n_teeth/gear_1.n_teeth*worm_wheel.n_teeth

start_speed = AngularSpeed(value=0, unit='rad/s')


trajectory = SCurveTrajectory(
    start_position=total_reduction_ratio*start_position,
    stop_position=total_reduction_ratio*intermediate_position,
    maximum_velocity=AngularSpeed(value=150, unit='rad/s'),
    maximum_acceleration=AngularAcceleration(value=200, unit='rad/s^2'),
    maximum_deceleration=AngularAcceleration(value=120, unit='rad/s^2'),
    start_velocity=total_reduction_ratio*start_speed,
)


position_PID = PIDController(Kp=40, Ki=50, Kd=0)
velocity_PID = PIDController(
    Kp=0.002,
    Ki=0.2,
    Kd=0,
    clamping=True,
    reference_min=-1,
    reference_max=1
)

powertrain = Powertrain(motor=motor)

encoder = AbsoluteRotaryEncoder(target=motor)
tachometer = Tachometer(target=motor)

position_control = PositionAndVelocityControl(
    encoder=encoder,
    tachometer=tachometer,
    powertrain=powertrain,
    position_PID=position_PID,
    velocity_PID=velocity_PID,
    trajectory=trajectory
)

motor_control = PWMControl(powertrain=powertrain)
motor_control.add_rule(rule=position_control)


# First Phase Simulation Set Up

gear_2.angular_position = start_position
gear_2.angular_speed = start_speed

intermediate_stop_condition = StopCondition(
    sensor=encoder,
    threshold=total_reduction_ratio*intermediate_position,
    operator=StopCondition.greater_than_or_equal_to
)

time_step = TimeInterval(value=0.0001, unit="sec")

solver = Solver(powertrain=powertrain)
solver.run(
    time_discretization=time_step,
    simulation_time=TimeInterval(value=1, unit='min'),
    motor_control=motor_control,
    stop_condition=intermediate_stop_condition
)


# First Phase Results Analysis

powertrain.plot(
    figsize=(8, 10),
    elements=['motor', 'gear 2'],
    variables=[
        'angular position',
        'angular speed',
        'angular acceleration',
        'driving torque',
        'load torque',
        'torque',
        'electric current',
        'pwm'
    ]
)


position_PID = PIDController(Kp=4000, Ki=50, Kd=0)
velocity_PID.reset()

position_control = PositionAndVelocityControl(
    encoder=encoder,
    tachometer=tachometer,
    powertrain=powertrain,
    position_PID=position_PID,
    velocity_PID=velocity_PID,
    trajectory=trajectory
)

motor_control = PWMControl(powertrain=powertrain)
motor_control.add_rule(rule=position_control)

powertrain.reset()

solver.run(
    time_discretization=time_step,
    simulation_time=TimeInterval(value=1, unit='min'),
    motor_control=motor_control,
    stop_condition=intermediate_stop_condition
)

powertrain.plot(
    figsize=(8, 10),
    elements=['motor', 'gear 2'],
    variables=[
        'angular position',
        'angular speed',
        'angular acceleration',
        'driving torque',
        'load torque',
        'torque',
        'electric current',
        'pwm'
    ]
)


# Following Phases Simulation Set Up

timer = Timer(
    start_time=powertrain.time[-1],
    duration=TimeInterval(value=1.1, unit='sec'),
)

keep_position = ConstantPWM(
    timer=timer,
    powertrain=powertrain,
    target_pwm_value=0
)

motor_control = PWMControl(powertrain=powertrain)
motor_control.add_rule(rule=keep_position)


solver = Solver(powertrain=powertrain)
solver.run(
    time_discretization=time_step,
    simulation_time=TimeInterval(value=1, unit='sec'),
    motor_control=motor_control,
)


powertrain.plot(
    figsize=(8, 10),
    elements=['motor', 'gear 2'],
    variables=[
        'angular position',
        'angular speed',
        'angular acceleration',
        'driving torque',
        'load torque',
        'torque',
        'electric current',
        'pwm'
    ]
)


def ext_torque(time, angular_position, angular_speed):
    return Torque(
        value=-3*(1-angular_position.cos(frequency=2)),
        unit='Nm'
    )

gear_2.external_torque = ext_torque


trajectory = SCurveTrajectory(
    start_position=motor.angular_position,
    stop_position=total_reduction_ratio*final_position,
    maximum_velocity=AngularSpeed(value=150, unit='rad/s'),
    maximum_acceleration=AngularAcceleration(value=200, unit='rad/s^2'),
    maximum_deceleration=AngularAcceleration(value=120, unit='rad/s^2'),
    start_velocity=motor.angular_speed,
    start_time=powertrain.time[-1]
)


position_PID.reset()
velocity_PID.reset()


position_control = PositionAndVelocityControl(
    encoder=encoder,
    tachometer=tachometer,
    powertrain=powertrain,
    position_PID=position_PID,
    velocity_PID=velocity_PID,
    trajectory=trajectory
)

motor_control = PWMControl(powertrain=powertrain)
motor_control.add_rule(rule=position_control)


# Simulation Set Up

final_stop_condition = StopCondition(
    sensor=encoder,
    threshold=total_reduction_ratio*final_position,
    operator=StopCondition.less_than_or_equal_to
)

solver = Solver(powertrain=powertrain)
solver.run(
    time_discretization=time_step,
    simulation_time=TimeInterval(value=1, unit='min'),
    motor_control=motor_control,
    stop_condition=final_stop_condition
)


powertrain.plot(
    figsize=(8, 10),
    elements=['motor', 'gear 2'],
    variables=[
        'angular position',
        'angular speed',
        'angular acceleration',
        'driving torque',
        'load torque',
        'torque',
        'electric current',
        'pwm'
    ]
)
