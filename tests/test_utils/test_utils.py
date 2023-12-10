from gearpy.mechanical_object import SpurGear, MatingMaster, MatingSlave
from gearpy.units import InertiaMoment, Length, AngularSpeed, Torque, Current
from gearpy.utils import add_gear_mating, add_fixed_joint, dc_motor_characteristics_animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from hypothesis import given, settings
from hypothesis.strategies import floats, one_of, sampled_from, booleans, none, tuples
import os
from pytest import mark, raises
from tests.conftest import simple_dc_motors, simple_spur_gears, flywheels, solved_transmissions
import warnings


@mark.utils
class TestAddGearMating:


    @mark.genuine
    @given(gear_1 = simple_spur_gears(),
           gear_2 = simple_spur_gears(),
           efficiency = floats(allow_nan = False, allow_infinity = False,
                               min_value = 0, exclude_min = False, max_value = 1, exclude_max = False))
    @settings(max_examples = 100)
    def test_function(self, gear_1, gear_2, efficiency):
        add_gear_mating(master = gear_1, slave = gear_2, efficiency = efficiency)

        assert gear_1.drives == gear_2
        assert gear_1.mating_role == MatingMaster
        assert gear_2.driven_by == gear_1
        assert gear_2.mating_role == MatingSlave
        assert gear_2.master_gear_ratio == gear_2.n_teeth/gear_1.n_teeth
        assert gear_2.master_gear_efficiency == efficiency


    @mark.error
    def test_raises_type_error(self, add_gear_mating_type_error):
        with raises(TypeError):
            add_gear_mating(**add_gear_mating_type_error)


    @mark.error
    def test_raises_value_error(self, add_gear_mating_value_error):
        gear_1 = SpurGear(name = 'gear 1', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        gear_2 = SpurGear(name = 'gear 2', n_teeth = 20, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        gear_3 = SpurGear(name = 'gear 3', n_teeth = 20, module = Length(2, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
        if add_gear_mating_value_error < 0 or add_gear_mating_value_error > 1:
            with raises(ValueError):
                add_gear_mating(master = gear_1, slave = gear_2, efficiency = add_gear_mating_value_error)
        else:
            with raises(ValueError):
                add_gear_mating(master = gear_1, slave = gear_3, efficiency = add_gear_mating_value_error)


@mark.utils
class TestAddFixedJoint:


    @mark.genuine
    @given(master = one_of(simple_dc_motors(), simple_spur_gears(), flywheels()),
           slave = one_of(simple_spur_gears(), flywheels()))
    @settings(max_examples = 100)
    def test_function(self, master, slave):
        add_fixed_joint(master = master, slave = slave)

        assert master.drives == slave
        assert slave.driven_by == master
        assert slave.master_gear_ratio == 1.0


    @mark.error
    def test_raises_type_error(self, add_fixed_joint_type_error):
        with raises(TypeError):
            add_fixed_joint(**add_fixed_joint_type_error)


@mark.utils
class TestDCMotorCharacteristicsAnimation:


    @mark.genuine
    @given(solved_transmission = solved_transmissions(),
           interval = floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 50),
           angular_speed_unit = sampled_from(elements = list(AngularSpeed._AngularSpeed__UNITS.keys())),
           torque_unit = sampled_from(elements = list(Torque._Torque__UNITS.keys())),
           current_unit = sampled_from(elements = list(Current._Current__UNITS.keys())),
           figsize = one_of(none(),
                            tuples(floats(min_value = 1, max_value = 10, allow_nan = False, allow_infinity = False),
                                   floats(min_value = 1, max_value = 10, allow_nan = False, allow_infinity = False))),
           marker_size = floats(allow_nan = False, allow_infinity = False, min_value = 1, max_value = 20),
           padding = floats(allow_nan = False, allow_infinity = False, min_value = 0.01, max_value = 1),
           show = booleans())
    @settings(max_examples = 10, deadline = None)
    def test_function(self, solved_transmission, interval, angular_speed_unit, torque_unit, current_unit, figsize,
                      marker_size, padding, show):
        warnings.filterwarnings('ignore', category = UserWarning)

        def call_animation(torque_speed_curve, torque_current_curve):
            animation = dc_motor_characteristics_animation(motor = solved_transmission.chain[0],
                                                           time = solved_transmission.time, interval = interval,
                                                           torque_speed_curve = torque_speed_curve,
                                                           torque_current_curve = torque_current_curve,
                                                           angular_speed_unit = angular_speed_unit,
                                                           torque_unit = torque_unit, current_unit = current_unit,
                                                           figsize = figsize, marker_size = marker_size,
                                                           padding = padding, show = show)

            assert isinstance(animation, FuncAnimation)
            animation_file_name = 'animation.gif'
            animation.save(animation_file_name)
            plt.close()
            if os.path.exists(animation_file_name):
                os.remove(animation_file_name)

        if solved_transmission.chain[0].electric_current_is_computable:
            call_animation(torque_speed_curve = True, torque_current_curve = True)
            call_animation(torque_speed_curve = False, torque_current_curve = True)
            call_animation(torque_speed_curve = True, torque_current_curve = True)
        else:
            call_animation(torque_speed_curve = True, torque_current_curve = False)


    @mark.error
    def test_raises_type_error(self, dc_motor_characteristics_animation_type_error):
        with raises(TypeError):
            dc_motor_characteristics_animation(**dc_motor_characteristics_animation_type_error)


    @mark.error
    def test_raises_value_error(self, dc_motor_characteristics_animation_value_error):
        with raises(ValueError):
            dc_motor_characteristics_animation(**dc_motor_characteristics_animation_value_error)
