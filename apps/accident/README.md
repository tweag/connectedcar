This application log the data concerning a drastic acceleration to our server. Here are some steps to follow to run this application

<!-- ### Server Side
We wrote our server application side using [flask](http://flask.pocoo.org/). Make sure to follow these steps in your terminal to run the server:
```
$ export FLASK_APP=myServer.py
$ python -m flask run --host=0.0.0.0
```
We recall that the local IP `0.0.0.0` is accessible from outside devices. -->

### MangOH application
First make sure that the sensors file are added to your MangOH device:
1. Enter to your device by entering in your terminal
```
$ ssh root@192.168.2.2
```
2. Inside the device terminal, do
```
# app status
```
and check if you have the application `redSensorToCloud`. If you don't, go outside of the device and do
```
$ update ~/mangOH/build/update_files/red/mangOH.wp76xx.update 192.168.2.2
```

Then go to the main directory (where the file `accident.adef` exists) install our application:
```
$ cfglegato
$ mkapp -i $LEGATO_ROOT/interfaces/modemServices -t wp76xx accident.adef
$ app install accident.wp76xx.update 192.168.2.2
```
