from .operator_base import OperatorBase
from .operator import (
    GreaterThan,
    GreaterThanOrEqualTo,
    EqualTo,
    LessThan,
    LessThanOrEqualTo
)
from gearpy.sensors import SensorBase
from gearpy.units import UnitBase


class StopCondition:
    """:py:class:`StopCondition <gearpy.utils.stop_condition.stop_condition.StopCondition>`
    object.

    Attributes
    ----------
    :py:attr:`sensor` : :py:class:`SensorBase <gearpy.sensors.sensor_base.SensorBase>`
        The sensor to be monitored to check if the stop condition is valid.
    :py:attr:`threshold` : :py:class:`UnitBase <gearpy.units.unit_base.UnitBase>`
        The threshold value that triggers the stop condition.
    :py:attr:`operator` : :py:class:`OperatorBase <gearpy.utils.stop_condition.operator_base.OperatorBase>`
        The comparison operator to use to check if the stop condition is valid.

    Methods
    -------
    :py:meth:`check_condition`
        It applies the comparison :py:attr:`operator` to the :py:attr:`sensor` value and the :py:attr:`threshold` value
        to check if the stop condition is valid.
    """

    greater_than = GreaterThan()
    greater_than_or_equal_to = GreaterThanOrEqualTo()
    equal_to = EqualTo()
    less_than = LessThan()
    less_than_or_equal_to = LessThanOrEqualTo()

    def __init__(
        self,
        sensor: SensorBase,
        threshold: UnitBase,
        operator: OperatorBase
    ):
        if not isinstance(sensor, SensorBase):
            raise TypeError(
                f"Parameter 'sensor' must be an instance of "
                f"{SensorBase.__name__!r}."
            )

        if not isinstance(threshold, UnitBase):
            raise TypeError(
                f"Parameter 'threshold' must be an instance of "
                f"{UnitBase.__name__!r}."
            )

        if not isinstance(operator, OperatorBase):
            raise TypeError(
                f"Parameter 'operator' must be an instance of "
                f"{OperatorBase.__name__!r}."
            )

        self.__sensor = sensor
        self.__threshold = threshold
        self.__operator = operator

    @property
    def sensor(self) -> SensorBase:
        """The sensor to be monitored to check if the stop condition is valid.

        Returns
        -------
        :py:class:`SensorBase <gearpy.sensors.sensor_base.SensorBase>`
            The sensor to be monitored to check if the stop condition is valid.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`sensor` is not an instance of
               :py:class:`SensorBase <gearpy.sensors.sensor_base.SensorBase>`.

        .. admonition:: See Also
           :class: seealso

           :py:class:`AbsoluteRotaryEncoder <gearpy.sensors.absolute_rotary_encoder.AbsoluteRotaryEncoder>` \n
           :py:class:`Amperometer <gearpy.sensors.amperometer.Amperometer>` \n
           :py:class:`Tachometer <gearpy.sensors.tachometer.Tachometer>`
        """
        return self.__sensor

    @property
    def threshold(self) -> UnitBase:
        """The threshold value that triggers the stop condition.

        Returns
        -------
        :py:class:`UnitBase <gearpy.units.unit_base.UnitBase>`
            The threshold value that triggers the stop condition.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`threshold` is not an instance of
               :py:class:`UnitBase <gearpy.units.unit_base.UnitBase>`.
        """
        return self.__threshold

    @property
    def operator(self) -> OperatorBase:
        """The comparison operator to use to check if the stop condition is
        valid. \n
        The available operators are:

        - :py:class:`StopCondition.greater_than <gearpy.utils.stop_condition.operator.GreaterThan>`
          to check if the :py:attr:`sensor` value is greater than the
          :py:attr:`threshold` value,
        - :py:class:`StopCondition.greater_than_or_equal_to <gearpy.utils.stop_condition.operator.GreaterThanOrEqualTo>`
          to check if the :py:attr:`sensor` value is greater than or equal to
          the :py:attr:`threshold` value,
        - :py:class:`StopCondition.equal_to <gearpy.utils.stop_condition.operator.EqualTo>`
          to check if the :py:attr:`sensor` value is equal to the
          :py:attr:`threshold` value,
        - :py:class:`StopCondition.less_than <gearpy.utils.stop_condition.operator.LessThan>`
          to check if the :py:attr:`sensor` value is less than the
          :py:attr:`threshold` value,
        - :py:class:`StopCondition.less_than_or_equal_to <gearpy.utils.stop_condition.operator.LessThanOrEqualTo>`
          to check if the :py:attr:`sensor` value is less than or equal to the
          :py:attr:`threshold` value.

        Returns
        -------
        :py:class:`OperatorBase <gearpy.utils.stop_condition.operator_base.OperatorBase>`
            The comparison operator to use to check if the stop condition is
            valid.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`operator` is not an instance of
               :py:class:`OperatorBase <gearpy.utils.stop_condition.operator_base.OperatorBase>`.
        """
        return self.__operator

    def check_condition(self) -> bool:
        """It applies the comparison :py:attr:`operator` to the
        :py:attr:`sensor` value and the :py:attr:`threshold` value to check if
        the stop condition is valid. \n
        If the stop condition is valid, then the
        :py:class:`Solver <gearpy.solver.Solver>` stops the computation even if
        it is not completed to the final simulation time.

        Returns
        -------
        :py:class:`bool`
            Whether stop condition is valid.
        """
        return self.operator(
            sensor_value=self.sensor.get_value(),
            threshold=self.threshold
        )
