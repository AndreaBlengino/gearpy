from gearpy.mechanical_objects import MotorBase, RotatingObject
from gearpy.sensors import AbsoluteRotaryEncoder
from gearpy.powertrain import Powertrain
from gearpy.units import AngularPosition
from gearpy.motor_control.rules.rules_base import RuleBase
from typing import Optional
from .utils import _compute_pwm_min


class StartProportionalToAngularPosition(RuleBase):
    """:py:class:`StartProportionalToAngularPosition <gearpy.motor_control.rules.start_proportional_to_angular_position.StartProportionalToAngularPosition>`
    object. \n
    It can be used to make a gradual start of the ``powertrain``'s motion, in
    order to avoid a peak in the ``powertrain``'s DC motor absorbed electric
    current. \n
    It computes a ``pwm`` to apply to the ``powertrain``'s DC motor which
    increases linearly with the ``encoder``'s ``target`` rotating object's
    ``angular_position``. The computed ``pwm`` starts from a minimum value,
    based on ``powertrain``'s elements properties and ``pwm_min_multiplier`` or
    solely on ``pwm_min`` parameter. The computed ``pwm`` increases up to ``1``
    when the ``encoder``'s ``target``'s ``angular_position`` equals
    ``target_angular_position``.

    Methods
    -------
    :py:meth:`apply`
        It computes the ``pwm`` to apply to the ``powertrain`` motor,
        proportional to the ``encoder``'s ``target`` ``angular_position`` until
        it reaches the ``target_angular_position``.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``encoder`` is not an instance of
             :py:class:`AbsoluteRotaryEncoder <gearpy.sensors.absolute_rotary_encoder.AbsoluteRotaryEncoder>`,
           - if ``powertrain`` is not an instance of
             :py:class:`Powertrain <gearpy.powertrain.Powertrain>`,
           - if the first element in ``powertrain`` is not an instance of
             :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`,
           - if an element of ``powertrain`` is not an instance of
             :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`,
           - if ``target_angular_position`` is not an instance of
             :py:class:`AngularPosition <gearpy.units.units.AngularPosition>`,
           - if ``pwm_min_multiplier`` is not a :py:class:`float` or an
             :py:class:`int`,
           - if ``pwm_min`` is defined and it is not a :py:class:`float` or an
             :py:class:`int`.
       ValueError
           - If ``powertrain.elements`` is an empty :py:class:`tuple`,
           - if the ``powertrain`` motor cannot compute ``electric_current``
             property
             (:py:attr:`DCMotor.electric_current <gearpy.mechanical_objects.dc_motor.DCMotor.electric_current>`),
           - if ``pwm_min_multiplier`` is less than or equal to ``1``,
           - if ``pwm_min`` is defined and it is negative or null.

    .. admonition:: See Also
       :class: seealso

       :py:attr:`DCMotor.pwm <gearpy.mechanical_objects.dc_motor.DCMotor.pwm>`
    """

    def __init__(
        self,
        encoder: AbsoluteRotaryEncoder,
        powertrain: Powertrain,
        target_angular_position: AngularPosition,
        pwm_min_multiplier: float | int,
        pwm_min: Optional[float] = None
    ):
        super().__init__()

        if not isinstance(encoder, AbsoluteRotaryEncoder):
            raise TypeError(
                f"Parameter 'encoder' must be an instance of "
                f"{AbsoluteRotaryEncoder.__name__!r}."
            )

        if not isinstance(powertrain, Powertrain):
            raise TypeError(
                f"Parameter 'powertrain' must be an instance of "
                f"{Powertrain.__name__!r}."
            )

        if not powertrain.elements:
            raise ValueError(
                "Parameter 'powertrain.elements' cannot be an empty tuple."
            )

        if not isinstance(powertrain.elements[0], MotorBase):
            raise TypeError(
                f"First element in 'powertrain' must be an instance of "
                f"{MotorBase.__name__!r}."
            )

        if not powertrain.elements[0].electric_current_is_computable:
            raise ValueError(
                "The motor in 'powertrain' cannot compute 'electric_current' "
                "property."
            )

        if not all(
            [isinstance(item, RotatingObject) for item in powertrain.elements]
        ):
            raise TypeError(
                f"All elements of 'powertrain' must be instances of "
                f"{RotatingObject.__name__!r}."
            )

        if not isinstance(target_angular_position, AngularPosition):
            raise TypeError(
                f"Parameter 'target_angular_position' must be an instance of "
                f"{AngularPosition.__name__!r}."
            )

        if not isinstance(pwm_min_multiplier, float | int):
            raise TypeError(
                "Parameter 'pwm_min_multiplier' must be a float or an integer."
            )

        if pwm_min_multiplier <= 1:
            raise ValueError(
                "Parameter 'pwm_min_multiplier' must be greater than 1."
            )

        if pwm_min is not None:
            if not isinstance(pwm_min, float | int):
                raise TypeError(
                    "Parameter 'pwm_min' must be a float or an integer."
                )

            if pwm_min <= 0:
                raise ValueError("Parameter 'pwm_min' must be positive.")

        self.__encoder = encoder
        self.__powertrain = powertrain
        self.__target_angular_position = target_angular_position
        self.__pwm_min_multiplier = pwm_min_multiplier
        self.__pwm_min = pwm_min

    def apply(self) -> None | float | int:
        """It computes the ``pwm`` to apply to the ``powertrain`` motor,
        proportional to the ``encoder``'s ``target`` ``angular_position`` until
        it reaches the ``target_angular_position``.

        Returns
        -------
        :py:class:`float` or :py:class:`int` or :py:obj:`None`
            PWM value to apply to the motor, proportional to the ``encoder``'s
            ``target`` ``angular_position``.

        .. admonition:: Notes
           :class: tip

           The ``powertrain``'s motor has a minimum ``pwm`` which, as is,
           cannot be used to control the motor, since at this value the motor
           will remain still. So, in order to properly control the motor
           motion, it is required to apply a ``pwm`` greater than the minimum
           ``pwm``, therefore the motor minimum ``pwm`` is multiplied by
           ``pwm_min_multiplier`` to get a starting ``pwm`` to be applied to
           the motor. \n
           If the motor's minimum ``pwm`` is null, then it is useless to
           multiply this value by ``pwm_min_multiplier`` in order to get a
           starting ``pwm``; therefore, only in this case, ``pwm_min`` is
           directly used as starting ``pwm``. \n
           First of all, the rule computes a *candidate* minimum applicable
           ``pwm`` as:
        """\
        r"""
           .. math::
               D_{min}^c \left( T_l \right) = \frac{1}{\eta_t} \,
               \frac{T_l}{T_{max}} \, \frac{i_{max} - i_0}{i_{max}} +
               \frac{i_0}{i_{max}}

           where:

           - :math:`D_{min}^c` is the *candidate* minimum applicable ``pwm``,
           - :math:`T_l` is the load torque on the ``powertrain``
             :py:attr:`DCMotor.load_torque <gearpy.mechanical_objects.dc_motor.DCMotor.load_torque>`,
           - :math:`T_{max}` is the maximum torque developed by the
             ``powertrain`` DC motor
             (:py:attr:`DCMotor.maximum_torque <gearpy.mechanical_objects.dc_motor.DCMotor.maximum_torque>`),
           - :math:`i_{max}` is the maximum electric current absorbed by the
             ``powertrain`` DC motor
             (:py:attr:`DCMotor.maximum_electric_current <gearpy.mechanical_objects.dc_motor.DCMotor.maximum_electric_current>`),
           - :math:`i_0` is the no load electric current absorbed by the
             ``powertrain`` DC motor
             (:py:attr:`DCMotor.no_load_electric_current <gearpy.mechanical_objects.dc_motor.DCMotor.no_load_electric_current>`),
           - :math:`\eta_t` is the ``powertrain`` overall efficiency, computed
             as:

           .. math::
               \eta_t = \prod_{i = 1}^N \eta_i

           where:

           - :math:`\eta_i` is the mechanical mating efficiency of the mating
             between two gears
             (:py:attr:`SpurGear.master_gear_efficiency <gearpy.mechanical_objects.spur_gear.SpurGear.master_gear_efficiency>`
             or
             :py:attr:`HelicalGear.master_gear_efficiency <gearpy.mechanical_objects.helical_gear.HelicalGear.master_gear_efficiency>`
             or
             :py:attr:`WormGear.master_gear_efficiency <gearpy.mechanical_objects.worm_gear.WormGear.master_gear_efficiency>`
             or
             :py:attr:`WormWheel.master_gear_efficiency <gearpy.mechanical_objects.worm_wheel.WormWheel.master_gear_efficiency>`),
           - :math:`N` is the total number of gear matings in the
             ``powertrain``.

           If both the load torque on the ``powertrain`` DC motor :math:`T_l`
           and the motor no load electric current :math:`i_0` are null, then
           also the computed *candidate* minimum applicable ``pwm``
           :math:`D_{min}^c` is null. Only in this case, the computed
           *candidate* minimum applicable ``pwm`` is discarded and it is taken
           into account the ``pwm_min`` parameter, which must have been set
           (don't used otherwise):

           .. math::
               D_{min} = D_{min}^p

           where:

           - :math:`D_{min}` is the minimum applicable ``pwm``,
           - :math:`D_{min}^p` is the ``pwm_min`` parameter.

           Otherwise, the *candidate* :math:`D_{min}` is multiplied by the
           ``pwm_min_multiplier`` parameter.

           .. math::
               D_{min} = D_{min}^c \, g

           where :math:`g` is the ``pwm_min_multiplier`` parameter.

           Then it checks the applicability condition, defined as:

           .. math::
               \theta \le \theta_t

           where:

           - :math:`\theta` is the ``encoder``'s ``target``
             ``angular_position``,
           - :math:`\theta_t` is the ``target_angular_position``.

           If the applicability condition is not met, then it returns
           :py:obj:`None`, otherwise it computes the ``pwm`` as:

           .. math::
               D \left( \theta \right) = \left( 1 - D_{min} \right)
               \frac{\theta}{\theta_t} + D_{min}
        """
        angular_position = self.__encoder.get_value()

        computed_pwm_min = self.__pwm_min_multiplier*_compute_pwm_min(
            powertrain=self.__powertrain
        )
        if computed_pwm_min != 0:
            pwm_min = computed_pwm_min
        else:
            if self.__pwm_min is None:
                raise ValueError("Missing 'pwm_min' parameter.")
            pwm_min = self.__pwm_min

        if angular_position <= self.__target_angular_position:
            return (1 - pwm_min)*angular_position / \
                self.__target_angular_position + pwm_min
