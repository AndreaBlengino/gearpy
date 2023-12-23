from gearpy.mechanical_object import SpurGear, MotorBase, RotatingObject, DCMotor
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from gearpy.transmission import Transmission
from gearpy.units import AngularPosition, Angle, Current
import numpy as np
from .rules_base import RuleBase
from typing import Union, Optional


class ReachAngularPosition(RuleBase):

    def __init__(self,
                 encoder: AbsoluteRotaryEncoder,
                 transmission: Transmission,
                 target_angular_position: AngularPosition,
                 braking_angle: Angle):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(f"Parameter 'encoder' must be an instance of {AbsoluteRotaryEncoder.__name__!r}.")

        if not isinstance(transmission, Transmission):
            raise TypeError(f"Parameter 'transmission' must be an instance of {Transmission.__name__!r}.")

        if not transmission.chain:
            raise ValueError("Parameter 'transmission.chain' cannot be an empty tuple.")

        if not isinstance(transmission.chain[0], MotorBase):
            raise TypeError(f"First element in 'transmission' must be an instance of {MotorBase.__name__!r}.")

        if not all([isinstance(item, RotatingObject) for item in transmission.chain]):
            raise TypeError(f"All elements of 'transmission' must be instances of {RotatingObject.__name__!r}.")

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(f"Parameter 'target_angular_position' must be an instance of {AngularPosition.__name__!r}.")

        if not isinstance(braking_angle, Angle):
            raise TypeError(f"Parameter 'braking_angle' must be an instance of {Angle.__name__!r}.")

        self.encoder = encoder
        self.transmission = transmission
        self.target_angular_position = target_angular_position
        self.braking_angle = braking_angle

    def apply(self) -> Union[float, int]:
        angular_position = self.encoder.get_value()

        regime_angular_position_error = _compute_static_error(braking_angle = self.braking_angle,
                                                              transmission = self.transmission)
        braking_starting_angle = self.target_angular_position - self.braking_angle + regime_angular_position_error

        if angular_position >= braking_starting_angle:
            return 1 - (angular_position - braking_starting_angle)/self.braking_angle


class StartProportionalToAngularPosition(RuleBase):

    def __init__(self,
                 encoder: AbsoluteRotaryEncoder,
                 transmission: Transmission,
                 target_angular_position: AngularPosition,
                 pwm_min_multiplier: Union[float, int],
                 pwm_min: Optional[float] = None):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(f"Parameter 'encoder' must be an instance of {AbsoluteRotaryEncoder.__name__!r}.")

        if not isinstance(transmission, Transmission):
            raise TypeError(f"Parameter 'transmission' must be an instance of {Transmission.__name__!r}.")

        if not transmission.chain:
            raise ValueError("Parameter 'transmission.chain' cannot be an empty tuple.")

        if not isinstance(transmission.chain[0], MotorBase):
            raise TypeError(f"First element in 'transmission' must be an instance of {MotorBase.__name__!r}.")

        if not all([isinstance(item, RotatingObject) for item in transmission.chain]):
            raise TypeError(f"All elements of 'transmission' must be instances of {RotatingObject.__name__!r}.")

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(f"Parameter 'target_angular_position' must be an instance of {AngularPosition.__name__!r}.")

        if not isinstance(pwm_min_multiplier, float) and not isinstance(pwm_min_multiplier, int):
            raise TypeError(f"Parameter 'pwm_min_multiplier' must be a float or an integer.")

        if pwm_min_multiplier <= 1:
            raise TypeError(f"Parameter 'pwm_min_multiplier' must be greater than 1.")

        if pwm_min is not None:
            if not isinstance(pwm_min, float) and not isinstance(pwm_min, int):
                raise TypeError(f"Parameter 'pwm_min' must be a float or an integer.")

            if pwm_min <= 0:
                raise TypeError(f"Parameter 'pwm_min' must be positive.")

        self.encoder = encoder
        self.transmission = transmission
        self.target_angular_position = target_angular_position
        self.pwm_min_multiplier = pwm_min_multiplier
        self.pwm_min = pwm_min

    def apply(self) -> Union[float, int]:
        angular_position = self.encoder.get_value()

        computed_pwm_min = self.pwm_min_multiplier*_compute_pwm_min(transmission = self.transmission)
        if computed_pwm_min != 0:
            pwm_min = computed_pwm_min
        else:
            if self.pwm_min is None:
                raise ValueError("Missing 'pwm_min' parameter.")
            pwm_min = self.pwm_min

        if angular_position <= self.target_angular_position:
            return (1 - pwm_min)*angular_position/self.target_angular_position + pwm_min


