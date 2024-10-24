from abc import ABC, abstractmethod
from gearpy.units import UnitBase


class OperatorBase(ABC):
    """:py:class:`OperatorBase <gearpy.utils.stop_condition.operator_base.OperatorBase>`
    object. \n
    Abstract base class for creating operator objects.

    .. admonition:: See Also
       :class: seealso

       :py:class:`GreaterThan <gearpy.utils.stop_condition.operator.GreaterThan>` \n
       :py:class:`GreaterThanOrEqualTo <gearpy.utils.stop_condition.operator.GreaterThanOrEqualTo>` \n
       :py:class:`EqualTo <gearpy.utils.stop_condition.operator.EqualTo>` \n
       :py:class:`LessThan <gearpy.utils.stop_condition.operator.LessThan>` \n
       :py:class:`LessThanOrEqualTo <gearpy.utils.stop_condition.operator.LessThanOrEqualTo>`
    """

    @abstractmethod
    def __call__(self, sensor_value: UnitBase, threshold: UnitBase) -> bool:
        if not isinstance(sensor_value, UnitBase):
            raise TypeError(
                f"Parameter 'sensor_value' must be an instance of "
                f"{UnitBase.__name__!r}."
            )

        if not isinstance(threshold, UnitBase):
            raise TypeError(
                f"Parameter 'threshold' must be an instance of "
                f"{UnitBase.__name__!r}."
            )
