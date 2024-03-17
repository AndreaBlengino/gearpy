from gearpy.mechanical_objects import Flywheel
from hypothesis import given, settings
from hypothesis.strategies import floats
from pytest import mark, raises
from tests.test_mechanical_objects.test_slave.conftest import basic_slaves
from tests.conftest import rotating_objects


@mark.slave
class TestSlaveDrivenBy:


    @mark.genuine
    @given(master_rotating_object = rotating_objects())
    @settings(max_examples = 100, deadline = None)
    def test_property(self, master_rotating_object):
        for slave in basic_slaves:
            slave.driven_by = master_rotating_object

            assert slave.driven_by == master_rotating_object


    @mark.error
    def test_raises_type_error(self, slave_driven_by_type_error):
        for slave in basic_slaves:
            with raises(TypeError):
                slave.driven_by = slave_driven_by_type_error


@mark.slave
class TestSlaveDrives:


    @mark.genuine
    @given(slave_rotating_object = rotating_objects())
    @settings(max_examples = 100, deadline = None)
    def test_property(self, slave_rotating_object):
        for slave in basic_slaves:
            slave.drives = slave_rotating_object

            assert slave.drives == slave_rotating_object


    @mark.error
    def test_raises_type_error(self, slave_drives_type_error):
        for slave in basic_slaves:
            with raises(TypeError):
                slave.drives = slave_drives_type_error


@mark.slave
class TestSlaveMasterGearRatio:


    @mark.genuine
    @given(master_gear_ratio = floats(allow_nan = False, allow_infinity = False, min_value = 0, exclude_min = True))
    @settings(max_examples = 100, deadline = None)
    def test_property(self, master_gear_ratio):
        for slave in basic_slaves:
            slave.master_gear_ratio = master_gear_ratio

            assert slave.master_gear_ratio == master_gear_ratio


    @mark.error
    def test_raises_type_error(self, slave_master_gear_ratio_type_error):
        for slave in basic_slaves:
            with raises(TypeError):
                slave.master_gear_ratio = slave_master_gear_ratio_type_error


    @mark.error
    def test_raises_value_error(self):
        for slave in basic_slaves:
            with raises(ValueError):
                slave.master_gear_ratio = -1.0


@mark.slave
class TestSlaveMasterGearEfficiency:


    @mark.genuine
    @given(master_gear_efficiency = floats(allow_nan = False, allow_infinity = False,
                                           min_value = 0, exclude_min = False, max_value = 1, exclude_max = False))
    @settings(max_examples = 100, deadline = None)
    def test_property(self, master_gear_efficiency):
        for slave in basic_slaves:
            if not isinstance(slave, Flywheel):
                slave.master_gear_efficiency = master_gear_efficiency

                assert slave.master_gear_efficiency == master_gear_efficiency


    @mark.error
    def test_raises_type_error(self, slave_master_gear_efficiency_type_error):
        for slave in basic_slaves:
            if not isinstance(slave, Flywheel):
                with raises(TypeError):
                    slave.master_gear_efficiency = slave_master_gear_efficiency_type_error


    @mark.error
    def test_raises_value_error(self, slave_master_gear_efficiency_value_error):
        for slave in basic_slaves:
            if not isinstance(slave, Flywheel):
                with raises(ValueError):
                    slave.master_gear_efficiency = slave_master_gear_efficiency_value_error