class StartLimitCurrent(RuleBase):

    def __init__(self,
                 encoder: AbsoluteRotaryEncoder,
                 tachometer: Tachometer,
                 motor: DCMotor,
                 target_angular_position: AngularPosition,
                 limit_electric_current: Current):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(f"Parameter 'encoder' must be an instance of {AbsoluteRotaryEncoder.__name__!r}.")

        if not isinstance(tachometer, Tachometer):
            raise TypeError(f"Parameter 'tachometer' must be an instance of {Tachometer.__name__!r}.")

        if not isinstance(motor, DCMotor):
            raise TypeError(f"Parameter 'motor' must be an instance of {DCMotor.__name__!r}.")

        if not motor.electric_current_is_computable:
            raise ValueError("Parameter 'motor' cannot compute 'electric_current' property.")

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(f"Parameter 'target_angular_position' must be an instance of {AngularPosition.__name__!r}.")

        if not isinstance(limit_electric_current, Current):
            raise TypeError(f"Parameter 'limit_electric_current' must be an instance of {Current.__name__!r}.")

        if limit_electric_current.value <= 0:
            raise ValueError("Parameter 'limit_electric_current' must be positive.")

        self.encoder = encoder
        self.tachometer = tachometer
        self.motor = motor
        self.limit_electric_current = limit_electric_current
        self.target_angular_position = target_angular_position

    def apply(self) -> Union[float, int]:
        angular_position = self.encoder.get_value()
        angular_speed = self.tachometer.get_value()
        no_load_speed = self.motor.no_load_speed
        maximum_electric_current = self.motor.maximum_electric_current
        no_load_electric_current = self.motor.no_load_electric_current
        speed_ratio = angular_speed/no_load_speed
        electric_ratio = self.limit_electric_current/maximum_electric_current

        if angular_position <= self.target_angular_position:
            return 1/2*(speed_ratio + electric_ratio +
                        np.sqrt(speed_ratio**2 + electric_ratio**2 +
                                2*speed_ratio*((self.limit_electric_current - 2*no_load_electric_current)/
                                                maximum_electric_current)))


def _compute_static_error(braking_angle: AngularPosition, transmission: Transmission):
    if not isinstance(braking_angle, AngularPosition):
        raise TypeError(f"Parameter 'braking_angle' must be an instance of {AngularPosition.__name__!r}.")

    maximum_torque = transmission.chain[0].maximum_torque
    load_torque = transmission.chain[0].load_torque

    transmission_efficiency = 1
    for element in transmission.chain:
        if isinstance(element, SpurGear):
            transmission_efficiency *= element.master_gear_efficiency

    if load_torque is not None:
        static_error = ((load_torque/maximum_torque)/transmission_efficiency)*braking_angle
    else:
        static_error = AngularPosition(0, 'rad')

    return static_error


def _compute_pwm_min(transmission: Transmission):
    maximum_torque = transmission.chain[0].maximum_torque
    if transmission.chain[0].time_variables['load torque']:
        load_torque = transmission.chain[0].time_variables['load torque'][0]
    else:
        load_torque = transmission.chain[0].load_torque
    no_load_electric_current = transmission.chain[0].no_load_electric_current
    maximum_electric_current = transmission.chain[0].maximum_electric_current

    transmission_efficiency = 1
    for element in transmission.chain:
        if isinstance(element, SpurGear):
            transmission_efficiency *= element.master_gear_efficiency

    return 1/transmission_efficiency*(load_torque/maximum_torque)*\
           ((maximum_electric_current - no_load_electric_current)/maximum_electric_current) + \
           no_load_electric_current/maximum_electric_current
