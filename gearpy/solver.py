from gearpy.mechanical_objects import (
    RotatingObject,
    MotorBase,
    GearBase,
    WormGear
)
from gearpy.motor_control import MotorControlBase
from gearpy.powertrain import Powertrain
from gearpy.units import (
    Time,
    TimeInterval,
    Torque,
    AngularSpeed,
    AngularAcceleration
)
from gearpy.utils import StopCondition
import numpy as np
from typing import Optional


NULL_ANGULAR_SPEED = AngularSpeed(0, 'rad/s')
NULL_ANGULAR_ACCELERATION = AngularAcceleration(0, 'rad/s^2')
NULL_TORQUE = Torque(0, 'Nm')


class Solver:
    r""":py:class:`Solver <gearpy.solver.Solver>` object.

    Methods
    -------
    :py:meth:`run`
        It runs the powertrain simulation.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``powertrain`` is not an instance of
             :py:class:`Powertrain <gearpy.powertrain.Powertrain>`,
           - if the first element in ``powertrain`` is not an instance of
             :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`,
           - if an element of ``powertrain`` is not an instance of
             :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`.
       ``ValueError``
           If
           :py:attr:`Powertrain.elements <gearpy.powertrain.Powertrain.elements>`
           is an empty :py:class:`tuple`.
    """

    def __init__(self, powertrain: Powertrain):
        if not isinstance(powertrain, Powertrain):
            raise TypeError(
                f"Parameter 'powertrain' must be an instance of "
                f"{Powertrain.__name__!r}."
            )

        if not powertrain.elements:
            raise ValueError(
                "Parameter 'powertrain.elements' cannot be an empty tuple."
            )

        if not isinstance(powertrain.elements[0], MotorBase):
            raise TypeError(
                f"First element in 'powertrain' must be an instance of "
                f"{MotorBase.__name__!r}."
            )

        if not all(
            [isinstance(element, RotatingObject)
                for element in powertrain.elements]
        ):
            raise TypeError(
                f"All elements of 'powertrain' must be instances of "
                f"{RotatingObject.__name__!r}."
            )

        self.__powertrain = powertrain
        self.__powertrain_is_locked = False

    def run(
        self,
        time_discretization: TimeInterval,
        simulation_time: TimeInterval,
        motor_control: Optional[MotorControlBase] = None,
        stop_condition: Optional[StopCondition] = None
    ) -> None:
        """It runs the powertrain simulation. \n
        The simulation is performed in several steps:

        - it computes the whole powertrain equivalent moment of inertia with
          respect to the last gear, by multiplying each element's moment of
          inertia, starting from the motor, by it gear ratio with respect to
          the following element in the powertrain elements and sum them up,
        - for each time step and for each powertrain element, it computes:

          - the angular position and angular speed, from the last element in
            the powertrain elements to the first one,
          - the driving torque, load torque, net torque, electrical current for
            motors (if computable), tangential force, bending stress and
            contact stress for gears (if computable), motor control rules (if
            available), simulation stopping condition (if available),
          - the angular acceleration of each powertrain element,

        - for each time step it performs a time integration to compute angular
          position and speed of the last element in the powertrain elements.

        Parameters
        ----------
        ``time_discretization`` : :py:class:`TimeInterval <gearpy.units.units.TimeInterval>`
            Time discretization to be used for the simulation.
        ``simulation_time`` : :py:class:`TimeInterval <gearpy.units.units.TimeInterval>`
            Duration of the simulation.
        ``motor_control`` : :py:class:`MotorControlBase <gearpy.motor_control.motor_control_base.MotorControlBase>`, optional
            Rules to control the powertrain motor.
        ``stop_condition`` : :py:class:`StopCondition <gearpy.utils.stop_condition.stop_condition.StopCondition>`, optional
            Simulation stopping condition.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               - If ``time_discretization`` is not an instance of
                 :py:class:`TimeInterval <gearpy.units.units.TimeInterval>`,
               - if ``simulation_time`` is not an instance of
                 :py:class:`TimeInterval <gearpy.units.units.TimeInterval>`,
               - if ``motor_control`` is not an instance of
                 :py:class:`MotorControlBase <gearpy.motor_control.motor_control_base.MotorControlBase>`,
               - if ``stop_condition`` is not an instance of
                 :py:class:`StopCondition <gearpy.utils.stop_condition.stop_condition.StopCondition>`,
               - if function ``external_torque`` of one gear in the powertrain
                 elements does not return an instance of
                 :py:class:`Torque <gearpy.units.units.Torque>`,
           ``ValueError``
               - If ``time_discretization`` is greater or equal to
                 ``simulation_time``,
               - if function ``external_torque`` has not been defined for any
                 gear of the powertrain.

        .. admonition:: Notes
           :class: tip

           If :py:attr:`Powertrain.time <gearpy.powertrain.Powertrain.time>` is
           an empty :py:class:`list`, it performs the simulation starting the
           time from ``0 sec``; otherwise it concatenates another simulation to
           existing values of time and time variables.
        """
        if not isinstance(time_discretization, TimeInterval):
            raise TypeError(
                f"Parameter 'time_discretization' must be an instance of "
                f"{TimeInterval.__name__!r}."
            )

        if not isinstance(simulation_time, TimeInterval):
            raise TypeError(
                f"Parameter 'simulation_time' must be an instance of "
                f"{TimeInterval.__name__!r}."
            )

        if time_discretization >= simulation_time:
            raise ValueError(
                "Parameter 'time_discretization' cannot be greater or equal "
                "to 'simulation_time'."
            )

        if not any(
            [element.external_torque is not None
                for element in self.__powertrain.elements
                if isinstance(element, GearBase)]
        ):
            raise ValueError(
                "The function 'external_torque' has not been defined for any "
                "gear of the powertrain. Add this function to a powertrain "
                "gear."
            )

        if not isinstance(motor_control, MotorControlBase) and \
                motor_control is not None:
            raise TypeError(
                f"Parameter 'motor_control' must be an instance of "
                f"{MotorControlBase.__name__!r}."
            )

        if not isinstance(stop_condition, StopCondition) and \
                stop_condition is not None:
            raise TypeError(
                f"Parameter 'stop_condition' must be an instance of "
                f"{StopCondition.__name__!r}."
            )

        self._compute_powertrain_inertia()
        if self.__powertrain.time:
            initial_time = self.__powertrain.time[-1]
            final_time = initial_time + simulation_time + time_discretization
        else:
            initial_time = Time(value=0, unit=time_discretization.unit)
            final_time = initial_time + simulation_time + time_discretization
            self.__powertrain.update_time(initial_time)
            self._compute_powertrain_variables(motor_control=motor_control)

        for k in np.arange(
            initial_time.value + time_discretization.value,
            final_time.value,
            time_discretization.value
        ):

            self.__powertrain.update_time(
                Time(value=float(k), unit=time_discretization.unit)
            )
            self._time_integration(time_discretization=time_discretization)
            self._compute_powertrain_variables(motor_control=motor_control)
            if stop_condition is not None:
                if stop_condition.check_condition():
                    break

    def _compute_powertrain_inertia(self):

        self.__powertrain_inertia_moment = \
            self.__powertrain.elements[0].inertia_moment
        for element in self.__powertrain.elements[1:]:
            self.__powertrain_inertia_moment *= element.master_gear_ratio
            self.__powertrain_inertia_moment += element.inertia_moment

    def _compute_powertrain_variables(
        self,
        motor_control: Optional[MotorControlBase]
    ):

        self._compute_angular_position_and_speed()
        self._check_powertrain_is_locked()
        if self.__powertrain_is_locked:
            self._compute_locked_powertrain_angular_speed_and_acceleration()
        self._compute_load_torque()
        self._compute_motor_control(motor_control=motor_control)
        self._compute_driving_torque()
        self._compute_torque()
        if not self.__powertrain_is_locked:
            self._compute_angular_acceleration()
        self._compute_force()
        self._compute_stress()
        self._compute_electric_current()
        self._update_time_variables()

    def _compute_angular_position_and_speed(self):

        for i in range(len(self.__powertrain.elements) - 2, -1, -1):
            gear_ratio = self.__powertrain.elements[i + 1].master_gear_ratio
            self._transmit_angular_position(gear_ratio=gear_ratio, i=i)
            self._transmit_angular_speed(gear_ratio=gear_ratio, i=i)

    def _transmit_angular_position(self, gear_ratio: float, i: int):

        self.__powertrain.elements[i].angular_position = \
            gear_ratio*self.__powertrain.elements[i + 1].angular_position

    def _transmit_angular_speed(self, gear_ratio: float, i: int):

        self.__powertrain.elements[i].angular_speed = \
            gear_ratio*self.__powertrain.elements[i + 1].angular_speed

    def _transmit_angular_acceleration(self, gear_ratio: float, i: int):

        self.__powertrain.elements[i].angular_acceleration = \
            gear_ratio * \
            self.__powertrain.elements[i + 1].angular_acceleration

    def _compute_motor_control(
        self,
        motor_control: Optional[MotorControlBase]
    ):

        if motor_control is not None:
            motor_control.apply_rules()

    def _compute_driving_torque(self):

        self.__powertrain.elements[0].compute_torque()

        for i in range(1, len(self.__powertrain.elements)):
            self.__powertrain.elements[i].driving_torque = \
                self.__powertrain.elements[i - 1].driving_torque * \
                self.__powertrain.elements[i].master_gear_efficiency * \
                self.__powertrain.elements[i].master_gear_ratio

    def _compute_load_torque(self):

        for i in range(len(self.__powertrain.elements) - 1, 0, -1):
            if hasattr(self.__powertrain.elements[i], 'external_torque'):
                if self.__powertrain.elements[i].external_torque is not None:
                    external_torque = \
                        self.__powertrain.elements[i].external_torque(
                            time=self.__powertrain.time[-1],
                            angular_position=self.__powertrain.elements[i].
                            angular_position,
                            angular_speed=self.__powertrain.elements[i].
                            angular_speed
                        )
                    if not isinstance(external_torque, Torque):
                        raise TypeError(
                            f"Function 'external_torque' of "
                            f"{self.__powertrain.elements[i].name!r} "
                            f"must return an instance of {Torque.__name__!r}."
                        )
                    self.__powertrain.elements[i].load_torque = external_torque

            self.__powertrain.elements[i - 1].load_torque = \
                self.__powertrain.elements[i].load_torque / \
                self.__powertrain.elements[i].master_gear_efficiency / \
                self.__powertrain.elements[i].master_gear_ratio

    def _compute_torque(self):

        for element in self.__powertrain.elements:
            element.torque = element.driving_torque - element.load_torque

    def _compute_force(self):

        for element in self.__powertrain.elements:
            if isinstance(element, GearBase | WormGear):
                if element.tangential_force_is_computable:
                    element.compute_tangential_force()

    def _compute_stress(self):

        for element in self.__powertrain.elements:
            if isinstance(element, GearBase):
                if element.bending_stress_is_computable:
                    element.compute_bending_stress()
                    if element.contact_stress_is_computable:
                        element.compute_contact_stress()

    def _compute_electric_current(self):

        if self.__powertrain.elements[0].electric_current_is_computable:
            self.__powertrain.elements[0].compute_electric_current()

    def _compute_angular_acceleration(self):

        self.__powertrain.elements[-1].angular_acceleration = \
            self.__powertrain.elements[-1].torque / \
            self.__powertrain_inertia_moment

        for i in range(len(self.__powertrain.elements) - 2, -1, -1):
            gear_ratio = self.__powertrain.elements[i + 1].master_gear_ratio
            self._transmit_angular_acceleration(gear_ratio=gear_ratio, i=i)

    def _update_time_variables(self):

        for element in self.__powertrain.elements:
            element.update_time_variables()

    def _time_integration(self, time_discretization: TimeInterval):

        self.__powertrain.elements[-1].angular_speed += \
            self.__powertrain.elements[-1].angular_acceleration * \
            time_discretization
        self.__powertrain.elements[-1].angular_position += \
            self.__powertrain.elements[-1].angular_speed*time_discretization

    def _check_powertrain_is_locked(self):

        motor = self.__powertrain.elements[0]
        if self.__powertrain.self_locking and (
            motor.pwm == 0 or
            (motor.pwm > 0 and motor.angular_speed < NULL_ANGULAR_SPEED) or
            (motor.pwm < 0 and motor.angular_speed > NULL_ANGULAR_SPEED)
        ):
            self.__powertrain_is_locked = True
            return

        if motor.torque is not None:
            if (motor.torque > NULL_TORQUE and motor.pwm > 0) or \
                    (motor.torque < NULL_TORQUE and motor.pwm < 0):
                self.__powertrain_is_locked = False

    def _compute_locked_powertrain_angular_speed_and_acceleration(self):

        for element in self.__powertrain.elements:
            element.angular_speed = NULL_ANGULAR_SPEED
            element.angular_acceleration = NULL_ANGULAR_ACCELERATION
