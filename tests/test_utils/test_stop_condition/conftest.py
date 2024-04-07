from gearpy.sensors import SensorBase
from gearpy.units import Current, UnitBase
from gearpy.utils import StopCondition
from gearpy.utils.stop_condition.operator_base import OperatorBase
from pytest import fixture
from tests.conftest import types_to_check, basic_amperometer


stop_condition_init_type_error_1 = [{'sensor': type_to_check, 'threshold': Current(1, 'A'),
                                     'operator': StopCondition.greater_than} for type_to_check in types_to_check
                                    if not isinstance(type_to_check, SensorBase)]

stop_condition_init_type_error_2 = [{'sensor': basic_amperometer, 'threshold': type_to_check,
                                     'operator': StopCondition.greater_than} for type_to_check in types_to_check
                                    if not isinstance(type_to_check, UnitBase)]

stop_condition_init_type_error_3 = [{'sensor': basic_amperometer, 'threshold': Current(1, 'A'),
                                     'operator': type_to_check} for type_to_check in types_to_check
                                    if not isinstance(type_to_check, OperatorBase)]

@fixture(params = [*stop_condition_init_type_error_1,
                   *stop_condition_init_type_error_2,
                   *stop_condition_init_type_error_3])
def stop_condition_init_type_error(request):
    return request.param


stop_condition_check_condition_type_error_1 = [{'sensor_value': type_to_check, 'threshold': Current(1, 'A')}
                                               for type_to_check in types_to_check if not isinstance(type_to_check, UnitBase)]

stop_condition_check_condition_type_error_2 = [{'sensor_value': Current(1, 'A'), 'threshold': type_to_check}
                                               for type_to_check in types_to_check if not isinstance(type_to_check, UnitBase)]

@fixture(params = [*stop_condition_check_condition_type_error_1,
                   *stop_condition_check_condition_type_error_2])
def stop_condition_check_condition_type_error(request):
    return request.param
