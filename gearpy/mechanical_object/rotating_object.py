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
        self.__inertia = inertia
        self.__time_variables = {'angle': [],
                                 'speed': [],
                                 'acceleration': [],
                                 'torque': []}

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
