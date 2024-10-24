from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Download our Android App'

@app.route('/api/<call>')
def apicall(call):
    match call:
        case "api":
            return "hello"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)