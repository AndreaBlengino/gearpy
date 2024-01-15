from gearpy.mechanical_object import RotatingObject, MotorBase, GearBase
from gearpy.motor_control import MotorControlBase
from gearpy.transmission import Transmission
from gearpy.units import Time, TimeInterval, Torque
import numpy as np
from typing import Optional


class Solver:
    r"""``gearpy.solver.Solver`` object.

    Attributes
    ----------
    :py:attr:`transmission` : Transmission
        Mechanical transmission to be simulated.

    Methods
    -------
    :py:meth:`run`
        Runs the mechanical transmission simulation.

    Raises
    ------
    TypeError
        - If ``transmission`` is not an instance of ``Transmission``,
        - if the first element in ``transmission`` is not an instance of ``MotorBase``,
        - if an element of ``transmission`` is not an instance of ``RotatingObject``,
        - if ``motor_control`` is not an instance of ``MotorControlBase``.
    ValueError
        If ``transmission.chain`` is an empty tuple.

    See Also
    --------
    :py:class:`gearpy.transmission.Transmission`
    :py:class:`gearpy.motor_control.motor_control.PWMControl`
    """
    def __init__(self, transmission: Transmission, motor_control: Optional[MotorControlBase] = None):
        if not isinstance(transmission, Transmission):
            raise TypeError(f"Parameter 'transmission' must be an instance of {Transmission.__name__!r}.")

        if not transmission.chain:
            raise ValueError("Parameter 'transmission.chain' cannot be an empty tuple.")

        if not isinstance(transmission.chain[0], MotorBase):
            raise TypeError(f"First element in 'transmission' must be an instance of {MotorBase.__name__!r}.")

        if not all([isinstance(item, RotatingObject) for item in transmission.chain]):
            raise TypeError(f"All elements of 'transmission' must be instances of {RotatingObject.__name__!r}.")

        if not isinstance(motor_control, MotorControlBase) and motor_control is not None:
            raise TypeError(f"Parameter 'motor_control' must be an instance of {MotorControlBase.__name__!r}.")

        self.transmission = transmission
        self.motor_control = motor_control

    def run(self, time_discretization: TimeInterval, simulation_time: TimeInterval):
        """Runs the mechanical transmission simulation. \n
        The simulation is performed in several steps:

        - it computes the whole mechanical transmission equivalent moment of inertia with respect to the last
          gear, by multiplying each element's moment of inertia, starting from the motor, by it gear ratio with respect
          to the following element in the transmission chain and sum them up
        - for each time step and for each mechanical transmission element, it computes:

          - the angular position and angular speed, from the last element in the transmission chain to the first one
          - the driving torque, load load torque, net torque, electrical current for motors (if computable), tangential
            force, bending stress and contact stress for gears (if computable)
          - the angular acceleration of each mechanical transmission element.

        - for each time step it performs a time integration to compute angular position and speed of the last element in
          the transmission chain.

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
            - if function ``external_torque`` of one gear in the transmission chain does not return an instance of
              ``Torque``.
        ValueError
            - If ``time_discretization`` is greater or equal to ``simulation_time``,
            - if function ``external_torque`` has not been defined for any gear of the transmission.

        Notes
        -----
        If ``transmission.chain.time`` is an empty list, it perform the simulation starting the time from ``0 sec``;
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
                    for element in self.transmission.chain if isinstance(element, GearBase)]):
            raise ValueError("The function 'external_torque' has not been defined for any gear of the transmission. "
                             "Add this function to a transmission gear.")

        self._compute_transmission_inertia()
        if self.transmission.time:
            initial_time = self.transmission.time[-1]
            final_time = initial_time + simulation_time + time_discretization
        else:
            initial_time = Time(value = 0, unit = time_discretization.unit)
            final_time = initial_time + simulation_time + time_discretization
            self.transmission.update_time(initial_time)
            self._compute_transmission_variables()

        for k in np.arange(initial_time.value + time_discretization.value, final_time.value, time_discretization.value):

            self.transmission.update_time(Time(value = float(k), unit = time_discretization.unit))
            self._time_integration(time_discretization = time_discretization)
            self._compute_transmission_variables()

    def _compute_transmission_inertia(self):

        self.transmission_inertia_moment = self.transmission.chain[0].inertia_moment
        for item in self.transmission.chain[1:]:
            self.transmission_inertia_moment *= item.master_gear_ratio
            self.transmission_inertia_moment += item.inertia_moment

    def _compute_transmission_variables(self):

        self._compute_angular_position_and_speed()
        self._compute_load_torque()
        self._compute_motor_control()
        self._compute_driving_torque()
        self._compute_torque()
        self._compute_force()
        self._compute_stress()
        self._compute_electric_current()
        self._compute_angular_acceleration()
        self._update_time_variables()

    def _compute_angular_position_and_speed(self):

        for i in range(len(self.transmission.chain) - 2, -1, -1):
            gear_ratio = self.transmission.chain[i + 1].master_gear_ratio
            self._transmit_angular_position(gear_ratio = gear_ratio, i = i)
            self._transmit_angular_speed(gear_ratio = gear_ratio, i = i)

    def _transmit_angular_position(self, gear_ratio, i):

        self.transmission.chain[i].angular_position = gear_ratio*self.transmission.chain[i + 1].angular_position

    def _transmit_angular_speed(self, gear_ratio, i):

        self.transmission.chain[i].angular_speed = gear_ratio*self.transmission.chain[i + 1].angular_speed

    def _transmit_angular_acceleration(self, gear_ratio, i):

        self.transmission.chain[i].angular_acceleration = gear_ratio*self.transmission.chain[i + 1].angular_acceleration

    def _compute_motor_control(self):

        if self.motor_control is not None:
            self.motor_control.apply_rules()

    def _compute_driving_torque(self):

        self.transmission.chain[0].compute_torque()

        for i in range(1, len(self.transmission.chain)):
            gear_ratio = self.transmission.chain[i].master_gear_ratio
            self.transmission.chain[i].driving_torque = gear_ratio*self.transmission.chain[i].master_gear_efficiency*\
                                                        self.transmission.chain[i - 1].driving_torque

    def _compute_load_torque(self):

        for i in range(len(self.transmission.chain) - 1, 0, -1):
            if hasattr(self.transmission.chain[i], 'external_torque'):
                if self.transmission.chain[i].external_torque is not None:
                    external_torque = \
                        self.transmission.chain[i].\
                            external_torque(time = self.transmission.time[-1],
                                            angular_position = self.transmission.chain[i].angular_position,
                                            angular_speed = self.transmission.chain[i].angular_speed)
                    if not isinstance(external_torque, Torque):
                        raise TypeError(f"Function 'external_torque' of {self.transmission.chain[i].name!r} "
                                        f"must return an instance of {Torque.__name__!r}.")
                    self.transmission.chain[i].load_torque = external_torque
            gear_ratio = self.transmission.chain[i].master_gear_ratio
            self.transmission.chain[i - 1].load_torque = self.transmission.chain[i].load_torque/gear_ratio

    def _compute_torque(self):

        for item in self.transmission.chain:
            item.torque = item.driving_torque - item.load_torque

    def _compute_force(self):

        for item in self.transmission.chain:
            if isinstance(item, GearBase):
                if item.tangential_force_is_computable:
                    item.compute_tangential_force()

    def _compute_stress(self):

        for item in self.transmission.chain:
            if isinstance(item, GearBase):
                if item.bending_stress_is_computable:
                    item.compute_bending_stress()
                    if item.contact_stress_is_computable:
                        item.compute_contact_stress()

    def _compute_electric_current(self):

        if self.transmission.chain[0].electric_current_is_computable:
            self.transmission.chain[0].compute_electric_current()

    def _compute_angular_acceleration(self):

        self.transmission.chain[-1].angular_acceleration = self.transmission.chain[-1].torque/\
                                                           self.transmission_inertia_moment

        for i in range(len(self.transmission.chain) - 2, -1, -1):
            gear_ratio = self.transmission.chain[i + 1].master_gear_ratio
            self._transmit_angular_acceleration(gear_ratio = gear_ratio, i = i)

    def _update_time_variables(self):

        for item in self.transmission.chain:
            item.update_time_variables()

    def _time_integration(self, time_discretization: TimeInterval):

        self.transmission.chain[-1].angular_speed += \
            self.transmission.chain[-1].angular_acceleration*time_discretization
        self.transmission.chain[-1].angular_position += \
            self.transmission.chain[-1].angular_speed*time_discretization
