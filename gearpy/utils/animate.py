from gearpy.mechanical_object import DCMotor
from gearpy.units import Time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Optional, Union


def dc_motor_characteristics_animation(motor: DCMotor,
                                       time: List[Time],
                                       interval: Optional[Union[float, int]] = 200,
                                       torque_speed_curve: Optional[bool] = True,
                                       torque_current_curve: Optional[bool] = True,
                                       angular_speed_unit: Optional[str] = 'rad/s',
                                       torque_unit: Optional[str] = 'Nm',
                                       current_unit: Optional[str] = 'A',
                                       figsize: Optional[tuple] = None,
                                       line_color: Optional[str] = None,
                                       marker_color: Optional[str] = None,
                                       marker_size: Optional[Union[float, int]] = None,
                                       padding: Optional[Union[float, int]] = 0.1,
                                       show: Optional[bool] = True) -> FuncAnimation:
    """Generates an animation of a DC motor torque-speed and torque-current characteristic curves and relative working
    points during the simulation. \n
    Each simulated time step is a frame on the animation. \n
    It generates two subplots, one for each characteristic curve. It is possible to isolate a single characteristic to
    be plotted with optional parameters ``torque_speed_curve`` and ``torque_current_curve``. \n
    The characteristic curves can be modified by the motor pulse width modulation ``pwm``. \n
    Plotted values' units are managed with optional parameters ``angular_speed_unit``, ``torque_unit`` and
    ``current_unit``. \n
    Aesthetic parameters are managed with optional parameters ``figsize``, ``line_color``, ``marker_color``,
    ``marker_size`` and  ``padding``.

    Parameters
    ----------
    motor : DCMotor
        DC motor whose characteristic curves and working point have to be animated.
    time : list
        List of ``Time`` computed by the solver.
    interval : float or int, optional
        Delay between animation frames in milliseconds. If not provided defaults to ``200``.
    torque_speed_curve : bool, optional
        Whether or not to plot the torque-speed characteristic curve. Default is ``True``.
    torque_current_curve : bool, optional
        Whether or not to plot the torque-current characteristic curve. Default is ``True``.
    angular_speed_unit : str, optional
        Symbol of the unit of measurement to which convert the angular speed values in the plot. It must be a string.
        Default is ``'rad/s'``.
    torque_unit : str, optional
        Symbol of the unit of measurement to which convert the torque values in the plot. It must be a string. Default
        is ``'Nm'``.
    current_unit : str, optional
        Symbol of the unit of measurement to which convert the electric current values in the plot. It must be a string.
        Default is ``'A'``.
    figsize : tuple, optional
        Width and height of the window size, in inches. If not provided defaults to ``[6.4, 4.8]``.
    line_color : str, optional
        Color of the characteristic curve lines. If not provided defaults to ``'#1f77b4'``.
    marker_color : str, optional
        Color of the motor working point marker. If not provided defaults to ``'#ff7f0e'``.
    marker_size : float or int, optional
        Size, in points, of the motor working point marker. If not provided defaults to ``6``.
    padding : float or int, optional
        Extra-space to be taken around each motor characteristics extreme points. It is expressed in percent points of
        the extreme point value. Default is ``0.1``, so it is taken 10% space around each characteristic extreme points.
    show : bool, optional
        Whether or not to show the animation. Default is ``True``.

    Raises
    ------
    TypeError
        - If ``motor`` is not an instance of ``DCMotor``,
        - if ``time`` is not a list,
        - if an element of ``time`` is not an instance of ``Time``,
        - if ``interval`` is not a float or an integer,
        - if ``torque_speed_curve`` is not a bool,
        - if ``torque_current_curve`` is not a bool,
        - if ``angular_speed_unit`` is not a string,
        - if ``torque_unit`` is not a string,
        - if ``current_unit`` is not a string,
        - if ``figsize`` is not a tuple,
        - if an element of ``figsize`` is not a float or an integer,
        - if ``line_color`` is not a string,
        - if ``marker_color`` is not a string,
        - if ``marker_size`` is not a float or an integer,
        - if ``padding`` is not a float or an integer,
        - if ``show`` is not a bool.
    ValueError
        - If ``time`` is an empty list,
        - if both ``torque_speed_curve`` and ``torque_current_curve`` are set to ``False``,
        - if ``torque_current_curve`` is set to ``True`` but ``motor`` cannot compute ``electric_current`` property,
        - if ``figsize`` has not exactly two elements: one for width and the other for height,
        - if ``padding`` is negative.

    See Also
    --------
    :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.angular_speed`
    :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.driving_torque`
    :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.electric_current`
    :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.time_variables`
    :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.pwm`
    """
    if not isinstance(motor, DCMotor):
        raise TypeError(f"Parameter 'motor' must be an instance of {DCMotor.__name__!r}.")

    if not isinstance(time, list):
        raise TypeError("Parameter 'time' must be a list.")

    if not time:
        raise ValueError("Parameter 'time' cannot be an empty list.")

    if not all([isinstance(instant, Time) for instant in time]):
            raise TypeError(f"Each element of 'time' must be an instance of {Time.__name__!r}.")

    if not isinstance(interval, float) and not isinstance(interval, int):
        raise TypeError("Parameter 'interval' must be a float or an integer.")

    if not isinstance(torque_speed_curve, bool):
        raise TypeError("Parameter 'torque_speed_curve' must be a bool.")

    if not isinstance(torque_current_curve, bool):
        raise TypeError("Parameter 'torque_current_curve' must be a bool.")

    if not torque_speed_curve and not torque_current_curve:
        raise ValueError("At least one of 'torque_speed_curve' and 'torque_current_curve' must be set to 'True'.")

    if torque_current_curve and not motor.electric_current_is_computable:
        raise ValueError("Parameter 'torque_current_curve' set to 'True', "
                         "but 'motor' cannot compute 'electric_current' property.")

    if not isinstance(angular_speed_unit, str):
        raise TypeError("Parameter 'angular_speed_unit' must be a string.")

    if not isinstance(torque_unit, str):
        raise TypeError("Parameter 'torque_unit' must be a string.")

    if not isinstance(current_unit, str):
        raise TypeError("Parameter 'current_unit' must be a string.")

    if figsize is not None:
        if not isinstance(figsize, tuple):
            raise TypeError("Parameter 'figsize' must be a tuple.")

        if len(figsize) != 2:
            raise ValueError("Parameter 'figsize' must contain two values, one for width and one for height.")

        if not all([isinstance(dimension, float) or isinstance(dimension, int) for dimension in figsize]):
            raise TypeError("All elements of 'figsize' must be floats or integers.")

    if line_color is not None:
        if not isinstance(line_color, str):
            raise TypeError("Parameter 'line_color' must be a string.")

    if marker_color is not None:
        if not isinstance(marker_color, str):
            raise TypeError("Parameter 'marker_color' must be a string.")

    if marker_size is not None:
        if not isinstance(marker_size, float) and not isinstance(marker_size, int):
            raise TypeError("Parameter 'marker_size' must be a float or an integer.")

    if not isinstance(padding, float) and not isinstance(padding, int):
        raise TypeError("Parameter 'padding' must be a float or an integer.")

    if padding < 0:
        raise ValueError("Parameter 'padding' must be positive or null.")

    if not isinstance(show, bool):
        raise TypeError("Parameter 'show' must be a bool.")

    fig, ax = plt.subplots(ncols = torque_speed_curve + torque_current_curve, nrows = 1,
                           sharey = 'all', figsize = figsize)

    motor_maximum_torque = motor.maximum_torque.to(torque_unit).value

    motor_instant_driving_torque = [torque.to(torque_unit).value
                                    for torque in motor.time_variables['driving torque']]

    total_padding = 1 + padding


    if torque_speed_curve:
        motor_instant_angular_speed = [speed.to(angular_speed_unit).value
                                       for speed in motor.time_variables['angular speed']]
        motor_no_speed = motor.no_load_speed.to(angular_speed_unit).value
        speeds = [-total_padding*motor_no_speed, total_padding*motor_no_speed]

        def compute_torque_speed_curve(maximum_torque, no_load_speed):
            return [maximum_torque*(1 - speed/no_load_speed) for speed in speeds]

        def compute_torque_speed_torques(i):
            if not motor.electric_current_is_computable:
                torques = compute_torque_speed_curve(maximum_torque = motor_maximum_torque,
                                                     no_load_speed = motor_no_speed)
                title = f'time = {time[i]}'
            else:
                pwm = motor.time_variables['pwm'][i]
                pwm_min = motor.no_load_electric_current/motor.maximum_electric_current
                if abs(pwm) <= pwm_min:
                    torques = [0, 0]
                elif pwm > pwm_min:
                    maximum_torque = \
                        motor.maximum_torque*((pwm*motor.maximum_electric_current - motor.no_load_electric_current)/
                                              (motor.maximum_electric_current - motor.no_load_electric_current))
                    no_load_speed = pwm*motor.no_load_speed

                    torques = compute_torque_speed_curve(maximum_torque = maximum_torque.to(torque_unit).value,
                                                         no_load_speed = no_load_speed.to(angular_speed_unit).value)
                else:
                    maximum_torque = \
                        motor.maximum_torque*((pwm*motor.maximum_electric_current + motor.no_load_electric_current)/
                                              (motor.maximum_electric_current - motor.no_load_electric_current))
                    no_load_speed = pwm*motor.no_load_speed

                    torques = compute_torque_speed_curve(maximum_torque = maximum_torque.to(torque_unit).value,
                                                         no_load_speed = no_load_speed.to(angular_speed_unit).value)
                title = f'time = {time[i]}      PWM = {pwm:.2f}'

            return torques, title

        torques, title = compute_torque_speed_torques(i = 0)

        ax_ts = ax[0] if torque_current_curve else ax

        ax_ts.axhline(y = 0, color = 'black', linewidth = 0.5)
        ax_ts.axvline(x = 0, color = 'black', linewidth = 0.5)

        line_ts, = ax_ts.plot(speeds, torques, color = line_color)

        point_ts, = ax_ts.plot(motor_instant_angular_speed[0], motor_instant_driving_torque[0],
                               marker = 'o', markerfacecolor = marker_color, markeredgecolor = marker_color,
                               markersize = marker_size)

        ax_ts.set_xlabel(f'angular speed ({angular_speed_unit})')
        ax_ts.set_ylabel(f'torque ({torque_unit})')

        ax_ts.set_xlim(-total_padding*motor_no_speed, total_padding*motor_no_speed)
        ax_ts.set_ylim(-total_padding*motor_maximum_torque, total_padding*motor_maximum_torque)

        ax_ts.tick_params(bottom = False, top = False, left = False, right = False)


    if torque_current_curve:
        motor_instant_electric_current = [current.to(current_unit).value
                                          for current in motor.time_variables['electric current']]
        motor_no_load_electric_current = motor.no_load_electric_current.to(current_unit).value
        motor_maximum_electric_current = motor.maximum_electric_current.to(current_unit).value
        currents = [-total_padding*motor_maximum_electric_current, total_padding*motor_maximum_electric_current]

        def compute_torque_current_curve(maximum_torque, no_load_electric_current, maximum_electric_current):
            return [maximum_torque/(maximum_electric_current - no_load_electric_current)*
                                   (current - no_load_electric_current) for current in currents]

        def compute_torque_current_torques(i):
            pwm = motor.time_variables['pwm'][i]
            pwm_min = motor.no_load_electric_current/motor.maximum_electric_current
            if abs(pwm) <= pwm_min:
                torques = [0, 0]
            elif pwm > pwm_min:
                torques = compute_torque_current_curve(maximum_torque = motor_maximum_torque,
                                                       no_load_electric_current = motor_no_load_electric_current,
                                                       maximum_electric_current = motor_maximum_electric_current)
            else:
                torques = compute_torque_current_curve(maximum_torque = -motor_maximum_torque,
                                                       no_load_electric_current = -motor_no_load_electric_current,
                                                       maximum_electric_current = -motor_maximum_electric_current)
            title = f'time = {time[i]}      PWM = {pwm:.2f}'

            return torques, title

        torques, title = compute_torque_current_torques(i = 0)

        ax_tc = ax[1] if torque_speed_curve else ax

        ax_tc.axhline(y = 0, color = 'black', linewidth = 0.5)
        ax_tc.axvline(x = 0, color = 'black', linewidth = 0.5)

        line_tc, = ax_tc.plot(currents, torques, color = line_color)

        point_tc, = ax_tc.plot(motor_instant_electric_current[0], motor_instant_driving_torque[0],
                               marker = 'o', markerfacecolor = marker_color, markeredgecolor = marker_color,
                               markersize = marker_size)

        ax_tc.set_xlabel(f'electric current ({current_unit})')
        ax_tc.set_ylabel(f'torque ({torque_unit})')

        ax_tc.set_xlim(-total_padding*motor_maximum_electric_current, total_padding*motor_maximum_electric_current)

        ax_tc.tick_params(bottom = False, top = False, left = False, right = False)


    fig.suptitle(title)
    plt.tight_layout()


    def update_animation(i):

        if torque_speed_curve:
            torques, title = compute_torque_speed_torques(i = i)
            line_ts.set_data(speeds, torques)
            point_ts.set_data([motor_instant_angular_speed[i]], [motor_instant_driving_torque[i]])

        if torque_current_curve:
            torques, title = compute_torque_current_torques(i = i)
            line_tc.set_data(currents, torques)
            point_tc.set_data([motor_instant_electric_current[i]], [motor_instant_driving_torque[i]])

        fig.suptitle(title)

        if torque_speed_curve and torque_current_curve:
            return line_ts, point_ts, line_tc, point_tc,
        elif torque_speed_curve and not torque_current_curve:
            return line_ts, point_ts,
        else:
            return line_tc, point_tc,


    animation = FuncAnimation(func = update_animation, fig = fig, frames = range(1, len(time), 1), interval = interval)

    if show:
        plt.show()

    return animation
