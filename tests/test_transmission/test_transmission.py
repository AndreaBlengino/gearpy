from copy import deepcopy
from gearpy.mechanical_object import DCMotor, SpurGear, MotorBase, GearBase
from gearpy.transmission import Transmission
from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, Current, Force, InertiaMoment, Length, \
    Stress, Torque, Time
from gearpy.utils import add_gear_mating, add_fixed_joint
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import lists, floats, sampled_from, booleans, one_of, none, integers, tuples
import matplotlib.pyplot as plt
import pandas as pd
from pytest import mark, raises
from tests.conftest import simple_dc_motors, simple_spur_gears, flywheels, transmissions, basic_transmission, \
    solved_transmissions
from tests.test_units.test_time.conftest import times
import warnings


@mark.transmission
class TestTransmissionInit:


    @mark.genuine
    @given(motor = simple_dc_motors(),
           flywheel = flywheels(),
           gears = lists(elements = simple_spur_gears(), min_size = 1))
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
        gear = SpurGear(name = 'not unique name', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        add_fixed_joint(master = motor, slave = gear)
        with raises(NameError):
            Transmission(motor = motor)


@mark.transmission
class TestTransmissionUpdateTime:


    @mark.genuine
    @given(transmission = transmissions(),
           instant = times())
    @settings(max_examples = 100, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, transmission, instant):
        transmission.update_time(instant = instant)

        assert transmission.time[-1] == instant


    @mark.error
    def test_raises_type_error(self, transmission_update_time_type_error):
        with raises(TypeError):
            basic_transmission.update_time(instant = transmission_update_time_type_error)


@mark.transmission
class TestTransmissionReset:


    @mark.genuine
    @given(transmission = solved_transmissions())
    @settings(max_examples = 100)
    def test_method(self, transmission):
        transmission_copy = deepcopy(transmission)
        transmission_copy.reset()

        assert transmission_copy.time == []

        for copied_element, original_element in zip(transmission_copy.chain, transmission.chain):
            assert copied_element.angular_position == original_element.time_variables['angular position'][0]
            assert copied_element.angular_speed == original_element.time_variables['angular speed'][0]
            assert copied_element.angular_acceleration == original_element.time_variables['angular acceleration'][0]
            assert copied_element.driving_torque == original_element.time_variables['driving torque'][0]
            assert copied_element.load_torque == original_element.time_variables['load torque'][0]
            assert copied_element.torque == original_element.time_variables['torque'][0]
            if isinstance(copied_element, MotorBase):
                if copied_element.electric_current_is_computable:
                    assert copied_element.electric_current == original_element.time_variables['electric current'][0]
            if isinstance(copied_element, GearBase):
                if copied_element.tangential_force_is_computable:
                    assert copied_element.tangential_force == original_element.time_variables['tangential force'][0]
                    if copied_element.bending_stress_is_computable:
                        assert copied_element.bending_stress == original_element.time_variables['bending stress'][0]
                        if copied_element.contact_stress_is_computable:
                            assert copied_element.contact_stress == original_element.time_variables['contact stress'][0]

            for variable_values in copied_element.time_variables.values():
                assert variable_values == []


@mark.transmission
class TestTransmissionSnapshot:


    @mark.genuine
    @given(solved_transmission = solved_transmissions(),
           target_time_fraction = floats(min_value = 1e-10, max_value = 1 - 1e-10, allow_nan = False, allow_infinity = False),
           angular_position_unit = sampled_from(elements = list(AngularPosition._AngularPosition__UNITS.keys())),
           angular_speed_unit = sampled_from(elements = list(AngularSpeed._AngularSpeed__UNITS.keys())),
           angular_acceleration_unit = sampled_from(elements = list(AngularAcceleration._AngularAcceleration__UNITS.keys())),
           torque_unit = sampled_from(elements = list(Torque._Torque__UNITS.keys())),
           driving_torque_unit = sampled_from(elements = list(Torque._Torque__UNITS.keys())),
           load_torque_unit = sampled_from(elements = list(Torque._Torque__UNITS.keys())),
           force_unit = sampled_from(elements = list(Force._Force__UNITS.keys())),
           stress_unit = sampled_from(elements = list(Stress._Stress__UNITS.keys())),
           current_unit = sampled_from(elements = list(Current._Current__UNITS.keys())),
           print_data = booleans())
    @settings(max_examples = 100, deadline = None)
    def test_method(self, solved_transmission, target_time_fraction, angular_position_unit, angular_speed_unit,
                    angular_acceleration_unit, torque_unit, driving_torque_unit, load_torque_unit, force_unit,
                    stress_unit, current_unit, print_data):

        target_time = target_time_fraction*(solved_transmission.time[-1] - solved_transmission.time[0])

        data = solved_transmission.snapshot(target_time = target_time, angular_position_unit = angular_position_unit,
                                            angular_speed_unit = angular_speed_unit,
                                            angular_acceleration_unit = angular_acceleration_unit,
                                            torque_unit = torque_unit, driving_torque_unit = driving_torque_unit,
                                            load_torque_unit = load_torque_unit, force_unit = force_unit,
                                            stress_unit = stress_unit, current_unit = current_unit,
                                            print_data = print_data)

        columns = [f'angular position ({angular_position_unit})', f'angular speed ({angular_speed_unit})',
                   f'angular acceleration ({angular_acceleration_unit})', f'torque ({torque_unit})',
                   f'driving torque ({driving_torque_unit})', f'load torque ({load_torque_unit})',
                   f'tangential force ({force_unit})', f'bending stress ({stress_unit})',
                   f'contact stress ({stress_unit})']
        if solved_transmission.chain[0].electric_current_is_computable:
            columns.append(f'electric current ({current_unit})')

        assert isinstance(data, pd.DataFrame)
        assert [element.name for element in solved_transmission.chain] == data.index.to_list()
        assert columns == data.columns.to_list()


    @mark.error
    def test_raises_type_error(self, transmission_snapshot_type_error):
        if transmission_snapshot_type_error:
            with raises(TypeError):
                basic_transmission.snapshot(**transmission_snapshot_type_error)
        else:
            transmission_copy = deepcopy(basic_transmission)
            transmission_copy.update_time(Time(1, 'sec'))
            transmission_copy.time[0] = 1
            with raises(TypeError):
                transmission_copy.snapshot(target_time = Time(1, 'sec'))


    @mark.error
    def test_raises_value_error(self, transmission_snapshot_value_error):
        if transmission_snapshot_value_error:
            with raises(ValueError):
                basic_transmission.snapshot(**transmission_snapshot_value_error)
        else:
            transmission_copy = deepcopy(basic_transmission)
            transmission_copy.time.clear()
            with raises(ValueError):
                transmission_copy.snapshot(target_time = Time(1, 'sec'))


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
           force_unit = sampled_from(elements = list(Force._Force__UNITS.keys())),
           stress_unit = sampled_from(elements = list(Stress._Stress__UNITS.keys())),
           current_unit = sampled_from(elements = list(Current._Current__UNITS.keys())),
           time_unit = sampled_from(elements = list(Time._Time__UNITS.keys())),
           figsize = one_of(none(), tuples(floats(min_value = 1, max_value = 10, allow_nan = False, allow_infinity = False),
                                           floats(min_value = 1, max_value = 10, allow_nan = False,allow_infinity = False))))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, solved_transmission, elements_index, single_element, elements_as_names, angular_position_unit,
                    angular_speed_unit, angular_acceleration_unit, torque_unit, force_unit, stress_unit, current_unit,
                    time_unit, figsize):
        warnings.filterwarnings('ignore', category = UserWarning)
        warnings.filterwarnings('ignore', category = RuntimeWarning)

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
                                 force_unit = force_unit, stress_unit = stress_unit, time_unit = time_unit,
                                 current_unit = current_unit, figsize = figsize)
        plt.close()

        solved_transmission.plot(elements = elements)
        plt.close()

        solved_transmission.plot(elements = [solved_transmission.chain[0]], variables = ['angular position'])
        plt.close()

        solved_transmission.plot(elements = list(solved_transmission.chain), variables = ['tangential force'])
        plt.close()

        solved_transmission.plot(elements = list(solved_transmission.chain), variables = ['bending stress'])
        plt.close()

        if solved_transmission.chain[0].electric_current_is_computable:
            solved_transmission.plot(elements = list(solved_transmission.chain[:2]), variables = ['electric current'])
            plt.close()


    @mark.error
    def test_raises_type_error(self, transmission_plot_type_error):
        with raises(TypeError):
            basic_transmission.plot(**transmission_plot_type_error)


    @mark.error
    def test_raises_value_error(self, transmission_plot_value_error):
        with raises(ValueError):
            basic_transmission.plot(**transmission_plot_value_error)
