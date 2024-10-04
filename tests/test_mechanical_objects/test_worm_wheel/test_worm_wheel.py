from gearpy.mechanical_objects import WormGear, WormWheel
from gearpy.units import Angle, Length
from gearpy.utils import add_worm_gear_mating
from hypothesis import given, settings
from hypothesis.strategies import text, floats, integers, sampled_from
from pytest import mark, raises
from tests.conftest import (
    basic_worm_gear_1,
    basic_worm_gear_2,
    basic_worm_wheel_1,
    basic_worm_wheel_2
)
from tests.test_units.test_inertia_moment.conftest import inertia_moments
from gearpy.mechanical_objects.mechanical_object_base import \
    WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES


@mark.worm_wheel
class TestWormWheelInit:

    @mark.genuine
    @given(
        name=text(min_size=1),
        n_teeth=integers(min_value=10, max_value=1000),
        inertia_moment=inertia_moments(),
        pressure_angle=sampled_from(
            elements=WORM_GEAR_AND_WHEEL_AVAILABLE_PRESSURE_ANGLES
        ),
        helix_angle_value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0.1,
            max_value=15
        ),
        module_value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0.1,
            max_value=10
        ),
        face_width_value=floats(
            allow_nan=False,
            allow_infinity=False,
            min_value=0.1,
            max_value=100
        )
    )
    @settings(max_examples=100, deadline=None)
    def test_method(
        self,
        name,
        n_teeth,
        inertia_moment,
        pressure_angle,
        helix_angle_value,
        module_value,
        face_width_value
    ):
        helix_angle = Angle(helix_angle_value, 'deg')
        module = Length(module_value, 'mm')
        face_width = Length(face_width_value, 'mm')
        gear = WormWheel(
            name=name,
            n_teeth=n_teeth,
            inertia_moment=inertia_moment,
            pressure_angle=pressure_angle,
            helix_angle=helix_angle,
            module=module,
            face_width=face_width
        )

        assert gear.name == name
        assert gear.n_teeth == n_teeth
        assert gear.inertia_moment == inertia_moment
        assert gear.pressure_angle == pressure_angle
        assert gear.helix_angle == helix_angle
        assert gear.module == module
        assert gear.face_width == face_width
        assert gear.reference_diameter == n_teeth*module

    @mark.error
    def test_raises_type_error(self, worm_wheel_init_type_error):
        with raises(TypeError):
            WormWheel(**worm_wheel_init_type_error)

    @mark.error
    def test_raises_value_error(self, worm_wheel_init_value_error):
        with raises(ValueError):
            WormWheel(**worm_wheel_init_value_error)


@mark.worm_wheel
class TestWormWheelBendingStressIsComputable:

    @mark.genuine
    def test_property(self):
        masters = [
            basic_worm_gear_1,
            basic_worm_gear_2,
            basic_worm_wheel_1,
            basic_worm_wheel_2
        ]
        slaves = [
            basic_worm_wheel_1,
            basic_worm_wheel_2,
            basic_worm_gear_1,
            basic_worm_gear_2
        ]

        for master, slave in zip(masters, slaves):
            add_worm_gear_mating(
                master=master,
                slave=slave,
                friction_coefficient=0
            )
            if isinstance(master, WormGear):
                worm_gear = master
                worm_wheel = slave
            else:
                worm_gear = slave
                worm_wheel = master
            if (worm_wheel.module is None) or \
               (worm_wheel.face_width is None) or \
               (worm_gear.reference_diameter is None):
                assert not worm_wheel.bending_stress_is_computable
            else:
                assert worm_wheel.bending_stress_is_computable
