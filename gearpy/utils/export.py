from gearpy.mechanical_objects import RotatingObject
from gearpy.units import Time
import pandas as pd
import os
from typing import Optional


def export_time_variables(rotating_object: RotatingObject,
                          file_path: str,
                          time_array: list[Time],
                          time_unit: Optional[str] = 'sec',
                          angular_position_unit: Optional[str] = 'rad',
                          angular_speed_unit: Optional[str] = 'rad/s',
                          angular_acceleration_unit: Optional[str] = 'rad/s^2',
                          torque_unit: Optional[str] = 'Nm',
                          driving_torque_unit: Optional[str] = 'Nm',
                          load_torque_unit: Optional[str] = 'Nm',
                          force_unit: Optional[str] = 'N',
                          stress_unit: Optional[str] = 'MPa',
                          current_unit: Optional[str] = 'A') -> None:

    if not isinstance(rotating_object, RotatingObject):
        raise TypeError(f"Parameter 'rotating_object' must be an instance of {RotatingObject.__name__!r}.")

    if not isinstance(file_path, str):
        raise TypeError("Parameter 'file_path' must be a string.")

    if not file_path:
        raise ValueError("Parameter 'file_path' cannot be an empty string.")

    if not isinstance(time_array, list):
        raise TypeError("Parameter 'time_array' must be a list.")

    if not time_array:
        raise ValueError("Parameter 'time_array' cannot be an empty list.")

    for instant in time_array:
        if not isinstance(instant, Time):
            raise TypeError(f"Each element of 'time_array' must be an instance of {Time.__name__!r}.")

    if not isinstance(time_unit, str):
        raise TypeError("Parameter 'time_unit' must be a string.")

    if not isinstance(angular_position_unit, str):
        raise TypeError("Parameter 'angular_position_unit' must be a string.")

    if not isinstance(angular_speed_unit, str):
        raise TypeError("Parameter 'angular_speed_unit' must be a string.")

    if not isinstance(angular_acceleration_unit, str):
        raise TypeError("Parameter 'angular_acceleration_unit' must be a string.")

    if not isinstance(torque_unit, str):
        raise TypeError("Parameter 'torque_unit' must be a string.")

    if not isinstance(driving_torque_unit, str):
        raise TypeError("Parameter 'driving_torque_unit' must be a string.")

    if not isinstance(load_torque_unit, str):
        raise TypeError("Parameter 'load_torque_unit' must be a string.")

    if not isinstance(force_unit, str):
        raise TypeError("Parameter 'force_unit' must be a string.")

    if not isinstance(stress_unit, str):
        raise TypeError("Parameter 'stress_unit' must be a string.")

    if not isinstance(current_unit, str):
        raise TypeError("Parameter 'current_unit' must be a string.")

    UNIT = {'angular position': angular_position_unit, 'angular speed': angular_speed_unit,
            'angular acceleration': angular_acceleration_unit, 'torque': torque_unit,
            'driving torque': driving_torque_unit, 'load torque': load_torque_unit,
            'tangential force': force_unit, 'bending stress': stress_unit, 'contact stress': stress_unit,
            'electric current': current_unit, 'pwm': ''}

    data = pd.DataFrame()

    data[f'time ({time_unit})'] = [instant.to(time_unit).value for instant in time_array]

    for variable in rotating_object.time_variables.keys():
        unit = UNIT[variable]
        if unit:
            data[f'{variable} ({unit})'] = [variable_snapshot.to(unit).value
                                            for variable_snapshot in rotating_object.time_variables[variable]]
        else:
            data[variable] = rotating_object.time_variables[variable]

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    if not file_path.endswith('.csv'):
        file_path += '.csv'

    data.to_csv(file_path, index = False)
