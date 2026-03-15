from gearpy.motor_control.utils import SCurveTrajectory
from gearpy.units import (
    AngularPosition,
    AngularSpeed,
    AngularAcceleration,
    Time
)
from hypothesis import given, settings
from hypothesis.strategies import booleans
from pytest import mark, raises
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_units.test_angular_acceleration.conftest import \
    angular_accelerations
from tests.test_units.test_time.conftest import times


class TestSCurveTrajectoryInit:

    @mark.genuine
    @given(
        start_position=angular_positions(),
        position_variation=angular_positions(min_value=1),
        velocity_variation=angular_speeds(min_value=1),
        maximum_acceleration=angular_accelerations(min_value=1),
        maximum_deceleration=angular_accelerations(min_value=1),
        start_velocity=angular_speeds(),
        stop_velocity=angular_speeds(),
        start_time=times(),
        backward_motion=booleans()
    )
    @settings(max_examples=100, deadline=None)
    def test_method(
        self,
        start_position,
        position_variation,
        velocity_variation,
        maximum_acceleration,
        maximum_deceleration,
        start_velocity,
        stop_velocity,
        start_time,
        backward_motion
    ):
        if not backward_motion:
            stop_position = start_position + position_variation
        else:
            stop_position = start_position - position_variation

        maximum_velocity = max(
            max(start_velocity, stop_velocity) + velocity_variation,
            AngularSpeed(1, 'rad/s')
        )

        trajectory = SCurveTrajectory(
            start_position=start_position,
            stop_position=stop_position,
            maximum_velocity=maximum_velocity,
            maximum_acceleration=maximum_acceleration,
            maximum_deceleration=maximum_deceleration,
            start_velocity=start_velocity,
            stop_velocity=stop_velocity,
            start_time=start_time
        )

        assert trajectory._SCurveTrajectory__start_position == start_position
        assert (
            trajectory._SCurveTrajectory__stop_position -
            (start_position + position_variation)
        ).to('rad').value <= 1e-10
        assert trajectory._SCurveTrajectory__maximum_velocity <= \
            maximum_velocity
        assert trajectory._SCurveTrajectory__maximum_acceleration <= \
            maximum_acceleration
        assert trajectory._SCurveTrajectory__maximum_deceleration <= \
            maximum_deceleration
        if not backward_motion:
            assert trajectory._SCurveTrajectory__start_velocity == \
                start_velocity
            assert trajectory._SCurveTrajectory__stop_velocity == stop_velocity
        else:
            assert trajectory._SCurveTrajectory__start_velocity == \
                -start_velocity
            assert trajectory._SCurveTrajectory__stop_velocity == \
                -stop_velocity
        assert trajectory._SCurveTrajectory__start_time == start_time

    @mark.error
    def test_raises_type_error(self, s_curve_trajectory_init_type_error):
        with raises(TypeError):
            SCurveTrajectory(**s_curve_trajectory_init_type_error)

    @mark.error
    def test_raises_value_error(self, s_curve_trajectory_init_value_error):
        with raises(ValueError):
            SCurveTrajectory(**s_curve_trajectory_init_value_error)


class TestSCurveTrajectoryCompute:

    @mark.genuine
    @given(
        start_position=angular_positions(),
        position_variation=angular_positions(min_value=1),
        velocity_variation=angular_speeds(min_value=1),
        maximum_acceleration=angular_accelerations(min_value=1),
        maximum_deceleration=angular_accelerations(min_value=1),
        start_velocity=angular_speeds(min_value=1),
        stop_velocity=angular_speeds(min_value=1),
        start_time=times(),
        backward_motion=booleans(),
        negative_start_velocity=booleans(),
        negative_stop_velocity=booleans()
    )
    @settings(max_examples=100, deadline=None)
    def test_method(
        self,
        start_position,
        position_variation,
        velocity_variation,
        maximum_acceleration,
        maximum_deceleration,
        start_velocity,
        stop_velocity,
        start_time,
        backward_motion,
        negative_start_velocity,
        negative_stop_velocity
    ):
        if negative_start_velocity:
            start_velocity = -start_velocity
        if negative_stop_velocity:
            stop_velocity = -stop_velocity

        if not backward_motion:
            stop_position = start_position + position_variation
        else:
            stop_position = start_position - position_variation

        maximum_velocity = max(
            max(start_velocity, stop_velocity) + velocity_variation,
            AngularSpeed(1, 'rad/s')
        )

        trajectory = SCurveTrajectory(
            start_position=start_position,
            stop_position=stop_position,
            maximum_velocity=maximum_velocity,
            maximum_acceleration=maximum_acceleration,
            maximum_deceleration=maximum_deceleration,
            start_velocity=start_velocity,
            stop_velocity=stop_velocity,
            start_time=start_time
        )

        time_before_start = start_time - Time(1, 'sec')
        position_before_start = trajectory.compute(time_before_start)
        assert isinstance(position_before_start, AngularPosition)
        if start_velocity.value > 0:
            assert position_before_start < start_position
        elif start_velocity.value < 0:
            assert position_before_start > start_position
        else:
            assert position_before_start == start_position

        time_before_uniform = start_time + \
            0.99*trajectory._SCurveTrajectory__acceleration_time
        position_before_uniform = trajectory.compute(time_before_uniform)
        assert isinstance(position_before_uniform, AngularPosition)

        time_before_deceleration = start_time + \
            trajectory._SCurveTrajectory__acceleration_time + \
            0.99*trajectory._SCurveTrajectory__uniform_time
        position_before_deceleration = trajectory.compute(time_before_deceleration)
        assert isinstance(position_before_deceleration, AngularPosition)

        time_before_stop = start_time + \
            trajectory._SCurveTrajectory__acceleration_time + \
            trajectory._SCurveTrajectory__uniform_time + \
            0.99*trajectory._SCurveTrajectory__deceleration_time
        position_before_stop = trajectory.compute(time_before_stop)
        assert isinstance(position_before_stop, AngularPosition)
            
        time_after_stop = start_time + \
            trajectory._SCurveTrajectory__acceleration_time + \
            trajectory._SCurveTrajectory__uniform_time + \
            trajectory._SCurveTrajectory__deceleration_time + \
            Time(1, 'sec')
        position_after_stop = trajectory.compute(time_after_stop)
        assert isinstance(position_after_stop, AngularPosition)
        if stop_velocity.value > 0:
            assert position_after_stop > stop_position
        elif stop_velocity.value < 0:
            assert position_after_stop < stop_position
        else:
            assert position_after_stop == stop_position

    @mark.error
    def test_raises_type_error(self, s_curve_trajectory_compute_type_error):
        s = SCurveTrajectory(
            start_position=AngularPosition(1, 'rad'),
            stop_position=AngularPosition(2, 'rad'),
            maximum_velocity=AngularSpeed(2, 'rad/s'),
            maximum_acceleration=AngularAcceleration(1, 'rad/s^2'),
            maximum_deceleration=AngularAcceleration(1, 'rad/s^2'),
        )
        with raises(TypeError):
            s.compute(s_curve_trajectory_compute_type_error)
