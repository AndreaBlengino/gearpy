from gearpy.mechanical_object import MotorBase, RotatingObject
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.transmission import Transmission
from gearpy.units import AngularPosition, Angle
from pytest import fixture
from tests.conftest import types_to_check, basic_transmission, basic_encoder, basic_spur_gear_1, basic_dc_motor_1


class TransmissionFake(Transmission):

    def __init__(self, chain: list):
        self.__chain = chain

    @property
    def chain(self):
        return self.__chain

    @chain.setter
    def chain(self, chain):
        self.__chain = chain

reach_angular_position_init_type_error_1 = [{'encoder': type_to_check, 'transmission': basic_transmission,
                                             'target_angular_position': AngularPosition(1, 'rad'),
                                             'braking_angle': Angle(1, 'rad')} for type_to_check in types_to_check
                                            if not isinstance(type_to_check, AbsoluteRotaryEncoder)]

reach_angular_position_init_type_error_2 = [{'encoder': basic_encoder, 'transmission': type_to_check,
                                             'target_angular_position': AngularPosition(1, 'rad'),
                                             'braking_angle': Angle(1, 'rad')} for type_to_check in types_to_check
                                            if not isinstance(type_to_check, Transmission)]

reach_angular_position_init_type_error_3 = [{'encoder': basic_encoder,
                                             'transmission': TransmissionFake([type_to_check, basic_spur_gear_1]),
                                             'target_angular_position': AngularPosition(1, 'rad'),
                                             'braking_angle': Angle(1, 'rad')} for type_to_check in types_to_check
                                            if not isinstance(type_to_check, MotorBase)]

reach_angular_position_init_type_error_4 = [{'encoder': basic_encoder,
                                             'transmission': TransmissionFake([basic_dc_motor_1, type_to_check]),
                                             'target_angular_position': AngularPosition(1, 'rad'),
                                             'braking_angle': Angle(1, 'rad')} for type_to_check in types_to_check
                                            if not isinstance(type_to_check, RotatingObject)]

reach_angular_position_init_type_error_5 = [{'encoder': basic_encoder, 'transmission': basic_transmission,
                                             'target_angular_position': type_to_check, 'braking_angle': Angle(1, 'rad')}
                                            for type_to_check in types_to_check
                                            if not isinstance(type_to_check, AngularPosition)]

reach_angular_position_init_type_error_6 = [{'encoder': basic_encoder, 'transmission': basic_transmission,
                                             'target_angular_position': AngularPosition(1, 'rad'),
                                             'braking_angle': type_to_check} for type_to_check in types_to_check
                                            if not isinstance(type_to_check, Angle)]

@fixture(params = [*reach_angular_position_init_type_error_1,
                   *reach_angular_position_init_type_error_2,
                   *reach_angular_position_init_type_error_3,
                   *reach_angular_position_init_type_error_4,
                   *reach_angular_position_init_type_error_5,
                   *reach_angular_position_init_type_error_6])
def reach_angular_position_init_type_error(request):
    return request.param
