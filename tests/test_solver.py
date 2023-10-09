from gearpy.solver import Solver
from hypothesis import given, settings
from hypothesis.strategies import floats, integers
import numpy as np
from pytest import mark, raises
from tests.conftest import transmissions


@mark.solver
class TestSolverInit:


    @mark.genuine
    @given(time_discretization = floats(min_value = 0, max_value = 1, exclude_min = True,
                                        allow_nan = False, allow_infinity = False),
           simulation_steps = integers(min_value = 2, max_value = 1000),
           transmission = transmissions())
    @settings(max_examples = 100)
    def test_method(self, time_discretization, simulation_steps, transmission):
        simulation_time = time_discretization*simulation_steps
        solver = Solver(time_discretization = time_discretization,
                        simulation_time = simulation_time,
                        transmission = transmission)

        assert solver.time_discretization == time_discretization
        assert solver.simulation_time == simulation_time
        assert solver.transmission_chain == transmission.chain
        assert solver.time == [0]


    @mark.error
    def test_raises_type_error(self, solver_init_type_error):
        with raises(TypeError):
            Solver(time_discretization = solver_init_type_error['time_discretization'],
                   simulation_time = solver_init_type_error['simulation_time'],
                   transmission = solver_init_type_error['transmission'])


    @mark.error
    def test_raises_value_error(self, solver_init_value_error):
        with raises(ValueError):
            Solver(time_discretization = solver_init_value_error['time_discretization'],
                   simulation_time = solver_init_value_error['simulation_time'],
                   transmission = solver_init_value_error['transmission'])


@mark.solver
class TestSolverRun:


    @mark.genuine
    @given(time_discretization = floats(min_value = 1e-10, max_value = 10, allow_nan = False, allow_infinity = False),
           simulation_steps = floats(min_value = 5, max_value = 1000, allow_nan = False, allow_infinity = False),
           transmission = transmissions(),
           initial_angle = floats(allow_nan = False, allow_infinity = False),
           initial_speed = floats(allow_nan = False, allow_infinity = False))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, time_discretization, simulation_steps, transmission, initial_angle, initial_speed):
        transmission.chain[-1].angle = initial_angle
        transmission.chain[-1].speed = initial_speed
        transmission.chain[-1].external_torque = lambda time, angle, speed: 0.001
        simulation_time = time_discretization*simulation_steps
        solver = Solver(time_discretization = time_discretization,
                        simulation_time = simulation_time,
                        transmission = transmission)
        solver.run()

        assert len(solver.time) == len(np.arange(time_discretization, simulation_time, time_discretization)) + 1
