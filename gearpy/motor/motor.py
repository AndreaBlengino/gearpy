from abc import abstractmethod
from gearpy.mechanical_object.rotating_object import RotatingObject


class MotorBase(RotatingObject):

    @abstractmethod
    def __init__(self, name):
        super().__init__(name = name)
        self.__drives = None

    @property
    @abstractmethod
    def drives(self):
        return self.__drives

    @drives.setter
    @abstractmethod
    def drives(self, drives):
        self.__drives = drives
