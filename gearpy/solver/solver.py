import numpy as np


class Solver:

    def __init__(self, time_discretization, simulation_time, transmission):

        self.time_discretization = time_discretization
        self.simulation_time = simulation_time
        self.transmission = transmission
        self.time = []

    def run(self):

        self._compute_transmission_inertia()
        self._compute_transmission_initial_state()

        for k in np.arange(0, self.simulation_time + self.time_discretization, self.time_discretization):

            self.time.append(k)

            self._compute_kinematic_variables()
            self._compute_driving_torque()
            self._compute_load_torque()
            self._compute_torque()
            self._time_integration()
            self._update_time_variables()

    def _compute_transmission_inertia(self):

        self.transmission_inertia = self.transmission[0].inertia
        for item in self.transmission[1:]:
            self.transmission_inertia *= item.master_gear_ratio
            self.transmission_inertia += item.inertia

    def _compute_transmission_initial_state(self):

        for i in range(len(self.transmission) - 2, -1, -1):
            gear_ratio = self.transmission[i + 1].master_gear_ratio
            self._compute_angle(gear_ratio = gear_ratio, i = i)
            self._compute_speed(gear_ratio = gear_ratio, i = i)

        self._compute_driving_torque()
        self._compute_load_torque()
        self._compute_torque()

        self.transmission[-1].acceleration = self.transmission[-1].torque/self.transmission_inertia

        for i in range(len(self.transmission) - 2, -1, -1):
            gear_ratio = self.transmission[i + 1].master_gear_ratio
            self._compute_acceleration(gear_ratio = gear_ratio, i = i)

    def _update_time_variables(self):

        for item in self.transmission:
            item.update_time_variables()

    def _compute_kinematic_variables(self):

        for i in range(len(self.transmission) - 2, -1, -1):
            gear_ratio = self.transmission[i + 1].master_gear_ratio
            self._compute_angle(gear_ratio = gear_ratio, i = i)
            self._compute_speed(gear_ratio = gear_ratio, i = i)
            self._compute_acceleration(gear_ratio = gear_ratio, i = i)

    def _compute_angle(self, gear_ratio, i):
        self.transmission[i].angle = gear_ratio*self.transmission[i + 1].angle

    def _compute_speed(self, gear_ratio, i):
        self.transmission[i].speed = gear_ratio*self.transmission[i + 1].speed

    def _compute_acceleration(self, gear_ratio, i):
        self.transmission[i].acceleration = gear_ratio*self.transmission[i + 1].acceleration

    def _compute_driving_torque(self):

        self.transmission[0].driving_torque = self.transmission[0].compute_torque()

        for i in range(1, len(self.transmission)):
            gear_ratio = self.transmission[i].master_gear_ratio
            self.transmission[i].driving_torque = gear_ratio*self.transmission[i - 1].driving_torque

    def _compute_load_torque(self):

        for i in range(len(self.transmission) - 1, 0, -1):
            if self.transmission[i].external_torque != 0:
                self.transmission[i].load_torque = self.transmission[i].external_torque
            gear_ratio = self.transmission[i].master_gear_ratio
            self.transmission[i - 1].load_torque = self.transmission[i].load_torque/gear_ratio

    def _compute_torque(self):

        for item in self.transmission:
            item.torque = item.driving_torque - item.load_torque

    def _time_integration(self):

        self.transmission[-1].acceleration = self.transmission[-1].torque/self.transmission_inertia
        self.transmission[-1].speed += self.transmission[-1].acceleration*self.time_discretization
        self.transmission[-1].angle += self.transmission[-1].speed*self.time_discretization
