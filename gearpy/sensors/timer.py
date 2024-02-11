from gearpy.units import Time, TimeInterval


class Timer:
    r"""``gearpy.sensors.timer.Timer`` object.

    Attributes
    ----------
    :py:attr:`start_time` : Time
        Start time after which the timer is active.
    :py:attr:`duration` : TimeInterval
        Time duration of the timer, starting from ``start_time``

    Methods
    -------
    :py:meth:`is_active`
        Checks if the simulation ``current_time`` is greater than or equal to ``start_time`` but lower than or equal
        to ``current_time`` + ``duration``.
    """

    def __init__(self, start_time: Time, duration: TimeInterval):
        if not isinstance(start_time, Time):
            raise TypeError(f"Parameter 'start_time' must be an instance of {Time.__name__!r}.")

        if not isinstance(duration, TimeInterval):
            raise TypeError(f"Parameter 'duration' must be an instance of {TimeInterval.__name__!r}.")

        self.__start_time = start_time
        self.__duration = duration

    @property
    def start_time(self) -> Time:
        """Start time after which the timer is active.

        Returns
        -------
        Time
            Start time after which the timer is active.

        Raises
        ------
        TypeError
            If ``start_time`` is not an instance of ``Time``.
        """
        return self.__start_time

    @property
    def duration(self) -> TimeInterval:
        """Time duration of the timer, starting from ``start_time``.

        Returns
        -------
        TimeInterval
            Time duration of the timer, starting from ``start_time``

        Raises
        ------
        TypeError
            If ``duration`` is not an instance of ``TimeInterval``.
        """
        return self.__duration

    def is_active(self, current_time: Time) -> bool:
        """Checks if the simulation ``current_time`` is greater than or equal to ``start_time`` but lower than or equal
        to ``current_time`` + ``duration``.

        Parameters
        ----------
        current_time : Time
            Current time of the simulation, to be compared with ``start_time`` and ``duration``.

        Returns
        -------
        bool
            Whether ``current_time`` is greater than or equal to ``start_time`` but lower than or equal to
            ``start_time`` + ``duration``.

        Raises
        ------
        TypeError
            If ``current_time`` is not an instance of ``Time``.
        """
        if not isinstance(current_time, Time):
            raise TypeError(f"Parameter 'current_time' must be an instance of {Time.__name__!r}.")

        return (current_time >= self.start_time) and ((current_time - self.start_time) <= self.duration)
