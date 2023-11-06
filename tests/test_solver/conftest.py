from gearpy.mechanical_object import RotatingObject, MotorBase, SpurGear, DCMotor
from gearpy.transmission import Transmission
from gearpy.units import AngularSpeed, InertiaMoment, Length, Torque, TimeInterval
from gearpy.utils import add_fixed_joint
from pytest import fixture
from tests.conftest import types_to_check, basic_spur_gear, basic_dc_motor


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

solver_init_type_error_1 = [{'time_discretization': type_to_check, 'simulation_time': TimeInterval(5, 'sec'),
                             'transmission': transmission_solver_init_type_error} for type_to_check in types_to_check
                            if not isinstance(type_to_check, TimeInterval)]

solver_init_type_error_2 = [{'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': type_to_check,
                             'transmission': transmission_solver_init_type_error} for type_to_check in types_to_check
                            if not isinstance(type_to_check, TimeInterval)]

solver_init_type_error_3 = [{'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': TimeInterval(5, 'sec'),
                             'transmission': type_to_check} for type_to_check in types_to_check
                            if not isinstance(type_to_check, Transmission)]

solver_init_type_error_4 = [{'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': TimeInterval(5, 'sec'),
                             'transmission': TransmissionFake([type_to_check, basic_spur_gear])}
                            for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)]

solver_init_type_error_5 = [{'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': TimeInterval(5, 'sec'),
                             'transmission': TransmissionFake([basic_dc_motor, type_to_check])}
                            for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)]

@fixture(params = [*solver_init_type_error_1,
                   *solver_init_type_error_2,
                   *solver_init_type_error_3,
                   *solver_init_type_error_4,
                   *solver_init_type_error_5])
def solver_init_type_error(request):
    return request.param

motor_transmission_solver_init_value_error = DCMotor(name = 'name', inertia_moment = InertiaMoment(1, 'kgm^2'),
                                                     no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
gear_transmission_solver_init_value_error = SpurGear(name = 'gear', n_teeth = 10, module = Length(1, 'mm'), inertia_moment = InertiaMoment(1, 'kgm^2'))
add_fixed_joint(master = motor_transmission_solver_init_value_error, slave = gear_transmission_solver_init_value_error)
transmission_solver_init_value_error = Transmission(motor = motor_transmission_solver_init_value_error)

@fixture(params = [{'time_discretization': TimeInterval(5, 'sec'), 'simulation_time': TimeInterval(1, 'sec'), 'transmission': transmission_solver_init_value_error},
                   {'time_discretization': TimeInterval(1, 'sec'), 'simulation_time': TimeInterval(5, 'sec'), 'transmission': TransmissionFake([])}])
def solver_init_value_error(request):
    return request.param
