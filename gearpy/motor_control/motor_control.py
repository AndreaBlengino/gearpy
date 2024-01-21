from gearpy.transmission import Transmission
from .motor_control_base import MotorControlBase
from .rules_base import RuleBase


class PWMControl(MotorControlBase):
    r"""``gearpy.motor_control.PWMControl`` object.

    Attributes
    ----------
    :py:attr:`transmission` : Transmission
        Transmission to be controlled by applying a ``pwm`` to its motor.
    :py:attr:`rules` : list
        List of the ``pwm`` rules to be applied.

    Methods
    -------
    :py:meth:`add_rule`
        Adds a ``rule`` to ``rules`` list.
    :py:meth:`apply_rules`
        Applies all the ``rules`` in order to get a valid ``pwm`` value to set to the ``transmission``'s motor.

    Raises
    ------
    TypeError
        - If ``transmission`` is not an instance of ``Transmission``,
        - if the first element in ``transmission`` is not an instance of ``MotorBase``,
        - if an element of ``transmission`` is not an instance of ``RotatingObject``.
    ValueError
        If ``transmission.chain`` is an empty tuple.

    See Also
    --------
    :py:attr:`gearpy.mechanical_object.mechanical_objects.DCMotor.pwm`
    """

    def __init__(self, transmission: Transmission):
        super().__init__(transmission = transmission)

    @property
    def transmission(self) -> Transmission:
        """Transmission to be controlled by applying a ``pwm`` to its motor.

        Returns
        -------
        Transmission
            Transmission to be controlled by applying a ``pwm`` to its motor.

        See Also
        --------
        :py:class:`gearpy.transmission.Transmission`
        """
        return super().transmission

    @property
    def rules(self) -> list:
        """List of the ``pwm`` rules to be applied.

        Returns
        -------
        list
            List of the ``pwm`` rules to be applied.

        See Also
        --------
        :py:mod:`rules`
        """
        return super().rules

    def add_rule(self, rule: RuleBase):
        """Adds a ``rule`` to ``rules`` list.

        Parameters
        ----------
        rule : RuleBase
            Rule to be added to ``rules`` list.

        Raises
        ------
        TypeError
            If ``rule`` is not an instance of ``RuleBase``.

        See Also
        --------
        :py:mod:`rules`
        """
        super().add_rule(rule = rule)

    def apply_rules(self):
        """Applies all the ``rules`` in order to get a valid ``pwm`` value to set to the ``transmission``'s motor. \n
        It loops over listed ``rules`` and applies all of them:

        - if a single rule returns a valid ``pwm``, then this value is set as ``transmission``'s motor ``pwm``,
        - if more than a single rule returns a valid ``pwm``, then it raises a ``ValueError``, since multiple rules are
          valid at the same time and it is not possible to identify which ``pwm`` value to use,
        - if no rule returns a valid ``pwm``, then it sets ``transmission``'s motor ``pwm`` to ``1``.

        Before settings the ``pwm``, its value is saturated in order to be within ``-1`` and ``1``.

        Raises
        ------
        ValueError
            If two different rules are applicable at the same time. Only a single applicable rule is allowed to a
            specific simulation time.
        """

        pwm_values = [rule.apply() for rule in super().rules]
        applied_rules = sum([pwm_value is not None for pwm_value in pwm_values])
        if applied_rules >= 2:
            raise ValueError("At least two rules are simultaneously applicable. Check PWM rules conditions.")
        elif applied_rules == 1:
            pwm = [self._saturate_pwm(pwm_value) for pwm_value in pwm_values if pwm_value is not None][0]
        else:
            pwm = 1

        self.transmission.chain[0].pwm = pwm

    @staticmethod
    def _saturate_pwm(pwm):
        return min(max(pwm, -1), 1)
