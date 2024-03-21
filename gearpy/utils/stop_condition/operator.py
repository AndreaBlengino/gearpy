from .operator_base import OperatorBase
from gearpy.units import UnitBase


class GreaterThan(OperatorBase):

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value = sensor_value, threshold = threshold)
        return sensor_value > threshold


class GreaterThanOrEqualTo(OperatorBase):

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value = sensor_value, threshold = threshold)
        return sensor_value >= threshold


class EqualTo(OperatorBase):

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value = sensor_value, threshold = threshold)
        return sensor_value == threshold


class LessThan(OperatorBase):

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value = sensor_value, threshold = threshold)
        return sensor_value < threshold


class LessThanOrEqualTo(OperatorBase):

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value = sensor_value, threshold = threshold)
        return sensor_value <= threshold
