from flask import Flask , request
import json

app = Flask(__name__)

@app.route("/" , methods = ['POST'])
def hello():
    data = request.get_json()
    print(data)
    # with open ('data.txt' , 'a+') as outfile:
    #     json.dump(data , outfile)
    return "Hello"
