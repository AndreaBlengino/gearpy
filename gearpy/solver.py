from gearpy.mechanical_object import RotatingObject, MotorBase, GearBase
from gearpy.transmission import Transmission
from gearpy.units import Time, TimeInterval
import numpy as np


class Solver:
    r"""``gearpy.solver.Solver`` object.

    Attributes
    ----------
    :py:attr:`time_discretization` : TimeInterval
        Time discretization to be used for the simulation.
    :py:attr:`simulation_time` : TimeInterval
        Duration of the simulation.
    :py:attr:`transmission` : Transmission
        Mechanical transmission to be simulated.

    Methods
    -------
    :py:meth:`run`
        Runs the mechanical transmission simulation.

    Raises
    ------
    TypeError
        - If ``time_discretization`` is not an instance of ``TimeInterval``,
        - if ``simulation_time`` is not an instance of ``TimeInterval``,
        - if ``transmission`` is not an instance of ``Transmission``,
        - if the first element in ``transmission`` is not an instance of ``MotorBase``,
        - if an element of ``transmission`` is not an instance of ``RotatingObject``.
    ValueError
        - If ``time_discretization`` is greater or equal to ``simulation_time``,
        - if ``transmission.chain`` is an empty tuple.
    """

    def __init__(self, time_discretization: TimeInterval, simulation_time: TimeInterval, transmission: Transmission):
        if not isinstance(time_discretization, TimeInterval):
            raise TypeError(f"Parameter 'time_discretization' must be an instance of {TimeInterval.__name__!r}.")

        if not isinstance(simulation_time, TimeInterval):
            raise TypeError(f"Parameter 'simulation_time' must be an instance of {TimeInterval.__name__!r}.")

        if not isinstance(transmission, Transmission):
            raise TypeError(f"Parameter 'transmission' must be an instance of {Transmission.__name__!r}.")

        if time_discretization >= simulation_time:
            raise ValueError("Parameter 'time_discretization' cannot be greater or equal to 'simulation_time'.")

        if not transmission.chain:
            raise ValueError("Parameter 'transmission.chain' cannot be an empty tuple.")

        if not isinstance(transmission.chain[0], MotorBase):
            raise TypeError(f"First element in 'transmission' must be an instance of {MotorBase.__name__!r}.")

        if not all([isinstance(item, RotatingObject) for item in transmission.chain]):
            raise TypeError(f"All elements of 'transmission' must be instances of {RotatingObject.__name__!r}.")

        self.time_discretization = time_discretization
        self.simulation_time = simulation_time
        self.transmission = transmission

    def run(self):
        """Runs the mechanical transmission simulation. \n
        Firstly it computes the whole mechanical transmission equivalent moment of inertia with respect to the last
        gear, by multiplying each element's moment of inertia, starting from the motor, by it gear ratio with respect to
        the following element in the transmission chain and sum them up. \n
        Then it compute the initial state in terms of angular position, speed and acceleration for each mechanical
        transmission element. \n
        Finally, for each time step and for each mechanical transmission element, it computes the kinematic variables,
        it computes the driving, load and net torque, it computes the angular acceleration of the last element in the
        transmission chain and perform a time integration to compute its angular speed and position.
        """
        self.transmission.update_time(Time(value = 0, unit = self.time_discretization.unit))
        self._compute_transmission_inertia()
        self._compute_transmission_initial_state()
        self._update_time_variables()

        for k in np.arange(self.time_discretization.value, self.simulation_time.value, self.time_discretization.value):

            self.transmission.update_time(Time(value = float(k), unit = self.time_discretization.unit))

            self._compute_kinematic_variables()
            self._compute_driving_torque()
            self._compute_load_torque()
            self._compute_torque()
            self._compute_force()
            self._compute_stress()
            self._time_integration()
            self._update_time_variables()

    def _compute_transmission_inertia(self):

        self.transmission_inertia_moment = self.transmission.chain[0].inertia_moment
        for item in self.transmission.chain[1:]:
            self.transmission_inertia_moment *= item.master_gear_ratio
            self.transmission_inertia_moment += item.inertia_moment

    def _compute_transmission_initial_state(self):

        for i in range(len(self.transmission.chain) - 2, -1, -1):
            gear_ratio = self.transmission.chain[i + 1].master_gear_ratio
            self._compute_angular_position(gear_ratio = gear_ratio, i = i)
            self._compute_angular_speed(gear_ratio = gear_ratio, i = i)

        self._compute_driving_torque()
        self._compute_load_torque()
        self._compute_torque()
        self._compute_force()
        self._compute_stress()

        self.transmission.chain[-1].angular_acceleration = self.transmission.chain[-1].torque/\
                                                           self.transmission_inertia_moment

        for i in range(len(self.transmission.chain) - 2, -1, -1):
            gear_ratio = self.transmission.chain[i + 1].master_gear_ratio
            self._compute_angular_acceleration(gear_ratio = gear_ratio, i = i)

    def _update_time_variables(self):

        for item in self.transmission.chain:
            item.update_time_variables()

    def _compute_kinematic_variables(self):

        for i in range(len(self.transmission.chain) - 2, -1, -1):
            gear_ratio = self.transmission.chain[i + 1].master_gear_ratio
            self._compute_angular_position(gear_ratio = gear_ratio, i = i)
            self._compute_angular_speed(gear_ratio = gear_ratio, i = i)
            self._compute_angular_acceleration(gear_ratio = gear_ratio, i = i)

    def _compute_angular_position(self, gear_ratio, i):

        self.transmission.chain[i].angular_position = gear_ratio*self.transmission.chain[i + 1].angular_position

    def _compute_angular_speed(self, gear_ratio, i):

        self.transmission.chain[i].angular_speed = gear_ratio*self.transmission.chain[i + 1].angular_speed

    def _compute_angular_acceleration(self, gear_ratio, i):

        self.transmission.chain[i].angular_acceleration = gear_ratio*self.transmission.chain[i + 1].angular_acceleration

    def _compute_driving_torque(self):

        self.transmission.chain[0].driving_torque = self.transmission.chain[0].compute_torque()

        for i in range(1, len(self.transmission.chain)):
            gear_ratio = self.transmission.chain[i].master_gear_ratio
            self.transmission.chain[i].driving_torque = gear_ratio*self.transmission.chain[i].master_gear_efficiency*\
                                                        self.transmission.chain[i - 1].driving_torque

    def _compute_load_torque(self):

        for i in range(len(self.transmission.chain) - 1, 0, -1):
            if hasattr(self.transmission.chain[i], 'external_torque'):
                if self.transmission.chain[i].external_torque is not None:
                    self.transmission.chain[i].load_torque = \
                        self.transmission.chain[i]. \
                            external_torque(time = self.transmission.time[-1],
                                            angular_position = self.transmission.chain[i].angular_position,
                                            angular_speed = self.transmission.chain[i].angular_speed)
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

    def _time_integration(self):

        self.transmission.chain[-1].angular_acceleration = self.transmission.chain[-1].torque/\
                                                           self.transmission_inertia_moment
        self.transmission.chain[-1].angular_speed += self.transmission.chain[-1].angular_acceleration*\
                                                     self.time_discretization
        self.transmission.chain[-1].angular_position += self.transmission.chain[-1].angular_speed*\
                                                        self.time_discretization
