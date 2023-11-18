from abc import ABC, abstractmethod
from . import gear_data
from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, Force, InertiaMoment, Length, Stress, \
    Time, Torque, UnitBase
from importlib import resources as imp_resources
import pandas as pd
from scipy.interpolate import interp1d
from typing import Callable, Dict, List, Union


LEWIS_FACTOR_DATA_FILE = (imp_resources.files(gear_data) / 'lewis_factor_table.csv')
LEWIS_FACTOR_DATA = pd.read_csv(LEWIS_FACTOR_DATA_FILE)
MINIMUM_TEETH_NUMBER = LEWIS_FACTOR_DATA.loc[LEWIS_FACTOR_DATA.index[0], 'number of teeth']
lewis_factor_function = interp1d(x = LEWIS_FACTOR_DATA['number of teeth'],
                                 y = LEWIS_FACTOR_DATA['Lewis factor'],
                                 fill_value = (LEWIS_FACTOR_DATA.loc[LEWIS_FACTOR_DATA.index[0], 'Lewis factor'],
                                               LEWIS_FACTOR_DATA.loc[LEWIS_FACTOR_DATA.index[-1], 'Lewis factor']),
                                 bounds_error = False)


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
    def __init__(self,
                 name: str,
                 n_teeth: int,
                 module: Length,
                 face_width: Length,
                 inertia_moment: InertiaMoment,
                 elastic_modulus: Stress):
        super().__init__(name = name, inertia_moment = inertia_moment)

        if not isinstance(n_teeth, int):
            raise TypeError("Parameter 'n_teeth' must be an integer.")

        if n_teeth < MINIMUM_TEETH_NUMBER:
            raise ValueError(f"Parameter 'n_teeth' must be greater or equal to {MINIMUM_TEETH_NUMBER}.")

        if module is not None:
            if not isinstance(module, Length):
                raise TypeError(f"Parameter 'module' must be an instance of {Length.__name__!r}.")

        if face_width is not None:
            if not isinstance(face_width, Length):
                raise TypeError(f"Parameter 'face_width' must be an instance of {Length.__name__!r}.")

        if elastic_modulus is not None:
            if not isinstance(elastic_modulus, Stress):
                raise TypeError(f"Parameter 'elastic_modulus' must be an instance of {Stress.__name__!r}.")

            if elastic_modulus.value <= 0:
                raise ValueError(f"Parameter 'elastic_modulus' must be positive.")

        self.__n_teeth = n_teeth
        self.__driven_by = None
        self.__drives = None
        self.__master_gear_ratio = None
        self.__master_gear_efficiency = 1
        self.__mating_role = None
        self.__external_torque = None
        self.__module = module
        self.__face_width = face_width
        self.__elastic_modulus = elastic_modulus

        if self.tangential_force_is_computable:
            self.__reference_diameter = n_teeth*module
            self.__tangential_force = None

            if self.bending_stress_is_computable:
                self.__bending_stress = None

                if self.contact_stress_is_computable:
                    self.__contact_stress = None

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
    def face_width(self) -> Length:
        return self.__face_width

    @property
    @abstractmethod
    def elastic_modulus(self) -> Stress:
        return self.__elastic_modulus

    @property
    @abstractmethod
    def lewis_factor(self): ...

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
    def tangential_force_is_computable(self) -> bool:
        return self.__module is not None

    @property
    @abstractmethod
    def bending_stress(self) -> Stress:
        return self.__bending_stress

    @bending_stress.setter
    @abstractmethod
    def bending_stress(self, bending_stress: Stress):
        if not isinstance(bending_stress, Stress):
            raise TypeError(f"Parameter 'bending_stress' must be an instance of {Stress.__name__!r}.")

        self.__bending_stress = bending_stress

    @abstractmethod
    def compute_bending_stress(self): ...

    @property
    @abstractmethod
    def bending_stress_is_computable(self) -> bool:
        return (self.__module is not None) and (self.__face_width is not None)

    @property
    @abstractmethod
    def contact_stress(self) -> Stress:
        return self.__contact_stress

    @contact_stress.setter
    @abstractmethod
    def contact_stress(self, contact_stress: Stress):
        if not isinstance(contact_stress, Stress):
            raise TypeError(f"Parameter 'contact_stress' must be an instance of {Stress.__name__!r}.")

        self.__contact_stress = contact_stress

    @abstractmethod
    def compute_contact_stress(self): ...

    @property
    @abstractmethod
    def contact_stress_is_computable(self) -> bool:
        return (self.__module is not None) and (self.__face_width is not None) and (self.__elastic_modulus is not None)

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
    def mating_role(self) -> 'Role':
        return self.__mating_role

    @mating_role.setter
    @abstractmethod
    def mating_role(self, mating_role):
        if hasattr(mating_role, '__name__'):
            if not issubclass(mating_role, Role):
                raise TypeError(f"Parameter 'mating_role' must be a subclass of {Role.__name__!r}.")
        else:
            raise TypeError(f"Parameter 'mating_role' must be a subclass of {Role.__name__!r}.")

        self.__mating_role = mating_role

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


class Role(ABC): ...
