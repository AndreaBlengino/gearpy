from gearpy.mechanical_object import DCMotor, SpurGear
from gearpy.motor_control import PWMControl
from gearpy.solver import Solver
from gearpy.powertrain import Powertrain
from gearpy.units import Torque, InertiaMoment, AngularSpeed, AngularPosition, TimeInterval
from gearpy.utils import add_fixed_joint
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import integers
import numpy as np
from pytest import mark, raises
from tests.conftest import powertrains, time_intervals, basic_solver
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_solver.conftest import PowertrainFake
import warnings


@mark.solver
class TestSolverInit:


    @mark.genuine
    @given(powertrain = powertrains())
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, powertrain):
        solver = Solver(powertrain = powertrain)

        assert solver.powertrain == powertrain


    @mark.error
    def test_raises_type_error(self, solver_init_type_error):
        with raises(TypeError):
            Solver(**solver_init_type_error)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            Solver(powertrain = PowertrainFake([]))


@mark.solver
class TestSolverRun:


    @mark.genuine
    @given(time_discretization_1 = time_intervals(),
           time_discretization_multiplier = integers(min_value = 1, max_value = 5),
           simulation_steps_1 = integers(min_value = 2, max_value = 100),
           simulation_steps_2 = integers(min_value = 2, max_value = 100),
           powertrain = powertrains(),
           initial_angular_position = angular_positions(),
           initial_angular_speed = angular_speeds())
    @settings(max_examples = 100, deadline = None)
    def test_method(self, time_discretization_1, time_discretization_multiplier, simulation_steps_1, simulation_steps_2,
                    powertrain, initial_angular_position, initial_angular_speed):
        warnings.filterwarnings('ignore', category = RuntimeWarning)

        powertrain.elements[-1].angular_position = initial_angular_position
        powertrain.elements[-1].angular_speed = initial_angular_speed
        powertrain.elements[-1].external_torque = lambda time, angular_position, angular_speed: Torque(0.001, 'Nm')
        motor_control = PWMControl(powertrain = powertrain)
        solver = Solver(powertrain = powertrain, motor_control = motor_control)
        simulation_time_1 = time_discretization_1*simulation_steps_1
        solver.run(time_discretization = time_discretization_1, simulation_time = simulation_time_1)

        assert len(powertrain.time) == len(np.arange(time_discretization_1.value,
                                                     simulation_time_1.value + time_discretization_1.value,
                                                     time_discretization_1.value)) + 1

        time_discretization_2 = time_discretization_1*time_discretization_multiplier
        simulation_time_2 = time_discretization_2*simulation_steps_2
        solver.run(time_discretization = time_discretization_2, simulation_time = simulation_time_2)

        assert len(powertrain.time) == len(np.arange(time_discretization_1.value,
                                                     simulation_time_1.value + time_discretization_1.value,
                                                     time_discretization_1.value)) + \
                                       len(np.arange(time_discretization_2.value,
                                                     simulation_time_2.value + time_discretization_2.value,
                                                     time_discretization_2.value)) + 1


    @mark.error
    def test_raises_type_error(self, solver_run_type_error):
        if solver_run_type_error:
            with raises(TypeError):
                basic_solver.run(**solver_run_type_error)
        else:
            motor = DCMotor(name = 'motor', no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
            gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
            add_fixed_joint(master = motor, slave = gear)
            gear.external_torque = lambda angular_position, angular_speed, time: 1
            powertrain = Powertrain(motor = motor)
            gear.angular_position = AngularPosition(0, 'rad')
            gear.angular_speed = AngularSpeed(0, 'rad/s')
            solver = Solver(powertrain = powertrain)
            with raises(TypeError):
                solver.run(time_discretization = TimeInterval(1, 'sec'), simulation_time = TimeInterval(10, 'sec'))


    @mark.error
    def test_raises_value_error(self, solver_run_value_error):
        if solver_run_value_error:
            with raises(ValueError):
                basic_solver.run(**solver_run_value_error)
        else:
            motor = DCMotor(name = 'motor', no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
            gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
            add_fixed_joint(master = motor, slave = gear)
            powertrain = Powertrain(motor = motor)
            gear.angular_position = AngularPosition(0, 'rad')
            gear.angular_speed = AngularSpeed(0, 'rad/s')
            solver = Solver(powertrain = powertrain)
            with raises(ValueError):
                solver.run(time_discretization = TimeInterval(1, 'sec'), simulation_time = TimeInterval(10, 'sec'))
