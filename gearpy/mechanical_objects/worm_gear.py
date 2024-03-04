from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, Angle, Force, InertiaMoment, Length, \
                         Time, Torque, UnitBase
from .mating_roles import MatingMaster, MatingSlave
from .mechanical_object_base import RotatingObject, Role, WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES, \
                                    worm_gear_and_wheel_maximum_helix_angle_function
from typing import Callable, Dict, List, Union, Optional


class WormGear(RotatingObject):

    def __init__(self,
                 name: str,
                 n_starts: int,
                 inertia_moment: InertiaMoment,
                 helix_angle: Angle,
                 pressure_angle: Angle,
                 reference_diameter: Optional[Length] = None):
        super().__init__(name = name,
                         inertia_moment = inertia_moment)

        if not isinstance(n_starts, int):
            raise TypeError(f"Parameter 'n_starts' must be an integer.")

        if n_starts < 1:
            raise ValueError(f"Parameter 'n_starts' must be equal to or greater than one.")

        if not isinstance(helix_angle, Angle):
            raise TypeError(f"Parameter 'helix_angle' must be an instance of {Angle.__name__!r}.")

        if not isinstance(pressure_angle, Angle):
            raise TypeError(f"Parameter 'pressure_angle' must be an instance of {Angle.__name__!r}.")

        if pressure_angle not in WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES:
            raise ValueError(f"Value {pressure_angle!r} for parameter 'pressure_angle' not available. "
                             f"Available pressure angles are: {WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES}")

        maximum_helix_angle = worm_gear_and_wheel_maximum_helix_angle_function(pressure_angle = pressure_angle)
        if helix_angle > maximum_helix_angle:
            raise ValueError(f"Parameter 'helix_angle' too high. For a {pressure_angle} 'pressure_angle', "
                             f"the maximum 'helix_angle' is {maximum_helix_angle}.")

        if reference_diameter is not None:
            if not isinstance(reference_diameter, Length):
                raise TypeError(f"Parameter 'reference_diameter' must be an instance of {Length.__name__!r}.")

        self.__n_starts = n_starts
        self.__helix_angle = helix_angle
        self.__pressure_angle = pressure_angle
        self.__reference_diameter = reference_diameter
        self.__self_locking = None
        self.__driven_by = None
        self.__drives = None
        self.__master_gear_ratio = None
        self.__master_gear_efficiency = 1
        self.__mating_role = None
        self.__external_torque = None

        if self.tangential_force_is_computable:
            self.__tangential_force = None
            self.time_variables['tangential force'] = []

    @property
    def name(self) -> str:
        return super().name

    @property
    def n_starts(self) -> int:
        return self.__n_starts

    @property
    def inertia_moment(self) -> InertiaMoment:
        return super().inertia_moment

    @property
    def helix_angle(self) -> Angle:
        return self.__helix_angle

    @property
    def pressure_angle(self) -> Angle:
        return self.__pressure_angle

    @property
    def reference_diameter(self) -> Optional[Length]:
        return self.__reference_diameter

    @property
    def self_locking(self) -> bool:
        return self.__self_locking

    @self_locking.setter
    def self_locking(self, self_locking: bool):
        if not isinstance(self_locking, bool):
            raise TypeError(f"Parameter 'self_locking' must be a boolean.")

        self.__self_locking = self_locking

    @property
    def driven_by(self) -> RotatingObject:
        return self.__driven_by

    @driven_by.setter
    def driven_by(self, driven_by: RotatingObject):
        if not isinstance(driven_by, RotatingObject):
            raise TypeError(f"Parameter 'driven_by' must be an instance of {RotatingObject.__name__!r}.")

        self.__driven_by = driven_by

    @property
    def drives(self) -> RotatingObject:
        return self.__drives

    @drives.setter
    def drives(self, drives: RotatingObject):
        if not isinstance(drives, RotatingObject):
            raise TypeError(f"Parameter 'drives' must be an instance of {RotatingObject.__name__!r}.")

        self.__drives = drives

    @property
    def master_gear_ratio(self) -> float:
        return self.__master_gear_ratio

    @master_gear_ratio.setter
    def master_gear_ratio(self, master_gear_ratio: float):
        if not isinstance(master_gear_ratio, float):
            raise TypeError("Parameter 'master_gear_ratio' must be a float.")

        if master_gear_ratio <= 0:
            raise ValueError("Parameter 'master_gear_ratio' must be positive.")

        self.__master_gear_ratio = master_gear_ratio

    @property
    def master_gear_efficiency(self) -> Union[float, int]:
        return self.__master_gear_efficiency

    @master_gear_efficiency.setter
    def master_gear_efficiency(self, master_gear_efficiency: Union[float, int]):
        if not isinstance(master_gear_efficiency, float) and not isinstance(master_gear_efficiency, int):
            raise TypeError("Parameter 'master_gear_efficiency' must be a float or an integer.")

        if master_gear_efficiency > 1 or master_gear_efficiency < 0:
            raise ValueError("Parameter 'master_gear_efficiency' must be within 0 and 1.")

        self.__master_gear_efficiency = master_gear_efficiency

    @property
    def mating_role(self) -> Role:
        return self.__mating_role

    @mating_role.setter
    def mating_role(self, mating_role: Role):
        if hasattr(mating_role, '__name__'):
            if not issubclass(mating_role, Role):
                raise TypeError(f"Parameter 'mating_role' must be a subclass of {Role.__name__!r}.")
        else:
            raise TypeError(f"Parameter 'mating_role' must be a subclass of {Role.__name__!r}.")

        self.__mating_role = mating_role

    @property
    def angular_position(self) -> AngularPosition:
        return super().angular_position

    @angular_position.setter
    def angular_position(self, angular_position: AngularPosition):
        super(WormGear, type(self)).angular_position.fset(self, angular_position)

    @property
    def angular_speed(self) -> AngularSpeed:
        return super().angular_speed

    @angular_speed.setter
    def angular_speed(self, angular_speed: AngularSpeed):
        super(WormGear, type(self)).angular_speed.fset(self, angular_speed)

    @property
    def angular_acceleration(self) -> AngularAcceleration:
        return super().angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        super(WormGear, type(self)).angular_acceleration.fset(self, angular_acceleration)

    @property
    def torque(self) -> Torque:
        return super().torque

    @torque.setter
    def torque(self, torque: Torque):
        super(WormGear, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Torque:
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Torque):
        super(WormGear, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Torque:
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Torque):
        super(WormGear, type(self)).load_torque.fset(self, load_torque)

    @property
    def tangential_force(self) -> Force:
        return self.__tangential_force

    @tangential_force.setter
    def tangential_force(self, tangential_force: Force):
        if not isinstance(tangential_force, Force):
            raise TypeError(f"Parameter 'tangential_force' must be an instance of {Force.__name__!r}.")

        self.__tangential_force = tangential_force

    def compute_tangential_force(self):
        if self.mating_role == MatingMaster:
            self.tangential_force = abs(self.load_torque)/(self.reference_diameter/2)*self.helix_angle.tan()
        elif self.mating_role == MatingSlave:
            self.tangential_force = abs(self.driving_torque)/(self.reference_diameter/2)*self.helix_angle.tan()
        else:
            raise ValueError("Gear mating not defined. "
                             "Use 'gearpy.utils.add_worm_gear_mating' to set up a mating between two gears.")

    @property
    def tangential_force_is_computable(self) -> bool:
        return self.__reference_diameter is not None

    @property
    def external_torque(self) -> Callable[[AngularPosition, AngularSpeed, Time], Torque]:
        return self.__external_torque

    @external_torque.setter
    def external_torque(self, external_torque: Callable[[AngularPosition, AngularSpeed, Time], Torque]):
        self.__external_torque = external_torque

    @property
    def time_variables(self) -> Dict[str, List[UnitBase]]:
        return super().time_variables

    def update_time_variables(self) -> None:
        super().update_time_variables()
        if self.tangential_force_is_computable:
            self.time_variables['tangential force'].append(self.tangential_force)
