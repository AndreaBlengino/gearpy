from gearpy.mechanical_object import DCMotor
from gearpy.units import Time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Optional


def dc_motor_characteristics_animation(motor: DCMotor,
                                       time: List[Time],
                                       interval: Optional[int] = 200,
                                       torque_speed_curve: Optional[bool] = True,
                                       torque_current_curve: Optional[bool] = True,
                                       angular_speed_unit: Optional[str] = 'rad/s',
                                       torque_unit: Optional[str] = 'Nm',
                                       current_unit: Optional[str] = 'A',
                                       figsize: Optional[tuple] = None):

    fig, ax = plt.subplots(ncols = torque_speed_curve + torque_current_curve, nrows = 1,
                           sharey = 'all', figsize = figsize)

    motor_maximum_torque = motor.maximum_torque.to(torque_unit).value

    motor_instant_angular_speed = [speed.to(angular_speed_unit).value for speed in motor.time_variables['angular speed']]
    motor_instant_driving_torque = [torque.to(torque_unit).value for torque in motor.time_variables['driving torque']]
    motor_instant_electric_current = [current.to(current_unit).value for current in motor.time_variables['electric current']]


    if torque_speed_curve:
        motor_no_speed = motor.no_load_speed.to(angular_speed_unit).value
        speeds = [-1.1*motor_no_speed, 1.1*motor_no_speed]

        def compute_torque_speed_curve(maximum_torque, no_load_speed):
            return [maximum_torque*(1 - speed/no_load_speed) for speed in speeds]

        def compute_torque_speed_torques(i):
            if not motor.pwm_is_computable:
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
                title = f'time = {time[i]}   -   PWM = {pwm:.2f}'

            return torques, title

        torques, title = compute_torque_speed_torques(i = 0)

        ax_ts = ax[0] if torque_current_curve else ax

        line_ts, = ax_ts.plot(speeds, torques)

        point_ts, = ax_ts.plot(motor_instant_angular_speed[0], motor_instant_driving_torque[0], marker = 'o')

        ax_ts.axhline(y = 0, color = 'black', linewidth = 0.5)
        ax_ts.axvline(x = 0, color = 'black', linewidth = 0.5)

        ax_ts.set_xlabel(f'angular speed ({angular_speed_unit})')
        ax_ts.set_ylabel(f'torque ({torque_unit})')

        ax_ts.set_xlim(-1.1*motor_no_speed, 1.1*motor_no_speed)
        ax_ts.set_ylim(-1.1*motor_maximum_torque, 1.1*motor_maximum_torque)

        ax_ts.tick_params(bottom = False, top = False, left = False, right = False)


    if torque_current_curve:
        motor_no_load_electric_current = motor.no_load_electric_current.to(current_unit).value
        motor_maximum_electric_current = motor.maximum_electric_current.to(current_unit).value
        currents = [-1.1*motor_maximum_electric_current, 1.1*motor_maximum_electric_current]

        def compute_torque_current_curve(maximum_torque, no_load_electric_current, maximum_electric_current):
            return [maximum_torque/(maximum_electric_current - no_load_electric_current)*
                                   (current - no_load_electric_current) for current in currents]

        def compute_torque_current_torques(i):
            if not motor.pwm_is_computable:
                torques = compute_torque_current_curve(maximum_torque = motor_maximum_torque,
                                                       no_load_electric_current = motor_no_load_electric_current,
                                                       maximum_electric_current = motor_maximum_electric_current)
                title = f'time = {time[i]}'
            else:
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
                title = f'time = {time[i]}   -   PWM = {pwm:.2f}'

            return torques, title

        torques, title = compute_torque_current_torques(i = 0)

        ax_tc = ax[1] if torque_speed_curve else ax

        line_tc, = ax_tc.plot(currents, torques)

        point_tc, = ax_tc.plot(motor_instant_electric_current[0], motor_instant_driving_torque[0], marker = 'o')

        ax_tc.axhline(y = 0, color = 'black', linewidth = 0.5)
        ax_tc.axvline(x = 0, color = 'black', linewidth = 0.5)

        ax_tc.set_xlabel(f'electric current ({current_unit})')
        ax_tc.set_ylabel(f'torque ({torque_unit})')

        ax_tc.set_xlim(-1.1*motor_maximum_electric_current, 1.1*motor_maximum_electric_current)

        ax_tc.tick_params(bottom = False, top = False, left = False, right = False)


    fig.suptitle(title)
    plt.tight_layout()


    def update_animation(i):

        if torque_speed_curve:
            torques, title = compute_torque_speed_torques(i = i)
            line_ts.set_data(speeds, torques)
            point_ts.set_data(motor_instant_angular_speed[i], motor_instant_driving_torque[i])

        if torque_current_curve:
            torques, title = compute_torque_current_torques(i = i)
            line_tc.set_data(currents, torques)
            point_tc.set_data(motor_instant_electric_current[i], motor_instant_driving_torque[i])

        fig.suptitle(title)

        if torque_speed_curve and torque_current_curve:
            return line_ts, point_ts, line_tc, point_tc,
        elif torque_speed_curve and not torque_current_curve:
            return line_ts, point_ts,
        else:
            return line_tc, point_tc,


    _ = FuncAnimation(func = update_animation, fig = fig, frames = range(1, len(time) + 1, 1), interval = interval)
    plt.show()
