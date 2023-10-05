from abc import abstractmethod
from .mechanical_object import MechanicalObject
from typing import Union


class RotatingObject(MechanicalObject):

    @abstractmethod
    def __init__(self, name: str, inertia: Union[float, int]):
        super().__init__(name = name)

        if not isinstance(inertia, float) and not isinstance(inertia, int):
            raise TypeError("Parameter 'inertia' must be a float or an integer.")

        if inertia <= 0:
            raise ValueError("Parameter 'inertia' must be positive.")

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
    def angle(self) -> Union[float, int]:
        return self.__angle

    @angle.setter
    @abstractmethod
    def angle(self, angle: Union[float, int]):
        if not isinstance(angle, float) and not isinstance(angle, int):
            raise TypeError("Parameter 'angle' must be a float or an integer.")

        self.__angle = angle

    @property
    @abstractmethod
    def speed(self) -> Union[float, int]:
        return self.__speed

    @speed.setter
    @abstractmethod
    def speed(self, speed: Union[float, int]):
        if not isinstance(speed, float) and not isinstance(speed, int):
            raise TypeError("Parameter 'speed' must be a float or an integer.")

        self.__speed = speed

    @property
    @abstractmethod
    def acceleration(self) -> Union[float, int]:
        return self.__acceleration

    @acceleration.setter
    @abstractmethod
    def acceleration(self, acceleration: Union[float, int]):
        if not isinstance(acceleration, float) and not isinstance(acceleration, int):
            raise TypeError("Parameter 'acceleration' must be a float or an integer.")

        self.__acceleration = acceleration

    @property
    @abstractmethod
    def torque(self) -> Union[float, int]:
        return self.__torque

    @torque.setter
    @abstractmethod
    def torque(self, torque: Union[float, int]):
        if not isinstance(torque, float) and not isinstance(torque, int):
            raise TypeError("Parameter 'torque' must be a float or an integer.")

        self.__torque = torque

    @property
    @abstractmethod
    def driving_torque(self) -> Union[float, int]:
        return self.__driving_torque

    @driving_torque.setter
    @abstractmethod
    def driving_torque(self, driving_torque: Union[float, int]):
        if not isinstance(driving_torque, float) and not isinstance(driving_torque, int):
            raise TypeError("Parameter 'driving_torque' must be a float or an integer.")

        self.__driving_torque = driving_torque

    @property
    @abstractmethod
    def load_torque(self) -> Union[float, int]:
        return self.__load_torque

    @load_torque.setter
    @abstractmethod
    def load_torque(self, load_torque: Union[float, int]):
        if not isinstance(load_torque, float) and not isinstance(load_torque, int):
            raise TypeError("Parameter 'load_torque' must be a float or an integer.")

        self.__load_torque = load_torque

    @property
    @abstractmethod
    def inertia(self) -> Union[float, int]:
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
