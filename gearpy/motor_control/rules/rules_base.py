from abc import ABC, abstractmethod


class RuleBase(ABC):
    """:py:class:`RuleBase <gearpy.motor_control.rules.rules_base.RuleBase>`
    object. \n
    Abstract base class for creating rules objects.

    .. admonition:: See Also
       :class: seealso

       :py:class:`ConstantPWM <gearpy.motor_control.rules.constant_pwm.ConstantPWM>` \n
       :py:class:`ReachAngularPosition <gearpy.motor_control.rules.reach_angular_position.ReachAngularPosition>` \n
       :py:class:`StartLimitCurrent <gearpy.motor_control.rules.start_limit_current.StartLimitCurrent>` \n
       :py:class:`StartProportionalToAngularPosition <gearpy.motor_control.rules.start_proportional_to_angular_position.StartProportionalToAngularPosition>`
    """

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def apply(self): ...
