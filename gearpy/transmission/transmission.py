from gearpy.motor.motor import MotorBase


class Transmission:

    def __init__(self, motor: MotorBase):
        if not isinstance(motor, MotorBase):
            raise TypeError("Parameter 'motor' must be an instance of MotorBase.")

        if motor.drives is None:
            raise ValueError("Parameter 'motor' is not connected to any other element. Call 'add_fixed_joint' "
                             "to join 'motor' with a GearBase's instance.")

        self.__chain = [motor]
        while self.__chain[-1].drives is not None:
            self.__chain.append(self.__chain[-1].drives)


    @property
    def chain(self):
        return self.__chain
