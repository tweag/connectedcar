To run this application follow these steps:

1. Open a terminal and run `$ ganache-cli`.
2. Open a second terminal and run
```
$ export FLASK_DEBUG=1
$ export FLASK_APP="app.py"
$ python -m flask run --host=0.0.0.0
```
3. Open a web browser (e.g. Chrome) on port http://localhost:5000.

The smart contract and the flask code is inspired from [here](https://github.com/adamyala/Your_First_Decentralized_Application_Python).
