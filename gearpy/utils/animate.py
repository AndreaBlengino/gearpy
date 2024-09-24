from gearpy.mechanical_objects import DCMotor
from gearpy.units import Time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Optional


def dc_motor_characteristics_animation(
    motor: DCMotor,
    time: list[Time],
    interval: Optional[float | int] = 200,
    torque_speed_curve: Optional[bool] = True,
    torque_current_curve: Optional[bool] = True,
    angular_speed_unit: Optional[str] = 'rad/s',
    torque_unit: Optional[str] = 'Nm',
    current_unit: Optional[str] = 'A',
    figsize: Optional[tuple] = None,
    line_color: Optional[str] = None,
    marker_color: Optional[str] = None,
    marker_size: Optional[float | int] = None,
    padding: Optional[float | int] = 0.1,
    show: Optional[bool] = True
) -> FuncAnimation:
    """It generates an animation of a
    :py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>`
    torque-speed and torque-current characteristic curves and relative working
    points during the simulation. \n
    Each simulated time step is a frame on the animation. \n
    It generates two subplots, one for each characteristic curve. It is
    possible to isolate a single characteristic to be plotted with optional
    parameters ``torque_speed_curve`` and ``torque_current_curve``. \n
    The characteristic curves can be modified by the motor pulse width
    modulation
    :py:attr:`DCMotor.pwm <gearpy.mechanical_objects.dc_motor.DCMotor.pwm>`. \n
    Plotted values' units are managed with optional parameters
    ``angular_speed_unit``, ``torque_unit`` and ``current_unit``. \n
    Aesthetic parameters are managed with optional parameters ``figsize``,
    ``line_color``, ``marker_color``, ``marker_size`` and  ``padding``.

    Parameters
    ----------
    ``motor`` : :py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>`
        DC motor whose characteristic curves and working point have to be
        animated.
    ``time`` : :py:class:`list`
        The list of ``Time`` computed by the solver.
    ``interval`` : :py:class:`float` or :py:class:`int`, optional
        Delay between animation frames in milliseconds. If not provided
        defaults to ``200``.
    ``torque_speed_curve`` : :py:class:`bool`, optional
        Whether to plot the torque-speed characteristic curve. Default is
        ``True``.
    ``torque_current_curve`` : :py:class:`bool`, optional
        Whether to plot the torque-current characteristic curve. Default is
        ``True``.
    ``angular_speed_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the angular speed
        values in the plot. It must be a string. Default is ``'rad/s'``. See
        :py:attr:`AngularSpeed.unit <gearpy.units.units.AngularSpeed.unit>` for
        more details.
    ``torque_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the torque values in
        the plot. It must be a string. Default is ``'Nm'``. See
        :py:attr:`Torque.unit <gearpy.units.units.Torque.unit>` for more
        details.
    ``current_unit`` : :py:class:`str`, optional
        Symbol of the unit of measurement to which convert the electric current
        values in the plot. It must be a string. Default is ``'A'``. See
        :py:attr:`Current.unit <gearpy.units.units.Current.unit>` for more
        details.
    ``figsize`` : :py:class:`tuple`, optional
        Width and height of the window size, in inches. If not provided
        defaults to ``[6.4, 4.8]``.
    ``line_color`` : :py:class:`str`, optional
        Color of the characteristic curve lines. If not provided defaults to
        ``'#1f77b4'``.
    ``marker_color`` : :py:class:`str`, optional
        Color of the motor working point marker. If not provided defaults to
        ``'#ff7f0e'``.
    ``marker_size`` : :py:class:`float` or :py:class:`int`, optional
        Size, in points, of the motor working point marker. If not provided
        defaults to ``6``.
    ``padding`` : :py:class:`float` or :py:class:`int`, optional
        Extra-space to be taken around each motor characteristics extreme
        points. It is expressed in percent points of
        the extreme point value. Default is ``0.1``, so it is taken 10% space
        around each characteristic extreme points.
    ``show`` : :py:class:`bool`, optional
        Whether to show the animation. Default is ``True``.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``motor`` is not an instance of
             :py:class:`DCMotor <gearpy.mechanical_objects.dc_motor.DCMotor>`,
           - if ``time`` is not a :py:class:`list`,
           - if an element of ``time`` is not an instance of
             :py:class:`Time <gearpy.units.units.Time>`,
           - if ``interval`` is not a :py:class:`float` or an :py:class:`int`,
           - if ``torque_speed_curve`` is not a :py:class:`bool`,
           - if ``torque_current_curve`` is not a :py:class:`bool`,
           - if ``angular_speed_unit`` is not a :py:class:`str`,
           - if ``torque_unit`` is not a :py:class:`str`,
           - if ``current_unit`` is not a :py:class:`str`,
           - if ``figsize`` is not a :py:class:`tuple`,
           - if an element of ``figsize`` is not a :py:class:`float` or an
             :py:class:`int`,
           - if ``line_color`` is not a :py:class:`str`,
           - if ``marker_color`` is not a :py:class:`str`,
           - if ``marker_size`` is not a :py:class:`float` or an
             :py:class:`int`,
           - if ``padding`` is not a :py:class:`float` or an :py:class:`int`,
           - if ``show`` is not a :py:class:`bool`.
       ``ValueError``
           - If ``time`` is an empty :py:class:`list`,
           - if both ``torque_speed_curve`` and ``torque_current_curve`` are
             set to ``False``,
           - if ``torque_current_curve`` is set to ``True`` but ``motor``
             cannot compute
             :py:attr:`DCMotor.electric_current <gearpy.mechanical_objects.dc_motor.DCMotor.electric_current>`
             property,
           - if ``figsize`` has not exactly two elements: one for width and the
             other for height,
           - if ``padding`` is negative.

    .. admonition:: See Also
       :class: seealso

       :py:attr:`DCMotor.angular_speed <gearpy.mechanical_objects.dc_motor.DCMotor.angular_speed>` \n
       :py:attr:`DCMotor.driving_torque <gearpy.mechanical_objects.dc_motor.DCMotor.driving_torque>` \n
       :py:attr:`DCMotor.electric_current <gearpy.mechanical_objects.dc_motor.DCMotor.electric_current>` \n
       :py:attr:`DCMotor.time_variables <gearpy.mechanical_objects.dc_motor.DCMotor.time_variables>` \n
       :py:attr:`DCMotor.pwm <gearpy.mechanical_objects.dc_motor.DCMotor.pwm>`
    """
    if not isinstance(motor, DCMotor):
        raise TypeError(
            f"Parameter 'motor' must be an instance of {DCMotor.__name__!r}."
        )

    if not isinstance(time, list):
        raise TypeError("Parameter 'time' must be a list.")

    if not time:
        raise ValueError("Parameter 'time' cannot be an empty list.")

    if not all([isinstance(instant, Time) for instant in time]):
        raise TypeError(
            f"Each element of 'time' must be an instance of {Time.__name__!r}."
        )

    if not isinstance(interval, float | int):
        raise TypeError("Parameter 'interval' must be a float or an integer.")

    if not isinstance(torque_speed_curve, bool):
        raise TypeError("Parameter 'torque_speed_curve' must be a bool.")

    if not isinstance(torque_current_curve, bool):
        raise TypeError("Parameter 'torque_current_curve' must be a bool.")

    if not torque_speed_curve and not torque_current_curve:
        raise ValueError(
            "At least one of 'torque_speed_curve' and 'torque_current_curve' "
            "must be set to 'True'."
        )

    if torque_current_curve and not motor.electric_current_is_computable:
        raise ValueError(
            "Parameter 'torque_current_curve' set to 'True', but 'motor' "
            "cannot compute 'electric_current' property."
        )

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
            raise ValueError(
                "Parameter 'figsize' must contain two values, one for width "
                "and one for height."
            )

        if not all(
            [isinstance(dimension, float | int) for dimension in figsize]
        ):
            raise TypeError(
                "All elements of 'figsize' must be floats or integers."
            )

    if line_color is not None:
        if not isinstance(line_color, str):
            raise TypeError("Parameter 'line_color' must be a string.")

    if marker_color is not None:
        if not isinstance(marker_color, str):
            raise TypeError("Parameter 'marker_color' must be a string.")

    if marker_size is not None:
        if not isinstance(marker_size, float | int):
            raise TypeError(
                "Parameter 'marker_size' must be a float or an integer."
            )

    if not isinstance(padding, float | int):
        raise TypeError("Parameter 'padding' must be a float or an integer.")

    if padding < 0:
        raise ValueError("Parameter 'padding' must be positive or null.")

    if not isinstance(show, bool):
        raise TypeError("Parameter 'show' must be a bool.")

    fig, ax = plt.subplots(
        ncols=torque_speed_curve + torque_current_curve,
        nrows=1,
        sharey='all',
        figsize=figsize
    )

    motor_maximum_torque = motor.maximum_torque.to(torque_unit).value

    motor_instant_driving_torque = [
        torque.to(torque_unit).value
        for torque in motor.time_variables['driving torque']
    ]

    total_padding = 1 + padding

    if torque_speed_curve:
        motor_instant_angular_speed = [
            speed.to(angular_speed_unit).value
            for speed in motor.time_variables['angular speed']
        ]
        motor_no_speed = motor.no_load_speed.to(angular_speed_unit).value
        speeds = [-total_padding*motor_no_speed, total_padding*motor_no_speed]

        def compute_torque_speed_curve(maximum_torque, no_load_speed):
            return [
                maximum_torque*(1 - speed/no_load_speed) for speed in speeds
            ]

        def compute_torque_speed_torques(i):
            if not motor.electric_current_is_computable:
                torques = compute_torque_speed_curve(
                    maximum_torque=motor_maximum_torque,
                    no_load_speed=motor_no_speed
                )
                title = f'time = {time[i]}'
            else:
                pwm = motor.time_variables['pwm'][i]
                pwm_min = motor.no_load_electric_current / \
                    motor.maximum_electric_current
                if abs(pwm) <= pwm_min:
                    torques = [0, 0]
                elif pwm > pwm_min:
                    maximum_torque = \
                        motor.maximum_torque*(
                            (pwm*motor.maximum_electric_current -
                                motor.no_load_electric_current) /
                            (motor.maximum_electric_current -
                                motor.no_load_electric_current)
                        )
                    no_load_speed = pwm*motor.no_load_speed

                    torques = compute_torque_speed_curve(
                        maximum_torque=maximum_torque.to(torque_unit).value,
                        no_load_speed=no_load_speed.to(
                            angular_speed_unit
                        ).value
                    )
                else:
                    maximum_torque = \
                        motor.maximum_torque*(
                            (pwm*motor.maximum_electric_current +
                                motor.no_load_electric_current) /
                            (motor.maximum_electric_current -
                                motor.no_load_electric_current)
                        )
                    no_load_speed = pwm*motor.no_load_speed

                    torques = compute_torque_speed_curve(
                        maximum_torque=maximum_torque.to(torque_unit).value,
                        no_load_speed=no_load_speed.to(
                            angular_speed_unit
                        ).value
                    )
                title = f'time = {time[i]}      PWM = {pwm:.2f}'

            return torques, title

        torques, title = compute_torque_speed_torques(i=0)

        ax_ts = ax[0] if torque_current_curve else ax

        ax_ts.axhline(y=0, color='black', linewidth=0.5)
        ax_ts.axvline(x=0, color='black', linewidth=0.5)

        line_ts, = ax_ts.plot(speeds, torques, color=line_color)

        point_ts, = ax_ts.plot(
            motor_instant_angular_speed[0],
            motor_instant_driving_torque[0],
            marker='o',
            markerfacecolor=marker_color,
            markeredgecolor=marker_color,
            markersize=marker_size
        )

        ax_ts.set_xlabel(f'angular speed ({angular_speed_unit})')
        ax_ts.set_ylabel(f'torque ({torque_unit})')

        ax_ts.set_xlim(
            -total_padding*motor_no_speed,
            total_padding*motor_no_speed
        )
        ax_ts.set_ylim(
            -total_padding*motor_maximum_torque,
            total_padding*motor_maximum_torque
        )

        ax_ts.tick_params(bottom=False, top=False, left=False, right=False)

    if torque_current_curve:
        motor_instant_electric_current = [
            current.to(current_unit).value
            for current in motor.time_variables['electric current']
        ]
        motor_no_load_electric_current = \
            motor.no_load_electric_current.to(current_unit).value
        motor_maximum_electric_current = \
            motor.maximum_electric_current.to(current_unit).value
        currents = [
            -total_padding*motor_maximum_electric_current,
            total_padding*motor_maximum_electric_current
        ]

        def compute_torque_current_curve(
                maximum_torque, no_load_electric_current,
                maximum_electric_current
        ):
            return [
                maximum_torque /
                (maximum_electric_current - no_load_electric_current) *
                (current - no_load_electric_current)
                for current in currents
            ]

        def compute_torque_current_torques(i):
            pwm = motor.time_variables['pwm'][i]
            pwm_min = \
                motor.no_load_electric_current/motor.maximum_electric_current
            if abs(pwm) <= pwm_min:
                torques = [0, 0]
            elif pwm > pwm_min:
                torques = compute_torque_current_curve(
                    maximum_torque=motor_maximum_torque,
                    no_load_electric_current=motor_no_load_electric_current,
                    maximum_electric_current=motor_maximum_electric_current
                )
            else:
                torques = compute_torque_current_curve(
                    maximum_torque=-motor_maximum_torque,
                    no_load_electric_current=-motor_no_load_electric_current,
                    maximum_electric_current=-motor_maximum_electric_current
                )
            title = f'time = {time[i]}      PWM = {pwm:.2f}'

            return torques, title

        torques, title = compute_torque_current_torques(i=0)

        ax_tc = ax[1] if torque_speed_curve else ax

        ax_tc.axhline(y=0, color='black', linewidth=0.5)
        ax_tc.axvline(x=0, color='black', linewidth=0.5)

        line_tc, = ax_tc.plot(currents, torques, color=line_color)

        point_tc, = ax_tc.plot(
            motor_instant_electric_current[0],
            motor_instant_driving_torque[0],
            marker='o',
            markerfacecolor=marker_color,
            markeredgecolor=marker_color,
            markersize=marker_size
        )

        ax_tc.set_xlabel(f'electric current ({current_unit})')
        ax_tc.set_ylabel(f'torque ({torque_unit})')

        ax_tc.set_xlim(
            -total_padding*motor_maximum_electric_current,
            total_padding*motor_maximum_electric_current
        )

        ax_tc.tick_params(bottom=False, top=False, left=False, right=False)

    fig.suptitle(title)
    plt.tight_layout()

    def update_animation(i):

        if torque_speed_curve:
            torques, title = compute_torque_speed_torques(i=i)
            line_ts.set_data(speeds, torques)
            point_ts.set_data(
                [motor_instant_angular_speed[i]],
                [motor_instant_driving_torque[i]]
            )

        if torque_current_curve:
            torques, title = compute_torque_current_torques(i=i)
            line_tc.set_data(currents, torques)
            point_tc.set_data(
                [motor_instant_electric_current[i]],
                [motor_instant_driving_torque[i]]
            )

        fig.suptitle(title)

        if torque_speed_curve and torque_current_curve:
            return line_ts, point_ts, line_tc, point_tc,
        elif torque_speed_curve and not torque_current_curve:
            return line_ts, point_ts,
        else:
            return line_tc, point_tc,

    animation = FuncAnimation(
        func=update_animation,
        fig=fig,
        frames=range(1, len(time), 1),
        interval=interval
    )

    if show:
        plt.show()

    return animation
