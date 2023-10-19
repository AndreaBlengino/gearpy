from gearpy.motor import MotorBase


class Transmission:
    r"""gearpy.transmission.transmission.Transmission object.

    Attributes
    ----------
    :py:attr:`chain` : tuple
        Elements in the transmission chain.

    Raises
    ------
    TypeError
        If ``motor`` parameter is not an instance of ``MotorBase``.
    ValueError
        If ``motor.drives`` is ``None``.
    """

    def __init__(self, motor: MotorBase):
        if not isinstance(motor, MotorBase):
            raise TypeError(f"Parameter 'motor' must be an instance of {MotorBase.__name__!r}.")

        if motor.drives is None:
            raise ValueError("Parameter 'motor' is not connected to any other element. Call 'add_fixed_joint' "
                             "to join 'motor' with a GearBase's instance.")

        chain = [motor]
        while chain[-1].drives is not None:
            chain.append(chain[-1].drives)

        self.__chain = tuple(chain)


    @property
    def chain(self) -> tuple:
        """Elements in the transmission chain. \n
        The first element is the driving motor, the next elements are in order, from the closest to the farthest from
        the motor. Each element is driven by the previous one and it drives the following one.

        Returns
        -------
        tuple
            Elements in the transmission chain.
        """
        return self.__chain
