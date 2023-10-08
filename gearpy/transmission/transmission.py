from gearpy.motor.motor import MotorBase


class Transmission:

    def __init__(self, motor: MotorBase):
        if not isinstance(motor, MotorBase):
            raise TypeError("Parameter 'motor' must be an instance of MotorBase.")

        if motor.drives is None:
            raise ValueError("Parameter 'motor' is not connected to any other element. Call 'add_fixed_joint' "
                             "to join 'motor' with a GearBase's instance.")

        chain = [motor]
        while chain[-1].drives is not None:
            chain.append(chain[-1].drives)

        self.__chain = tuple(chain)


    @property
    def chain(self):
        return self.__chain
