from gearpy.units import (
    AngularPosition,
    AngularSpeed,
    AngularAcceleration,
    Time
)
import numpy as np


class SCurveTrajectory:
    """:py:class:`SCurveTrajectory <gearpy.motor_control.utils.s_curve_trajectory.SCurveTrajectory>`
    object. \n
    It computes the S curve trajectory from the ``start_position`` to the
    ``stop_position``.
    The trajectory is divided into three parts:

    - a constant acceleration part at ``maximum_acceleration``,
    - a uniform velocity part at ``maximum_velocity``,
    - a constant deceleration part at ``maximum_deceleration``.

    The starting conditions, at the ``start_time``, are the ``start_position``
    and the ``start_velocity``; while the final conditions are the
    ``stop_position`` and ``stop_velocity``. \n
    The ``stop_position`` may also be lower than (but not equal to) the
    ``start_position`` for backward motion.

    Methods
    -------
    :py:meth:`compute`
        It computes the angular position at the given ``time`` instant,
        according to the S curve trajectory from the ``start_position`` to the
        ``stop_position``.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``start_position`` is not an instance of
             :py:class:`AngularPosition <gearpy.units.AngularPosition>`,
           - if ``stop_position`` is not an instance of
             :py:class:`AngularPosition <gearpy.units.AngularPosition>`,
           - if ``maximum_velocity`` is not an instance of
             :py:class:`AngularSpeed <gearpy.units.AngularSpeed>`,
           - if ``maximum_acceleration`` is not an instance of
             :py:class:`AngularAcceleration <gearpy.units.AngularAcceleration>`,
           - if ``maximum_deceleration`` is not an instance of
             :py:class:`AngularAcceleration <gearpy.units.AngularAcceleration>`,
           - if ``start_velocity`` is not an instance of
             :py:class:`AngularSpeed <gearpy.units.AngularSpeed>`,
           - if ``stop_velocity`` is not an instance of
             :py:class:`AngularSpeed <gearpy.units.AngularSpeed>`,
           - if ``start_time`` is not an instance of
             :py:class:`Time <gearpy.units.Time>`.
       ``ValueError``
           - If ``start_position`` and ``stop_position`` are equal,
           - if ``maximum_velocity`` is not positive,
           - if ``maximum_acceleration`` is not positive,
           - if ``maximum_deceleration`` is not positive,
           - if ``start_velocity`` is geater than ``maximum_velocity``,
           - if ``stop_velocity`` is greater than ``maximum_velocity``.
    """

    def __init__(
        self,
        start_position: AngularPosition,
        stop_position: AngularPosition,
        maximum_velocity: AngularSpeed,
        maximum_acceleration: AngularAcceleration,
        maximum_deceleration: AngularAcceleration,
        start_velocity: AngularSpeed | None = None,
        stop_velocity: AngularSpeed | None = None,
        start_time: Time | None = None
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
        r"""It computes the angular position at the given ``time`` instant,
        according to the S curve trajectory from the ``start_position`` to the
        ``stop_position``.

        Parameters
        ----------
        ``time`` : :py:class:`Time <gearpy.units.units.Time>`
            Specific instant of time in which to calculate the angular
            position in accordance with the S curve.

        Returns
        -------
        :py:class:`AngularPosition <gearpy.units.AngularPosition>`
            Angular position according to S curve trajectory at the given
            ``time``.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If ``time`` is not an instance of
               :py:class:`Time <gearpy.units.units.Time>`.

        .. admonition:: Notes
            :class: tip

            The input parameter ``time`` :math:`t` is compared to the S curve
            trajectory parameters, to establish the motion regime at that time
            instant. Five cases are be possibile:

            1. :math:`t \lt t_0`:
               The ``time`` :math:`t` instant preceeds the ``start_time``
               :math:`t_0`. The motion regime is uniform velocity at
               ``start_velocity`` :math:`\dot{\theta}_0`.
               The angular position :math:`\theta` is computed as:

               .. math::
                   \theta = \dot{\theta}_0 t_l + \theta_0

               where :math:`t_l = t - t_0`.

            2. :math:`t_0 \le t \lt t_0 + t_A`:
               The ``time`` :math:`t` instant is greater than the
               ``start_time`` :math:`t_0`, but lower than the duration
               :math:`t_0 + t_A`. The motion regime is uniform acceleration at
               ``maximum_acceleration`` :math:`\ddot{\theta}_{A,max}`.
               The angular position :math:`\theta` is computed as:

               .. math::
                   \theta = \frac{1}{2} \ddot{\theta}_{A,max} t^2_l +
                   \dot{\theta}_0 t_l + \theta_0

               where :math:`t_l = t - t_0`.

            3. :math:`t_0 + t_A \le t \lt t_0 + t_A + t_U`
               The ``time`` :math:`t` instant is greater than the duration
               :math:`t_0 + t_A`, but lower than the duration
               :math:`t_0 + t_A + t_U`. The motion regime is uniform velocity
               at ``maximum_velocity`` :math:`\dot{\theta}_{max}`.
               The angular position :math:`\theta` is computed as:

               .. math::
                   \theta = \dot{\theta}_{max} t_l + \theta_0 + \theta_A

               where :math:`t_l = t - t_0 - t_A`.

            4. :math:`t_0 + t_A + t_U \le t \lt t_1`
               The ``time`` :math:`t` instant is greater than the duration
               :math:`t_0 + t_A + t_U`, but lower than the duration
               :math:`t_1`. The motion regime is uniform deceleration at
               ``maximum_deceleration`` :math:`\ddot{\theta}_{D,max}`.
               The angular position :math:`\theta` is computed as:

               .. math::
                   \theta = - \frac{1}{2} \ddot{\theta}_{D,max} t^2_l +
                   \dot{\theta}_{max} t_l + \theta_0 + \theta_A + \theta_U

               where :math:`t_l = t - t_0 - t_A - t_U`.

            5. :math:`t \ge t_1`
               The ``time`` :math:`t` instant is greater than the duration
               :math:`t_1`. The motion regime is uniform velocity at
               ``stop_velocity`` :math:`\dot{\theta}_1`.
               The angular position :math:`\theta` is computed as:

               .. math::
                   \theta = \dot{\theta}_1 t_l + \theta_1

               where :math:`t_l = t - t_0 - t_A - t_U - t_D`.

            In some cases, the difference between ``stop_position``
            :math:`\theta_1` and ``start_position`` :math:`\theta_0` is small
            compared to the acceleration and deceleration distances
            :math:`\theta_A` and :math:`\theta_D`. In that case, there is no
            room for uniform velocity regime at ``maximum_velocity``
            :math:`\dot{\theta}_{max}`, so the step 3 is skipped and the
            ``maximum_velocity`` is not reached.

            The acceleration duration :math:`t_A` is computed as:

            .. math::
                t_A = \frac{\dot{\theta}_{max} -
                \dot{\theta}_0}{\ddot{\theta}_{A,max}}

            The uniform duration :math:`t_U` is computed as:

            .. math::
                t_U = \frac{\theta_U}{\dot{\theta}_{max}}

            The deceleration duration :math:`t_D` is computed as:

            .. math::
                t_D = \frac{\dot{\theta}_{max} -
                \dot{\theta}_1}{\ddot{\theta}_{D,max}}

            The acceleration distance :math:`\theta_A` is computed as:

            .. math::
                \theta_A = \frac{1}{2} \frac{\dot{\theta}_{max}^2 -
                \dot{\theta}_0^2}{\ddot{\theta}_{A,max}}

            The uniform distance :math:`\theta_U` is computed as:

            .. math::
                \theta_U = | \theta_1 - \theta_0 | - \theta_A - \theta_D

            The deceleration distance :math:`\theta_D` is computed as:

            .. math::
                \theta_D = \frac{1}{2} \frac{\dot{\theta}_{max}^2 -
                \dot{\theta}_1^2}{\ddot{\theta}_{D,max}}

            The stop time is computed as:

            .. math::
                t_1 = t_0 + t_A + t_U + t_D

            Here the list of the parameters used in the above equations:

            - :math:`\theta` is the angular position,
            - :math:`\dot{\theta}_{max}` is the ``maximum_velocity``,
            - :math:`\ddot{\theta}_{A,max}` is the ``maximum_acceleration``,
            - :math:`\ddot{\theta}_{D,max}` is the ``maximum_deceleration``,
            - :math:`\theta_0` is the ``start_position``,
            - :math:`\theta_1` is the ``stop_position``,
            - :math:`\dot{\theta}_0` is the ``start_velocity``,
            - :math:`\dot{\theta}_1` ``stop_velocity``,
            - :math:`t_0` is the ``start_time``.
        """
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
                    self.__uniform_distance.value,
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
