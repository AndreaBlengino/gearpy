from gearpy.units import (
    AngularPosition,
    AngularSpeed,
    AngularAcceleration,
    Time
)
import numpy as np


class SCurveTrajectory:

    def __init__(
        self,
        start_position: AngularPosition,
        stop_position: AngularPosition,
        maximum_velocity: AngularSpeed,
        maximum_acceleration: AngularAcceleration,
        maximum_deceleration: AngularAcceleration,
        start_velocity: AngularSpeed | None = None,
        stop_velocity: AngularSpeed | None = None,
        start_time: Time | None = None,
    ):
        if not isinstance(start_position, AngularPosition):
            raise TypeError(
                f"Parameter 'start_position' must be an instance of "
                f"{AngularPosition.__name__!r}."
            )

        if not isinstance(stop_position, AngularPosition):
            raise TypeError(
                f"Parameter 'stop_position' must be an instance of "
                f"{AngularPosition.__name__!r}."
            )

        if not isinstance(maximum_velocity, AngularSpeed):
            raise TypeError(
                f"Parameter 'maximum_velocity' must be an instance of "
                f"{AngularSpeed.__name__!r}."
            )

        if not isinstance(maximum_acceleration, AngularAcceleration):
            raise TypeError(
                f"Parameter 'maximum_acceleration' must be an instance of "
                f"{AngularAcceleration.__name__!r}."
            )

        if not isinstance(maximum_deceleration, AngularAcceleration):
            raise TypeError(
                f"Parameter 'maximum_deceleration' must be an instance of "
                f"{AngularAcceleration.__name__!r}."
            )

        if start_velocity is None:
            start_velocity = AngularSpeed(value=0, unit="rad/s")
        else:
            if not isinstance(start_velocity, AngularSpeed):
                raise TypeError(
                    f"Parameter 'start_velocity' must be an instance of "
                    f"{AngularSpeed.__name__!r}."
                )

        if stop_velocity is None:
            stop_velocity = AngularSpeed(value=0, unit="rad/s")
        else:
            if not isinstance(stop_velocity, AngularSpeed):
                raise TypeError(
                    f"Parameter 'stop_velocity' must be an instance of "
                    f"{AngularSpeed.__name__!r}."
                )

        if start_time is None:
            start_time = Time(value=0, unit="sec")
        else:
            if not isinstance(start_time, Time):
                raise TypeError(
                    f"Parameter 'start_time' must be an instance of "
                    f"{Time.__name__!r}."
                )

        if start_position == stop_position:
            raise ValueError(
                "Parameters 'start_position' and 'stop_position' cannot be "
                "equal."
            )

        if maximum_velocity.value <= 0:
            raise ValueError("Parameters 'maximum_velocity' must be positive.")

        if maximum_acceleration.value <= 0:
            raise ValueError(
                "Parameters 'maximum_acceleration' must be positive."
            )

        if maximum_deceleration.value <= 0:
            raise ValueError(
                "Parameters 'maximum_deceleration' must be positive."
            )

        if start_velocity > maximum_velocity:
            raise ValueError(
                "Parameter 'start_velocity' cannot be greater than "
                "'maximum_velocity'."
            )

        if stop_velocity > maximum_velocity:
            raise ValueError(
                "Parameter 'stop_velocity' cannot be greater than "
                "'maximum_velocity'."
            )

        start_position.to("rad", inplace=True)
        stop_position.to("rad", inplace=True)
        maximum_velocity.to("rad/s", inplace=True)
        maximum_acceleration.to("rad/s^2", inplace=True)
        maximum_deceleration.to("rad/s^2", inplace=True)
        start_velocity.to("rad/s", inplace=True)
        stop_velocity.to("rad/s", inplace=True)
        start_time.to("sec", inplace=True)

        self.__position_excursion = stop_position - start_position
        if self.__position_excursion.value < 0:
            stop_position = start_position + abs(self.__position_excursion)
            start_velocity = -start_velocity
            stop_velocity = -stop_velocity

        self.__acceleration_distance = AngularPosition(
            value=(
                maximum_velocity.value**2 - start_velocity.value**2
            )/2/maximum_acceleration.value,
            unit="rad"
        )
        self.__acceleration_time = Time(
            value=(
                maximum_velocity.value - start_velocity.value
            )/maximum_acceleration.value,
            unit="sec"
        )

        self.__deceleration_distance = AngularPosition(
            value=(
                maximum_velocity.value**2 - stop_velocity.value**2
            )/2/maximum_deceleration.value,
            unit="rad"
        )
        self.__deceleration_time = Time(
            value=(
                maximum_velocity.value - stop_velocity.value
            )/maximum_deceleration.value,
            unit="sec"
        )

        self.__uniform_distance = abs(stop_position - start_position) - \
            self.__acceleration_distance - self.__deceleration_distance
        self.__uniform_time = Time(
            value=self.__uniform_distance.value/maximum_velocity.value,
            unit="sec"
        )

        if self.__uniform_distance.value <= 0:
            maximum_velocity = AngularSpeed(
                value=np.sqrt(
                    (2*maximum_acceleration.value*maximum_deceleration.value*
                    abs(stop_position - start_position).value +
                    maximum_deceleration.value*start_velocity.value**2 +
                    maximum_acceleration.value*stop_velocity.value**2)/
                    (maximum_acceleration + maximum_deceleration).value
                ),
                unit="rad/s"
            )
            self.__maximum_velocity = maximum_velocity

            self.__acceleration_distance = AngularPosition(
                value=(
                    maximum_velocity.value**2 - start_velocity.value**2
                )/2/maximum_acceleration.value,
                unit="rad"
            )
            self.__acceleration_time = Time(
                value=(
                    maximum_velocity - start_velocity
                ).value/maximum_acceleration.value,
                unit="sec"
            )

            self.__deceleration_distance = AngularPosition(
                value=(
                    maximum_velocity.value**2 - stop_velocity.value**2
                )/2/maximum_deceleration.value,
                unit="rad"
            )
            self.__deceleration_time = Time(
                value=(
                    maximum_velocity - stop_velocity
                ).value/maximum_deceleration.value,
                unit="sec"
            )

            self.__uniform_distance = AngularPosition(value=0, unit="rad")
            self.__uniform_time = Time(value=0, unit="sec")

        self.__start_position = start_position
        self.__stop_position = stop_position
        self.__maximum_velocity = maximum_velocity
        self.__maximum_acceleration = maximum_acceleration
        self.__maximum_deceleration = maximum_deceleration
        self.__start_velocity = start_velocity
        self.__stop_velocity = stop_velocity
        self.__start_time = start_time

    def compute(self, time: Time) -> AngularPosition:
        if not isinstance(time, Time):
            raise TypeError(
                f"Parameter 'time' must be an instance of {Time.__name__!r}.")

        t = time.to("sec", inplace=True).value
        if time < self.__start_time:
            t_l = t - self.__start_time.value
            current_position = AngularPosition(
                value=self.__start_velocity.value*t_l +
                    self.__start_position.value,
                unit="rad",
            )
        elif time < self.__start_time + self.__acceleration_time:
            t_l = t - self.__start_time.value
            current_position = AngularPosition(
                value=1/2*self.__maximum_acceleration.value*t_l**2 +
                    self.__start_velocity.value*t_l +
                    self.__start_position.value,
                unit="rad",
            )
        elif time < self.__start_time + self.__acceleration_time + \
                self.__uniform_time:
            t_l = t - self.__start_time.value - self.__acceleration_time.value
            current_position = AngularPosition(
                value=self.__maximum_velocity.value*t_l +
                    self.__start_position.value +
                    self.__acceleration_distance.value,
                unit="rad",
            )
        elif time < self.__start_time + self.__acceleration_time + \
                self.__uniform_time + self.__deceleration_time:
            t_l = t - self.__start_time.value - \
                self.__acceleration_time.value - self.__uniform_time.value
            current_position = AngularPosition(
                value=-1/2*self.__maximum_deceleration.value*t_l**2 +
                    self.__maximum_velocity.value*t_l +
                    self.__start_position.value +
                    self.__acceleration_distance.value +
                    self.__uniform_distance.value ,
                unit="rad",
            )
        else:
            t_l = t - self.__start_time.value - \
                self.__acceleration_time.value - self.__uniform_time.value - \
                self.__deceleration_time.value
            current_position = AngularPosition(
                value=self.__stop_velocity.value*t_l +
                    self.__stop_position.value,
                unit="rad",
            )

        if self.__position_excursion.value < 0:
            current_position = 2*self.__start_position - current_position

        return current_position
