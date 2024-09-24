from gearpy.powertrain import Powertrain
from .motor_control_base import MotorControlBase
from gearpy.motor_control.rules.rules_base import RuleBase


class PWMControl(MotorControlBase):
    r""":py:class:`PWMControl <gearpy.motor_control.pwm_control.PWMControl>`
    object.

    Attributes
    ----------
    :py:attr:`rules` : :py:class:`list`
        The list of the ``pwm`` rules to be applied.

    Methods
    -------
    :py:meth:`add_rule`
        It adds a ``rule`` to :py:attr:`rules` list.
    :py:meth:`apply_rules`
        It applies all the :py:attr:`rules` in order to get a valid ``pwm``
        value to set to the ``powertrain``'s motor.

    .. admonition:: Raises
       :class: warning

       ``TypeError``
           - If ``powertrain`` is not an instance of
             :py:class:`Powertrain <gearpy.powertrain.Powertrain>`,
           - if the first element in ``powertrain`` is not an instance of
             :py:class:`MotorBase <gearpy.mechanical_objects.mechanical_object_base.MotorBase>`,
           - if an element of ``powertrain`` is not an instance of
             :py:class:`RotatingObject <gearpy.mechanical_objects.mechanical_object_base.RotatingObject>`.
       ``ValueError``
           If ``powertrain.elements`` is an empty tuple.

    .. admonition:: See Also
       :class: seealso

       :py:attr:`DCMotor.pwm <gearpy.mechanical_objects.dc_motor.DCMotor.pwm>`
    """

    def __init__(self, powertrain: Powertrain):
        super().__init__(powertrain=powertrain)

        self.__powertrain = powertrain
        self.__rules = []

    @property
    def rules(self) -> list:
        """List of the ``pwm`` rules to be applied.

        Returns
        -------
        :py:class:`list`
            The list of the ``pwm`` rules to be applied.

        .. admonition:: See Also
           :class: seealso

           :py:mod:`rules` module
        """
        return self.__rules

    def add_rule(self, rule: RuleBase) -> None:
        """It adds a ``rule`` to :py:attr:`rules` list.

        Parameters
        ----------
        ``rule`` : :py:class:`RuleBase <gearpy.motor_control.rules.rules_base.RuleBase>`
            Rule to be added to :py:attr:`rules` list.

        .. admonition:: Raises
           :class: warning

           ``TypeError``
               If ``rule`` is not an instance of
               :py:class:`RuleBase <gearpy.motor_control.rules.rules_base.RuleBase>`.

        .. admonition:: See Also
           :class: seealso

           :py:mod:`rules` module
        """
        super().add_rule(rule=rule)

        self.__rules.append(rule)

    def apply_rules(self) -> None:
        """It applies all the :py:attr:`rules` in order to get a valid ``pwm``
        value to set to the ``powertrain``'s motor. \n
        It loops over listed :py:attr:`rules` and applies all of them:

        - if a single rule returns a valid ``pwm``, then this value is set as
          ``powertrain``'s motor ``pwm``,
        - if more than a single rule returns a valid ``pwm``, then it raises a
          ``ValueError``, since multiple rules are valid at the same time and
          it is not possible to identify which ``pwm`` value to use,
        - if no rule returns a valid ``pwm``, then it sets ``powertrain``'s
          motor ``pwm`` to ``1``.

        Before settings the ``pwm``, its value is saturated in order to be
        within ``-1`` and ``1``.

        .. admonition:: Raises
           :class: warning

           ``ValueError``
               If two different rules are applicable at the same time. Only a
               single applicable rule is allowed to a specific simulation time.
        """
        pwm_values = [rule.apply() for rule in self.__rules]
        applied_rules = sum(
            [pwm_value is not None for pwm_value in pwm_values]
        )
        if applied_rules >= 2:
            raise ValueError(
                "At least two rules are simultaneously applicable. Check PWM "
                "rules conditions."
            )
        elif applied_rules == 1:
            pwm = [
                self._saturate_pwm(pwm_value)
                for pwm_value in pwm_values if pwm_value is not None
            ][0]
        else:
            pwm = 1

        self.__powertrain.elements[0].pwm = pwm

    @staticmethod
    def _saturate_pwm(pwm) -> float | int:
        return min(max(pwm, -1), 1)
