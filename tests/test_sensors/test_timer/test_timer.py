from gearpy.sensors import Timer
from gearpy.units import Time, TimeInterval
from hypothesis import given, settings
from pytest import mark, raises
from tests.conftest import basic_timer
from tests.test_units.test_time.conftest import times
from tests.test_units.test_time_interval.conftest import time_intervals


@mark.sensors
class TestTimerInit:


    @mark.genuine
    @given(starting_time = times(),
           duration = time_intervals())
    @settings(max_examples = 100)
    def test_method(self, starting_time, duration):
        timer = Timer(start_time = starting_time, duration = duration)

        assert isinstance(timer, Timer)


    @mark.error
    def test_raises_type_error(self, timer_init_type_error):
        with raises(TypeError):
            Timer(**timer_init_type_error)


@mark.sensors
class TestTimerStartTime:


    @mark.genuine
    @given(start_time = times())
    @settings(max_examples = 100)
    def test_property(self, start_time):
        timer = Timer(start_time = start_time, duration = TimeInterval(5, 'sec'))

        assert timer.start_time == start_time


@mark.sensors
class TestTimerDuration:


    @mark.genuine
    @given(duration = time_intervals())
    @settings(max_examples = 100)
    def test_property(self, duration):
        timer = Timer(start_time = Time(0, 'sec'), duration = duration)

        assert timer.duration == duration


@mark.sensors
class TestTimerIsActive:


    @mark.genuine
    @given(starting_time = times(),
           duration = time_intervals(),
           current_time = times())
    @settings(max_examples = 100)
    def test_method(self, starting_time, duration, current_time):
        timer = Timer(start_time = starting_time, duration = duration)
        is_active = timer.is_active(current_time = current_time)

        if (current_time >= starting_time) and ((current_time - starting_time) <= duration):
            assert is_active is True
        else:
            assert is_active is False


    @mark.error
    def test_raises_type_error(self, timer_is_active_type_error):
        with raises(TypeError):
            basic_timer.is_active(*timer_is_active_type_error)
