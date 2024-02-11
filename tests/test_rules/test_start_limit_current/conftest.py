from gearpy.mechanical_objects import DCMotor
from gearpy.sensors import AbsoluteRotaryEncoder, Tachometer
from gearpy.units import AngularPosition, Current
from pytest import fixture
from tests.conftest import types_to_check, basic_encoder, basic_tachometer, basic_dc_motor_1, basic_dc_motor_2


start_limit_current_init_type_error_1 = [{'encoder': type_to_check, 'tachometer': basic_tachometer,
                                          'motor': basic_dc_motor_2, 'target_angular_position': AngularPosition(1, 'rad'),
                                          'limit_electric_current': Current(1, 'A')} for type_to_check in types_to_check
                                         if not isinstance(type_to_check, AbsoluteRotaryEncoder)]

start_limit_current_init_type_error_2 = [{'encoder': basic_encoder, 'tachometer': type_to_check,
                                          'motor': basic_dc_motor_2, 'target_angular_position': AngularPosition(1, 'rad'),
                                          'limit_electric_current': Current(1, 'A')} for type_to_check in types_to_check
                                         if not isinstance(type_to_check, Tachometer)]

start_limit_current_init_type_error_3 = [{'encoder': basic_encoder, 'tachometer': basic_tachometer,
                                          'motor': type_to_check, 'target_angular_position': AngularPosition(1, 'rad'),
                                          'limit_electric_current': Current(1, 'A')} for type_to_check in types_to_check
                                         if not isinstance(type_to_check, DCMotor)]

start_limit_current_init_type_error_4 = [{'encoder': basic_encoder, 'tachometer': basic_tachometer,
                                          'motor': basic_dc_motor_2, 'target_angular_position': type_to_check,
                                          'limit_electric_current': Current(1, 'A')} for type_to_check in types_to_check
                                         if not isinstance(type_to_check, AngularPosition)]

start_limit_current_init_type_error_5 = [{'encoder': basic_encoder, 'tachometer': basic_tachometer,
                                          'motor': basic_dc_motor_2, 'target_angular_position': AngularPosition(1, 'rad'),
                                          'limit_electric_current': type_to_check} for type_to_check in types_to_check
                                         if not isinstance(type_to_check, Current)]

@fixture(params = [*start_limit_current_init_type_error_1,
                   *start_limit_current_init_type_error_2,
                   *start_limit_current_init_type_error_3,
                   *start_limit_current_init_type_error_4,
                   *start_limit_current_init_type_error_5])
def start_limit_current_init_type_error(request):
    return request.param


@fixture(params = [{'encoder': basic_encoder, 'tachometer': basic_tachometer, 'motor': basic_dc_motor_1, 'target_angular_position': AngularPosition(1, 'rad'), 'limit_electric_current': Current(1, 'A')},
                   {'encoder': basic_encoder, 'tachometer': basic_tachometer, 'motor': basic_dc_motor_2, 'target_angular_position': AngularPosition(1, 'rad'), 'limit_electric_current': Current(0, 'A')}])
def start_limit_current_init_value_error(request):
    return request.param
