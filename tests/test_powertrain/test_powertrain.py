from copy import deepcopy
from gearpy.mechanical_objects import DCMotor, SpurGear, MotorBase, GearBase
from gearpy.powertrain import Powertrain
from gearpy.units import AngularAcceleration, AngularPosition, AngularSpeed, Current, Force, InertiaMoment, Length, \
    Stress, Torque, Time
from gearpy.utils import add_gear_mating, add_fixed_joint
from hypothesis import given, settings, HealthCheck
from hypothesis.strategies import lists, floats, sampled_from, booleans, one_of, none, integers, tuples
import matplotlib.pyplot as plt
import pandas as pd
from pytest import mark, raises
from tests.conftest import simple_dc_motors, simple_spur_gears, flywheels, powertrains, basic_powertrain, \
    solved_powertrains
from tests.test_units.test_time.conftest import times
import warnings


@mark.powertrain
class TestPowertrainInit:


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

        powertrain = Powertrain(motor = motor)

        assert isinstance(powertrain.elements, tuple)
        assert powertrain.elements
        assert len(powertrain.elements) == len(gears) + 2
        assert powertrain.elements[0] == motor
        assert powertrain.elements[1] == flywheel
        for elements_element, gear in zip(powertrain.elements[2:], gears):
            assert elements_element == gear


    @mark.error
    def test_raises_type_error(self, powertrain_init_type_error):
        with raises(TypeError):
            Powertrain(motor = powertrain_init_type_error)


    @mark.error
    def test_raises_value_error(self):
        motor = DCMotor(name = 'motor', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
        with raises(ValueError):
            Powertrain(motor = motor)


    @mark.error
    def test_raises_name_error(self):
        motor = DCMotor(name = 'not unique name', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
        gear = SpurGear(name = 'not unique name', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        add_fixed_joint(master = motor, slave = gear)
        with raises(NameError):
            Powertrain(motor = motor)


@mark.powertrain
class TestPowertrainUpdateTime:


    @mark.genuine
    @given(powertrain = powertrains(),
           instant = times())
    @settings(max_examples = 100, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, powertrain, instant):
        powertrain.update_time(instant = instant)

        assert powertrain.time[-1] == instant


    @mark.error
    def test_raises_type_error(self, powertrain_update_time_type_error):
        with raises(TypeError):
            basic_powertrain.update_time(instant = powertrain_update_time_type_error)


@mark.powertrain
class TestPowertrainReset:


    @mark.genuine
    @given(powertrain = solved_powertrains())
    @settings(max_examples = 100, deadline = None, suppress_health_check = [HealthCheck.too_slow])
    def test_method(self, powertrain):
        powertrain_copy = deepcopy(powertrain)
        powertrain_copy.reset()

        assert powertrain_copy.time == []

        for copied_element, original_element in zip(powertrain_copy.elements, powertrain.elements):
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


@mark.powertrain
class TestPowertrainSnapshot:


    @mark.genuine
    @given(solved_powertrain = solved_powertrains(),
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
    def test_method(self, solved_powertrain, target_time_fraction, angular_position_unit, angular_speed_unit,
                    angular_acceleration_unit, torque_unit, driving_torque_unit, load_torque_unit, force_unit,
                    stress_unit, current_unit, print_data):

        target_time = target_time_fraction*(solved_powertrain.time[-1] - solved_powertrain.time[0])

        data = solved_powertrain.snapshot(target_time = target_time, angular_position_unit = angular_position_unit,
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
        if solved_powertrain.elements[0].electric_current_is_computable:
            columns.append(f'electric current ({current_unit})')
        columns.append('pwm')

        assert isinstance(data, pd.DataFrame)
        assert [element.name for element in solved_powertrain.elements] == data.index.to_list()
        assert columns == data.columns.to_list()


    @mark.error
    def test_raises_type_error(self, powertrain_snapshot_type_error):
        if powertrain_snapshot_type_error:
            with raises(TypeError):
                basic_powertrain.snapshot(**powertrain_snapshot_type_error)
        else:
            powertrain_copy = deepcopy(basic_powertrain)
            powertrain_copy.update_time(Time(1, 'sec'))
            powertrain_copy.time[0] = 1
            with raises(TypeError):
                powertrain_copy.snapshot(target_time = Time(1, 'sec'))


    @mark.error
    def test_raises_value_error(self, powertrain_snapshot_value_error):
        if powertrain_snapshot_value_error:
            with raises(ValueError):
                basic_powertrain.snapshot(**powertrain_snapshot_value_error)
        else:
            powertrain_copy = deepcopy(basic_powertrain)
            powertrain_copy.time.clear()
            with raises(ValueError):
                powertrain_copy.snapshot(target_time = Time(1, 'sec'))


@mark.powertrain
class TestPowertrainPlot:


    @mark.genuine
    @given(solved_powertrain = solved_powertrains(),
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
           figsize = one_of(none(),
                            tuples(floats(min_value = 1, max_value = 10, allow_nan = False, allow_infinity = False),
                                   floats(min_value = 1, max_value = 10, allow_nan = False,allow_infinity = False))))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, solved_powertrain, elements_index, single_element, elements_as_names, angular_position_unit,
                    angular_speed_unit, angular_acceleration_unit, torque_unit, force_unit, stress_unit, current_unit,
                    time_unit, figsize):
        warnings.filterwarnings('ignore', category = UserWarning)
        warnings.filterwarnings('ignore', category = RuntimeWarning)

        if elements_index is not None:
            valid_index = [index for index in elements_index if index < len(solved_powertrain.elements)]
            elements = [solved_powertrain.elements[index] for index in valid_index]
            if not elements or single_element:
                elements = [solved_powertrain.elements[0]]
            if elements_as_names:
                elements = [element.name for element in elements]
        else:
            elements = None

        solved_powertrain.plot(elements = elements, angular_position_unit = angular_position_unit,
                               angular_speed_unit = angular_speed_unit,
                               angular_acceleration_unit = angular_acceleration_unit, torque_unit = torque_unit,
                               force_unit = force_unit, stress_unit = stress_unit, time_unit = time_unit,
                               current_unit = current_unit, figsize = figsize)
        plt.close()

        solved_powertrain.plot(elements = elements)
        plt.close()

        solved_powertrain.plot(elements = [solved_powertrain.elements[0]], variables = ['angular position'])
        plt.close()

        solved_powertrain.plot(elements = list(solved_powertrain.elements), variables = ['tangential force'])
        plt.close()

        solved_powertrain.plot(elements = list(solved_powertrain.elements), variables = ['bending stress'])
        plt.close()

        if solved_powertrain.elements[0].electric_current_is_computable:
            solved_powertrain.plot(elements = list(solved_powertrain.elements[:2]), variables = ['electric current'])
            plt.close()

        solved_powertrain.plot(elements = list(solved_powertrain.elements), variables = ['pwm'])
        plt.close()


    @mark.error
    def test_raises_type_error(self, powertrain_plot_type_error):
        with raises(TypeError):
            basic_powertrain.plot(**powertrain_plot_type_error)


    @mark.error
    def test_raises_value_error(self, powertrain_plot_value_error):
        with raises(ValueError):
            basic_powertrain.plot(**powertrain_plot_value_error)
