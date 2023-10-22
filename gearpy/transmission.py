from collections import Counter
from gearpy.mechanical_object import MotorBase
from gearpy.units import Time
import pandas as pd
from scipy.interpolate import interp1d


class Transmission:
    r"""``gearpy.transmission.Transmission`` object.

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

        counts = Counter([element.name for element in chain])
        for name, count in counts.items():
            if count > 1:
                raise NameError(f"Found {count} elements with the same name {name!r}, "
                                f"each element must have a unique name.")

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


    def snapshot(self,
                 time: list,
                 target_time: Time,
                 angular_position_unit: str = 'rad',
                 angular_speed_unit: str = 'rad/s',
                 angular_acceleration_unit: str = 'rad/s^2',
                 torque_unit: str = 'Nm',
                 driving_torque_unit: str = 'Nm',
                 load_torque_unit: str = 'Nm',
                 print_data: bool = True) -> pd.DataFrame:

        if not isinstance(time, list):
            raise TypeError("Parameter 'time' must be a list.")

        if not all([isinstance(instant, Time) for instant in time]):
            raise TypeError(f"Every element of the 'time' list must be an instance of {Time.__name__!r}.")

        if not time:
            raise ValueError("Parameter 'time' cannot be an empty list.")

        if not isinstance(target_time, Time):
            raise TypeError(f"Parameter 'target_time' must be an instance of {Time.__name__!r}.")

        if not isinstance(angular_position_unit, str):
            raise TypeError(f"Parameter 'angular_position_unit' must be a string.")

        if not isinstance(angular_speed_unit, str):
            raise TypeError(f"Parameter 'angular_speed_unit' must be a string.")

        if not isinstance(angular_acceleration_unit, str):
            raise TypeError(f"Parameter 'angular_acceleration_unit' must be a string.")

        if not isinstance(torque_unit, str):
            raise TypeError(f"Parameter 'torque_unit' must be a string.")

        if not isinstance(driving_torque_unit, str):
            raise TypeError(f"Parameter 'driving_torque_unit' must be a string.")

        if not isinstance(load_torque_unit, str):
            raise TypeError(f"Parameter 'load_torque_unit' must be a string.")

        if not isinstance(print_data, bool):
            raise TypeError(f"Parameter 'print_data' must be a bool.")

        data = pd.DataFrame(columns = [f'angular position ({angular_position_unit})',
                                       f'angular speed ({angular_speed_unit})',
                                       f'angular acceleration ({angular_acceleration_unit})',
                                       f'torque ({torque_unit})',
                                       f'driving torque ({driving_torque_unit})',
                                       f'load torque ({load_torque_unit})'])

        for element in self.chain:
            for variable, unit in zip(['angular position', 'angular speed', 'angular acceleration',
                                       'torque', 'driving torque', 'load torque'],
                                      [angular_position_unit, angular_speed_unit, angular_acceleration_unit,
                                       torque_unit, driving_torque_unit, load_torque_unit]):
                interpolation_function = interp1d(x = [instant.to('sec').value for instant in time],
                                                  y = [value.to(unit).value
                                                       for value in element.time_variables[variable]])
                data.loc[element.name, f'{variable} ({unit})'] = interpolation_function(target_time.to('sec').value).take(0)

        if print_data:
            print(f'Mechanical Transmission Status at Time = {target_time}')
            print(data.to_string())

        return data
