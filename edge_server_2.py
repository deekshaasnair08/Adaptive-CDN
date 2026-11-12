from flask import Flask
import time
import random

app = Flask(__name__)

@app.route('/file')
def serve():
    delay = random.uniform(0.1, 2.5)  # same range
    time.sleep(delay)
    return "Served by Server 2"

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(port=5002, threaded=True)