from abc import abstractmethod
from gearpy.mechanical_object.rotating_object import RotatingObject
from typing import Callable, Union


class GearBase(RotatingObject):

    @abstractmethod
    def __init__(self, name: str, n_teeth: int, inertia: float):
        super().__init__(name = name, inertia = inertia)

        if not isinstance(n_teeth, int):
            raise TypeError("Parameter 'n_teeth' must be an integer.")

        if n_teeth <= 0:
            raise ValueError("Parameter 'n_teeth' must be positive.")

        self.__n_teeth = n_teeth
        self.__driven_by = None
        self.__drives = None
        self.__master_gear_ratio = None
        self.__master_gear_efficiency = 1
        self.__external_torque = None

    @property
    @abstractmethod
    def n_teeth(self) -> int:
        return self.__n_teeth

    @property
    @abstractmethod
    def driven_by(self) -> RotatingObject:
        return self.__driven_by

    @driven_by.setter
    @abstractmethod
    def driven_by(self, driven_by: RotatingObject):
        if not isinstance(driven_by, RotatingObject):
            raise TypeError("Parameter 'drives' must be a RotatingObject")

        self.__driven_by = driven_by

    @property
    @abstractmethod
    def drives(self) -> RotatingObject:
        return self.__drives

    @drives.setter
    @abstractmethod
    def drives(self, drives: RotatingObject):
        if not isinstance(drives, RotatingObject):
            raise TypeError("Parameter 'drives' must be a RotatingObject")

        self.__drives = drives

    @property
    @abstractmethod
    def master_gear_ratio(self) -> float:
        return self.__master_gear_ratio

    @master_gear_ratio.setter
    @abstractmethod
    def master_gear_ratio(self, master_gear_ratio: float):
        if not isinstance(master_gear_ratio, float):
            raise TypeError("Parameter 'master_gear_ratio' must be a float.")

        if master_gear_ratio <= 0:
            raise ValueError("Parameter 'master_gear_ratio' must be positive.")

        self.__master_gear_ratio = master_gear_ratio

    @property
    @abstractmethod
    def master_gear_efficiency(self) -> Union[float, int]:
        return self.__master_gear_efficiency

    @master_gear_efficiency.setter
    @abstractmethod
    def master_gear_efficiency(self, master_gear_efficiency: Union[float, int]):
        if not isinstance(master_gear_efficiency, float) and not isinstance(master_gear_efficiency, int):
            raise TypeError("Parameter 'master_gear_efficiency' must be a float or an integer.")

        if master_gear_efficiency > 1 or master_gear_efficiency < 0:
            raise ValueError("Parameter 'master_gear_efficiency' must be within 0 and 1.")

        self.__master_gear_efficiency = master_gear_efficiency

    @property
    @abstractmethod
    def external_torque(self) -> Callable:
        return self.__external_torque

    @external_torque.setter
    @abstractmethod
    def external_torque(self, external_torque: Callable):
        if not isinstance(external_torque, Callable):
            raise TypeError("Parameter 'external_torque' must be callable.")

        self.__external_torque = external_torque
