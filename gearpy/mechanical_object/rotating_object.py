from abc import abstractmethod
from gearpy.units import Acceleration, Angle, Inertia, Speed, Torque
from .mechanical_object import MechanicalObject


class RotatingObject(MechanicalObject):

    @abstractmethod
    def __init__(self, name: str, inertia: Inertia):
        super().__init__(name = name)

        if not isinstance(inertia, Inertia):
            raise TypeError("Parameter 'inertia' must be an instance of Inertia.")

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
    def angle(self) -> Angle:
        return self.__angle

    @angle.setter
    @abstractmethod
    def angle(self, angle: Angle):
        if not isinstance(angle, Angle):
            raise TypeError("Parameter 'angle' must be an instance of Angle.")

        self.__angle = angle

    @property
    @abstractmethod
    def speed(self) -> Speed:
        return self.__speed

    @speed.setter
    @abstractmethod
    def speed(self, speed: Speed):
        if not isinstance(speed, Speed):
            raise TypeError("Parameter 'speed' must be an instance of Speed.")

        self.__speed = speed

    @property
    @abstractmethod
    def acceleration(self) -> Acceleration:
        return self.__acceleration

    @acceleration.setter
    @abstractmethod
    def acceleration(self, acceleration: Acceleration):
        if not isinstance(acceleration, Acceleration):
            raise TypeError("Parameter 'acceleration' must be an instance of Acceleration.")

        self.__acceleration = acceleration

    @property
    @abstractmethod
    def torque(self) -> Torque:
        return self.__torque

    @torque.setter
    @abstractmethod
    def torque(self, torque: Torque):
        if not isinstance(torque, Torque):
            raise TypeError("Parameter 'torque' must be an instance of Torque.")

        self.__torque = torque

    @property
    @abstractmethod
    def driving_torque(self) -> Torque:
        return self.__driving_torque

    @driving_torque.setter
    @abstractmethod
    def driving_torque(self, driving_torque: Torque):
        if not isinstance(driving_torque, Torque):
            raise TypeError("Parameter 'driving_torque' must be an instance of Torque.")

        self.__driving_torque = driving_torque

    @property
    @abstractmethod
    def load_torque(self) -> Torque:
        return self.__load_torque

    @load_torque.setter
    @abstractmethod
    def load_torque(self, load_torque: Torque):
        if not isinstance(load_torque, Torque):
            raise TypeError("Parameter 'load_torque' must be an instance of Torque.")

        self.__load_torque = load_torque

    @property
    @abstractmethod
    def inertia(self) -> Inertia:
        return self.__inertia

    @property
    @abstractmethod
    def time_variables(self) -> dict:
        return self.__time_variables

    @abstractmethod
    def update_time_variables(self):
        self.__time_variables['angle'].append(self.__angle)
        self.__time_variables['speed'].append(self.__speed)
        self.__time_variables['acceleration'].append(self.__acceleration)
        self.__time_variables['torque'].append(self.__torque)
        self.__time_variables['driving torque'].append(self.__driving_torque)
        self.__time_variables['load torque'].append(self.__load_torque)
