from gearpy.units import TimeInterval


class PIDController:
    """.. versionadded:: 1.3.0

    :py:class:`PIDController <gearpy.motor_control.utils.pid_controller.PIDController>`
    object. \n
    Proportional-integral-derivative controller which computes the reference
    value, used to keep a variable under control with respect to a set value,
    based on current value and control parameters.

    Methods
    -------
    :py:meth:`compute`
        It computes the reference value based on current error.
    :py:meth:`reset`
        It resets the stored cumulative error integral, used for integrative
        part, and the previous error, used for derivative part.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If :py:attr:`Kp` is not a :py:class:`float` or an :py:class:`int`,
           - if :py:attr:`Ki` is not a :py:class:`float` or an :py:class:`int`,
           - if :py:attr:`Kd` is not a :py:class:`float` or an :py:class:`int`,
           - if :py:attr:`clamping` is not a :py:class:`bool`,
           - if :py:attr:`reference_min` is not a :py:class:`float` or an
             :py:class:`int`,
           - if :py:attr:`reference_max` is not a :py:class:`float` or an
             :py:class:`int`.
       ``ValueError``
           If ``reference_min`` is lower than ``reference_max``.
    """

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
        r"""It computes the reference value based on current error.

        Parameters
        ----------
        ``error`` : :py:class:`float` or :py:class:`int`
            Current error.
        ``time_step`` : :py:class:`Time <gearpy.units.units.TimeInterval>`
            Time interval to be used for integrative and derivative parts.

        Returns
        -------
        :py:class:`float` or :py:class:`int`
            Reference value to be used for control.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If :py:attr:`error` is not a :py:class:`float` or an
                 :py:class:`int`,
               - if :py:attr:`time_step` is not an instance of
                 :py:class:`Time <gearpy.units.units.TimeInterval>`.

        .. admonition:: Notes
            :class: tip

            The reference value is computed as:

            .. math::
                u(t) = K_P e(t) + K_I \int_0^t e(\tau) d \tau + K_D
                \frac{d e(t)}{d t}

            where:

            - :math:`u(t)` is the reference value,
            - :math:`e(t)` is the current ``error``,
            - :math:`K_P` is the proportional constant ``Kp``,
            - :math:`K_I` is the integral constant ``Ki``,
            - :math:`K_D` is the derivative constant ``Kd``.

            The integral part is approximated with:

            .. math::
                \int_0^t e(\tau) d \tau \approx \frac{1}{2}(e_i + e_{i - 1}) dt

            and the derivative part is approximated with:

            .. math::
                \frac{d e(t)}{d t} \approx \frac{e_i - e_{i - 1}}{dt}

            where:

            - :math:`e_i` is the current ``error``,
            - :math:`e_{i - 1}` is the error at the previous time step,
            - :math:`dt` is the ``time_step``.

            If the reference value :math:`u(t)` exceeds the limits
            ``reference_min`` or ``reference_max``, then it is saturated to
            these values. In this case, if ``clamping`` is ``True``, then the
            cumulative error is not updated (anti-windup).
        """
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
        """It resets the stored cumulative error integral, used for integrative
        part, and the previous error, used for derivative part.
        """
        self.__cumulative_error = 0
        self.__previous_error = 0
