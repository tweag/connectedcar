from flask import Flask , request
import json

app = Flask(__name__)

DATA_FILENAME = 'data.json'

with open(DATA_FILENAME, mode='w', encoding='utf-8') as f:
    json.dump([], f)

@app.route("/" , methods = ['POST'])
def hello():
    data = request.get_json()
    with open (DATA_FILENAME) as outfile:
        oldData = json.load(outfile)
        oldData.append(data)
    with open (DATA_FILENAME, mode = 'w') as outfile:
        outfile.write (json.dumps(oldData))
    return "Hello"
