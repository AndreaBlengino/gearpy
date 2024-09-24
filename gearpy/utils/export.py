from gearpy.mechanical_objects import RotatingObject
from gearpy.units import Time
import pandas as pd
import os
from typing import Optional


def export_time_variables(
    rotating_object: RotatingObject,
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
    current_unit: Optional[str] = 'A'
) -> None:
    """It xports the computed time variables of a rotating object to a file. \n
    The exported file is a ``.csv`` file. The time variables are exported in a
    tabular form, in which each column is a time variable and each row is a
    simulated time step. The columns are separated by a comma. The first
    column reports the simulated time steps and the first row reports the
    column names.

    Parameters
    ----------
    ``rotating_object`` : :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
        The rotating object whose time variables are to be exported.
    ``file_path`` : :py:class:`str`
        Path to the file in which to save the time variables. It must be a
        non-empty :py:class:`str`.
    ``time_array`` : :py:class:`list`
        Simulated time steps. It must be a non-empty :py:class:`list`.
    ``time_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the time values in
        the exported file. It must be a :py:class:`str`. Default is ``'sec'``.
        See :py:attr:`Time.unit <gearpy.units.units.Time.unit>` for more
        details.
    ``angular_position_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the angular position
        values in the exported file. It must be a :py:class:`str`. Default is
        ``'rad'``. See
        :py:attr:`AngularPosition.unit <gearpy.units.units.AngularPosition.unit>`
        for more details.
    ``angular_speed_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the angular speed
        values in the exported file. It must be a :py:class:`str`. Default is
        ``'rad/s'``. See :py:attr:`AngularSpeed.unit <gearpy.units.units.AngularSpeed.unit>`
        for more details.
    ``angular_acceleration_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the angular
        acceleration values in the exported file. It must be a :py:class:`str`.
        Default is ``'rad/s^2'``. See
        :py:attr:`AngularAcceleration.unit <gearpy.units.units.AngularAcceleration.unit>`
        for more details.
    ``torque_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the torque values in
        the exported file. It must be a :py:class:`str`. Default is ``'Nm'``.
        See :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
        details.
    ``driving_torque_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the torque values in
        the exported file. It must be a :py:class:`str`. Default is ``'Nm'``.
        See :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
        details.
    ``load_torque_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the torque values in
        the exported file. It must be a :py:class:`str`. Default is ``'Nm'``.
        See :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
        details.
    ``force_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the force values in
        the exported file. It must be a :py:class:`str`. Default is ``'N'``.
        See :py:attr:`Force.unit <gearpy.units.units.Force.unit>` for more
        details.
    ``stress_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the stress values in
        the exported file. It must be a :py:class:`str`. Default is ``'MPa'``.
        See :py:attr:`Stress.unit <gearpy.units.units.Stress.unit>` for more
        details.
    ``current_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the electric current
        values in the exported file. It must be a :py:class:`str`. Default is
        ``'A'``. See :py:attr:`Current.unit <gearpy.units.units.Current.unit>`
        for more details.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``rotating_object`` is not an instance of
             :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`,
           - if ``file_path`` is not a :py:class:`str`,
           - if ``time_array`` is not a :py:class:`list`,
           - if an element of ``time_array`` is not an instance of
             :py:class:`Time <gearpy.units.units.Time>` or a
             :py:class:`str`,
           - if ``time_unit`` is not a :py:class:`str`,
           - if ``angular_position_unit`` is not a :py:class:`str`,
           - if ``angular_speed_unit`` is not a :py:class:`str`,
           - if ``angular_acceleration_unit`` is not a :py:class:`str`,
           - if ``torque_unit`` is not a :py:class:`str`,
           - if ``driving_torque_unit`` is not a :py:class:`str`,
           - if ``load_torque_unit`` is not a :py:class:`str`,
           - if ``force_unit`` is not a :py:class:`str`,
           - if ``stress_unit`` is not a :py:class:`str`,
           - if ``current_unit`` is not a :py:class:`str`.
       ``ValueError``
           - If ``file_path`` is an empty :py:class:`str`,
           - if ``time_array`` is an empty :py:class:`list`.
    """
    if not isinstance(rotating_object, RotatingObject):
        raise TypeError(
            f"Parameter 'rotating_object' must be an instance of "
            f"{RotatingObject.__name__!r}."
        )

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
            raise TypeError(
                f"Each element of 'time_array' must be an instance of "
                f"{Time.__name__!r}."
            )

    if not isinstance(time_unit, str):
        raise TypeError("Parameter 'time_unit' must be a string.")

    if not isinstance(angular_position_unit, str):
        raise TypeError("Parameter 'angular_position_unit' must be a string.")

    if not isinstance(angular_speed_unit, str):
        raise TypeError("Parameter 'angular_speed_unit' must be a string.")

    if not isinstance(angular_acceleration_unit, str):
        raise TypeError(
            "Parameter 'angular_acceleration_unit' must be a string."
        )

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

    UNIT = {
        'angular position': angular_position_unit,
        'angular speed': angular_speed_unit,
        'angular acceleration': angular_acceleration_unit,
        'torque': torque_unit,
        'driving torque': driving_torque_unit,
        'load torque': load_torque_unit,
        'tangential force': force_unit,
        'bending stress': stress_unit,
        'contact stress': stress_unit,
        'electric current': current_unit,
        'pwm': ''
    }

    data = pd.DataFrame()

    data[f'time ({time_unit})'] = [
        instant.to(time_unit).value for instant in time_array
    ]

    for variable in rotating_object.time_variables.keys():
        unit = UNIT[variable]
        if unit:
            data[f'{variable} ({unit})'] = [
                variable_snapshot.to(unit).value
                for variable_snapshot
                in rotating_object.time_variables[variable]
            ]
        else:
            data[variable] = rotating_object.time_variables[variable]

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    if not file_path.endswith('.csv'):
        file_path += '.csv'

    data.to_csv(file_path, index=False)
