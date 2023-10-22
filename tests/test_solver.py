from gearpy.solver import Solver
from gearpy.units import Torque, Time
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import floats, integers
import numpy as np
from pytest import mark, raises
from tests.conftest import transmissions, time_intervals
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds


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
        assert solver.transmission_chain == transmission.chain
        assert solver.time == [Time(value = 0, unit = time_discretization.unit)]


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
        transmission.chain[-1].angular_position = initial_angular_position
        transmission.chain[-1].angular_speed = initial_angular_speed
        transmission.chain[-1].external_torque = lambda time, angular_position, angular_speed: Torque(0.001, 'Nm')
        simulation_time = time_discretization*simulation_steps
        solver = Solver(time_discretization = time_discretization,
                        simulation_time = simulation_time,
                        transmission = transmission)
        solver.run()

        assert len(solver.time) == len(np.arange(time_discretization.value, simulation_time.value, time_discretization.value)) + 1
