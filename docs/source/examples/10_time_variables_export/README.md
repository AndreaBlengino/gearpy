### System in Analysis

The complete example code is available 
[here](https://github.com/AndreaBlengino/gearpy/blob/master/docs/source/examples/10_time_variables_export/time_variables_export.py).  
The mechanical powertrain to be studied is the one described in the 
[1 - Simple Powertrain](https://gearpy.readthedocs.io/en/latest/examples/1_simple_powertrain/index.html) 
example.  
We want to export the computed time variables to some files in order
to save and analyze them afterward. 

### Time Variables Export

After running the simulation, we can export the time variables of each
rotating object in the powertrain with:

```python
powertrain.export_time_variables(folder_path = 'data')
```

and write the name of the folder in which to save the files, `'data'`
in this case. In that folder `gearpy` saves a file for each rotating
object in the powertrain, and it uses the name of the rotating object
to name the file.  
We can open and analyze these file with [pandas](https://pandas.pydata.org),
which is a dependency of `gearpy`, so it is already installed:

```python
import os
import pandas as pd

motor_data = pd.read_csv(os.path.join('data', 'motor.csv'))

print(motor_data.head(11).to_string())
```

```text
    time (sec)  angular position (rad)  angular speed (rad/s)  angular acceleration (rad/s^2)  torque (Nm)  driving torque (Nm)  load torque (Nm)  pwm
0          0.0                0.000000               0.000000                      608.727069     0.007142             0.010000          0.002858    1
1          0.5              152.181767             304.363535                      443.582951     0.005205             0.008062          0.002858    1
2          1.0              415.259272             526.155010                      323.241473     0.003793             0.006650          0.002858    1
3          1.5              759.147146             687.775747                      235.547939     0.002764             0.005621          0.002858    1
4          2.0             1161.922004             805.549716                      171.645151     0.002014             0.004872          0.002858    1
5          2.5             1607.608149             891.372292                      125.078819     0.001468             0.004325          0.002858    1
6          3.0             2084.564000             953.911701                       91.145662     0.001069             0.003927          0.002858    1
7          3.5             2584.306266             999.484532                       66.418373     0.000779             0.003637          0.002858    1
8          4.0             3100.653125            1032.693719                       48.399454     0.000568             0.003426          0.002858    1
9          4.5             3629.099848            1056.893446                       35.268964     0.000414             0.003272          0.002858    1
10         5.0             4166.363812            1074.527928                       25.700699     0.000302             0.003159          0.002858    1
```

We have printed only the first eleven rows of the file.  
We can see that there is a column for each available time variable
and each row is a simulated time step.
