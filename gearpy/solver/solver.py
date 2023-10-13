from gearpy.mechanical_object import RotatingObject
from gearpy.motor import MotorBase
from gearpy.transmission import Transmission
from gearpy.units import Time, TimeInterval
import numpy as np


class Solver:

    def __init__(self, time_discretization: TimeInterval, simulation_time: TimeInterval, transmission: Transmission):
        if not isinstance(time_discretization, TimeInterval):
            raise TypeError("Parameter 'time_discretization' must be an instance of TimeInterval.")

        if not isinstance(simulation_time, TimeInterval):
            raise TypeError("Parameter 'simulation_time' must be an instance of TimeInterval.")

        if not isinstance(transmission, Transmission):
            raise TypeError("Parameter 'transmission' must be an instance of Transmission.")

        if time_discretization >= simulation_time:
            raise ValueError("Parameter 'time_discretization' cannot be greater or equal to 'simulation_time'.")

        if not transmission.chain:
            raise ValueError("Parameter 'transmission.chain' cannot be an empty list.")

        if not isinstance(transmission.chain[0], MotorBase):
            raise TypeError("First element in 'transmission' must be an instance of MotorBase.")

        if not all([isinstance(item, RotatingObject) for item in transmission.chain]):
            raise TypeError("All elements of 'transmission' must be instances of RotatingObject.")

        self.time_discretization = time_discretization
        self.simulation_time = simulation_time
        self.transmission_chain = transmission.chain
        self.time = [Time(value = 0, unit = time_discretization.unit)]

    def run(self):

        self._compute_transmission_inertia()
        self._compute_transmission_initial_state()
        self._update_time_variables()

        for k in np.arange(self.time_discretization.value, self.simulation_time.value, self.time_discretization.value):

            self.time.append(Time(value = float(k), unit = self.time_discretization.unit))

            self._compute_kinematic_variables()
            self._compute_driving_torque()
            self._compute_load_torque()
            self._compute_torque()
            self._time_integration()
            self._update_time_variables()

    def _compute_transmission_inertia(self):

        self.transmission_inertia = self.transmission_chain[0].inertia
        for item in self.transmission_chain[1:]:
            self.transmission_inertia *= item.master_gear_ratio
            self.transmission_inertia += item.inertia

    def _compute_transmission_initial_state(self):

        for i in range(len(self.transmission_chain) - 2, -1, -1):
            gear_ratio = self.transmission_chain[i + 1].master_gear_ratio
            self._compute_angle(gear_ratio = gear_ratio, i = i)
            self._compute_speed(gear_ratio = gear_ratio, i = i)

        self._compute_driving_torque()
        self._compute_load_torque()
        self._compute_torque()

        self.transmission_chain[-1].acceleration = self.transmission_chain[-1].torque/self.transmission_inertia

        for i in range(len(self.transmission_chain) - 2, -1, -1):
            gear_ratio = self.transmission_chain[i + 1].master_gear_ratio
            self._compute_acceleration(gear_ratio = gear_ratio, i = i)

    def _update_time_variables(self):

        for item in self.transmission_chain:
            item.update_time_variables()

    def _compute_kinematic_variables(self):

        for i in range(len(self.transmission_chain) - 2, -1, -1):
            gear_ratio = self.transmission_chain[i + 1].master_gear_ratio
            self._compute_angle(gear_ratio = gear_ratio, i = i)
            self._compute_speed(gear_ratio = gear_ratio, i = i)
            self._compute_acceleration(gear_ratio = gear_ratio, i = i)

    def _compute_angle(self, gear_ratio, i):

        self.transmission_chain[i].angle = gear_ratio*self.transmission_chain[i + 1].angle

    def _compute_speed(self, gear_ratio, i):

        self.transmission_chain[i].speed = gear_ratio*self.transmission_chain[i + 1].speed

    def _compute_acceleration(self, gear_ratio, i):

        self.transmission_chain[i].acceleration = gear_ratio*self.transmission_chain[i + 1].acceleration

    def _compute_driving_torque(self):

        self.transmission_chain[0].driving_torque = self.transmission_chain[0].compute_torque()

        for i in range(1, len(self.transmission_chain)):
            gear_ratio = self.transmission_chain[i].master_gear_ratio
            self.transmission_chain[i].driving_torque = gear_ratio*self.transmission_chain[i].master_gear_efficiency*\
                                                        self.transmission_chain[i - 1].driving_torque

    def _compute_load_torque(self):

        for i in range(len(self.transmission_chain) - 1, 0, -1):
            if self.transmission_chain[i].external_torque is not None:
                self.transmission_chain[i].load_torque = \
                    self.transmission_chain[i].external_torque(time = self.time[-1],
                                                               angle = self.transmission_chain[i].angle,
                                                               speed = self.transmission_chain[i].speed)
            gear_ratio = self.transmission_chain[i].master_gear_ratio
            self.transmission_chain[i - 1].load_torque = self.transmission_chain[i].load_torque/gear_ratio

    def _compute_torque(self):

        for item in self.transmission_chain:
            item.torque = item.driving_torque - item.load_torque

    def _time_integration(self):

        self.transmission_chain[-1].acceleration = self.transmission_chain[-1].torque/self.transmission_inertia
        self.transmission_chain[-1].speed += self.transmission_chain[-1].acceleration*self.time_discretization
        self.transmission_chain[-1].angle += self.transmission_chain[-1].speed*self.time_discretization
