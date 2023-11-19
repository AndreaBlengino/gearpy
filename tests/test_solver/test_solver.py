from gearpy.mechanical_object import DCMotor, SpurGear
from gearpy.solver import Solver
from gearpy.transmission import Transmission
from gearpy.units import Torque, InertiaMoment, AngularSpeed, AngularPosition, TimeInterval
from gearpy.utils import add_fixed_joint
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import floats, integers
import numpy as np
from pytest import mark, raises
from tests.conftest import transmissions, time_intervals
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds
import warnings


@mark.solver
class TestSolverInit:


    @mark.genuine
    @given(time_discretization = time_intervals(),
           simulation_steps = integers(min_value = 2, max_value = 1000),
           transmission = transmissions())
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, time_discretization, simulation_steps, transmission):
        simulation_time = time_discretization*simulation_steps
        solver = Solver(time_discretization = time_discretization,
                        simulation_time = simulation_time,
                        transmission = transmission)

        assert solver.time_discretization == time_discretization
        assert solver.simulation_time == simulation_time
        assert solver.transmission == transmission


    @mark.error
    def test_raises_type_error(self, solver_init_type_error):
        with raises(TypeError):
            Solver(**solver_init_type_error)


    @mark.error
    def test_raises_value_error(self, solver_init_value_error):
        with raises(ValueError):
            Solver(**solver_init_value_error)


@mark.solver
class TestSolverRun:


    @mark.genuine
    @given(time_discretization = time_intervals(),
           simulation_steps = floats(min_value = 5, max_value = 1000, allow_nan = False, allow_infinity = False),
           transmission = transmissions(),
           initial_angular_position = angular_positions(),
           initial_angular_speed = angular_speeds())
    @settings(max_examples = 100, deadline = None)
    def test_method(self, time_discretization, simulation_steps, transmission, initial_angular_position, initial_angular_speed):
        warnings.filterwarnings('ignore', category = RuntimeWarning)

        transmission.chain[-1].angular_position = initial_angular_position
        transmission.chain[-1].angular_speed = initial_angular_speed
        transmission.chain[-1].external_torque = lambda time, angular_position, angular_speed: Torque(0.001, 'Nm')
        simulation_time = time_discretization*simulation_steps
        solver = Solver(time_discretization = time_discretization,
                        simulation_time = simulation_time,
                        transmission = transmission)
        solver.run()

        assert len(transmission.time) == len(np.arange(time_discretization.value,
                                                       simulation_time.value + time_discretization.value,
                                                       time_discretization.value)) + 1


    @mark.error
    def test_raises_type_error(self):
        motor = DCMotor(name = 'motor', no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
        add_fixed_joint(master = motor, slave = gear)
        gear.external_torque = lambda angular_position, angular_speed, time: 1
        transmission = Transmission(motor = motor)
        gear.angular_position = AngularPosition(0, 'rad')
        gear.angular_speed = AngularSpeed(0, 'rad/s')
        solver = Solver(time_discretization = TimeInterval(1, 'sec'),
                        simulation_time = TimeInterval(10, 'sec'),
                        transmission = transmission)
        with raises(TypeError):
            solver.run()


    @mark.error
    def test_raises_value_error(self):
        motor = DCMotor(name = 'motor', no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        gear = SpurGear(name = 'gear', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
        add_fixed_joint(master = motor, slave = gear)
        transmission = Transmission(motor = motor)
        gear.angular_position = AngularPosition(0, 'rad')
        gear.angular_speed = AngularSpeed(0, 'rad/s')
        solver = Solver(time_discretization = TimeInterval(1, 'sec'),
                        simulation_time = TimeInterval(10, 'sec'),
                        transmission = transmission)
        with raises(ValueError):
            solver.run()
