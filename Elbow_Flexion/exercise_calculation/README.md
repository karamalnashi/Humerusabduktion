## Elbow flexion


* to run a system

$ pipenv run Mqtt.py

## Die Nachrichten, die Anwendung erhalten soll
$ in file (f.py) finden Sie:
* Die Nachricht, die die Anwendung dazu veranlasst, zu arbeiten und nach dem Patienten zu suchen.
* Die Meldung soll die Frage des Programms beantworten, ob dies der richtige Patient ist oder nicht, der auf der Kamera erscheint.Die Informationen des Patienten werden über diese Nachricht gesendet
* Die Meldung dient nach Beendigung des Trainings dazu, die Trainingsarbeit zu stoppen
## Maximum and minimum values

* the maximum and minimum values are update automatically 
* in order to change the limit, replace the value_min and value_max with any number


For example (code line 74),

** per = np.interp(angle, (value_min, value_max), (0, 100))
** bar = np.interp(angle, (value_min, value_max), (650, 100))

change
** per = np.interp(angle, (190, 350), (0, 100))
** bar = np.interp(angle, (190 , 350), (650, 100))
