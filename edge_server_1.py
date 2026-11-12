from flask import Flask
import time
import random

app = Flask(__name__)

@app.route('/file')
def serve():
    delay = random.uniform(0.1, 2.5)  # dynamic load
    time.sleep(delay)
    return "Served by Server 1"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(port=5001, threaded=True)