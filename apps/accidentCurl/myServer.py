from flask import Flask , jsonify , request
app = Flask(__name__)

@app.route("/" , methods = ['POST'])
def hello():
    data = request.get_json()
    print(data)
    counter = data['counter']
    print(counter)
    return "Hello"
