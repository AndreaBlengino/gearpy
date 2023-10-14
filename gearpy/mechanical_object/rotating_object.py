from abc import abstractmethod
from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, InertiaMoment, Torque
from .mechanical_object import MechanicalObject


class RotatingObject(MechanicalObject):

    @abstractmethod
    def __init__(self, name: str, inertia_moment: InertiaMoment):
        super().__init__(name = name)

        if not isinstance(inertia_moment, InertiaMoment):
            raise TypeError(f"Parameter 'inertia_moment' must be an instance of {InertiaMoment.__name__!r}.")

        self.__angular_position = None
        self.__angular_speed = None
        self.__angular_acceleration = None
        self.__torque = None
        self.__driving_torque = None
        self.__load_torque = None
        self.__inertia_moment = inertia_moment
        self.__time_variables = {'angular position': [],
                                 'angular speed': [],
                                 'angular acceleration': [],
                                 'torque': [],
                                 'driving torque': [],
                                 'load torque': []}

    @property
    @abstractmethod
    def angular_position(self) -> AngularPosition:
        return self.__angular_position

    @angular_position.setter
    @abstractmethod
    def angular_position(self, angular_position: AngularPosition):
        if not isinstance(angular_position, AngularPosition):
            raise TypeError(f"Parameter 'angular_position' must be an instance of {AngularPosition.__name__!r}.")

        self.__angular_position = angular_position

    @property
    @abstractmethod
    def angular_speed(self) -> AngularSpeed:
        return self.__angular_speed

    @angular_speed.setter
    @abstractmethod
    def angular_speed(self, angular_speed: AngularSpeed):
        if not isinstance(angular_speed, AngularSpeed):
            raise TypeError(f"Parameter 'angular_speed' must be an instance of {AngularSpeed.__name__!r}.")

        self.__angular_speed = angular_speed

    @property
    @abstractmethod
    def angular_acceleration(self) -> AngularAcceleration:
        return self.__angular_acceleration

    @angular_acceleration.setter
    @abstractmethod
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        if not isinstance(angular_acceleration, AngularAcceleration):
            raise TypeError(f"Parameter 'angular_acceleration' must be an instance of "
                            f"{AngularAcceleration.__name__!r}.")

        self.__angular_acceleration = angular_acceleration

    @property
    @abstractmethod
    def torque(self) -> Torque:
        return self.__torque

    @torque.setter
    @abstractmethod
    def torque(self, torque: Torque):
        if not isinstance(torque, Torque):
            raise TypeError(f"Parameter 'torque' must be an instance of {Torque.__name__!r}.")

        self.__torque = torque

    @property
    @abstractmethod
    def driving_torque(self) -> Torque:
        return self.__driving_torque

    @driving_torque.setter
    @abstractmethod
    def driving_torque(self, driving_torque: Torque):
        if not isinstance(driving_torque, Torque):
            raise TypeError(f"Parameter 'driving_torque' must be an instance of {Torque.__name__!r}.")

        self.__driving_torque = driving_torque

    @property
    @abstractmethod
    def load_torque(self) -> Torque:
        return self.__load_torque

    @load_torque.setter
    @abstractmethod
    def load_torque(self, load_torque: Torque):
        if not isinstance(load_torque, Torque):
            raise TypeError(f"Parameter 'load_torque' must be an instance of {Torque.__name__!r}.")

        self.__load_torque = load_torque

    @property
    @abstractmethod
    def inertia_moment(self) -> InertiaMoment:
        return self.__inertia_moment

    @property
    @abstractmethod
    def time_variables(self) -> dict:
        return self.__time_variables

    @abstractmethod
    def update_time_variables(self):
        self.__time_variables['angular position'].append(self.__angular_position)
        self.__time_variables['angular speed'].append(self.__angular_speed)
        self.__time_variables['angular acceleration'].append(self.__angular_acceleration)
        self.__time_variables['torque'].append(self.__torque)
        self.__time_variables['driving torque'].append(self.__driving_torque)
        self.__time_variables['load torque'].append(self.__load_torque)
