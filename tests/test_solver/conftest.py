from gearpy.mechanical_objects import RotatingObject, MotorBase, SpurGear, DCMotor
from gearpy.motor_control import MotorControlBase
from gearpy.powertrain import Powertrain
from gearpy.units import AngularSpeed, InertiaMoment, Length, Torque, TimeInterval
from gearpy.utils import add_fixed_joint
from pytest import fixture
from tests.conftest import types_to_check, basic_spur_gear_1, basic_dc_motor_1, basic_powertrain


motor_powertrain_solver_init_type_error = DCMotor(name = 'name', inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                    no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
gear_powertrain_solver_init_type_error = SpurGear(name = 'gear', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
add_fixed_joint(master = motor_powertrain_solver_init_type_error, slave = gear_powertrain_solver_init_type_error)
powertrain_solver_init_type_error = Powertrain(motor = motor_powertrain_solver_init_type_error)

class PowertrainFake(Powertrain):

    def __init__(self, elements: list):
        self.__elements = elements

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, elements):
        self.__elements = elements

solver_init_type_error_1 = [{'powertrain': type_to_check} for type_to_check in types_to_check
                            if not isinstance(type_to_check, Powertrain)]

solver_init_type_error_2 = [{'powertrain': PowertrainFake([type_to_check, basic_spur_gear_1])}
                            for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)]

solver_init_type_error_3 = [{'powertrain': PowertrainFake([basic_dc_motor_1, type_to_check])}
                            for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)]

solver_init_type_error_4 = [{'powertrain': basic_powertrain, 'motor_control': type_to_check}
                            for type_to_check in types_to_check if not isinstance(type_to_check, MotorControlBase)
                            and type_to_check is not None]

@fixture(params = [*solver_init_type_error_1,
                   *solver_init_type_error_2,
                   *solver_init_type_error_3,
                   *solver_init_type_error_4])
def solver_init_type_error(request):
    return request.param


solver_run_type_error_1 = [{'time_discretization': type_to_check, 'simulation_time': TimeInterval(1, 'sec')}
                           for type_to_check in types_to_check if not isinstance(type_to_check, TimeInterval)]

solver_run_type_error_2 = [{'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': type_to_check}
                           for type_to_check in types_to_check if not isinstance(type_to_check, TimeInterval)]

solver_run_type_error_3 = [{}]

@fixture(params = [*solver_run_type_error_1,
                   *solver_run_type_error_2,
                   *solver_run_type_error_3])
def solver_run_type_error(request):
    return request.param


@fixture(params = [{'time_discretization': TimeInterval(5, 'sec'), 'simulation_time': TimeInterval(1, 'sec')},
                   {}])
def solver_run_value_error(request):
    return request.param
