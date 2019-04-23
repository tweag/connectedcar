from flask import Flask, abort, request
import json

app = Flask(__name__)


@app.route('/mangOH', methods=['POST'])
def mangOH():
    if not request.json:
        abort(400)
    print (request.json)
    return json.dumps(request.json)


if __name__ == '__main__':
    app.run(debug=True)
