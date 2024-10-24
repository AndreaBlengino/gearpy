from gearpy.mechanical_objects import SpurGear
from gearpy.powertrain import Powertrain
from gearpy.units import AngularPosition, Angle


def _compute_static_error(
    braking_angle: Angle,
    powertrain: Powertrain
) -> Angle | AngularPosition:
    maximum_torque = powertrain.elements[0].maximum_torque
    load_torque = powertrain.elements[0].load_torque

    powertrain_efficiency = 1
    for element in powertrain.elements:
        if isinstance(element, SpurGear):
            powertrain_efficiency *= element.master_gear_efficiency

    if load_torque is not None:
        static_error = (
            (load_torque/maximum_torque)/powertrain_efficiency
        )*braking_angle
    else:
        static_error = AngularPosition(0, 'rad')

    return static_error


def _compute_pwm_min(powertrain: Powertrain) -> float | int:
    maximum_torque = powertrain.elements[0].maximum_torque
    if powertrain.elements[0].time_variables['load torque']:
        load_torque = powertrain.elements[0].time_variables['load torque'][0]
    else:
        load_torque = powertrain.elements[0].load_torque
    no_load_electric_current = powertrain.elements[0].no_load_electric_current
    maximum_electric_current = powertrain.elements[0].maximum_electric_current

    powertrain_efficiency = 1
    for element in powertrain.elements:
        if isinstance(element, SpurGear):
            powertrain_efficiency *= element.master_gear_efficiency

    return 1/powertrain_efficiency*(load_torque/maximum_torque)*(
        (maximum_electric_current - no_load_electric_current) /
        maximum_electric_current
    ) + no_load_electric_current/maximum_electric_current
