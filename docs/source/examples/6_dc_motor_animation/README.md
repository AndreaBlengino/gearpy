### System in Analysis

The complete example code is available 
[here](https://github.com/AndreaBlengino/gearpy/blob/master/docs/source/examples/6_dc_motor_animation/dc_motor_animation.py).  
The mechanical powertrain to be studied is the one described in the 
[5 - DC Motor PWM Control](https://gearpy.readthedocs.io/en/latest/examples/5_dc_motor_pwm_control/index.html) 
example.  

### Model Set Up

We can get an animation of the DC motor's working characteristics:

```python
from gearpy.utils import dc_motor_characteristics_animation

dc_motor_characteristics_animation(motor = motor,
                                   time = powertrain.time,
                                   interval = 10,
                                   figsize = (10, 5),
                                   torque_unit = 'mNm',
                                   current_unit = 'mA')
```

![](animations/animation_1.gif)

On the left hand side there is the torque-speed characteristic, while on
the right hand side there is the torque-current characteristic and the 
orange dot is the working point of the motor. The characteristics can 
vary based on the PWM value.
