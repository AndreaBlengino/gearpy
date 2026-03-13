from gearpy.units import TimeInterval


class PIDController:

    def __init__(
        self,
        Kp: float | int,
        Ki: float | int,
        Kd: float | int,
        clamping: bool = False,
        reference_min: float | int | None = None,
        reference_max: float | int | None = None
    ):
        if not isinstance(Kp, float | int):
            raise TypeError("Parameter 'Kp' must be a float or an integer.")

        if not isinstance(Ki, float | int):
            raise TypeError("Parameter 'Ki' must be a float or an integer.")

        if not isinstance(Kd, float | int):
            raise TypeError("Parameter 'Kd' must be a float or an integer.")

        if not isinstance(clamping, bool):
            raise TypeError("Parameter 'clamping' must be a bool.")

        if not isinstance(reference_min, float | int) and \
                reference_min is not None:
            raise TypeError(
                "Parameter 'reference_min' must be a float or an integer."
            )

        if not isinstance(reference_max, float | int) and \
                reference_max is not None:
            raise TypeError(
                "Parameter 'reference_max' must be a float or an integer."
            )

        if reference_min is not None and reference_max is not None:
            if reference_min >= reference_max:
                raise ValueError(
                    "Parameter 'reference_min' must be lower than "
                    "'reference_max'"
                )

        self.__Kp = Kp
        self.__Ki = Ki
        self.__Kd = Kd
        self.__clamping = clamping
        self.__reference_min = reference_min
        self.__reference_max = reference_max

        self.__cumulative_error = 0
        self.__previous_error = 0

    def compute(
        self,
        error: float | int,
        time_step: TimeInterval
    ) -> float | int:
        if not isinstance(error, float | int):
            raise TypeError("Parameter 'error' must be a float or an integer.")

        if not isinstance(time_step, TimeInterval):
            raise TypeError(
                f"Parameter 'time_step' must be an instance of "
                f"{TimeInterval.__name__!r}."
            )

        time_step.to("sec", inplace=True)
        proportional = self.__Kp*error
        integral = self.__Ki*self.__cumulative_error
        derivative = self.__Kd*(error - self.__previous_error)/time_step.value

        self.__previous_error = error
        reference = proportional + integral + derivative

        saturation = False
        if self.__reference_max is not None:
            if reference > self.__reference_max:
                reference = self.__reference_max
                saturation = True
        if self.__reference_min is not None:
            if reference < self.__reference_min:
                reference = self.__reference_min
                saturation = True

        if not self.__clamping or not saturation:
            self.__cumulative_error += (
                error + self.__previous_error
            )*time_step.value/2
        return reference

    def reset(self) -> None:
        self.__cumulative_error = 0
        self.__previous_error = 0
