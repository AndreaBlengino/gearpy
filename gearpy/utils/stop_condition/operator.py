from .operator_base import OperatorBase
from gearpy.units import UnitBase


class GreaterThan(OperatorBase):
    """:py:class:`GreaterThan <gearpy.utils.stop_condition.operator.GreaterThan>`
    object.

    It compares a ``sensor_value`` to a ``threshold`` and returns ``True`` is
    the former is greater than the latter, ``False`` otherwise.
    """

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value=sensor_value, threshold=threshold)
        return sensor_value > threshold


class GreaterThanOrEqualTo(OperatorBase):
    """:py:class:`GreaterThanOrEqualTo <gearpy.utils.stop_condition.operator.GreaterThanOrEqualTo>`
    object.

    It compares a ``sensor_value`` to a ``threshold`` and returns ``True`` is
    the former is greater than or equal to the latter, ``False`` otherwise.
    """

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value=sensor_value, threshold=threshold)
        return sensor_value >= threshold


class EqualTo(OperatorBase):
    """:py:class:`EqualTo <gearpy.utils.stop_condition.operator.EqualTo>` object.

    It compares a ``sensor_value`` to a ``threshold`` and returns ``True`` is
    the former is equal to the latter, ``False`` otherwise.
    """

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value=sensor_value, threshold=threshold)
        return sensor_value == threshold


class LessThan(OperatorBase):
    """:py:class:`LessThan <gearpy.utils.stop_condition.operator.LessThan>`
    object.

    It compares a ``sensor_value`` to a ``threshold`` and returns ``True`` is
    the former is less than the latter, ``False`` otherwise.
    """

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value=sensor_value, threshold=threshold)
        return sensor_value < threshold


class LessThanOrEqualTo(OperatorBase):
    """:py:class:`LessThanOrEqualTo <gearpy.utils.stop_condition.operator.LessThanOrEqualTo>`
    object.

    It compares a ``sensor_value`` to a ``threshold`` and returns ``True`` is
    the former is less than or equal to the latter, ``False`` otherwise.
    """

    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        super().__call__(sensor_value=sensor_value, threshold=threshold)
        return sensor_value <= threshold
