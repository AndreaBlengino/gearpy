from gearpy.motor.motor import MotorBase


class Transmission:

    def __init__(self, motor: MotorBase):

        self.chain = [motor]
        while self.chain[-1].drives is not None:
            self.chain.append(self.chain[-1].drives)
