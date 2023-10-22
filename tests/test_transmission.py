from gearpy.mechanical_object import DCMotor, SpurGear
from gearpy.solver import Solver
from gearpy.transmission import Transmission
from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, InertiaMoment, Torque, Time
from gearpy.utils import add_gear_mating, add_fixed_joint
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import lists, floats, sampled_from, booleans
import pandas as pd
from pytest import mark, raises
from tests.conftest import dc_motors, spur_gears, flywheels, time_intervals, transmissions, basic_transmission
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds


@mark.transmission
class TestTransmissionInit:


    @mark.genuine
    @given(motor = dc_motors(),
           flywheel = flywheels(),
           gears = lists(elements = spur_gears(), min_size = 1))
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.too_slow])
    def test_property(self, motor, flywheel, gears):
        add_fixed_joint(master = motor, slave = flywheel)
        add_fixed_joint(master = flywheel, slave = gears[0])

        for i in range(0, len(gears) - 1):
            if i%2 == 0:
                add_gear_mating(master = gears[i], slave = gears[i + 1], efficiency = 1)
            else:
                add_fixed_joint(master = gears[i], slave = gears[i + 1])

        transmission = Transmission(motor = motor)

        assert isinstance(transmission.chain, tuple)
        assert transmission.chain
        assert len(transmission.chain) == len(gears) + 2
        assert transmission.chain[0] == motor
        assert transmission.chain[1] == flywheel
        for chain_element, gear in zip(transmission.chain[2:], gears):
            assert chain_element == gear


    @mark.error
    def test_raises_type_error(self, transmission_init_type_error):
        with raises(TypeError):
            Transmission(motor = transmission_init_type_error)


    @mark.error
    def test_raises_value_error(self):
        motor = DCMotor(name = 'motor', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
        with raises(ValueError):
            Transmission(motor = motor)


    @mark.error
    def test_raises_name_error(self):
        motor = DCMotor(name = 'not unique name', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
        gear = SpurGear(name = 'not unique name', n_teeth = 10, inertia_moment = InertiaMoment(1, 'kgm^2'))
        add_fixed_joint(master = motor, slave = gear)
        with raises(NameError):
            Transmission(motor = motor)


@mark.transmission
class TestTransmissionSnapshot:


    @mark.genuine
    @given(time_discretization = time_intervals(),
           simulation_steps = floats(min_value = 5, max_value = 1000, allow_nan = False, allow_infinity = False),
           transmission = transmissions(),
           initial_angular_position = angular_positions(),
           initial_angular_speed = angular_speeds(),
           target_time_fraction = floats(min_value = 1e-10, max_value = 1 - 1e-10, allow_nan = False, allow_infinity = False),
           angular_position_unit = sampled_from(elements = list(AngularPosition._AngularPosition__UNITS.keys())),
           angular_speed_unit = sampled_from(elements = list(AngularSpeed._AngularSpeed__UNITS.keys())),
           angular_acceleration_unit = sampled_from(elements = list(AngularAcceleration._AngularAcceleration__UNITS.keys())),
           torque_unit = sampled_from(elements = list(Torque._Torque__UNITS.keys())),
           driving_torque_unit = sampled_from(elements = list(Torque._Torque__UNITS.keys())),
           load_torque_unit = sampled_from(elements = list(Torque._Torque__UNITS.keys())),
           print_data = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_method(self, time_discretization, simulation_steps, transmission, initial_angular_position,
                    initial_angular_speed, target_time_fraction, angular_position_unit, angular_speed_unit,
                    angular_acceleration_unit, torque_unit, driving_torque_unit, load_torque_unit, print_data):
        transmission.chain[-1].angular_position = initial_angular_position
        transmission.chain[-1].angular_speed = initial_angular_speed
        transmission.chain[-1].external_torque = lambda time, angular_position, angular_speed: Torque(0.001, 'Nm')
        simulation_time = time_discretization*simulation_steps
        solver = Solver(time_discretization = time_discretization,
                        simulation_time = simulation_time,
                        transmission = transmission)
        solver.run()

        data = transmission.snapshot(time = solver.time, target_time = (simulation_time - time_discretization)*target_time_fraction,
                                     angular_position_unit = angular_position_unit, angular_speed_unit = angular_speed_unit,
                                     angular_acceleration_unit = angular_acceleration_unit, torque_unit = torque_unit,
                                     driving_torque_unit = driving_torque_unit, load_torque_unit = load_torque_unit,
                                     print_data = print_data)

        assert isinstance(data, pd.DataFrame)
        assert [element.name for element in transmission.chain] == data.index.to_list()
        assert [f'angular position ({angular_position_unit})', f'angular speed ({angular_speed_unit})',
                f'angular acceleration ({angular_acceleration_unit})', f'torque ({torque_unit})',
                f'driving torque ({driving_torque_unit})', f'load torque ({load_torque_unit})']


    @mark.error
    def test_raises_type_error(self, transmission_snapshot_type_error):
        with raises(TypeError):
            basic_transmission.snapshot(**transmission_snapshot_type_error)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            basic_transmission.snapshot(time = [], target_time = Time(1, 'sec'))
