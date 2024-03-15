from gearpy.mechanical_objects import MatingMaster, MatingSlave, WormGear, HelicalGear
from gearpy.units import AngularSpeed, Torque, Current, Angle, InertiaMoment
from gearpy.utils import add_gear_mating, add_worm_gear_mating, add_fixed_joint, dc_motor_characteristics_animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from hypothesis import given, settings
from hypothesis.strategies import floats, one_of, sampled_from, booleans, none, tuples
import os
from pytest import mark, raises
from tests.conftest import dc_motors, spur_gears, helical_gears, flywheels, worm_gears, worm_wheels
from tests.test_utils.conftest import motor_1, powertrain_1, motor_2, powertrain_2
import warnings


@mark.utils
class TestAddGearMating:


    @mark.genuine
    @given(gear_1 = spur_gears(),
           gear_2 = spur_gears(),
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
        with raises(ValueError):
            add_gear_mating(**add_gear_mating_value_error)


@mark.utils
class TestAddWormGearMating:


    @mark.genuine
    @given(worm_gear = worm_gears(pressure_angle = Angle(20, 'deg')),
           worm_wheel = worm_wheels(pressure_angle = Angle(20, 'deg')),
           friction_coefficient = floats(allow_nan = False, allow_infinity = False, min_value = 0,
                                         exclude_min = False, max_value = 1, exclude_max = False))
    @settings(max_examples = 100)
    def test_function(self, worm_gear, worm_wheel, friction_coefficient):
        for master, slave in zip([worm_gear, worm_wheel], [worm_wheel, worm_gear]):
            if isinstance(slave, WormGear):
                efficiency = (master.pressure_angle.cos() - friction_coefficient/master.helix_angle.tan())/ \
                             (master.pressure_angle.cos() + friction_coefficient*master.helix_angle.tan())
                if efficiency < 0:
                    return
            add_worm_gear_mating(master = master, slave = slave, friction_coefficient = friction_coefficient)

            assert master.drives == slave
            assert master.mating_role == MatingMaster
            assert slave.driven_by == master
            assert slave.mating_role == MatingSlave
            if isinstance(master, WormGear):
                assert slave.master_gear_ratio == worm_wheel.n_teeth/worm_gear.n_starts
                assert slave.master_gear_efficiency == (master.pressure_angle.cos() - friction_coefficient*master.helix_angle.tan())/ \
                                                       (master.pressure_angle.cos() + friction_coefficient/master.helix_angle.tan())
            else:
                assert slave.master_gear_ratio == worm_gear.n_starts/worm_wheel.n_teeth
                assert slave.master_gear_efficiency == (master.pressure_angle.cos() - friction_coefficient/master.helix_angle.tan())/ \
                                                       (master.pressure_angle.cos() + friction_coefficient*master.helix_angle.tan())
            assert worm_gear.self_locking == (friction_coefficient > worm_gear.pressure_angle.cos()*worm_gear.helix_angle.tan())


    @mark.error
    def test_raises_type_error(self, add_worm_gear_mating_type_error):
        with raises(TypeError):
            add_worm_gear_mating(**add_worm_gear_mating_type_error)


    @mark.error
    def test_raises_value_error(self, add_worm_gear_mating_value_error):
        with raises(ValueError):
            add_worm_gear_mating(**add_worm_gear_mating_value_error)


@mark.utils
class TestAddFixedJoint:


    @mark.genuine
    @given(master = one_of(dc_motors(), spur_gears(), helical_gears(), flywheels(), worm_gears(), worm_wheels()),
           slave = one_of(spur_gears(), helical_gears(), flywheels(), worm_gears(), worm_wheels()))
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


    @mark.error
    def test_raises_value_error(self):
        gear = HelicalGear(name = 'master', n_teeth = 10, helix_angle = Angle(20, 'deg'),
                           inertia_moment = InertiaMoment(1, 'kgm^2'))
        with raises(ValueError):
            add_fixed_joint(master = gear, slave = gear)


@mark.utils
class TestDCMotorCharacteristicsAnimation:


    @mark.genuine
    @given(interval = floats(allow_nan = False, allow_infinity = False, min_value = 10, max_value = 30),
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
    def test_function(self, interval, angular_speed_unit, torque_unit, current_unit, figsize, marker_size, padding, show):
        warnings.filterwarnings('ignore', category = UserWarning)

        def call_animation(motor, powertrain, torque_speed_curve, torque_current_curve):
            animation = dc_motor_characteristics_animation(motor = motor, time = powertrain.time, interval = interval,
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

        for motor, powertrain in zip([motor_1, motor_2], [powertrain_1, powertrain_2]):
            if motor.electric_current_is_computable:
                call_animation(motor = motor, powertrain = powertrain, torque_speed_curve = True, torque_current_curve = True)
                call_animation(motor = motor, powertrain = powertrain, torque_speed_curve = False, torque_current_curve = True)
            else:
                call_animation(motor = motor, powertrain = powertrain, torque_speed_curve = True, torque_current_curve = False)


    @mark.error
    def test_raises_type_error(self, dc_motor_characteristics_animation_type_error):
        with raises(TypeError):
            dc_motor_characteristics_animation(**dc_motor_characteristics_animation_type_error)


    @mark.error
    def test_raises_value_error(self, dc_motor_characteristics_animation_value_error):
        with raises(ValueError):
            dc_motor_characteristics_animation(**dc_motor_characteristics_animation_value_error)
