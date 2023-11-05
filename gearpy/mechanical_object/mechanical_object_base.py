from abc import ABC, abstractmethod
from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, Force, InertiaMoment, Length, Time, \
    Torque, UnitBase
from typing import Callable, Dict, List, Union


class MechanicalObject(ABC):

    @abstractmethod
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Parameter 'name' must be a string.")

        if name == '':
            raise ValueError("Parameter 'name' cannot be an empty string")

        self.__name = name

    @property
    @abstractmethod
    def name(self) -> str:
        return self.__name


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
    def time_variables(self) -> Dict[str, List[UnitBase]]:
        return self.__time_variables

    @abstractmethod
    def update_time_variables(self):
        self.__time_variables['angular position'].append(self.__angular_position)
        self.__time_variables['angular speed'].append(self.__angular_speed)
        self.__time_variables['angular acceleration'].append(self.__angular_acceleration)
        self.__time_variables['torque'].append(self.__torque)
        self.__time_variables['driving torque'].append(self.__driving_torque)
        self.__time_variables['load torque'].append(self.__load_torque)


class MotorBase(RotatingObject):

    @abstractmethod
    def __init__(self, name: str, inertia_moment: InertiaMoment):
        super().__init__(name = name, inertia_moment = inertia_moment)
        self.__drives = None

    @property
    @abstractmethod
    def drives(self) -> RotatingObject:
        return self.__drives

    @drives.setter
    @abstractmethod
    def drives(self, drives: RotatingObject):
        if not isinstance(drives, RotatingObject):
            raise TypeError(f"Parameter 'drives' must be a {RotatingObject.__name__!r}")

        self.__drives = drives

    @property
    @abstractmethod
    def angular_position(self) -> AngularPosition:
        return super().angular_position

    @angular_position.setter
    @abstractmethod
    def angular_position(self, angular_position: AngularPosition):
        super(MotorBase, type(self)).angular_position.fset(self, angular_position)

    @property
    @abstractmethod
    def angular_speed(self) -> AngularSpeed:
        return super().angular_speed

    @angular_speed.setter
    @abstractmethod
    def angular_speed(self, angular_speed: AngularSpeed):
        super(MotorBase, type(self)).angular_speed.fset(self, angular_speed)

    @property
    @abstractmethod
    def angular_acceleration(self) -> AngularAcceleration:
        return super().angular_acceleration

    @angular_acceleration.setter
    @abstractmethod
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        super(MotorBase, type(self)).angular_acceleration.fset(self, angular_acceleration)

    @property
    @abstractmethod
    def torque(self) -> Torque:
        return super().torque

    @torque.setter
    @abstractmethod
    def torque(self, torque: Torque):
        super(MotorBase, type(self)).torque.fset(self, torque)

    @property
    @abstractmethod
    def driving_torque(self) -> Torque:
        return super().driving_torque

    @driving_torque.setter
    @abstractmethod
    def driving_torque(self, driving_torque: Torque):
        super(MotorBase, type(self)).driving_torque.fset(self, driving_torque)

    @property
    @abstractmethod
    def load_torque(self) -> Torque:
        return super().load_torque

    @load_torque.setter
    @abstractmethod
    def load_torque(self, load_torque: Torque):
        super(MotorBase, type(self)).load_torque.fset(self, load_torque)

    @abstractmethod
    def compute_torque(self) -> Torque: ...


class GearBase(RotatingObject):

    @abstractmethod
    def __init__(self, name: str, n_teeth: int, module: Length, inertia_moment: InertiaMoment):
        super().__init__(name = name, inertia_moment = inertia_moment)

        if not isinstance(n_teeth, int):
            raise TypeError("Parameter 'n_teeth' must be an integer.")

        if n_teeth <= 0:
            raise ValueError("Parameter 'n_teeth' must be positive.")

        if not isinstance(module, Length):
            raise TypeError(f"Parameter 'module' must be an instance of {Length.__name__!r}.")

        self.__n_teeth = n_teeth
        self.__module = module
        self.__reference_diameter = n_teeth*module
        self.__tangential_force = None
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
    def module(self) -> Length:
        return self.__module

    @property
    @abstractmethod
    def reference_diameter(self) -> Length:
        return self.__reference_diameter

    @property
    @abstractmethod
    def driven_by(self) -> RotatingObject:
        return self.__driven_by

    @driven_by.setter
    @abstractmethod
    def driven_by(self, driven_by: RotatingObject):
        if not isinstance(driven_by, RotatingObject):
            raise TypeError(f"Parameter 'driven_by' must be a {RotatingObject.__name__!r}")

        self.__driven_by = driven_by

    @property
    @abstractmethod
    def drives(self) -> RotatingObject:
        return self.__drives

    @drives.setter
    @abstractmethod
    def drives(self, drives: RotatingObject):
        if not isinstance(drives, RotatingObject):
            raise TypeError(f"Parameter 'drives' must be a {RotatingObject.__name__!r}")

        self.__drives = drives

    @property
    @abstractmethod
    def angular_position(self) -> AngularPosition:
        return super().angular_position

    @angular_position.setter
    @abstractmethod
    def angular_position(self, angular_position: AngularPosition):
        super(GearBase, type(self)).angular_position.fset(self, angular_position)

    @property
    @abstractmethod
    def angular_speed(self) -> AngularSpeed:
        return super().angular_speed

    @angular_speed.setter
    @abstractmethod
    def angular_speed(self, angular_speed: AngularSpeed):
        super(GearBase, type(self)).angular_speed.fset(self, angular_speed)

    @property
    @abstractmethod
    def angular_acceleration(self) -> AngularAcceleration:
        return super().angular_acceleration

    @angular_acceleration.setter
    @abstractmethod
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        super(GearBase, type(self)).angular_acceleration.fset(self, angular_acceleration)

    @property
    @abstractmethod
    def torque(self) -> Torque:
        return super().torque

    @torque.setter
    @abstractmethod
    def torque(self, torque: Torque):
        super(GearBase, type(self)).torque.fset(self, torque)

    @property
    @abstractmethod
    def driving_torque(self) -> Torque:
        return super().driving_torque

    @driving_torque.setter
    @abstractmethod
    def driving_torque(self, driving_torque: Torque):
        super(GearBase, type(self)).driving_torque.fset(self, driving_torque)

    @property
    @abstractmethod
    def load_torque(self) -> Torque:
        return super().load_torque

    @load_torque.setter
    @abstractmethod
    def load_torque(self, load_torque: Torque):
        super(GearBase, type(self)).load_torque.fset(self, load_torque)

    @property
    @abstractmethod
    def tangential_force(self) -> Force:
        return self.__tangential_force

    @tangential_force.setter
    @abstractmethod
    def tangential_force(self, tangential_force: Force):
        if not isinstance(tangential_force, Force):
            raise TypeError(f"Parameter 'tangential_force' must be an instance of {Force.__name__!r}.")

        self.__tangential_force = tangential_force

    @abstractmethod
    def compute_tangential_force(self): ...

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
    def external_torque(self) -> Callable[[AngularPosition, AngularSpeed, Time], Torque]:
        return self.__external_torque

    @external_torque.setter
    @abstractmethod
    def external_torque(self, external_torque: Callable[[AngularPosition, AngularSpeed, Time], Torque]):
        if not isinstance(external_torque, Callable):
            raise TypeError("Parameter 'external_torque' must be callable.")

        self.__external_torque = external_torque
