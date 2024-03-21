from .operator_base import OperatorBase
from .operator import HigherThan, HigherThanOrEqualTo, EqualTo, LessThan, LessThanOrEqualTo
from gearpy.sensors import SensorBase
from gearpy.units import UnitBase


class StopCondition:

    higher_than = HigherThan()
    higher_than_or_equal_to = HigherThanOrEqualTo()
    equal_to = EqualTo()
    less_than = LessThan()
    less_than_or_equal_to = LessThanOrEqualTo()

    def __init__(self, sensor: SensorBase, threshold: UnitBase, operator: OperatorBase):
        self.__sensor = sensor
        self.__threshold = threshold
        self.__operator = operator

    @property
    def sensor(self) -> SensorBase:
        return self.__sensor

    @property
    def threshold(self) -> UnitBase:
        return self.__threshold

    @property
    def operator(self) -> OperatorBase:
        return self.__operator

    def check_condition(self) -> bool:
        return self.operator(self.sensor.get_value(), self.threshold)
