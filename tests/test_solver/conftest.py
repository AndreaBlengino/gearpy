from gearpy.mechanical_object import RotatingObject, MotorBase, SpurGear, DCMotor
from gearpy.motor_control import MotorControlBase
from gearpy.transmission import Transmission
from gearpy.units import AngularSpeed, InertiaMoment, Length, Torque, TimeInterval
from gearpy.utils import add_fixed_joint
from pytest import fixture
from tests.conftest import types_to_check, basic_spur_gear_1, basic_dc_motor_1, basic_transmission


motor_transmission_solver_init_type_error = DCMotor(name = 'name', inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                    no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
gear_transmission_solver_init_type_error = SpurGear(name = 'gear', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
add_fixed_joint(master = motor_transmission_solver_init_type_error, slave = gear_transmission_solver_init_type_error)
transmission_solver_init_type_error = Transmission(motor = motor_transmission_solver_init_type_error)

class TransmissionFake(Transmission):

    def __init__(self, chain: list):
        self.__chain = chain

    @property
    def chain(self):
        return self.__chain

    @chain.setter
    def chain(self, chain):
        self.__chain = chain

solver_init_type_error_1 = [{'transmission': type_to_check} for type_to_check in types_to_check
                            if not isinstance(type_to_check, Transmission)]

solver_init_type_error_2 = [{'transmission': TransmissionFake([type_to_check, basic_spur_gear_1])}
                            for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)]

solver_init_type_error_3 = [{'transmission': TransmissionFake([basic_dc_motor_1, type_to_check])}
                            for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)]

solver_init_type_error_4 = [{'transmission': basic_transmission, 'motor_control': type_to_check}
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
