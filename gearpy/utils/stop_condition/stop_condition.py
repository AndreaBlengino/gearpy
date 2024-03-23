from .operator_base import OperatorBase
from .operator import GreaterThan, GreaterThanOrEqualTo, EqualTo, LessThan, LessThanOrEqualTo
from gearpy.sensors import SensorBase
from gearpy.units import UnitBase


class StopCondition:
    """``gearpy.utils.stop_condition.stop_condition.StopCondition`` object.

    Attributes
    ----------
    :py:attr:`sensor` : SensorBase
        The sensor to be monitored to check if the stop condition is valid.
    :py:attr:`threshold` : UnitBase
        The threshold value that triggers the stop condition.
    :py:attr:`operator` : OperatorBase
        The comparison operator to use to check if the stop condition is valid.

    Methods
    -------
    :py:meth:`check_condition`
        Applies the comparison ``operator`` to the ``sensor`` value and the ``threshold`` value to check if the stop
        condition is valid.
    """

    greater_than = GreaterThan()
    greater_than_or_equal_to = GreaterThanOrEqualTo()
    equal_to = EqualTo()
    less_than = LessThan()
    less_than_or_equal_to = LessThanOrEqualTo()

    def __init__(self, sensor: SensorBase, threshold: UnitBase, operator: OperatorBase):
        if not isinstance(sensor, SensorBase):
            raise TypeError(f"Parameter 'sensor' must be an instance of {SensorBase.__name__!r}.")

        if not isinstance(threshold, UnitBase):
            raise TypeError(f"Parameter 'threshold' must be an instance of {UnitBase.__name__!r}.")

        if not isinstance(operator, OperatorBase):
            raise TypeError(f"Parameter 'operator' must be an instance of {OperatorBase.__name__!r}.")

        self.__sensor = sensor
        self.__threshold = threshold
        self.__operator = operator

    @property
    def sensor(self) -> SensorBase:
        """The sensor to be monitored to check if the stop condition is valid.

        Returns
        -------
        SensorBase
            The sensor to be monitored to check if the stop condition is valid.

        Raises
        ------
        TypeError
            If ``sensor`` is not an instance of ``SensorBase``'s concrete class.

        See Also
        --------
        :py:class:`gearpy.sensors.absolute_rotary_encoder.AbsoluteRotaryEncoder`
        :py:class:`gearpy.sensors.amperometer.Amperometer`
        :py:class:`gearpy.sensors.tachometer.Tachometer`
        """
        return self.__sensor

    @property
    def threshold(self) -> UnitBase:
        """The threshold value that triggers the stop condition.

        Raises
        ------
        TypeError
            If ``threshold`` is not an instance of ``UnitBase``'s concrete class.

        Returns
        -------
        UnitBase
            The threshold value that triggers the stop condition.
        """
        return self.__threshold

    @property
    def operator(self) -> OperatorBase:
        """The comparison operator to use to check if the stop condition is valid. \n
        The available operators are:

        - ``StopCondition.greater_than`` to check if the :py:attr:`sensor` value is greater than the
          :py:attr:`threshold` value,
        - ``StopCondition.greater_than_or_equal_to`` to check if the :py:attr:`sensor` value is greater than or equal to
          the :py:attr:`threshold` value,
        - ``StopCondition.equal_to`` to check if the :py:attr:`sensor` value is equal to the :py:attr:`threshold` value,
        - ``StopCondition.less_than`` to check if the :py:attr:`sensor` value is less than the :py:attr:`threshold`
          value,
        - ``StopCondition.less_than_or_equal_to`` to check if the :py:attr:`sensor` value is less than or equal to the
          :py:attr:`threshold` value.

        Raises
        ------
        TypeError
            If ``operator`` is not an instance of ``OperatorBase``'s concrete class.

        Returns
        -------
        OperatorBase
            The comparison operator to use to check if the stop condition is valid.
        """
        return self.__operator

    def check_condition(self) -> bool:
        """Applies the comparison :py:attr:`operator` to the :py:attr:`sensor` value and the :py:attr:`threshold` value
        to check if the stop condition is valid. \n
        If the stop condition is valid, then the ``Solver`` stops the computation even if it is not completed to the
        final simulation time.

        Returns
        -------
        bool
            Whether stop condition is valid.
        """
        return self.operator(self.sensor.get_value(), self.threshold)
