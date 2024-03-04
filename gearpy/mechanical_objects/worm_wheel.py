from gearpy.units import AngularPosition, AngularSpeed, AngularAcceleration, Angle, Force, InertiaMoment, Length, \
                         Stress, Time, Torque, UnitBase
from math import pi
from .mechanical_object_base import RotatingObject, Role, WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES, \
                                    worm_gear_and_wheel_maximum_helix_angle_function, worm_wheel_lewis_factor_function
from .mating_roles import MatingMaster, MatingSlave
from .helical_gear import HelicalGear
from typing import Callable, Dict, List, Union, Optional


class WormWheel(HelicalGear):

    def __init__(self,
                 name: str,
                 n_teeth: int,
                 inertia_moment: InertiaMoment,
                 helix_angle: Angle,
                 pressure_angle: Angle,
                 module: Optional[Length] = None,
                 face_width: Optional[Length] = None):
        super().__init__(name = name,
                         n_teeth = n_teeth,
                         module = module,
                         face_width = face_width,
                         inertia_moment = inertia_moment,
                         helix_angle = helix_angle,
                         elastic_modulus = None)

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

        self.__helix_angle = helix_angle
        self.__pressure_angle = pressure_angle

        if self.tangential_force_is_computable:
            self.time_variables['tangential force'] = []

            if self.bending_stress_is_computable:
                self.time_variables['bending stress'] = []
                self.__lewis_factor = worm_wheel_lewis_factor_function(pressure_angle = pressure_angle)

    @property
    def name(self) -> str:
        return super().name

    @property
    def n_teeth(self) -> int:
        return super().n_teeth

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
    def module(self) -> Optional[Length]:
        return super().module

    @property
    def reference_diameter(self) -> Optional[Length]:
        return super().reference_diameter

    @property
    def face_width(self) -> Optional[Length]:
        return super().face_width

    @property
    def lewis_factor(self) -> Optional[float]:
        return self.__lewis_factor

    @property
    def driven_by(self) -> RotatingObject:
        return super().driven_by

    @driven_by.setter
    def driven_by(self, driven_by: RotatingObject):
        super(WormWheel, type(self)).driven_by.fset(self, driven_by)

    @property
    def drives(self) -> RotatingObject:
        return super().drives

    @drives.setter
    def drives(self, drives: RotatingObject):
        super(WormWheel, type(self)).drives.fset(self, drives)

    @property
    def master_gear_ratio(self) -> float:
        return super().master_gear_ratio

    @master_gear_ratio.setter
    def master_gear_ratio(self, master_gear_ratio: float):
        super(WormWheel, type(self)).master_gear_ratio.fset(self, master_gear_ratio)

    @property
    def master_gear_efficiency(self) -> Union[float, int]:
        return super().master_gear_efficiency

    @master_gear_efficiency.setter
    def master_gear_efficiency(self, master_gear_efficiency: Union[float, int]):
        super(WormWheel, type(self)).master_gear_efficiency.fset(self, master_gear_efficiency)

    @property
    def mating_role(self) -> Role:
        return super().mating_role

    @mating_role.setter
    def mating_role(self, mating_role: Role):
        super(WormWheel, type(self)).mating_role.fset(self, mating_role)

    @property
    def angular_position(self) -> AngularPosition:
        return super().angular_position

    @angular_position.setter
    def angular_position(self, angular_position: AngularPosition):
        super(WormWheel, type(self)).angular_position.fset(self, angular_position)

    @property
    def angular_speed(self) -> AngularSpeed:
        return super().angular_speed

    @angular_speed.setter
    def angular_speed(self, angular_speed: AngularSpeed):
        super(WormWheel, type(self)).angular_speed.fset(self, angular_speed)

    @property
    def angular_acceleration(self) -> AngularAcceleration:
        return super().angular_acceleration

    @angular_acceleration.setter
    def angular_acceleration(self, angular_acceleration: AngularAcceleration):
        super(WormWheel, type(self)).angular_acceleration.fset(self, angular_acceleration)

    @property
    def torque(self) -> Torque:
        return super().torque

    @torque.setter
    def torque(self, torque: Torque):
        super(WormWheel, type(self)).torque.fset(self, torque)

    @property
    def driving_torque(self) -> Torque:
        return super().driving_torque

    @driving_torque.setter
    def driving_torque(self, driving_torque: Torque):
        super(WormWheel, type(self)).driving_torque.fset(self, driving_torque)

    @property
    def load_torque(self) -> Torque:
        return super().load_torque

    @load_torque.setter
    def load_torque(self, load_torque: Torque):
        super(WormWheel, type(self)).load_torque.fset(self, load_torque)

    @property
    def tangential_force(self) -> Force:
        return super().tangential_force

    @tangential_force.setter
    def tangential_force(self, tangential_force: Force):
        super(WormWheel, type(self)).tangential_force.fset(self, tangential_force)

    def compute_tangential_force(self):
        if self.mating_role == MatingMaster:
            self.tangential_force = abs(self.load_torque)/(self.reference_diameter/2)
        elif self.mating_role == MatingSlave:
            self.tangential_force = abs(self.driving_torque)/(self.reference_diameter/2)
        else:
            raise ValueError("Gear mating not defined.")

    @property
    def tangential_force_is_computable(self) -> bool:
        return super().tangential_force_is_computable

    @property
    def bending_stress(self) -> Stress:
        return super().bending_stress

    @bending_stress.setter
    def bending_stress(self, bending_stress: Stress):
        super(WormWheel, type(self)).bending_stress.fset(self, bending_stress)

    def compute_bending_stress(self):
        if self.mating_role == MatingMaster:
            normal_pitch = pi*self.drives.reference_diameter*self.drives.helix_angle.sin()/self.n_teeth
            effective_face_width = min(self.face_width, 0.67*self.drives.reference_diameter)
        elif self.mating_role == MatingSlave:
            normal_pitch = pi*self.driven_by.reference_diameter*self.driven_by.helix_angle.sin()/self.n_teeth
            effective_face_width = min(self.face_width, 0.67*self.driven_by.reference_diameter)
        else:
            raise ValueError("Gear mating not defined.")
        self.bending_stress = self.tangential_force/(normal_pitch*effective_face_width)/self.lewis_factor

    @property
    def bending_stress_is_computable(self) -> bool:
        if self.mating_role == MatingMaster:
            return super().bending_stress_is_computable and (self.drives.reference_diameter is not None)
        if self.mating_role == MatingSlave:
            return super().bending_stress_is_computable and (self.driven_by.reference_diameter is not None)
        else:
            return super().bending_stress_is_computable

    @property
    def external_torque(self) -> Callable[[AngularPosition, AngularSpeed, Time], Torque]:
        return super().external_torque

    @external_torque.setter
    def external_torque(self, external_torque: Callable[[AngularPosition, AngularSpeed, Time], Torque]):
        super(WormWheel, type(self)).external_torque.fset(self, external_torque)

    @property
    def time_variables(self) -> Dict[str, List[UnitBase]]:
        return super().time_variables

    def update_time_variables(self) -> None:
        super().update_time_variables()
