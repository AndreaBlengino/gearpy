from gearpy.mechanical_object import DCMotor, SpurGear
from gearpy.solver import Solver
from gearpy.transmission import Transmission
from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, InertiaMoment, Torque, Time
from gearpy.utils import add_gear_mating, add_fixed_joint
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import lists, floats, sampled_from, booleans, one_of, none, integers
import matplotlib.pyplot as plt
import pandas as pd
from pytest import mark, raises
from tests.conftest import dc_motors, spur_gears, flywheels, time_intervals, transmissions, basic_transmission, solved_transmissions
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_units.test_time.conftest import times
import warnings


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
class TestTransmissionUpdateTime:

    @mark.genuine
    @given(transmission = transmissions(),
           instant = times())
    @settings(max_examples = 100)
    def test_method(self, transmission, instant):
        transmission.update_time(instant = instant)

        assert transmission.time[-1] == instant


    @mark.error
    def test_raises_type_error(self, transmission_update_time_type_error):
        with raises(TypeError):
            basic_transmission.update_time(instant = transmission_update_time_type_error)


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

        data = transmission.snapshot(target_time = (simulation_time - time_discretization)*target_time_fraction,
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
            if transmission_snapshot_type_error:
                basic_transmission.snapshot(**transmission_snapshot_type_error)
            else:
                basic_transmission.update_time(Time(1, 'sec'))
                basic_transmission.time[0] = 1
                basic_transmission.snapshot(target_time = Time(1, 'sec'))


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            basic_transmission.time.clear()
            basic_transmission.snapshot(target_time = Time(1, 'sec'))


@mark.transmission
class TestTransmissionPlot:


    @mark.genuine
    @given(solved_transmission = solved_transmissions(),
           elements_index = one_of(none(), lists(integers(min_value = 0, max_value = 4), min_size = 1)),
           single_element = booleans(),
           elements_as_names = booleans(),
           angular_position_unit = sampled_from(elements = list(AngularPosition._AngularPosition__UNITS.keys())),
           angular_speed_unit = sampled_from(elements = list(AngularSpeed._AngularSpeed__UNITS.keys())),
           angular_acceleration_unit = sampled_from(elements = list(AngularAcceleration._AngularAcceleration__UNITS.keys())),
           torque_unit = sampled_from(elements = list(Torque._Torque__UNITS.keys())),
           time_unit = sampled_from(elements = list(Time._Time__UNITS.keys())))
    @settings(max_examples = 20, deadline = None)
    def test_method(self, solved_transmission, elements_index, single_element, elements_as_names, angular_position_unit,
                    angular_speed_unit, angular_acceleration_unit, torque_unit, time_unit):
        warnings.filterwarnings("ignore", category = UserWarning)

        if elements_index is not None:
            valid_index = [index for index in elements_index if index < len(solved_transmission.chain)]
            elements = [solved_transmission.chain[index] for index in valid_index]
            if not elements or single_element:
                elements = [solved_transmission.chain[0]]
            if elements_as_names:
                elements = [element.name for element in elements]
        else:
            elements = None

        solved_transmission.plot(elements = elements, angular_position_unit = angular_position_unit,
                                 angular_speed_unit = angular_speed_unit,
                                 angular_acceleration_unit = angular_acceleration_unit, torque_unit = torque_unit,
                                 time_unit = time_unit)
        plt.close()


    @mark.error
    def test_raises_type_error(self, transmission_plot_type_error):
        with raises(TypeError):
            basic_transmission.plot(**transmission_plot_type_error)


    @mark.error
    def test_raises_value_error(self, transmission_plot_value_error):
        with raises(ValueError):
            basic_transmission.plot(**transmission_plot_value_error)
