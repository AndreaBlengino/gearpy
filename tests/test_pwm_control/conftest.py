from gearpy.mechanical_object import MotorBase, RotatingObject
from gearpy.motor_control import RuleBase
from gearpy.transmission import Transmission
from pytest import fixture
from tests.conftest import types_to_check, basic_spur_gear_1, basic_dc_motor_1


class TransmissionFake(Transmission):

    def __init__(self, chain: list):
        self.__chain = chain

    @property
    def chain(self):
        return self.__chain

    @chain.setter
    def chain(self, chain):
        self.__chain = chain

pwm_control_init_type_error_1 = [{'transmission': type_to_check} for type_to_check in types_to_check
                                 if not isinstance(type_to_check, Transmission)]

pwm_control_init_type_error_2 = [{'transmission': TransmissionFake([type_to_check, basic_spur_gear_1])}
                                 for type_to_check in types_to_check if not isinstance(type_to_check, MotorBase)]

pwm_control_init_type_error_3 = [{'transmission': TransmissionFake([basic_dc_motor_1, type_to_check])}
                                 for type_to_check in types_to_check if not isinstance(type_to_check, RotatingObject)]

@fixture(params = [*pwm_control_init_type_error_1,
                   *pwm_control_init_type_error_2,
                   *pwm_control_init_type_error_3])
def pwm_control_init_type_error(request):
    return request.param


@fixture(params = [type_to_check for type_to_check in types_to_check if not isinstance(type_to_check, RuleBase)])
def pwm_control_add_rule_type_error(request):
    return request.param
