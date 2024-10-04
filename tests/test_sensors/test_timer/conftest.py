from gearpy.units import Time, TimeInterval
from gearpy.sensors import Timer
from hypothesis.strategies import composite
from pytest import fixture
from tests.conftest import types_to_check
from tests.test_units.test_time.conftest import times
from tests.test_units.test_time_interval.conftest import time_intervals


@composite
def timers(draw):
    start_time = draw(times())
    duration = draw(time_intervals())

    return Timer(start_time=start_time, duration=duration)


timer_init_type_error_1 = [
    {'start_time': type_to_check, 'duration': TimeInterval(5, 'sec')}
    for type_to_check in types_to_check if not isinstance(type_to_check, Time)
]

timer_init_type_error_2 = [
    {'start_time': Time(0, 'sec'), 'duration': type_to_check}
    for type_to_check in types_to_check if not isinstance(type_to_check, Time)
    and not isinstance(type_to_check, TimeInterval)
]


@fixture(params=[*timer_init_type_error_1, *timer_init_type_error_2])
def timer_init_type_error(request):
    return request.param


@fixture(
    params=[
        type_to_check for type_to_check in types_to_check
        if not isinstance(type_to_check, Time)
    ]
)
def timer_is_active_type_error(request):
    return request.param
