from abc import abstractmethod
from .mechanical_object import MechanicalObject


class RotatingObject(MechanicalObject):

    @abstractmethod
    def __init__(self, name, inertia):
        super().__init__(name = name)
        self.__angle = None
        self.__speed = None
        self.__acceleration = None
        self.__torque = None
        self.__driving_torque = None
        self.__load_torque = None
        self.__inertia = inertia
        self.__time_variables = {'angle': [],
                                 'speed': [],
                                 'acceleration': [],
                                 'torque': [],
                                 'driving torque': [],
                                 'load torque': []}

    @property
    @abstractmethod
    def angle(self):
        return self.__angle

    @angle.setter
    @abstractmethod
    def angle(self, angle):
        self.__angle = angle

    @property
    @abstractmethod
    def speed(self):
        return self.__speed

    @speed.setter
    @abstractmethod
    def speed(self, speed):
        self.__speed = speed

    @property
    @abstractmethod
    def acceleration(self):
        return self.__acceleration

    @acceleration.setter
    @abstractmethod
    def acceleration(self, acceleration):
        self.__acceleration = acceleration

    @property
    @abstractmethod
    def torque(self):
        return self.__torque

    @torque.setter
    @abstractmethod
    def torque(self, torque):
        self.__torque = torque

    @property
    @abstractmethod
    def driving_torque(self):
        return self.__driving_torque

    @driving_torque.setter
    @abstractmethod
    def driving_torque(self, driving_torque):
        self.__driving_torque = driving_torque

    @property
    @abstractmethod
    def load_torque(self):
        return self.__load_torque

    @load_torque.setter
    @abstractmethod
    def load_torque(self, load_torque):
        self.__load_torque = load_torque

    @property
    @abstractmethod
    def inertia(self):
        return self.__inertia

    @property
    @abstractmethod
    def time_variables(self):
        return self.__time_variables

    @abstractmethod
    def update_time_variables(self):
        self.__time_variables['angle'].append(self.__angle)
        self.__time_variables['speed'].append(self.__speed)
        self.__time_variables['acceleration'].append(self.__acceleration)
        self.__time_variables['torque'].append(self.__torque)
        self.__time_variables['driving torque'].append(self.__driving_torque)
        self.__time_variables['load torque'].append(self.__load_torque)
