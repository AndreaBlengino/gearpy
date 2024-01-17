from collections import Counter
from gearpy.mechanical_object import MotorBase, RotatingObject, GearBase
from gearpy.units import Time
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
from typing import List, Tuple, Union, Optional


VARIABLES_SORT_ORDER = {'angular position': 0, 'angular speed': 1, 'angular acceleration': 2, 'torque': 3,
                        'driving torque': 4, 'load torque': 5, 'tangential force': 6, 'bending stress': 7,
                        'contact stress': 8, 'electric current': 9, 'pwm': 10}


class Transmission:
    r"""``gearpy.transmission.Transmission`` object.

    Attributes
    ----------
    :py:attr:`chain` : tuple
        Elements in the transmission chain.
    :py:attr:`time` : list
        Simulated time steps.

    Methods
    -------
    :py:meth:`plot`
        Plots time variables for each element in the mechanical transmission chain.
    :py:meth:`reset`
        Resets computed time variables.
    :py:meth:`snapshot`
        Computes a snapshot of the time variables of the elements in the mechanical transmission at the specified
        ``target_time``.
    :py:meth:`update_time`
        Updates the ``Transmission.time`` list by appending the ``instant`` simulated time step.

    Raises
    ------
    TypeError
        If ``motor`` parameter is not an instance of ``MotorBase``.
    ValueError
        If ``motor`` is not connected to any other element.
    NameError
        If two or more elements in the transmission chain share the same name.
    """

    def __init__(self, motor: MotorBase):
        if not isinstance(motor, MotorBase):
            raise TypeError(f"Parameter 'motor' must be an instance of {MotorBase.__name__!r}.")

        if motor.drives is None:
            raise ValueError("Parameter 'motor' is not connected to any other element. Call 'add_fixed_joint' "
                             "to join 'motor' with a GearBase's instance.")

        chain = [motor]
        while chain[-1].drives is not None:
            chain.append(chain[-1].drives)

        counts = Counter([element.name for element in chain])
        for name, count in counts.items():
            if count > 1:
                raise NameError(f"Found {count} elements with the same name {name!r}, "
                                f"each element must have a unique name.")

        self.__chain = tuple(chain)
        self.__time = []


    @property
    def chain(self) -> Tuple[RotatingObject]:
        """Elements in the transmission chain. \n
        The first element is the driving motor, the next elements are in order, from the closest to the farthest from
        the motor. Each element is driven by the previous one and it drives the following one.

        Returns
        -------
        tuple
            Elements in the transmission chain.

        See Also
        --------
        :py:class:`gearpy.mechanical_object.mechanical_objects.DCMotor`
        :py:class:`gearpy.mechanical_object.mechanical_objects.Flywheel`
        :py:class:`gearpy.mechanical_object.mechanical_objects.SpurGear`
        """
        return self.__chain


    @property
    def time(self) -> List[Time]:
        """List of the simulated time steps. \n
        During simulation, the solver appends a simulated time step to this list. \n
        Every element of this list must be an instance of ``gearpy.units.Time``.

        Returns
        -------
        list
            List of the simulated time steps.

        See Also
        --------
        :py:class:`gearpy.units.units.Time`
        :py:class:`gearpy.solver.Solver`
        """
        return self.__time


    def update_time(self, instant: Time):
        """Updates the ``Transmission.time`` list by appending the ``instant`` simulated time step.

        Parameters
        ----------
        instant : Time
            Simulated time step to be added to ``Transmission.time`` list.

        Raises
        ------
        TypeError
            If ``instant`` is not an instance of ``gearpy.units.Time``.

        See Also
        --------
        :py:attr:`time`
        """
        if not isinstance(instant, Time):
            raise TypeError(f"Parameter 'instant' must be instances of {Time.__name__!r}.")

        self.__time.append(instant)


    def reset(self):
        """Resets computed time variables. \n
        For each element in the mechanical transmission chain, it resets each time variables and also ``time`` property.

        See Also
        --------
        :py:attr:`time`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.time_variables`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.Flywheel.time_variables`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.SpurGear.time_variables`
        """
        self.__time = []

        for element in self.chain:
            element.angular_position = element.time_variables['angular position'][0]
            element.angular_speed = element.time_variables['angular speed'][0]
            element.angular_acceleration = element.time_variables['angular acceleration'][0]
            element.torque = element.time_variables['torque'][0]
            element.driving_torque = element.time_variables['driving torque'][0]
            element.load_torque = element.time_variables['load torque'][0]
            if isinstance(element, MotorBase):
                if element.electric_current_is_computable:
                    element.electric_current = element.time_variables['electric current'][0]
                element.pwm = element.time_variables['pwm'][0]
            if isinstance(element, GearBase):
                if element.tangential_force_is_computable:
                    element.tangential_force = element.time_variables['tangential force'][0]
                    if element.bending_stress_is_computable:
                        element.bending_stress = element.time_variables['bending stress'][0]
                        if element.contact_stress_is_computable:
                            element.contact_stress = element.time_variables['contact stress'][0]

            for variable in element.time_variables.keys():
                element.time_variables[variable] = []


    def snapshot(self,
                 target_time: Time,
                 variables: Optional[List[str]] = None,
                 angular_position_unit: Optional[str] = 'rad',
                 angular_speed_unit: Optional[str] = 'rad/s',
                 angular_acceleration_unit: Optional[str] = 'rad/s^2',
                 torque_unit: Optional[str] = 'Nm',
                 driving_torque_unit: Optional[str] = 'Nm',
                 load_torque_unit: Optional[str] = 'Nm',
                 force_unit: Optional[str] = 'N',
                 stress_unit: Optional[str] = 'MPa',
                 current_unit: Optional[str] = 'A',
                 print_data: Optional[bool] = True) -> pd.DataFrame:
        """Computes a snapshot of the time variables of the elements in the mechanical transmission at the specified
        ``target_time``. \n
        It returns a ``pandas.DataFrame`` with the computed time variables. Each element in the transmission chain is a
        row of the DataFrame, while the columns are the time variables ``'angular position'``, ``'angular speed'``,
        ``'angular acceleration'``, ``'torque'``, ``'driving torque'`` and ``'load torque'``. The motor can have
        additional variables ``'electric current'`` and ``'pwm'``, while gears can have additional parameters
        ``'tangential force'``, ``'bending stress'`` and ``'contact stress'``, depending on instantiation parameters. \n
        It is possible to select the variables to be printed with the ``variables`` list. \n
        Each time variable is converted to the relative unit passed as optional parameter. \n
        If the ``target_time`` is not among simulated time steps in the ``time`` list, it computes a linear
        interpolation from the two closest simulated time steps.

        Parameters
        ----------
        target_time : Time
            Time to which compute the mechanical transmission time variables snapshot. It must be within minimum and
            maximum simulated time steps in ``time`` parameter.
        variables : list, optional
            Time variables to be printed. Default is all available time variables.
        angular_position_unit : str, optional
            Symbol of the unit of measurement to which convert the angular position in the DataFrame. It must be a
            string. Default is ``'rad'``.
        angular_speed_unit : str, optional
            Symbol of the unit of measurement to which convert the angular speed in the DataFrame. It must be a string.
            Default is ``'rad/s'``.
        angular_acceleration_unit : str, optional
            Symbol of the unit of measurement to which convert the angular acceleration in the DataFrame. It must be a
            string. Default is ``'rad/s^2'``.
        torque_unit : str, optional
            Symbol of the unit of measurement to which convert the torque in the DataFrame. It must be a string. Default
            is ``'Nm'``.
        driving_torque_unit : str, optional
            Symbol of the unit of measurement to which convert the driving torque in the DataFrame. It must be a string.
            Default is ``'Nm'``.
        load_torque_unit : str, optional
            Symbol of the unit of measurement to which convert the load torque in the DataFrame. It must be a string.
            Default is ``'Nm'``.
        force_unit : str, optional
            Symbol of the unit of measurement to which convert the force values in the DataFrame. It must be a string.
            Default is ``'N'``.
        stress_unit : str, optional
            Symbol of the unit of measurement to which convert the stress values in the DataFrame. It must be a string.
            Default is ``'MPa'``.
        current_unit : str, optional
            Symbol of the unit of measurement to which convert the electric current values in the DataFrame. It must be
            a string. Default is ``'A'``.
        print_data : bool, optional
            Whether or not to print the computed time variables DataFrame. Default is ``True``.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing time variables values at the specified ``target_time`` for each element in the
            transmission chain.

        Raises
        ------
        TypeError
            - If an element of ``time`` is not an instance of ``Time``,
            - if ``target_time`` is not an instance of ``Time``,
            - if ``variables`` is not a list,
            - if an element of ``variables`` is not a string,
            - if ``angular_position_unit`` is not a string,
            - if ``angular_speed_unit`` is not a string,
            - if ``angular_acceleration_unit`` is not a string,
            - if ``torque_unit`` is not a string,
            - if ``driving_torque_unit`` is not a string,
            - if ``load_torque_unit`` is not a string,
            - if ``force_unit`` is not a string,
            - if ``stress_unit`` is not a string,
            - if ``current_unit`` is not a string,
            - if ``print_data`` is not a bool.
        ValueError
            - If ``time`` is an empty list,
            - if ``target_time`` is outside simulation interval,
            - if ``variables`` is an empty list,
            - if an element of ``variables`` is not a valid time variable.

        See Also
        --------
        :py:attr:`time`
        :py:attr:`chain`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.time_variables`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.Flywheel.time_variables`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.SpurGear.time_variables`
        """
        if not all([isinstance(instant, Time) for instant in self.time]):
            raise TypeError(f"Every element of the 'time' list must be an instance of {Time.__name__!r}.")

        if not self.time:
            raise ValueError("Parameter 'time' cannot be an empty list.")

        if not isinstance(target_time, Time):
            raise TypeError(f"Parameter 'target_time' must be an instance of {Time.__name__!r}.")

        if (target_time < min(self.time)) or (target_time > max(self.time)):
            raise ValueError(f"Parameter 'target_time' must be within simulation interval "
                             f"{min(self.time)} - {max(self.time)}.")

        if variables is not None:
            if not isinstance(variables, list):
                raise TypeError("Parameter 'variables' must be a list.")

            if not variables:
                raise ValueError("Parameter 'variables' cannot be an empty list.")

            valid_variables = []
            for element in self.chain:
                valid_variables.extend(element.time_variables.keys())
            valid_variables = list(set(valid_variables))
            valid_variables.sort(key = lambda variable: VARIABLES_SORT_ORDER[variable])
            for variable in variables:
                if not isinstance(variable, str):
                    raise TypeError("Each element of 'variables' must be a string.")

                if variable not in valid_variables:
                    raise ValueError(f"Invalid variable {variable!r}. Available variables are: {valid_variables}.")

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

        if not isinstance(print_data, bool):
            raise TypeError("Parameter 'print_data' must be a bool.")

        if variables is None:
            variables = []
            for element in self.chain:
                variables.extend(element.time_variables.keys())
        variables = list(set(variables))
        variables.sort(key = lambda variable: VARIABLES_SORT_ORDER[variable])

        UNITS = {'angular position': angular_position_unit, 'angular speed': angular_speed_unit,
                 'angular acceleration': angular_acceleration_unit, 'torque': torque_unit,
                 'driving torque': driving_torque_unit, 'load torque': load_torque_unit, 'tangential force': force_unit,
                 'bending stress': stress_unit, 'contact stress': stress_unit, 'electric current': current_unit,
                 'pwm': ''}

        columns = [f'{variable} ({UNITS[variable]})' if UNITS[variable] != '' else variable for variable in variables]
        data = pd.DataFrame(columns = columns)

        for element in self.chain:
            for variable, unit in zip(['angular position', 'angular speed', 'angular acceleration',
                                       'torque', 'driving torque', 'load torque'],
                                      [angular_position_unit, angular_speed_unit, angular_acceleration_unit,
                                       torque_unit, driving_torque_unit, load_torque_unit]):
                if variable in variables:
                    interpolation_function = interp1d(x = [instant.to('sec').value for instant in self.time],
                                                      y = [value.to(unit).value
                                                           for value in element.time_variables[variable]])
                    data.loc[element.name, f'{variable} ({unit})'] = interpolation_function(target_time.to('sec').value).take(0)

            if isinstance(element, MotorBase):
                interpolation_function = interp1d(x = [instant.to('sec').value for instant in self.time],
                                                  y = element.time_variables['pwm'])
                data.loc[element.name, 'pwm'] = interpolation_function(target_time.to('sec').value).take(0)

                if 'electric current' in variables:
                    if element.electric_current_is_computable:
                        interpolation_function = interp1d(x = [instant.to('sec').value for instant in self.time],
                                                          y = [value.to(current_unit).value
                                                               for value in element.time_variables['electric current']])
                        data.loc[element.name, f'electric current ({current_unit})'] = \
                            interpolation_function(target_time.to('sec').value).take(0)

            if isinstance(element, GearBase):
                variable_list = []
                unit_list  = []
                if element.tangential_force_is_computable and 'tangential force' in variables:
                    variable_list.append('tangential force')
                    unit_list.append(force_unit)
                    if element.bending_stress_is_computable and 'bending stress' in variables:
                        variable_list.append('bending stress')
                        unit_list.append(stress_unit)
                        if element.contact_stress_is_computable and 'contact stress' in variables:
                            variable_list.append('contact stress')
                            unit_list.append(stress_unit)

                for variable, unit in zip(variable_list, unit_list):
                    interpolation_function = interp1d(x = [instant.to('sec').value for instant in self.time],
                                                      y = [value.to(unit).value
                                                           for value in element.time_variables[variable]])
                    data.loc[element.name, f'{variable} ({unit})'] = interpolation_function(target_time.to('sec').value).take(0)

        data.fillna(value = '', inplace = True)

        if print_data:
            print(f'Mechanical Transmission Status at Time = {target_time}')
            print(data.to_string())

        return data


    def plot(self,
             elements: Optional[List[Union[RotatingObject, str]]] = None,
             variables: Optional[List[str]] = None,
             angular_position_unit: Optional[str] = 'rad',
             angular_speed_unit: Optional[str] = 'rad/s',
             angular_acceleration_unit: Optional[str] = 'rad/s^2',
             torque_unit: Optional[str] = 'Nm',
             force_unit: Optional[str] = 'N',
             stress_unit: Optional[str] = 'MPa',
             current_unit: Optional[str] = 'A',
             time_unit: Optional[str] = 'sec',
             figsize: Optional[tuple] = None):
        """Plots time variables for selected elements in the mechanical transmission chain. \n
        It generates a grid of subplots, one column for each selected element of the transmission chain and one rows for
        each selected time variable. \n
        The available elements are those in ``chain`` tuple and the available variables are: ``'angular position'``,
        ``'angular speed'``, ``'angular acceleration'``, ``'torque'``, ``'driving torque'`` and ``'load torque'``. The
        motor can have additional variables ``electric current`` and ``pwm`` while gears can have additional variables
        ``tangential force``, ``bending stress`` and ``contact stress``, depending on instantiation parameters. \n
        The time variables are plotted in the described order, from the top row to the bottom one; torques are grouped
        together in a single row as well as stresses are grouped together.
        Plotted values' units are managed with optional parameters. \n
        Elements to be plotted can be passed as instances or names (strings) in a list.

        Parameters
        ----------
        elements : list, optional
            Elements of the transmission chain which time variables have to be plotted. Each single element can be
            passed as instance or name (string). Default is all elements in the transmission chain.
        variables : list, optional
            Time variables to be plotted. Default is all available time variables.
        angular_position_unit : str, optional
            Symbol of the unit of measurement to which convert the angular position values in the plot. It must be a
            string. Default is ``'rad'``.
        angular_speed_unit : str, optional
            Symbol of the unit of measurement to which convert the angular speed values in the plot. It must be a
            string. Default is ``'rad/s'``.
        angular_acceleration_unit : str, optional
            Symbol of the unit of measurement to which convert the angular acceleration values in the plot. It must be a
            string. Default is ``'rad/s^2'``.
        torque_unit : str, optional
            Symbol of the unit of measurement to which convert the torque values in the plot. It must be a string.
            Default is ``'Nm'``.
        force_unit : str, optional
            Symbol of the unit of measurement to which convert the force values in the plot. It must be a string.
            Default is ``'N'``.
        stress_unit : str, optional
            Symbol of the unit of measurement to which convert the stress values in the plot. It must be a string.
            Default is ``'MPa'``.
        current_unit : str, optional
            Symbol of the unit of measurement to which convert the electric current values in the plot. It must be a
            string. Default is ``'A'``.
        time_unit : str, optional
            Symbol of the unit of measurement to which convert the time values in the plot. It must be a string. Default
            is ``'sec'``.
        figsize : tuple, optional
            Width and height of the window size, in inches. If not provided defaults to ``[6.4, 4.8]``.

        Raises
        ------
        TypeError
            - If ``elements`` is not a list,
            - if an element of ``elements`` is not an instance of ``RotatingObject`` or a string,
            - if ``variables`` is not a list,
            - if an element of ``variables`` is not a string,
            - if ``angular_position_unit`` is not a string,
            - if ``angular_speed_unit`` is not a string,
            - if ``angular_acceleration_unit`` is not a string,
            - if ``torque_unit`` is not a string,
            - if ``force_unit`` is not a string,
            - if ``stress_unit`` is not a string,
            - if ``current_unit`` is not a string,
            - if ``time_unit`` is not a string,
            - if ``figsize`` is not a tuple,
            - if an element of ``figsize`` is not a float or an integer.
        ValueError
            - If ``elements`` is an empty list,
            - if an element of ``elements`` is not in ``Transmission.chain``,
            - if ``variables`` is an empty list,
            - if an element of ``variables`` is not a valid time variable,
            - if ``figsize`` has not exactly two elements: one for width and the other for height.

        See Also
        --------
        :py:attr:`time`
        :py:attr:`chain`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.time_variables`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.Flywheel.time_variables`
        :py:attr:`gearpy.mechanical_object.mechanical_objects.SpurGear.time_variables`
        """
        if elements is not None:
            if not isinstance(elements, list):
                raise TypeError("Parameter 'elements' must be a list.")

            if not elements:
                raise ValueError("Parameter 'elements' cannot be an empty list.")

            valid_element_names = [valid_element.name for valid_element in self.chain]
            for element in elements:
                if not isinstance(element, RotatingObject) and not isinstance(element, str):
                    raise TypeError(f"Each element of 'elements' must be an instance of {RotatingObject.__name__!r}"
                                    f"or a string.")

                if isinstance(element, RotatingObject):
                    if element not in self.chain:
                        raise ValueError(f"Element {element.name!r} not found in the transmission chain. "
                                         f"Available elements are: {valid_element_names}.")
                else:
                    if element not in valid_element_names:
                        raise ValueError(f"Element {element!r} not found in the transmission chain. "
                                         f"Available elements are: {valid_element_names}.")

        if variables is not None:
            if not isinstance(variables, list):
                raise TypeError("Parameter 'variables' must be a list.")

            if not variables:
                raise ValueError("Parameter 'variables' cannot be an empty list.")

            valid_variables = []
            for element in self.chain:
                valid_variables.extend(element.time_variables.keys())
            valid_variables = list(set(valid_variables))
            valid_variables.sort(key = lambda variable: VARIABLES_SORT_ORDER[variable])
            for variable in variables:
                if not isinstance(variable, str):
                    raise TypeError("Each element of 'variables' must be a string.")

                if variable not in valid_variables:
                    raise ValueError(f"Invalid variable {variable!r}. Available variables are: {valid_variables}.")

        if not isinstance(angular_position_unit, str):
            raise TypeError("Parameter 'angular_position_unit' must be a string.")

        if not isinstance(angular_speed_unit, str):
            raise TypeError("Parameter 'angular_speed_unit' must be a string.")

        if not isinstance(angular_acceleration_unit, str):
            raise TypeError("Parameter 'angular_acceleration_unit' must be a string.")

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
                raise ValueError("Parameter 'figsize' must contain two values, one for width and one for height.")

            if not all([isinstance(dimension, float) or isinstance(dimension, int) for dimension in figsize]):
                raise TypeError("All elements of 'figsize' must be floats or integers.")

        if elements is None:
            elements = self.chain
        else:
            elements = [element for element in self.chain if element in elements or element.name in elements]
        n_elements = len(elements)

        if variables is None:
            variables = []
            for element in elements:
                variables.extend(element.time_variables.keys())
        variables = list(set(variables))
        variables.sort(key = lambda variable: VARIABLES_SORT_ORDER[variable])

        kinematic_variables = [variable for variable in variables
                               if 'torque' not in variable and 'force' not in variable
                               and 'stress' not in variable and 'electric' not in variable and 'pwm' not in variable]
        torques_variables = [variable for variable in variables if 'torque' in variable]
        forces_variables = [variable for variable in variables if 'force' in variable]
        stress_variables = [variable for variable in variables if 'stress' in variable]
        electric_variables = [variable for variable in variables if 'electric' in variable]
        pwm_variables = [variable for variable in variables if 'pwm' in variable]

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

        UNITS = {'angular position': angular_position_unit, 'angular speed': angular_speed_unit,
                 'angular acceleration': angular_acceleration_unit, 'torque': torque_unit,
                 'driving torque': torque_unit, 'load torque': torque_unit, 'tangential force': force_unit,
                 'bending stress': stress_unit, 'contact stress': stress_unit, 'electric current': current_unit,
                 'pwm': ''}

        fig, ax = plt.subplots(nrows = n_variables, ncols = n_elements, sharex = 'all',
                               layout = 'constrained', figsize = figsize)

        for i, item in enumerate(elements, 0):
            if n_variables > 1:
                axes = ax[:, i] if n_elements > 1 else ax
            else:
                axes = [ax[i]] if n_elements > 1 else [ax]
            axes[0].set_title(item.name)

            for j, variable in enumerate(kinematic_variables, 0):
                axes[j].plot(time_values, [variable_value.to(UNITS[variable]).value
                                           for variable_value in item.time_variables[variable]])

            for variable in torques_variables:
                label = variable.replace('torque', '').replace(' ', '')
                label = 'net' if label == '' else label
                axes[torques_variables_index].plot(time_values,
                                                   [variable_value.to(UNITS[variable]).value
                                                    for variable_value in item.time_variables[variable]],
                                                   label = label)

            if isinstance(item, MotorBase):
                if item.electric_current_is_computable and electric_variables:
                    axes[electric_variables_index].plot(time_values,
                                                          [variable_value.to(UNITS['electric current']).value
                                                           for variable_value in item.time_variables['electric current']])

                if pwm_variables:
                    axes[pwm_variables_index].plot(time_values,
                                                   item.time_variables['pwm'])

            else:
                if electric_variables:
                    axes[electric_variables_index].axis('off')
                if pwm_variables:
                    axes[pwm_variables_index].axis('off')

            if isinstance(item, GearBase):
                if item.tangential_force_is_computable:
                    for variable in forces_variables:
                        axes[forces_variables_index].plot(time_values,
                                                          [variable_value.to(UNITS[variable]).value
                                                           for variable_value in item.time_variables[variable]])

                    for variable in stress_variables:
                        if (variable == 'bending stress' and item.bending_stress_is_computable) or \
                                (variable == 'contact stress' and item.contact_stress_is_computable):
                            axes[stress_variables_index].plot(time_values,
                                                              [variable_value.to(UNITS[variable]).value
                                                               for variable_value in item.time_variables[variable]],
                                                              label = variable.replace('stress', '').replace(' ', ''))

                        if stress_variables \
                                and not item.bending_stress_is_computable and not item.contact_stress_is_computable:
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
            if isinstance(item, MotorBase):
                pass
            elif isinstance(item, GearBase):
                if forces_variables and not item.tangential_force_is_computable:
                    last_row_index -= 1
                if stress_variables and \
                        (not item.bending_stress_is_computable or 'bending stress' not in stress_variables) and \
                        (not item.contact_stress_is_computable or 'contact stress' not in stress_variables):
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
            axes[last_row_index].xaxis.set_tick_params(which = 'both', labelbottom = True)

        if n_variables > 1:
            first_column_axes = ax[:, 0] if n_elements > 1 else ax
        else:
            first_column_axes = [ax[0]] if n_elements > 1 else [ax]

        for j, variable in enumerate(kinematic_variables, 0):
            first_column_axes[j].set_ylabel(f'{variable} ({UNITS[variable]})')

        if torques_variables:
            first_column_axes[torques_variables_index].set_ylabel(f'torque ({torque_unit})')
            first_column_axes[torques_variables_index].legend(title = 'torque', frameon = True)

        if forces_variables:
            for i, item in enumerate(elements, 0):
                if isinstance(item, GearBase):
                    if item.tangential_force_is_computable:
                        if n_variables > 1:
                            axes = ax[:, i] if n_elements > 1 else ax
                        else:
                            axes = [ax[i]] if n_elements > 1 else [ax]
                        axes[forces_variables_index].set_ylabel(f'force ({force_unit})')
                        break

        if stress_variables:
            for i, item in enumerate(elements, 0):
                if isinstance(item, GearBase):
                    if item.bending_stress_is_computable:
                        if n_variables > 1:
                            axes = ax[:, i] if n_elements > 1 else ax
                        else:
                            axes = [ax[i]] if n_elements > 1 else [ax]
                        axes[stress_variables_index].set_ylabel(f'stress ({stress_unit})')
                        axes[stress_variables_index].legend(title = 'stress', frameon = True)
                        break

        if electric_variables:
            if isinstance(elements[0], MotorBase):
                if elements[0].electric_current_is_computable:
                    if n_variables > 1:
                        axes = ax[:, 0] if n_elements > 1 else ax
                    else:
                        axes = [ax[0]] if n_elements > 1 else [ax]
                    axes[electric_variables_index].set_ylabel(f'electric current ({current_unit})')

        if pwm_variables:
            if isinstance(elements[0], MotorBase):
                if n_variables > 1:
                    axes = ax[:, 0] if n_elements > 1 else ax
                else:
                    axes = [ax[0]] if n_elements > 1 else [ax]
                axes[pwm_variables_index].set_ylabel('PWM')

        if n_elements > 1 or n_variables > 1:
            for axi in ax.flatten():
                axi.tick_params(bottom = False, top = False, left = False, right = False)
        else:
            ax.tick_params(bottom = False, top = False, left = False, right = False)

        plt.show()
