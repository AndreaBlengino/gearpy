from gearpy.mechanical_objects import GearBase, MotorBase, WormGear
from hypothesis import given, settings
from pytest import mark, raises
from tests.test_mechanical_objects.test_rotating_object.conftest import \
    basic_rotating_objects
from tests.test_units.test_angular_acceleration.conftest import \
    angular_accelerations
from tests.test_units.test_angular_position.conftest import angular_positions
from tests.test_units.test_angular_speed.conftest import angular_speeds
from tests.test_units.test_torque.conftest import torques
from tests.test_units.test_force.conftest import forces
from tests.test_units.test_stress.conftest import stresses
from tests.test_units.test_current.conftest import currents


@mark.rotating_object
class TestRotatingObjectAngularPosition:

    @mark.genuine
    @given(angular_position=angular_positions())
    @settings(max_examples=100, deadline=None)
    def test_property(self, angular_position):
        for rotating_object in basic_rotating_objects:
            rotating_object.angular_position = angular_position

            assert rotating_object.angular_position == angular_position

    @mark.error
    def test_raises_type_error(
        self,
        rotating_object_angular_position_type_error
    ):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.angular_position = \
                    rotating_object_angular_position_type_error


@mark.rotating_object
class TestRotatingObjectAngularSpeed:

    @mark.genuine
    @given(angular_speed=angular_speeds())
    @settings(max_examples=100, deadline=None)
    def test_property(self, angular_speed):
        for rotating_object in basic_rotating_objects:
            rotating_object.angular_speed = angular_speed

            assert rotating_object.angular_speed == angular_speed

    @mark.error
    def test_raises_type_error(self, rotating_object_angular_speed_type_error):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.angular_speed = \
                    rotating_object_angular_speed_type_error


@mark.rotating_object
class TestRotatingObjectAngularAcceleration:

    @mark.genuine
    @given(angular_acceleration=angular_accelerations())
    @settings(max_examples=100, deadline=None)
    def test_property(self, angular_acceleration):
        for rotating_object in basic_rotating_objects:
            rotating_object.angular_acceleration = angular_acceleration

            assert rotating_object.angular_acceleration == angular_acceleration

    @mark.error
    def test_raises_type_error(
        self,
        rotating_object_angular_acceleration_type_error
    ):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.angular_acceleration = \
                    rotating_object_angular_acceleration_type_error


@mark.rotating_object
class TestRotatingObjectTorque:

    @mark.genuine
    @given(torque=torques())
    @settings(max_examples=100, deadline=None)
    def test_property(self, torque):
        for rotating_object in basic_rotating_objects:
            rotating_object.torque = torque

            assert rotating_object.torque == torque

    @mark.error
    def test_raises_type_error(self, rotating_object_torque_type_error):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.torque = rotating_object_torque_type_error


@mark.rotating_object
class TestRotatingObjectDrivingTorque:

    @mark.genuine
    @given(driving_torque=torques())
    @settings(max_examples=100, deadline=None)
    def test_property(self, driving_torque):
        for rotating_object in basic_rotating_objects:
            rotating_object.driving_torque = driving_torque

            assert rotating_object.driving_torque == driving_torque

    @mark.error
    def test_raises_type_error(
        self,
        rotating_object_driving_torque_type_error
    ):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.driving_torque = \
                    rotating_object_driving_torque_type_error


@mark.rotating_object
class TestRotatingObjectLoadTorque:

    @mark.genuine
    @given(load_torque=torques())
    @settings(max_examples=100, deadline=None)
    def test_property(self, load_torque):
        for rotating_object in basic_rotating_objects:
            rotating_object.load_torque = load_torque

            assert rotating_object.load_torque == load_torque

    @mark.error
    def test_raises_type_error(self, rotating_object_load_torque_type_error):
        for rotating_object in basic_rotating_objects:
            with raises(TypeError):
                rotating_object.load_torque = \
                    rotating_object_load_torque_type_error


