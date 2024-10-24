from abc import ABC, abstractmethod
from gearpy.mechanical_objects import MotorBase, RotatingObject
from gearpy.powertrain import Powertrain
from gearpy.motor_control.rules.rules_base import RuleBase


class MotorControlBase(ABC):
    """:py:class:`MotorControlBase <gearpy.motor_control.motor_control_base.MotorControlBase>`
    object. \n
    Abstract base class for creating motor control objects.

    .. admonition:: See Also
       :class: seealso

       :py:class:`PWMControl <gearpy.motor_control.pwm_control.PWMControl>`
    """

    @abstractmethod
    def __init__(self, powertrain: Powertrain):
        if not isinstance(powertrain, Powertrain):
            raise TypeError(
                f"Parameter 'powertrain' must be an instance of "
                f"{Powertrain.__name__!r}."
            )

        if not powertrain.elements:
            raise ValueError(
                "Parameter 'powertrain.elements' cannot be an empty tuple."
            )

        if not isinstance(powertrain.elements[0], MotorBase):
            raise TypeError(
                f"First element in 'powertrain' must be an instance of "
                f"{MotorBase.__name__!r}."
            )

        if not all(
            [isinstance(item, RotatingObject) for item in powertrain.elements]
        ):
            raise TypeError(
                f"All elements of 'powertrain' must be instances of "
                f"{RotatingObject.__name__!r}."
            )

    @property
    @abstractmethod
    def rules(self) -> list: ...

    @abstractmethod
    def add_rule(self, rule: RuleBase):
        if not isinstance(rule, RuleBase):
            raise TypeError(
                f"Parameter 'rule' must be an instance of "
                f"{RuleBase.__name__!r}."
            )

    @abstractmethod
    def apply_rules(self): ...
