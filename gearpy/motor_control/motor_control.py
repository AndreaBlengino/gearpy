from gearpy.mechanical_object import SpurGear
from gearpy.transmission import Transmission
from gearpy.units import AngularPosition
from .motor_control_base import MotorControlBase
from typing import Callable, Any, Union


class PWMControl(MotorControlBase):

    def __init__(self, transmission: Transmission):
        super().__init__(transmission = transmission)

    @property
    def transmission(self) -> Transmission:
        return super().transmission

    @property
    def rules(self) -> list:
        return super().rules

    def add_rule(self, rule: Callable[Any, Union[float, int]]):
        super().add_rule(rule = rule)

    def apply_rules(self):

        pwm_values = [rule() for rule in super().rules]
        applied_rules = sum([pwm_value is not None for pwm_value in pwm_values])
        if applied_rules >= 2:
            raise ValueError("At least two rules are simultaneously applicable. Check PWM rules conditions.")
        elif applied_rules == 1:
            pwm = [self.saturate_pwm(pwm_value) for pwm_value in pwm_values if pwm_value is not None][0]
        else:
            pwm = 1

        self.transmission.chain[0].pwm = pwm

    def compute_static_error(self, braking_angle: AngularPosition):
        if not isinstance(braking_angle, AngularPosition):
            raise TypeError(f"Parameter 'braking_angle' must be an instance of {AngularPosition.__name__!r}.")

        maximum_torque = self.transmission.chain[0].maximum_torque
        load_torque = self.transmission.chain[0].load_torque

        transmission_efficiency = 1
        for element in self.transmission.chain:
            if isinstance(element, SpurGear):
                transmission_efficiency *= element.master_gear_efficiency

        if load_torque is not None:
            static_error = ((load_torque/maximum_torque)/transmission_efficiency)*braking_angle
        else:
            static_error = AngularPosition(0, 'rad')

        return static_error

    def compute_pwm_min(self):
        maximum_torque = self.transmission.chain[0].maximum_torque
        if self.transmission.chain[0].time_variables['load torque']:
            load_torque = self.transmission.chain[0].time_variables['load torque'][0]
        else:
            load_torque = self.transmission.chain[0].load_torque
        no_load_electric_current = self.transmission.chain[0].no_load_electric_current
        maximum_electric_current = self.transmission.chain[0].maximum_electric_current

        transmission_efficiency = 1
        for element in self.transmission.chain:
            if isinstance(element, SpurGear):
                transmission_efficiency *= element.master_gear_efficiency

        return 1/transmission_efficiency*(load_torque/maximum_torque)*\
               ((maximum_electric_current - no_load_electric_current)/maximum_electric_current) + \
               no_load_electric_current/maximum_electric_current

    @staticmethod
    def saturate_pwm(pwm):
        return min(max(pwm, -1), 1)