@mark.rotating_object
class TestRotatingObjectTimeVariables:

    @mark.genuine
    def test_property(self):
        for rotating_object in basic_rotating_objects:
            time_variables = rotating_object.time_variables

            time_variables_list = [
                'angular position',
                'angular speed',
                'angular acceleration',
                'torque',
                'driving torque',
                'load torque'
            ]
            if isinstance(rotating_object, MotorBase):
                if rotating_object.electric_current_is_computable:
                    time_variables_list.append('electric current')
            if isinstance(rotating_object, GearBase | WormGear):
                if rotating_object.tangential_force_is_computable:
                    time_variables_list.append('tangential force')
            if isinstance(rotating_object, GearBase):
                if rotating_object.bending_stress_is_computable:
                    time_variables_list.append('bending stress')
                    if rotating_object.contact_stress_is_computable:
                        time_variables_list.append('contact stress')

            assert isinstance(time_variables, dict)
            assert time_variables_list == list(time_variables.keys())
            assert all([value == [] for value in time_variables.values()])


@mark.rotating_object
class TestRotatingObjectUpdateTimeVariables:

    @mark.genuine
    @given(
        angular_position=angular_positions(),
        angular_speed=angular_speeds(),
        angular_acceleration=angular_accelerations(),
        torque=torques(),
        driving_torque=torques(),
        load_torque=torques(),
        tangential_force=forces(),
        bending_stress=stresses(),
        contact_stress=stresses(),
        electric_current=currents()
    )
    def test_method(
        self,
        angular_position,
        angular_speed,
        angular_acceleration,
        torque,
        driving_torque,
        load_torque,
        tangential_force,
        bending_stress,
        contact_stress,
        electric_current
    ):
        for rotating_object in basic_rotating_objects:
            rotating_object.angular_position = angular_position
            rotating_object.angular_speed = angular_speed
            rotating_object.angular_acceleration = angular_acceleration
            rotating_object.torque = torque
            rotating_object.driving_torque = driving_torque
            rotating_object.load_torque = load_torque
            if isinstance(rotating_object, MotorBase):
                if rotating_object.electric_current_is_computable:
                    rotating_object.electric_current = electric_current
            if isinstance(rotating_object, GearBase | WormGear):
                if rotating_object.tangential_force_is_computable:
                    rotating_object.tangential_force = tangential_force
            if isinstance(rotating_object, GearBase):
                if rotating_object.bending_stress_is_computable:
                    rotating_object.bending_stress = bending_stress
                    if rotating_object.contact_stress_is_computable:
                        rotating_object.contact_stress = contact_stress

            rotating_object.update_time_variables()
            time_variables = rotating_object.time_variables

            time_variables_list = [
                'angular position',
                'angular speed',
                'angular acceleration',
                'torque',
                'driving torque',
                'load torque'
            ]
            if isinstance(rotating_object, MotorBase):
                if rotating_object.electric_current_is_computable:
                    time_variables_list.append('electric current')
                time_variables_list.append('pwm')
            if isinstance(rotating_object, GearBase | WormGear):
                if rotating_object.tangential_force_is_computable:
                    time_variables_list.append('tangential force')
            if isinstance(rotating_object, GearBase):
                if rotating_object.bending_stress_is_computable:
                    time_variables_list.append('bending stress')
                    if rotating_object.contact_stress_is_computable:
                        time_variables_list.append('contact stress')

            assert isinstance(time_variables, dict)
            assert time_variables_list == list(time_variables.keys())
            assert time_variables['angular position'][-1] == angular_position
            assert time_variables['angular speed'][-1] == angular_speed
            assert time_variables['angular acceleration'][-1] == \
                angular_acceleration
            assert time_variables['torque'][-1] == torque
            assert time_variables['driving torque'][-1] == driving_torque
            assert time_variables['load torque'][-1] == load_torque
            if isinstance(rotating_object, MotorBase):
                if rotating_object.electric_current_is_computable:
                    assert time_variables['electric current'][-1] == \
                        electric_current
            if isinstance(rotating_object, GearBase | WormGear):
                if rotating_object.tangential_force_is_computable:
                    assert time_variables['tangential force'][-1] == \
                        tangential_force
            if isinstance(rotating_object, GearBase):
                if rotating_object.bending_stress_is_computable:
                    assert time_variables['bending stress'][-1] == \
                        bending_stress
                    if rotating_object.contact_stress_is_computable:
                        assert time_variables['contact stress'][-1] == \
                            contact_stress
