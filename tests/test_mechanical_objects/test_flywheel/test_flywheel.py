from gearpy.mechanical_objects import Flywheel
from gearpy.units import InertiaMoment
from hypothesis import given, settings
from hypothesis.strategies import text
from pytest import mark, raises
from tests.test_units.test_inertia_moment.conftest import inertia_moments


@mark.flywheel
class TestFlywheelInit:


    @mark.genuine
    @given(name = text(min_size = 1),
           inertia_moment = inertia_moments())
    @settings(max_examples = 100)
    def test_method(self, name, inertia_moment):
        flywheel = Flywheel(name = name, inertia_moment = inertia_moment)

        assert flywheel.name == name
        assert flywheel.inertia_moment == inertia_moment


    @mark.error
    def test_raises_type_error(self, flywheel_init_type_error):
        with raises(TypeError):
            Flywheel(**flywheel_init_type_error)


    @mark.error
    def test_raises_value_error(self):
        with raises(ValueError):
            Flywheel(name = '', inertia_moment = InertiaMoment(1, 'kgm^2'))
