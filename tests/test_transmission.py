from gearpy import DCMotor, Transmission, add_gear_mating, add_fixed_joint
from hypothesis import given, settings
from hypothesis.strategies import lists
from pytest import mark, raises
from tests.conftest import dc_motors, spur_gears


@mark.transmission
class TestTransmissionInit:


    @mark.genuine
    @given(motor = dc_motors(),
           gears = lists(elements = spur_gears(), min_size = 1))
    @settings(max_examples = 100)
    def test_method(self, motor, gears):
        add_fixed_joint(master = motor, slave = gears[0])

        for i in range(0, len(gears) - 1):
            if i%2 == 0:
                add_gear_mating(master = gears[i], slave = gears[i + 1], efficiency = 1)
            else:
                add_fixed_joint(master = gears[i], slave = gears[i + 1])

        transmission = Transmission(motor = motor)

        assert isinstance(transmission.chain, list)
        assert transmission.chain
        assert len(transmission.chain) == len(gears) + 1
        assert transmission.chain[0] == motor
        for chain_element, gear in zip(transmission.chain[1:], gears):
            assert chain_element == gear


    @mark.error
    def test_raises_type_error(self, transmission_init_type_error):
        with raises(TypeError):
            Transmission(motor = transmission_init_type_error)


    @mark.error
    def test_raises_value_error(self):
        motor = DCMotor(name = 'motor', inertia = 1, no_load_speed = 1, maximum_torque = 1)
        with raises(ValueError):
            Transmission(motor = motor)