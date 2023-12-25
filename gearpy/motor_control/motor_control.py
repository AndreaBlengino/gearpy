from gearpy.transmission import Transmission
from gearpy.units import Angle
from .motor_control_base import MotorControlBase
from .rules import _compute_static_error, _compute_pwm_min
from .rules_base import RuleBase


class PWMControl(MotorControlBase):

    def __init__(self, transmission: Transmission):
        super().__init__(transmission = transmission)

    @property
    def transmission(self) -> Transmission:
        return super().transmission

    @property
    def rules(self) -> list:
        return super().rules

    def add_rule(self, rule: RuleBase):
        super().add_rule(rule = rule)

    def apply_rules(self):

        pwm_values = [rule.apply() for rule in super().rules]
        applied_rules = sum([pwm_value is not None for pwm_value in pwm_values])
        if applied_rules >= 2:
            raise ValueError("At least two rules are simultaneously applicable. Check PWM rules conditions.")
        elif applied_rules == 1:
            pwm = [self.saturate_pwm(pwm_value) for pwm_value in pwm_values if pwm_value is not None][0]
        else:
            pwm = 1

        self.transmission.chain[0].pwm = pwm

    def compute_static_error(self, braking_angle: Angle):
        if not isinstance(braking_angle, Angle):
            raise TypeError(f"Parameter 'braking_angle' must be an instance of {Angle.__name__!r}.")

        return _compute_static_error(transmission = self.transmission, braking_angle = braking_angle)

    def compute_pwm_min(self):
        return _compute_pwm_min(transmission = self.transmission)

    @staticmethod
    def saturate_pwm(pwm):
        return min(max(pwm, -1), 1)
