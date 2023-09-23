from abc import abstractmethod
from gearpy.mechanical_object.rotating_object import RotatingObject


class GearBase(RotatingObject):

    @abstractmethod
    def __init__(self, name, n_teeth, inertia):
        super().__init__(name = name, inertia = inertia)
        self.__n_teeth = n_teeth
        self.__driven_by = None
        self.__drives = None
        self.__master_gear_ratio = None

    @property
    @abstractmethod
    def n_teeth(self):
        return self.__n_teeth

    @property
    @abstractmethod
    def driven_by(self):
        return self.__driven_by

    @driven_by.setter
    @abstractmethod
    def driven_by(self, driven_by):
        self.__driven_by = driven_by

    @property
    @abstractmethod
    def drives(self):
        return self.__drives

    @drives.setter
    @abstractmethod
    def drives(self, drives):
        self.__drives = drives

    @property
    @abstractmethod
    def master_gear_ratio(self):
        return self.__master_gear_ratio

    @master_gear_ratio.setter
    @abstractmethod
    def master_gear_ratio(self, master_gear_ratio):
        self.__master_gear_ratio = master_gear_ratio
