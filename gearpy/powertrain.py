from collections import Counter
from gearpy.mechanical_objects import (
    MotorBase,
    RotatingObject,
    GearBase,
    WormGear
)
from gearpy.units import Time
from gearpy.utils import export_time_variables
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.interpolate import interp1d
from typing import Optional


VARIABLES_SORT_ORDER = {
    'angular position': 0,
    'angular speed': 1,
    'angular acceleration': 2,
    'torque': 3,
    'driving torque': 4,
    'load torque': 5,
    'tangential force': 6,
    'bending stress': 7,
    'contact stress': 8,
    'electric current': 9,
    'pwm': 10
}


class Powertrain:
    r""":py:class:`Powertrain <gearpy.powertrain.Powertrain>` object.

    Attributes
    ----------
    :py:attr:`elements` : :py:class:`tuple`
        Elements in the powertrain.
    :py:attr:`time` : :py:class:`list`
        Simulated time steps.
    :py:attr:`self_locking` : :py:class:`bool`
        Whether the powertrain can only be moved by the motor and not by the
        effect of the load.

    Methods
    -------
    :py:meth:`plot`
        It plots time variables for each element in the powertrain's
        :py:attr:`elements`.
    :py:meth:`reset`
        It resets the computed time variables.
    :py:meth:`snapshot`
        Computes a snapshot of the time variables of the elements in the
        powertrain at the specified ``target_time``.
    :py:meth:`update_time`
        It updates the :py:attr:`time` by appending the ``instant`` simulated
        time step.
    :py:meth:`export_time_variables`
        It exports the powertrain's rotating objects' computed time variables
        to some files.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           If ``motor`` parameter is not an instance of
           :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`.
       ``ValueError``
           If ``motor`` is not connected to any other element.
       ``NameError``
           If two or more elements in the powertrain elements share the same
           ``name``.
    """

    def __init__(self, motor: MotorBase):
        if not isinstance(motor, MotorBase):
            raise TypeError(
                f"Parameter 'motor' must be an instance of "
                f"{MotorBase.__name__!r}."
            )

        if motor.drives is None:
            raise ValueError(
                "Parameter 'motor' is not connected to any other element. "
                "Call 'add_fixed_joint' to join 'motor' with a GearBase's "
                "instance."
            )

        elements = [motor]
        while elements[-1].drives is not None:
            elements.append(elements[-1].drives)

        counts = Counter([element.name for element in elements])
        for name, count in counts.items():
            if count > 1:
                raise NameError(
                    f"Found {count} elements with the same name {name!r}, "
                    f"each element must have a unique name."
                )

        self.__elements = tuple(elements)
        self.__time = []
        self.__self_locking = False
        for element in self.elements:
            if isinstance(element, WormGear):
                if element.self_locking:
                    self.__self_locking = True

    @property
    def elements(self) -> tuple[RotatingObject]:
        """Rotating objects in the powertrain. \n
        The first element is the driving motor, the next elements are in order,
        from the closest to the farthest from the motor. Each element is driven
        by the previous one and it drives the following one.

        Returns
        -------
        :py:class:`tuple`
            Rotating objects in the powertrain.

        .. admonition:: See Also
           :class: seealso

           :py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>` \n
           :py:class:`Flywheel <gearpy.mechanical_objects.flywheel.Flywheel>` \n
           :py:class:`HelicalGear <gearpy.mechanical_objects.helical_gear.HelicalGear>` \n
           :py:class:`SpurGear <gearpy.mechanical_objects.spur_gear.SpurGear>` \n
           :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>` \n
           :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`
        """
        return self.__elements

    @property
    def time(self) -> list[Time]:
        """List of the simulated time steps. \n
        During computation, the solver appends a simulated time step to this
        list at each iteration. \n
        Every element of this list must be an instance of
        :py:class:`Time <gearpy.units.units.Time>`.

        Returns
        -------
        :py:class:`list`
            The :py:class:`list` of the simulated time steps.

        .. admonition:: See Also
           :class: seealso

           :py:meth:`Solver.run() <gearpy.solver.Solver.run>`
        """
        return self.__time

    @property
    def self_locking(self) -> bool:
        """Whether the powertrain can only be moved by the motor and not by the
        effect of the load. \n
        This property is given by the presence of a self-locking mating between
        a
        :py:class:`WormGear <gearpy.mechanical_objects.worm_gear.WormGear>` and
        a
        :py:class:`WormWheel <gearpy.mechanical_objects.worm_wheel.WormWheel>`
        in the powertrain. This type of gear mating can be self-locking if the
        amount of friction is high enough with respect to the gear pressure and
        helix angles. \n
        If the powertrain is self-locking, then it can only be moved by the
        motor and not by the load, even if the load torque is greater than the
        motor driving torque. \n
        Once the property is defined at the
        :py:class:`Powertrain <gearpy.powertrain.Powertrain>` instantiation, it
        cannot be changed afterward.

        Returns
        -------
        :py:class:`bool`
            Whether the powertrain can only be moved by the motor and not by
            the effect of the load.

        .. admonition:: See Also
           :class: seealso

           :py:attr:`WormGear.self_locking <gearpy.mechanical_objects.worm_gear.WormGear.self_locking>`
        """
        return self.__self_locking

    def update_time(self, instant: Time) -> None:
        """It updates the :py:attr:`time` by appending the ``instant``
        simulated time step.

        Parameters
        ----------
        ``instant`` : :py:class:`Time <gearpy.units.units.Time>`
            Simulated time step to be added to :py:attr:`time`.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If ``instant`` is not an instance of
               :py:class:`Time <gearpy.units.units.Time>`.
        """
        if not isinstance(instant, Time):
            raise TypeError(
                f"Parameter 'instant' must be instances of {Time.__name__!r}."
            )

        self.__time.append(instant)

    def reset(self) -> None:
        """It resets the computed time variables. \n
        For each element in the powertrain's :py:attr:`elements`, it resets
        each time variables and also :py:attr:`time`
        property.

        .. admonition:: See Also
           :class: seealso

           :py:attr:`DCMotor.time_variables <gearpy.mechanical_objects.dc_motor.DCMotor.time_variables>` \n
           :py:attr:`Flywheel.time_variables <gearpy.mechanical_objects.flywheel.Flywheel.time_variables>` \n
           :py:attr:`HelicalGear.time_variables <gearpy.mechanical_objects.helical_gear.HelicalGear.time_variables>` \n
           :py:attr:`SpurGear.time_variables <gearpy.mechanical_objects.spur_gear.SpurGear.time_variables>` \n
           :py:attr:`WormGear.time_variables <gearpy.mechanical_objects.worm_gear.WormGear.time_variables>` \n
           :py:attr:`WormWheel.time_variables <gearpy.mechanical_objects.worm_wheel.WormWheel.time_variables>`
        """
        self.__time = []

        for element in self.elements:
            element.angular_position = element.time_variables[
                'angular position'
            ][0]
            element.angular_speed = element.time_variables['angular speed'][0]
            element.angular_acceleration = element.time_variables[
                'angular acceleration'
            ][0]
            element.torque = element.time_variables['torque'][0]
            element.driving_torque = element.time_variables[
                'driving torque'
            ][0]
            element.load_torque = element.time_variables['load torque'][0]
            if isinstance(element, MotorBase):
                if element.electric_current_is_computable:
                    element.electric_current = element.time_variables[
                        'electric current'
                    ][0]
                element.pwm = element.time_variables['pwm'][0]
            if isinstance(element, GearBase):
                if element.tangential_force_is_computable:
                    element.tangential_force = element.time_variables[
                        'tangential force'
                    ][0]
                    if element.bending_stress_is_computable:
                        element.bending_stress = element.time_variables[
                            'bending stress'
                        ][0]
                        if element.contact_stress_is_computable:
                            element.contact_stress = element.time_variables[
                                'contact stress'
                            ][0]

            for variable in element.time_variables.keys():
                element.time_variables[variable] = []

    def snapshot(
        self,
        target_time: Time,
        variables: Optional[list[str]] = None,
        angular_position_unit: Optional[str] = 'rad',
        angular_speed_unit: Optional[str] = 'rad/s',
        angular_acceleration_unit: Optional[str] = 'rad/s^2',
        torque_unit: Optional[str] = 'Nm',
        driving_torque_unit: Optional[str] = 'Nm',
        load_torque_unit: Optional[str] = 'Nm',
        force_unit: Optional[str] = 'N',
        stress_unit: Optional[str] = 'MPa',
        current_unit: Optional[str] = 'A',
        print_data: Optional[bool] = True
    ) -> pd.DataFrame:
        """It computes a snapshot of the time variables of the elements in the
        powertrain at the specified ``target_time``. \n
        It returns a :py:class:`pandas.DataFrame` with the computed time
        variables. Each element in the powertrain's :py:attr:`elements` is a
        row of the DataFrame, while the columns are the time variables
        ``'angular position'``, ``'angular speed'``,
        ``'angular acceleration'``, ``'torque'``, ``'driving torque'`` and
        ``'load torque'``.
        The motor can have additional variables ``'electric current'`` and
        ``'pwm'``, while gears can have additional parameters
        ``'tangential force'``, ``'bending stress'`` and ``'contact stress'``,
        depending on instantiation parameters. \n
        It is possible to select the variables to be printed with the
        ``variables`` parameter. \n
        Each time variable is converted to the relative unit passed as
        optional parameter. \n
        If the ``target_time`` is not among simulated time steps in the
        :py:attr:`time` property, it computes a linear interpolation from the
        two closest simulated time steps.

        Parameters
        ----------
        ``target_time`` : :py:class:`Time <gearpy.units.units.Time>`
            The time to which compute the powertrain time variables' snapshot.
            It must be an instance of
            :py:class:`Time <gearpy.units.units.Time>`, whose value must be
            within minimum and maximum simulated time steps in :py:attr:`time`
            property.
        ``variables`` : :py:class:`list`, optional
            Time variables to be printed. It must be a :py:class:`list`.
            Default is all available time variables.
        ``angular_position_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the angular
            position values in the DataFrame. It must be a :py:class:`str`.
            Default is ``'rad'``. See
            :py:attr:`AngularPosition.unit <gearpy.units.units.AngularPosition.unit>`
            for more details.
        ``angular_speed_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the angular
            speed values in the DataFrame. It must be a :py:class:`str`.
            Default is ``'rad/s'``. See
            :py:attr:`AngularSpeed.unit <gearpy.units.units.AngularSpeed.unit>`
            for more details.
        ``angular_acceleration_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the angular
            acceleration values in the DataFrame. It must be a :py:class:`str`.
            Default is ``'rad/s^2'``. See
            :py:attr:`AngularAcceleration.unit <gearpy.units.units.AngularAcceleration.unit>`
            for more details.
        ``torque_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the torque
            values in the DataFrame. It must be a :py:class:`str`. Default is
            ``'Nm'``. See
            :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
            details.
        ``driving_torque_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the driving
            torque values in the DataFrame. It must be a :py:class:`str`.
            Default is ``'Nm'``. See
            :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
            details.
        ``load_torque_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the load torque
            values in the DataFrame. It must be a :py:class:`str`. Default is
            ``'Nm'``. See
            :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
            details.
        ``force_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the force values
            in the DataFrame. It must be a :py:class:`str`. Default is ``'N'``.
            See :py:attr:`Force.unit <gearpy.units.units.Force.unit>` for more
            details.
        ``stress_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the stress
            values in the DataFrame. It must be a :py:class:`str`. Default is
            ``'MPa'``. See
            :py:attr:`Stress.unit <gearpy.units.units.Stress.unit>` for more
            details.
        ``current_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the electric
            current values in the DataFrame. It must be a :py:class:`str`.
            Default is ``'A'``. See
            :py:attr:`Current.unit <gearpy.units.units.Current.unit>` for more
            details.
        ``print_data`` : :py:class:`bool`, optional
            Whether to print the computed time variables DataFrame. Default is
            ``True``.

        Returns
        -------
        :py:class:`pandas.DataFrame`
            The DataFrame containing time variables values at the specified
            ``target_time`` for each element in the powertrain's
            :py:attr:`elements`.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If an element of ``time`` is not an instance of
                 :py:class:`Time <gearpy.units.units.Time>`,
               - if ``target_time`` is not an instance of
                 :py:class:`Time <gearpy.units.units.Time>`,
               - if ``variables`` is not a :py:class:`list`,
               - if an element of ``variables`` is not a :py:class:`str`,
               - if ``angular_position_unit`` is not a :py:class:`str`,
               - if ``angular_speed_unit`` is not a :py:class:`str`,
               - if ``angular_acceleration_unit`` is not a :py:class:`str`,
               - if ``torque_unit`` is not a :py:class:`str`,
               - if ``driving_torque_unit`` is not a :py:class:`str`,
               - if ``load_torque_unit`` is not a :py:class:`str`,
               - if ``force_unit`` is not a :py:class:`str`,
               - if ``stress_unit`` is not a :py:class:`str`,
               - if ``current_unit`` is not a :py:class:`str`,
               - if ``print_data`` is not a :py:class:`bool`.
           ``ValueError``
               - If ``time`` is an empty :py:class:`list`,
               - if ``target_time`` is outside simulation interval,
               - if ``variables`` is an empty :py:class:`list`,
               - if an element of ``variables`` is not a valid time variable.

        .. admonition:: See Also
           :class: seealso

           :py:attr:`time` \n
           :py:attr:`elements` \n
           :py:attr:`DCMotor.time_variables <gearpy.mechanical_objects.dc_motor.DCMotor.time_variables>` \n
           :py:attr:`Flywheel.time_variables <gearpy.mechanical_objects.flywheel.Flywheel.time_variables>` \n
           :py:attr:`HelicalGear.time_variables <gearpy.mechanical_objects.helical_gear.HelicalGear.time_variables>` \n
           :py:attr:`SpurGear.time_variables <gearpy.mechanical_objects.spur_gear.SpurGear.time_variables>` \n
           :py:attr:`WormGear.time_variables <gearpy.mechanical_objects.worm_gear.WormGear.time_variables>` \n
           :py:attr:`WormWheel.time_variables <gearpy.mechanical_objects.worm_wheel.WormWheel.time_variables>`
        """
        if not all([isinstance(instant, Time) for instant in self.time]):
            raise TypeError(
                f"Each element of the 'time' list must be an instance of "
                f"{Time.__name__!r}."
            )

        if not self.time:
            raise ValueError("Parameter 'time' cannot be an empty list.")

        if not isinstance(target_time, Time):
            raise TypeError(
                f"Parameter 'target_time' must be an instance of "
                f"{Time.__name__!r}."
            )

        if (target_time < min(self.time)) or (target_time > max(self.time)):
            raise ValueError(
                f"Parameter 'target_time' must be within simulation interval "
                f"{min(self.time)} - {max(self.time)}."
            )

        if variables is not None:
            if not isinstance(variables, list):
                raise TypeError("Parameter 'variables' must be a list.")

            if not variables:
                raise ValueError(
                    "Parameter 'variables' cannot be an empty list."
                )

            valid_variables = []
            for element in self.elements:
                valid_variables.extend(element.time_variables.keys())
            valid_variables = list(set(valid_variables))
            valid_variables.sort(
                key=lambda variable: VARIABLES_SORT_ORDER[variable]
            )
            for variable in variables:
                if not isinstance(variable, str):
                    raise TypeError(
                        "Each element of 'variables' must be a string."
                    )

                if variable not in valid_variables:
                    raise ValueError(
                        f"Invalid variable {variable!r}. Available variables "
                        f"are: {valid_variables}."
                    )

        if not isinstance(angular_position_unit, str):
            raise TypeError(
                "Parameter 'angular_position_unit' must be a string."
            )

        if not isinstance(angular_speed_unit, str):
            raise TypeError(
                "Parameter 'angular_speed_unit' must be a string."
            )

        if not isinstance(angular_acceleration_unit, str):
            raise TypeError(
                "Parameter 'angular_acceleration_unit' must be a string."
            )

        if not isinstance(torque_unit, str):
            raise TypeError("Parameter 'torque_unit' must be a string.")

        if not isinstance(driving_torque_unit, str):
            raise TypeError(
                "Parameter 'driving_torque_unit' must be a string."
            )

        if not isinstance(load_torque_unit, str):
            raise TypeError("Parameter 'load_torque_unit' must be a string.")

        if not isinstance(force_unit, str):
            raise TypeError("Parameter 'force_unit' must be a string.")

        if not isinstance(stress_unit, str):
            raise TypeError("Parameter 'stress_unit' must be a string.")

        if not isinstance(current_unit, str):
            raise TypeError("Parameter 'current_unit' must be a string.")

        if not isinstance(print_data, bool):
            raise TypeError("Parameter 'print_data' must be a bool.")

        if variables is None:
            variables = []
            for element in self.elements:
                variables.extend(element.time_variables.keys())
        variables = list(set(variables))
        variables.sort(key=lambda variable: VARIABLES_SORT_ORDER[variable])

        UNITS = {
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

        columns = [
            f'{variable} ({UNITS[variable]})'
            if UNITS[variable] != '' else variable for variable in variables
        ]
        data = pd.DataFrame(columns=columns)

        for element in self.elements:
            for variable, unit in zip(
                [
                    'angular position',
                    'angular speed',
                    'angular acceleration',
                    'torque',
                    'driving torque',
                    'load torque'
                ],
                [
                    angular_position_unit,
                    angular_speed_unit,
                    angular_acceleration_unit,
                    torque_unit,
                    driving_torque_unit,
                    load_torque_unit
                ]
            ):
                if variable in variables:
                    interpolation_function = interp1d(
                        x=[instant.to('sec').value for instant in self.time],
                        y=[
                            value.to(unit).value
                            for value in element.time_variables[variable]
                        ]
                    )
                    data.loc[element.name, f'{variable} ({unit})'] = \
                        interpolation_function(
                        target_time.to('sec').value
                    ).take(0)

            if isinstance(element, MotorBase):
                interpolation_function = interp1d(
                    x=[instant.to('sec').value for instant in self.time],
                    y=element.time_variables['pwm']
                )
                data.loc[element.name, 'pwm'] = interpolation_function(
                    target_time.to('sec').value
                ).take(0)

                if 'electric current' in variables:
                    if element.electric_current_is_computable:
                        interpolation_function = interp1d(
                            x=[
                                instant.to('sec').value
                                for instant in self.time
                            ],
                            y=[
                                value.to(current_unit).value
                                for value in
                                element.time_variables['electric current']
                            ]
                        )
                        data.loc[
                            element.name,
                            f'electric current ({current_unit})'
                        ] = interpolation_function(
                            target_time.to('sec').value
                        ).take(0)

            if isinstance(element, GearBase | WormGear):
                variable_list = []
                unit_list = []
                if element.tangential_force_is_computable and \
                        'tangential force' in variables:
                    variable_list.append('tangential force')
                    unit_list.append(force_unit)
                    if isinstance(element, GearBase):
                        if element.bending_stress_is_computable and \
                                'bending stress' in variables:
                            variable_list.append('bending stress')
                            unit_list.append(stress_unit)
                            if element.contact_stress_is_computable and \
                                    'contact stress' in variables:
                                variable_list.append('contact stress')
                                unit_list.append(stress_unit)

                for variable, unit in zip(variable_list, unit_list):
                    interpolation_function = interp1d(
                        x=[instant.to('sec').value for instant in self.time],
                        y=[
                            value.to(unit).value
                            for value in element.time_variables[variable]
                        ]
                    )
                    data.loc[
                        element.name,
                        f'{variable} ({unit})'
                    ] = interpolation_function(
                        target_time.to('sec').value
                    ).take(0)

        if print_data:
            print(f'Mechanical Powertrain Status at Time = {target_time}')
            print(data.astype(float).fillna(value='').to_string())

        return data

    def plot(
        self,
        elements: Optional[list[RotatingObject | str]] = None,
        variables: Optional[list[str]] = None,
        angular_position_unit: Optional[str] = 'rad',
        angular_speed_unit: Optional[str] = 'rad/s',
        angular_acceleration_unit: Optional[str] = 'rad/s^2',
        torque_unit: Optional[str] = 'Nm',
        force_unit: Optional[str] = 'N',
        stress_unit: Optional[str] = 'MPa',
        current_unit: Optional[str] = 'A',
        time_unit: Optional[str] = 'sec',
        figsize: Optional[tuple] = None
    ) -> None:
        """It plots time variables for selected ``elements`` in the
        powertrain's :py:attr:`elements`. \n
        It generates a grid of subplots, one column for each selected element
        of the powertrain's :py:attr:`elements` and one row for each selected
        time variable. \n
        The available elements are listed in :py:attr:`elements` and the
        available variables are: ``'angular position'``, ``'angular speed'``,
        ``'angular acceleration'``, ``'torque'``, ``'driving torque'`` and
        ``'load torque'``. The motor can have additional variables
        ``electric current`` and ``pwm`` while gears can have additional
        variables ``tangential force``, ``bending stress`` and
        ``contact stress``, depending on instantiation parameters. \n
        The time variables are plotted in the described order, from the top
        row to the bottom one; torques are grouped together in a single row as
        well as stresses are grouped together. Plotted values' units are
        managed with optional parameters. \n
        Elements to be plotted can be passed as instances or names
        (:py:class:`str`) in a :py:class:`list`.

        Parameters
        ----------
        ``elements`` : :py:class:`list`, optional
            Elements of the powertrain's :py:attr:`elements` which time
            variables have to be plotted. Each single element can be passed as
            instance or name (:py:class:`str`). Default is all elements in the
            powertrain's :py:attr:`elements`.
        ``variables`` : :py:class:`list`, optional
            Time variables to be plotted. Default is all available time
            variables.
        ``angular_position_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the angular
            position values in the plot. It must be a :py:class:`str`. Default
            is ``'rad'``. See
            :py:attr:`AngularPosition.unit <gearpy.units.units.AngularPosition.unit>`
            for more details.
        ``angular_speed_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the angular
            speed values in the plot. It must be a :py:class:`str`. Default is
            ``'rad/s'``. See
            :py:attr:`AngularSpeed.unit <gearpy.units.units.AngularSpeed.unit>`
            for more details.
        ``angular_acceleration_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the angular
            acceleration values in the plot. It must be a :py:class:`str`.
            Default is ``'rad/s^2'``. See
            :py:attr:`AngularAcceleration.unit <gearpy.units.units.AngularAcceleration.unit>`
            for more details.
        ``torque_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the torque
            values in the plot. It must be a :py:class:`str`. Default is
            ``'Nm'``. See
            :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
            details.
        ``force_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the force values
            in the plot. It must be a :py:class:`str`. Default is ``'N'``. See
            :py:attr:`Force.unit <gearpy.units.units.Force.unit>` for more
            details.
        ``stress_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the stress
            values in the plot. It must be a :py:class:`str`. Default is
            ``'MPa'``. See
            :py:attr:`Stress.unit <gearpy.units.units.Stress.unit>` for more
            details.
        ``current_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the electric
            current values in the plot. It must be a :py:class:`str`. Default
            is ``'A'``. See
            :py:attr:`Current.unit <gearpy.units.units.Current.unit>` for more
            details.
        ``time_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the time values
            in the plot. It must be a :py:class:`str`. Default is ``'sec'``.
            See :py:attr:`Time.unit <gearpy.units.units.Time.unit>` for more
            details.
        ``figsize`` : :py:class:`tuple`, optional
            Width and height of the window size, in inches. If not provided
            defaults to ``[6.4, 4.8]``.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``elements`` is not a :py:class:`list`,
               - if an element of ``elements`` is not an instance of
                 :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`
                 or a :py:class:`str`,
               - if ``variables`` is not a :py:class:`list`,
               - if an element of ``variables`` is not a :py:class:`str`,
               - if ``angular_position_unit`` is not a :py:class:`str`,
               - if ``angular_speed_unit`` is not a :py:class:`str`,
               - if ``angular_acceleration_unit`` is not a :py:class:`str`,
               - if ``torque_unit`` is not a :py:class:`str`,
               - if ``force_unit`` is not a :py:class:`str`,
               - if ``stress_unit`` is not a :py:class:`str`,
               - if ``current_unit`` is not a :py:class:`str`,
               - if ``time_unit`` is not a :py:class:`str`,
               - if ``figsize`` is not a :py:class:`tuple`,
               - if an element of ``figsize`` is not a :py:class:`float` or an
                 :py:class:`int`.
           ``ValueError``
               - If ``elements`` is an empty :py:class:`list`,
               - if an element of ``elements`` is not in :py:attr:`elements`,
               - if ``variables`` is an empty :py:class:`list`,
               - if an element of ``variables`` is not a valid time variable,
               - if ``figsize`` has not exactly two elements: one for width and
                 the other for height.

        .. admonition:: See Also
           :class: seealso

           :py:attr:`time` \n
           :py:attr:`elements` \n
           :py:attr:`DCMotor.time_variables <gearpy.mechanical_objects.dc_motor.DCMotor.time_variables>` \n
           :py:attr:`Flywheel.time_variables <gearpy.mechanical_objects.flywheel.Flywheel.time_variables>` \n
           :py:attr:`HelicalGear.time_variables <gearpy.mechanical_objects.helical_gear.HelicalGear.time_variables>` \n
           :py:attr:`SpurGear.time_variables <gearpy.mechanical_objects.spur_gear.SpurGear.time_variables>` \n
           :py:attr:`WormGear.time_variables <gearpy.mechanical_objects.worm_gear.WormGear.time_variables>` \n
           :py:attr:`WormWheel.time_variables <gearpy.mechanical_objects.worm_wheel.WormWheel.time_variables>`
        """
        if elements is not None:
            if not isinstance(elements, list):
                raise TypeError("Parameter 'elements' must be a list.")

            if not elements:
                raise ValueError(
                    "Parameter 'elements' cannot be an empty list."
                )

            valid_element_names = [
                valid_element.name for valid_element in self.elements
            ]
            for element in elements:
                if not isinstance(element, RotatingObject | str):
                    raise TypeError(
                        f"Each element of 'elements' must be an instance of "
                        f"{RotatingObject.__name__!r} or a string."
                    )

                if isinstance(element, RotatingObject):
                    if element not in self.elements:
                        raise ValueError(
                            f"Element {element.name!r} not found in the "
                            f"powertrain elements. Available elements are: "
                            f"{valid_element_names}."
                        )
                else:
                    if element not in valid_element_names:
                        raise ValueError(
                            f"Element {element!r} not found in the powertrain "
                            f"elements. Available elements are: "
                            f"{valid_element_names}."
                        )

        if variables is not None:
            if not isinstance(variables, list):
                raise TypeError("Parameter 'variables' must be a list.")

            if not variables:
                raise ValueError(
                    "Parameter 'variables' cannot be an empty list."
                )

            valid_variables = []
            for element in self.elements:
                valid_variables.extend(element.time_variables.keys())
            valid_variables = list(set(valid_variables))
            valid_variables.sort(
                key=lambda variable: VARIABLES_SORT_ORDER[variable]
            )
            for variable in variables:
                if not isinstance(variable, str):
                    raise TypeError(
                        "Each element of 'variables' must be a string."
                    )

                if variable not in valid_variables:
                    raise ValueError(
                        f"Invalid variable {variable!r}. Available variables "
                        f"are: {valid_variables}."
                    )

        if not isinstance(angular_position_unit, str):
            raise TypeError(
                "Parameter 'angular_position_unit' must be a string."
            )

        if not isinstance(angular_speed_unit, str):
            raise TypeError("Parameter 'angular_speed_unit' must be a string.")

        if not isinstance(angular_acceleration_unit, str):
            raise TypeError(
                "Parameter 'angular_acceleration_unit' must be a string."
            )

        if not isinstance(torque_unit, str):
            raise TypeError("Parameter 'torque_unit' must be a string.")

        if not isinstance(force_unit, str):
            raise TypeError("Parameter 'force_unit' must be a string.")

        if not isinstance(stress_unit, str):
            raise TypeError("Parameter 'stress_unit' must be a string.")

        if not isinstance(current_unit, str):
            raise TypeError("Parameter 'current_unit' must be a string.")

        if not isinstance(time_unit, str):
            raise TypeError("Parameter 'time_unit' must be a string.")

        if figsize is not None:
            if not isinstance(figsize, tuple):
                raise TypeError("Parameter 'figsize' must be a tuple.")

            if len(figsize) != 2:
                raise ValueError(
                    "Parameter 'figsize' must contain two values, one for "
                    "width and one for height."
                )

            if not all(
                [isinstance(dimension, float | int) for dimension in figsize]
            ):
                raise TypeError(
                    "All elements of 'figsize' must be floats or integers."
                )

        if elements is None:
            elements = self.elements
        else:
            elements = [
                element for element in self.elements
                if element in elements or element.name in elements
            ]
        n_elements = len(elements)

        if variables is None:
            variables = []
            for element in elements:
                variables.extend(element.time_variables.keys())
        variables = list(set(variables))
        variables.sort(key=lambda variable: VARIABLES_SORT_ORDER[variable])

        kinematic_variables = [
            variable for variable in variables
            if 'torque' not in variable and 'force' not in variable and
            'stress' not in variable and 'electric' not in variable and
            'pwm' not in variable
        ]
        torques_variables = [
            variable for variable in variables if 'torque' in variable
        ]
        forces_variables = [
            variable for variable in variables if 'force' in variable
        ]
        stress_variables = [
            variable for variable in variables if 'stress' in variable
        ]
        electric_variables = [
            variable for variable in variables if 'electric' in variable
        ]
        pwm_variables = [
            variable for variable in variables if 'pwm' in variable
        ]

        torques_variables_index = len(kinematic_variables)
        forces_variables_index = len(kinematic_variables)
        stress_variables_index = len(kinematic_variables)
        electric_variables_index = len(kinematic_variables)
        pwm_variables_index = len(kinematic_variables)

        n_variables = len(kinematic_variables)
        if torques_variables:
            n_variables += 1
            forces_variables_index += 1
            stress_variables_index += 1
            electric_variables_index += 1
            pwm_variables_index += 1
        if forces_variables:
            n_variables += 1
            stress_variables_index += 1
            electric_variables_index += 1
            pwm_variables_index += 1
        if stress_variables:
            n_variables += 1
            electric_variables_index += 1
            pwm_variables_index += 1
        if electric_variables:
            n_variables += 1
            pwm_variables_index += 1
        if pwm_variables:
            n_variables += 1

        time_values = [instant.to(time_unit).value for instant in self.time]

        UNITS = {
            'angular position': angular_position_unit,
            'angular speed': angular_speed_unit,
            'angular acceleration': angular_acceleration_unit,
            'torque': torque_unit,
            'driving torque': torque_unit,
            'load torque': torque_unit,
            'tangential force': force_unit,
            'bending stress': stress_unit,
            'contact stress': stress_unit,
            'electric current': current_unit,
            'pwm': ''
        }

        _, ax = plt.subplots(
            nrows=n_variables,
            ncols=n_elements,
            sharex='all',
            layout='constrained',
            figsize=figsize
        )

        stress_legend_items = {}

        for i, element in enumerate(elements, 0):
            if n_variables > 1:
                axes = ax[:, i] if n_elements > 1 else ax
            else:
                axes = [ax[i]] if n_elements > 1 else [ax]
            axes[0].set_title(element.name)

            for j, variable in enumerate(kinematic_variables, 0):
                axes[j].plot(
                    time_values,
                    [
                        variable_value.to(UNITS[variable]).value
                        for variable_value in element.time_variables[variable]
                    ]
                )

            for variable in torques_variables:
                label = variable.replace('torque', '').replace(' ', '')
                label = 'net' if label == '' else label
                axes[torques_variables_index].plot(
                    time_values,
                    [
                        variable_value.to(UNITS[variable]).value
                        for variable_value in element.time_variables[variable]
                    ],
                    label=label
                )

            if isinstance(element, MotorBase):
                if element.electric_current_is_computable and \
                        electric_variables:
                    axes[electric_variables_index].plot(
                        time_values,
                        [
                            variable_value.to(UNITS['electric current']).value
                            for variable_value
                            in element.time_variables['electric current']
                        ]
                    )

                if pwm_variables:
                    axes[pwm_variables_index].plot(
                        time_values,
                        element.time_variables['pwm']
                    )

            else:
                if electric_variables:
                    axes[electric_variables_index].axis('off')
                if pwm_variables:
                    axes[pwm_variables_index].axis('off')

            if isinstance(element, GearBase | WormGear):
                if element.tangential_force_is_computable:
                    for variable in forces_variables:
                        axes[forces_variables_index].plot(
                            time_values,
                            [
                                variable_value.to(UNITS[variable]).value
                                for variable_value
                                in element.time_variables[variable]
                            ]
                        )

                    if isinstance(element, GearBase):
                        for variable in stress_variables:
                            if (variable == 'bending stress' and
                                element.bending_stress_is_computable) or \
                                    (variable == 'contact stress' and
                                     element.contact_stress_is_computable):
                                axes[stress_variables_index].plot(
                                    time_values,
                                    [
                                        variable_value.to(
                                            UNITS[variable]
                                        ).value
                                        for variable_value
                                        in element.time_variables[variable]
                                    ],
                                    label=variable.replace(
                                        'stress',
                                        ''
                                    ).replace(' ', '')
                                )
                                handles, labels = axes[
                                    stress_variables_index
                                ].get_legend_handles_labels()
                                for handle, label in zip(handles, labels):
                                    if label not in stress_legend_items.keys():
                                        stress_legend_items[label] = handle

                            if (
                                stress_variables and
                                not element.bending_stress_is_computable and
                                not element.contact_stress_is_computable
                            ):
                                axes[stress_variables_index].axis('off')

                    else:
                        if stress_variables:
                            axes[stress_variables_index].axis('off')

                else:
                    if forces_variables:
                        axes[forces_variables_index].axis('off')
                    if stress_variables:
                        axes[stress_variables_index].axis('off')

            else:
                if forces_variables:
                    axes[forces_variables_index].axis('off')
                if stress_variables:
                    axes[stress_variables_index].axis('off')

            last_row_index = n_variables - 1
            if isinstance(element, MotorBase):
                if not electric_variables and not pwm_variables:
                    if forces_variables:
                        last_row_index -= 1
                    if stress_variables:
                        last_row_index -= 1
            elif isinstance(element, GearBase | WormGear):
                if forces_variables and \
                        not element.tangential_force_is_computable:
                    last_row_index -= 1
                if isinstance(element, WormGear):
                    if stress_variables:
                        last_row_index -= 1
                if isinstance(element, GearBase):
                    if (
                        stress_variables and
                        (
                            not element.bending_stress_is_computable or
                            'bending stress' not in stress_variables
                        ) and
                        (
                            not element.contact_stress_is_computable or
                            'contact stress' not in stress_variables
                        )
                    ):
                        last_row_index -= 1
                if electric_variables:
                    last_row_index -= 1
                if pwm_variables:
                    last_row_index -= 1
            else:
                if forces_variables:
                    last_row_index -= 1
                if stress_variables:
                    last_row_index -= 1
                if electric_variables:
                    last_row_index -= 1
                if pwm_variables:
                    last_row_index -= 1

            axes[last_row_index].set_xlabel(f'time ({time_unit})')
            axes[last_row_index].xaxis.set_tick_params(
                which='both',
                labelbottom=True
            )

        if n_variables > 1:
            first_column_axes = ax[:, 0] if n_elements > 1 else ax
        else:
            first_column_axes = [ax[0]] if n_elements > 1 else [ax]

        for j, variable in enumerate(kinematic_variables, 0):
            first_column_axes[j].set_ylabel(f'{variable} ({UNITS[variable]})')

        if torques_variables:
            first_column_axes[torques_variables_index].set_ylabel(
                f'torque ({torque_unit})'
            )
            first_column_axes[torques_variables_index].legend(
                title='torque',
                frameon=True
            )

        if forces_variables:
            for i, element in enumerate(elements, 0):
                if isinstance(element, GearBase | WormGear):
                    if element.tangential_force_is_computable:
                        if n_variables > 1:
                            axes = ax[:, i] if n_elements > 1 else ax
                        else:
                            axes = [ax[i]] if n_elements > 1 else [ax]
                        axes[forces_variables_index].set_ylabel(
                            f'force ({force_unit})'
                        )
                        break

        if stress_variables:
            for i, element in enumerate(elements, 0):
                if isinstance(element, GearBase):
                    if element.bending_stress_is_computable:
                        if n_variables > 1:
                            axes = ax[:, i] if n_elements > 1 else ax
                        else:
                            axes = [ax[i]] if n_elements > 1 else [ax]
                        axes[stress_variables_index].set_ylabel(
                            f'stress ({stress_unit})'
                        )
                        axes[stress_variables_index].legend(
                            title='stress',
                            frameon=True,
                            labels=stress_legend_items.keys(),
                            handles=stress_legend_items.values()
                        )
                        break

        if electric_variables:
            if isinstance(elements[0], MotorBase):
                if elements[0].electric_current_is_computable:
                    if n_variables > 1:
                        axes = ax[:, 0] if n_elements > 1 else ax
                    else:
                        axes = [ax[0]] if n_elements > 1 else [ax]
                    axes[electric_variables_index].set_ylabel(
                        f'electric current ({current_unit})'
                    )

        if pwm_variables:
            if isinstance(elements[0], MotorBase):
                if n_variables > 1:
                    axes = ax[:, 0] if n_elements > 1 else ax
                else:
                    axes = [ax[0]] if n_elements > 1 else [ax]
                axes[pwm_variables_index].set_ylabel('PWM')

        if n_elements > 1 or n_variables > 1:
            for axi in ax.flatten():
                axi.tick_params(
                    bottom=False,
                    top=False,
                    left=False,
                    right=False
                )
        else:
            ax.tick_params(bottom=False, top=False, left=False, right=False)

        plt.show()

    def export_time_variables(
        self,
        folder_path: str,
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
        """It exports the powertrain's :py:attr:`elements`' computed time
        variables to some files. \n
        It creates a file for each rotating object in the powertrain's
        :py:attr:`elements`. The file name is taken from the rotating object's
        ``name``. \n
        The exported files are a ``.csv`` files. The time variables are
        exported in a tabular form, in which each column is a time variable and
        each row is a simulated time step. The columns are separated by a
        comma. The first column reports the simulated time steps and the first
        row reports the column names.

        Parameters
        ----------
        ``folder_path`` : :py:class:`str`
            Path to the folder in which to save the time variables' files. It
            must be a non-empty :py:class:`str`.
        ``time_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the time values
            in the exported files. It must be a :py:class:`str`. Default is
            ``'sec'``. See :py:attr:`Time.unit <gearpy.units.units.Time.unit>`
            for more details.
        ``angular_position_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the angular
            position values in the exported files. It must be a
            :py:class:`str`. Default is ``'rad'``. See
            :py:attr:`AngularPosition.unit <gearpy.units.units.AngularPosition.unit>`
            for more details.
        ``angular_speed_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the angular
            speed values in the exported files. It must be a :py:class:`str`.
            Default is ``'rad/s'``. See
            :py:attr:`AngularSpeed.unit <gearpy.units.units.AngularSpeed.unit>`
            for more details.
        ``angular_acceleration_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the angular
            acceleration values in the exported files. It must be a
            :py:class:`str`. Default is ``'rad/s^2'``. See
            :py:attr:`AngularAcceleration.unit <gearpy.units.units.AngularAcceleration.unit>`
            for more details.
        ``torque_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the torque
            values in the exported files. It must be a :py:class:`str`. Default
            is ``'Nm'``. See
            :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
            details.
        ``driving_torque_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the driving
            torque values in the exported files. It must be a :py:class:`str`.
            Default is ``'Nm'``. See
            :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
            details.
        ``load_torque_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the load torque
            values in the exported files. It must be a :py:class:`str`. Default
            is ``'Nm'``. See
            :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
            details.
        ``force_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the force values
            in the exported files. It must be a :py:class:`str`. Default is
            ``'N'``. See :py:attr:`Force.unit <gearpy.units.units.Force.unit>`
            for more details.
        ``stress_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the stress
            values in the exported files. It must be a :py:class:`str`. Default
            is ``'MPa'``. See
            :py:attr:`Stress.unit <gearpy.units.units.Stress.unit>` for more
            details.
        ``current_unit`` : :py:class:`str`, optional
            Symbol of the unit of measurement to which convert the electric
            current values in the exported files. It must be a :py:class:`str`.
            Default is ``'A'``. See
            :py:attr:`Current.unit <gearpy.units.units.Current.unit>` for more
            details.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``folder_path`` is not a :py:class:`str`,
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
               If ``folder_path`` is an empty :py:class:`str`.
        """
        if not isinstance(folder_path, str):
            raise TypeError("Parameter 'folder_path' must be a string.")

        if not folder_path:
            raise ValueError(
                "Parameter 'folder_path' cannot be an empty string."
            )

        if not isinstance(time_unit, str):
            raise TypeError("Parameter 'time_unit' must be a string.")

        if not isinstance(angular_position_unit, str):
            raise TypeError(
                "Parameter 'angular_position_unit' must be a string."
            )

        if not isinstance(angular_speed_unit, str):
            raise TypeError(
                "Parameter 'angular_speed_unit' must be a string."
            )

        if not isinstance(angular_acceleration_unit, str):
            raise TypeError(
                "Parameter 'angular_acceleration_unit' must be a string."
            )

        if not isinstance(torque_unit, str):
            raise TypeError("Parameter 'torque_unit' must be a string.")

        if not isinstance(driving_torque_unit, str):
            raise TypeError(
                "Parameter 'driving_torque_unit' must be a string."
            )

        if not isinstance(load_torque_unit, str):
            raise TypeError("Parameter 'load_torque_unit' must be a string.")

        if not isinstance(force_unit, str):
            raise TypeError("Parameter 'force_unit' must be a string.")

        if not isinstance(stress_unit, str):
            raise TypeError("Parameter 'stress_unit' must be a string.")

        if not isinstance(current_unit, str):
            raise TypeError("Parameter 'current_unit' must be a string.")

        for element in self.elements:
            export_time_variables(
                rotating_object=element,
                file_path=os.path.join(folder_path, element.name),
                time_array=self.time,
                time_unit=time_unit,
                angular_position_unit=angular_position_unit,
                angular_speed_unit=angular_speed_unit,
                angular_acceleration_unit=angular_acceleration_unit,
                torque_unit=torque_unit,
                driving_torque_unit=driving_torque_unit,
                load_torque_unit=load_torque_unit,
                force_unit=force_unit,
                stress_unit=stress_unit,
                current_unit=current_unit
            )
