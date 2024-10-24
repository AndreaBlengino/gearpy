from gearpy.units import Time, TimeInterval


class Timer:
    r""":py:class:`Timer <gearpy.sensors.timer.Timer>` object.

    Attributes
    ----------
    :py:attr:`start_time` : :py:class:`Time <gearpy.units.units.Time>`
        Start time after which the timer is active.
    :py:attr:`duration` : :py:class:`TimeInterval <gearpy.units.units.TimeInterval>`
        Time duration of the timer, starting from :py:attr:`start_time`

    Methods
    -------
    :py:meth:`is_active`
        It checks if the simulation ``current_time`` is greater than or equal
        to :py:attr:`start_time` but lower than or equal to the sum of
        ``current_time`` and :py:attr:`duration`.
    """

    def __init__(self, start_time: Time, duration: TimeInterval):
        if not isinstance(start_time, Time):
            raise TypeError(
                f"Parameter 'start_time' must be an instance of "
                f"{Time.__name__!r}."
            )

        if not isinstance(duration, TimeInterval):
            raise TypeError(
                f"Parameter 'duration' must be an instance of "
                f"{TimeInterval.__name__!r}."
            )

        self.__start_time = start_time
        self.__duration = duration

    @property
    def start_time(self) -> Time:
        """Start time after which the timer is active.

        Returns
        -------
        :py:class:`Time <gearpy.units.units.Time>`
            Start time after which the timer is active.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`start_time` is not an instance of
               :py:class:`Time <gearpy.units.units.Time>`.
        """
        return self.__start_time

    @property
    def duration(self) -> TimeInterval:
        """Time duration of the timer, starting from :py:attr:`start_time`.

        Returns
        -------
        :py:class:`TimeInterval <gearpy.units.units.TimeInterval>`
            Time duration of the timer, starting from :py:attr:`start_time`

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If :py:attr:`duration` is not an instance of
               :py:class:`TimeInterval <gearpy.units.units.TimeInterval>`.
        """
        return self.__duration

    def is_active(self, current_time: Time) -> bool:
        """It checks if the simulation ``current_time`` is greater than or
        equal to :py:attr:`start_time` but lower than or equal to the sum of
        ``current_time`` and :py:attr:`duration`.

        Parameters
        ----------
        ``current_time`` : :py:class:`Time <gearpy.units.units.Time>`
            Current time of the simulation, to be compared with
            :py:attr:`start_time` and :py:attr:`duration`.

        Returns
        -------
        :py:class:`bool`
            Whether ``current_time`` is greater than or equal to
            :py:attr:`start_time` but lower than or equal to the sum of
            :py:attr:`start_time` and :py:attr:`duration`.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If ``current_time`` is not an instance of
               :py:class:`Time <gearpy.units.units.Time>`.
        """
        if not isinstance(current_time, Time):
            raise TypeError(
                f"Parameter 'current_time' must be an instance of "
                f"{Time.__name__!r}."
            )

        return (current_time >= self.start_time) and \
            ((current_time - self.start_time) <= self.duration)
