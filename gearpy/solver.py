from gearpy.mechanical_objects import RotatingObject, MotorBase, GearBase
from gearpy.motor_control import MotorControlBase
from gearpy.powertrain import Powertrain
from gearpy.units import Time, TimeInterval, Torque, AngularSpeed, AngularAcceleration
import numpy as np
from typing import Optional


NULL_ANGULAR_SPEED = AngularSpeed(0, 'rad/s')
NULL_ANGULAR_ACCELERATION = AngularAcceleration(0, 'rad/s^2')
NULL_TORQUE = Torque(0, 'Nm')


class Solver:
    r"""``gearpy.solver.Solver`` object.

    Attributes
    ----------
    :py:attr:`powertrain` : Powertrain
        Mechanical powertrain to be simulated.

    Methods
    -------
    :py:meth:`run`
        Runs the powertrain simulation.

    Raises
    ------
    TypeError
        - If ``powertrain`` is not an instance of ``Powertrain``,
        - if the first element in ``powertrain`` is not an instance of ``MotorBase``,
        - if an element of ``powertrain`` is not an instance of ``RotatingObject``,
        - if ``motor_control`` is not an instance of ``MotorControlBase``.
    ValueError
        If ``powertrain.elements`` is an empty tuple.

    See Also
    --------
    :py:class:`gearpy.powertrain.Powertrain`
    :py:class:`gearpy.motor_control.pwm_control.PWMControl`
    """

    def __init__(self, powertrain: Powertrain, motor_control: Optional[MotorControlBase] = None):
        if not isinstance(powertrain, Powertrain):
            raise TypeError(f"Parameter 'powertrain' must be an instance of {Powertrain.__name__!r}.")

        if not powertrain.elements:
            raise ValueError("Parameter 'powertrain.elements' cannot be an empty tuple.")

        if not isinstance(powertrain.elements[0], MotorBase):
            raise TypeError(f"First element in 'powertrain' must be an instance of {MotorBase.__name__!r}.")

        if not all([isinstance(element, RotatingObject) for element in powertrain.elements]):
            raise TypeError(f"All elements of 'powertrain' must be instances of {RotatingObject.__name__!r}.")

        if not isinstance(motor_control, MotorControlBase) and motor_control is not None:
            raise TypeError(f"Parameter 'motor_control' must be an instance of {MotorControlBase.__name__!r}.")

        self.powertrain = powertrain
        self.motor_control = motor_control
        self.__powertrain_is_locked = False

    def run(self, time_discretization: TimeInterval, simulation_time: TimeInterval):
        """Runs the powertrain simulation. \n
        The simulation is performed in several steps:

        - it computes the whole powertrain equivalent moment of inertia with respect to the last
          gear, by multiplying each element's moment of inertia, starting from the motor, by it gear ratio with respect
          to the following element in the powertrain elements and sum them up
        - for each time step and for each powertrain element, it computes:

          - the angular position and angular speed, from the last element in the powertrain elements to the first one
          - the driving torque, load torque, net torque, electrical current for motors (if computable), tangential
            force, bending stress and contact stress for gears (if computable)
          - the angular acceleration of each powertrain element.

        - for each time step it performs a time integration to compute angular position and speed of the last element in
          the powertrain elements.

        Parameters
        ----------
        time_discretization : TimeInterval
            Time discretization to be used for the simulation.
        simulation_time : TimeInterval
            Duration of the simulation.

        Raises
        ------
        TypeError
            - If ``time_discretization`` is not an instance of ``TimeInterval``,
            - if ``simulation_time`` is not an instance of ``TimeInterval``,
            - if function ``external_torque`` of one gear in the powertrain elements does not return an instance of
              ``Torque``.
        ValueError
            - If ``time_discretization`` is greater or equal to ``simulation_time``,
            - if function ``external_torque`` has not been defined for any gear of the powertrain.

        Notes
        -----
        If ``powertrain.elements.time`` is an empty list, it performs the simulation starting the time from ``0 sec``;
        otherwise it concatenates another simulation to existing values of time and time variables.

        See Also
        --------
        :py:class:`gearpy.units.units.TimeInterval`
        """
        if not isinstance(time_discretization, TimeInterval):
            raise TypeError(f"Parameter 'time_discretization' must be an instance of {TimeInterval.__name__!r}.")

        if not isinstance(simulation_time, TimeInterval):
            raise TypeError(f"Parameter 'simulation_time' must be an instance of {TimeInterval.__name__!r}.")

        if time_discretization >= simulation_time:
            raise ValueError("Parameter 'time_discretization' cannot be greater or equal to 'simulation_time'.")

        if not any([element.external_torque is not None
                    for element in self.powertrain.elements if isinstance(element, GearBase)]):
            raise ValueError("The function 'external_torque' has not been defined for any gear of the powertrain. "
                             "Add this function to a powertrain gear.")

        self._compute_powertrain_inertia()
        if self.powertrain.time:
            initial_time = self.powertrain.time[-1]
            final_time = initial_time + simulation_time + time_discretization
        else:
            initial_time = Time(value = 0, unit = time_discretization.unit)
            final_time = initial_time + simulation_time + time_discretization
            self.powertrain.update_time(initial_time)
            self._compute_powertrain_variables()

        for k in np.arange(initial_time.value + time_discretization.value, final_time.value, time_discretization.value):

            self.powertrain.update_time(Time(value = float(k), unit = time_discretization.unit))
            self._time_integration(time_discretization = time_discretization)
            self._compute_powertrain_variables()

    def _compute_powertrain_inertia(self):

        self.powertrain_inertia_moment = self.powertrain.elements[0].inertia_moment
        for element in self.powertrain.elements[1:]:
            self.powertrain_inertia_moment *= element.master_gear_ratio
            self.powertrain_inertia_moment += element.inertia_moment

    def _compute_powertrain_variables(self):

        self._compute_angular_position_and_speed()
        self._check_powertrain_is_locked()
        if self.__powertrain_is_locked:
            self._compute_locked_powertrain_angular_speed_and_acceleration()
        self._compute_load_torque()
        self._compute_motor_control()
        self._compute_driving_torque()
        self._compute_torque()
        if not self.__powertrain_is_locked:
            self._compute_angular_acceleration()
        self._compute_force()
        self._compute_stress()
        self._compute_electric_current()
        self._update_time_variables()

    def _compute_angular_position_and_speed(self):

        for i in range(len(self.powertrain.elements) - 2, -1, -1):
            gear_ratio = self.powertrain.elements[i + 1].master_gear_ratio
            self._transmit_angular_position(gear_ratio = gear_ratio, i = i)
            self._transmit_angular_speed(gear_ratio = gear_ratio, i = i)

    def _transmit_angular_position(self, gear_ratio, i):

        self.powertrain.elements[i].angular_position = gear_ratio*self.powertrain.elements[i + 1].angular_position

    def _transmit_angular_speed(self, gear_ratio, i):

        self.powertrain.elements[i].angular_speed = gear_ratio*self.powertrain.elements[i + 1].angular_speed

    def _transmit_angular_acceleration(self, gear_ratio, i):

        self.powertrain.elements[i].angular_acceleration = \
                gear_ratio*self.powertrain.elements[i + 1].angular_acceleration

    def _compute_motor_control(self):

        if self.motor_control is not None:
            self.motor_control.apply_rules()

    def _compute_driving_torque(self):

        self.powertrain.elements[0].compute_torque()

        for i in range(1, len(self.powertrain.elements)):
            self.powertrain.elements[i].driving_torque = self.powertrain.elements[i - 1].driving_torque* \
                                                         self.powertrain.elements[i].master_gear_efficiency* \
                                                         self.powertrain.elements[i].master_gear_ratio

    def _compute_load_torque(self):

        for i in range(len(self.powertrain.elements) - 1, 0, -1):
            if hasattr(self.powertrain.elements[i], 'external_torque'):
                if self.powertrain.elements[i].external_torque is not None:
                    external_torque = \
                        self.powertrain.elements[i].\
                        external_torque(time = self.powertrain.time[-1],
                                        angular_position = self.powertrain.elements[i].angular_position,
                                        angular_speed = self.powertrain.elements[i].angular_speed)
                    if not isinstance(external_torque, Torque):
                        raise TypeError(f"Function 'external_torque' of {self.powertrain.elements[i].name!r} "
                                        f"must return an instance of {Torque.__name__!r}.")
                    self.powertrain.elements[i].load_torque = external_torque

            self.powertrain.elements[i - 1].load_torque = self.powertrain.elements[i].load_torque/ \
                                                          self.powertrain.elements[i].master_gear_efficiency/ \
                                                          self.powertrain.elements[i].master_gear_ratio

    def _compute_torque(self):

        for element in self.powertrain.elements:
            element.torque = element.driving_torque - element.load_torque

    def _compute_force(self):

        for element in self.powertrain.elements:
            if isinstance(element, GearBase):
                if element.tangential_force_is_computable:
                    element.compute_tangential_force()

    def _compute_stress(self):

        for element in self.powertrain.elements:
            if isinstance(element, GearBase):
                if element.bending_stress_is_computable:
                    element.compute_bending_stress()
                    if element.contact_stress_is_computable:
                        element.compute_contact_stress()

    def _compute_electric_current(self):

        if self.powertrain.elements[0].electric_current_is_computable:
            self.powertrain.elements[0].compute_electric_current()

    def _compute_angular_acceleration(self):

        self.powertrain.elements[-1].angular_acceleration = self.powertrain.elements[-1].torque/\
                                                            self.powertrain_inertia_moment

        for i in range(len(self.powertrain.elements) - 2, -1, -1):
            gear_ratio = self.powertrain.elements[i + 1].master_gear_ratio
            self._transmit_angular_acceleration(gear_ratio = gear_ratio, i = i)

    def _update_time_variables(self):

        for element in self.powertrain.elements:
            element.update_time_variables()

    def _time_integration(self, time_discretization: TimeInterval):

        self.powertrain.elements[-1].angular_speed += \
            self.powertrain.elements[-1].angular_acceleration*time_discretization
        self.powertrain.elements[-1].angular_position += \
            self.powertrain.elements[-1].angular_speed*time_discretization

    def _check_powertrain_is_locked(self):

        motor = self.powertrain.elements[0]
        if self.powertrain.self_locking and (motor.pwm == 0 or
                                             (motor.pwm > 0 and motor.angular_speed < NULL_ANGULAR_SPEED) or
                                             (motor.pwm < 0 and motor.angular_speed > NULL_ANGULAR_SPEED)):
            self.__powertrain_is_locked = True
            return

        if motor.torque is not None:
            if (motor.torque > NULL_TORQUE and motor.pwm > 0) or (motor.torque < NULL_TORQUE and motor.pwm < 0):
                self.__powertrain_is_locked = False

    def _compute_locked_powertrain_angular_speed_and_acceleration(self):

        for element in self.powertrain.elements:
            element.angular_speed = NULL_ANGULAR_SPEED
            element.angular_acceleration = NULL_ANGULAR_ACCELERATION
