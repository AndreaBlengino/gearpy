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
