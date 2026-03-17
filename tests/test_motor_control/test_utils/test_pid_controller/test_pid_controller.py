from gearpy.motor_control.utils import PIDController
from hypothesis import given, settings
from hypothesis.strategies import booleans, floats
from pytest import mark, raises
from tests.test_units.test_time_interval.conftest import time_intervals


@mark.motor_control
class TestPIDControllerInit:

    @mark.genuine
    @given(
        Kp=floats(allow_nan=False, allow_infinity=False),
        Ki=floats(allow_nan=False, allow_infinity=False),
        Kd=floats(allow_nan=False, allow_infinity=False),
        clamping=booleans(),
        reference_min=floats(
            min_value=-1000,
            max_value=1000,
            allow_nan=False,
            allow_infinity=False
        ),
        reference_range=floats(
            min_value=1,
            max_value=1000,
            allow_nan=False,
            allow_infinity=False
        ),
    )
    @settings(max_examples=100, deadline=None)
    def test_method(
        self,
        Kp,
        Ki,
        Kd,
        clamping,
        reference_min,
        reference_range
    ):
        pid = PIDController(
            Kp=Kp,
            Ki=Ki,
            Kd=Kd,
            clamping=clamping,
            reference_min=reference_min,
            reference_max=reference_min + reference_range
        )

        assert pid._PIDController__Kp == Kp
        assert pid._PIDController__Ki == Ki
        assert pid._PIDController__Kd == Kd
        assert pid._PIDController__clamping == clamping
        assert pid._PIDController__reference_min == reference_min
        assert pid._PIDController__reference_max == \
            reference_min + reference_range
        assert pid._PIDController__cumulative_error == 0
        assert pid._PIDController__previous_error == 0

    @mark.error
    def test_raises_type_error(self, pid_controller_init_type_error):
        with raises(TypeError):
            PIDController(**pid_controller_init_type_error)

    @mark.error
    def test_raises_value_error(self, pid_controller_init_value_error):
        with raises(ValueError):
            PIDController(**pid_controller_init_value_error)


@mark.motor_control
class TestPIDControllerCompute:

    @mark.genuine
    @given(
        Kp=floats(allow_nan=False, allow_infinity=False),
        Ki=floats(allow_nan=False, allow_infinity=False),
        Kd=floats(allow_nan=False, allow_infinity=False),
        clamping=booleans(),
        reference_min=floats(
            min_value=-1000,
            max_value=1000,
            allow_nan=False,
            allow_infinity=False
        ),
        reference_range=floats(
            min_value=1,
            max_value=1000,
            allow_nan=False,
            allow_infinity=False
        ),
        error=floats(allow_nan=False, allow_infinity=False),
        time_step=time_intervals()
    )
    @settings(max_examples=100, deadline=None)
    def test_method(
        self,
        Kp,
        Ki,
        Kd,
        clamping,
        reference_min,
        reference_range,
        error,
        time_step
    ):
        pid = PIDController(
            Kp=Kp,
            Ki=Ki,
            Kd=Kd,
            clamping=clamping,
            reference_min=reference_min,
            reference_max=reference_min + reference_range
        )

        reference = pid.compute(error=error, time_step=time_step)

        assert isinstance(reference, float | int)
        assert pid._PIDController__previous_error == error

    @mark.error
    def test_raises_type_error(self, pid_controller_compute_type_error):
        pid = PIDController(Kp=1, Ki=1, Kd=1)
        with raises(TypeError):
            pid.compute(**pid_controller_compute_type_error)


@mark.motor_control
class TestPIDControllerReset:

    @mark.genuine
    @given(
        Kp=floats(allow_nan=False, allow_infinity=False),
        Ki=floats(allow_nan=False, allow_infinity=False),
        Kd=floats(allow_nan=False, allow_infinity=False),
        clamping=booleans(),
        reference_min=floats(
            min_value=-1000,
            max_value=1000,
            allow_nan=False,
            allow_infinity=False
        ),
        reference_range=floats(
            min_value=1,
            max_value=1000,
            allow_nan=False,
            allow_infinity=False
        ),
        error=floats(allow_nan=False, allow_infinity=False),
        time_step=time_intervals()
    )
    @settings(max_examples=100, deadline=None)
    def test_method(
        self,
        Kp,
        Ki,
        Kd,
        clamping,
        reference_min,
        reference_range,
        error,
        time_step
    ):
        pid = PIDController(
            Kp=Kp,
            Ki=Ki,
            Kd=Kd,
            clamping=clamping,
            reference_min=reference_min,
            reference_max=reference_min + reference_range
        )

        pid.compute(error=error, time_step=time_step)

        assert pid._PIDController__previous_error == error

        pid.reset()

        assert pid._PIDController__previous_error == 0
        assert pid._PIDController__cumulative_error == 0
