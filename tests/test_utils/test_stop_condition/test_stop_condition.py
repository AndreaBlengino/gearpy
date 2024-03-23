from gearpy.mechanical_objects import DCMotor
from gearpy.sensors import AbsoluteRotaryEncoder, Amperometer, SensorBase, Tachometer
from gearpy.units import AngularPosition, AngularSpeed, Current, InertiaMoment, Torque, UnitBase
from gearpy.utils import StopCondition
from gearpy.utils.stop_condition.operator_base import OperatorBase
from hypothesis import given, settings
from hypothesis.strategies import sampled_from, one_of
from pytest import mark, raises
from tests.conftest import basic_amperometer, basic_encoder, basic_tachometer
from tests.test_units.test_current.conftest import currents
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds


threshold_map = {basic_amperometer: Current(1, 'A'), basic_encoder: AngularPosition(1, 'rot'),
                 basic_tachometer: AngularSpeed(100, 'rad/s')}


@mark.utils
class TestStopConditionInit:


    @mark.genuine
    @given(sensor = sampled_from(elements = [basic_amperometer, basic_encoder, basic_tachometer]),
           operator = sampled_from(elements = [StopCondition.greater_than, StopCondition.greater_than_or_equal_to,
                                               StopCondition.equal_to, StopCondition.less_than,
                                               StopCondition.less_than_or_equal_to]))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, sensor, operator):
        threshold = threshold_map[sensor]
        condition = StopCondition(sensor = sensor, threshold = threshold, operator = operator)

        assert isinstance(condition.sensor, SensorBase)
        assert condition.sensor == sensor
        assert isinstance(condition.threshold, UnitBase)
        assert condition.threshold == threshold
        assert isinstance(condition.operator, OperatorBase)
        assert condition.operator == operator


    @mark.error
    def test_raises_type_error(self, stop_condition_init_type_error):
        with raises(TypeError):
            StopCondition(**stop_condition_init_type_error)


@mark.utils
class TestStopConditionCheckCondition:

    @mark.genuine
    @given(threshold = one_of(angular_positions(), angular_speeds(), currents()),
           operator = sampled_from(elements = [StopCondition.greater_than, StopCondition.greater_than_or_equal_to,
                                               StopCondition.equal_to, StopCondition.less_than,
                                               StopCondition.less_than_or_equal_to]))
    @settings(max_examples = 100, deadline = None)
    def test_method(self, threshold, operator):
        motor = DCMotor(name = 'motor', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(10, 'Nm'),
                        no_load_electric_current = Current(0, 'A'), maximum_electric_current = Current(5, 'A'))

        if isinstance(threshold, AngularPosition):
            motor.angular_position = AngularPosition(1, 'rot')
            sensor = AbsoluteRotaryEncoder(target = motor)
        elif isinstance(threshold, AngularSpeed):
            motor.angular_speed = AngularSpeed(10, 'rad/s')
            sensor = Tachometer(target = motor)
        elif isinstance(threshold, Current):
            motor.electric_current = Current(1, 'A')
            sensor = Amperometer(target = motor)

        condition = StopCondition(sensor = sensor, threshold = threshold, operator = operator)
        condition_is_valid = condition.check_condition()

        if operator == StopCondition.greater_than:
            assert condition_is_valid == (sensor.get_value() > threshold)
        elif operator == StopCondition.greater_than_or_equal_to:
            assert condition_is_valid == (sensor.get_value() >= threshold)
        elif operator == StopCondition.equal_to:
            assert condition_is_valid == (sensor.get_value() == threshold)
        elif operator == StopCondition.less_than:
            assert condition_is_valid == (sensor.get_value() < threshold)
        elif operator == StopCondition.less_than_or_equal_to:
            assert condition_is_valid == (sensor.get_value() <= threshold)

    @mark.error
    def test_raises_type_error(self, stop_condition_check_condition_type_error):
        for operator in [StopCondition.greater_than, StopCondition.greater_than_or_equal_to, StopCondition.equal_to,
                         StopCondition.less_than, StopCondition.less_than_or_equal_to]:
            with raises(TypeError):
                operator(**stop_condition_check_condition_type_error)
