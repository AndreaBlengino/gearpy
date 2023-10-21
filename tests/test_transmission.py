from gearpy.mechanical_object import DCMotor
from gearpy.transmission import Transmission
from gearpy.units import AngularSpeed, InertiaMoment, Torque
from gearpy.utils import add_gear_mating, add_fixed_joint
from hypothesis import given, settings
from hypothesis.strategies import lists
from pytest import mark, raises
from tests.conftest import dc_motors, spur_gears, flywheels


@mark.transmission
class TestTransmissionInit:


    @mark.genuine
    @given(motor = dc_motors(),
           gears = lists(elements = spur_gears(), min_size = 1),
           flywheel = flywheels())
    @settings(max_examples = 100)
    def test_method(self, motor, gears, flywheel):
        add_fixed_joint(master = motor, slave = flywheel)
        add_fixed_joint(master = flywheel, slave = gears[0])

        for i in range(0, len(gears) - 1):
            if i%2 == 0:
                add_gear_mating(master = gears[i], slave = gears[i + 1], efficiency = 1)
            else:
                add_fixed_joint(master = gears[i], slave = gears[i + 1])

        transmission = Transmission(motor = motor)

        assert isinstance(transmission.chain, tuple)
        assert transmission.chain
        assert len(transmission.chain) == len(gears) + 2
        assert transmission.chain[0] == motor
        assert transmission.chain[1] == flywheel
        for chain_element, gear in zip(transmission.chain[2:], gears):
            assert chain_element == gear


    @mark.error
    def test_raises_type_error(self, transmission_init_type_error):
        with raises(TypeError):
            Transmission(motor = transmission_init_type_error)


    @mark.error
    def test_raises_value_error(self):
        motor = DCMotor(name = 'motor', inertia_moment = InertiaMoment(1, 'kgm^2'),
                        no_load_speed = AngularSpeed(1000, 'rpm'), maximum_torque = Torque(1, 'Nm'))
        with raises(ValueError):
            Transmission(motor = motor)
