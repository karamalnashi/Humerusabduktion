## Elbow flexion


* to run a system

$ pipenv run performance_calculation_automated.py



## Maximum and minimum values

* the maximum and minimum values are update automatically 
* in order to change the limit, replace the value_min and value_max with any number


For example (code line 74),

** per = np.interp(angle, (value_min, value_max), (0, 100))
** bar = np.interp(angle, (value_min, value_max), (650, 100))

change
** per = np.interp(angle, (190, 350), (0, 100))
** bar = np.interp(angle, (190 , 350), (650, 100))
