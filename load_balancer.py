from flask import Flask, jsonify
from flask_cors import CORS
import requests
import time
import random

app = Flask(__name__)
CORS(app)

# 🔹 SERVERS
servers = {
    "Server 1": "http://localhost:5001",
    "Server 2": "http://localhost:5002",
    "Server 3": "http://localhost:5003"
}

# 🔹 HISTORY (for prediction)
history = {
    "Server 1": [],
    "Server 2": [],
    "Server 3": []
}

# 🔹 USAGE TRACKING (for fairness)
usage_count = {
    "Server 1": 0,
    "Server 2": 0,
    "Server 3": 0
}

# 🔮 PREDICTION FUNCTION
def predict(times):
    if len(times) < 3:
        return sum(times) / len(times) if times else 0
    return 0.6 * times[-1] + 0.3 * times[-2] + 0.1 * times[-3]

# 📈 TREND PENALTY
def trend_penalty(times):
    if len(times) >= 3 and times[-1] > times[-2] > times[-3]:
        return 50
    return 0

@app.route('/request')
def route_request():
    best_server = None
    best_score = float('inf')
    best_time = 0

    # 🔀 RANDOMIZE ORDER (avoid bias)
    server_list = list(servers.items())
    random.shuffle(server_list)

    for name, url in server_list:
        try:
            start = time.time()
            res = requests.get(f"{url}/file", timeout=2)
            response_time = int((time.time() - start) * 1000)

            # 🔄 UPDATE HISTORY
            history[name].append(response_time)
            if len(history[name]) > 5:
                history[name].pop(0)

            predicted = predict(history[name])
            penalty = trend_penalty(history[name])

            # 🧠 FINAL BALANCED SCORE
            score = (
                0.6 * response_time +
                0.2 * predicted +
                penalty +
                (usage_count[name] * 30) +   # fairness penalty
                random.randint(0, 10)        # small randomness
            )

            print(f"{name} → RT: {response_time}, Pred: {predicted}, Usage: {usage_count[name]}, Score: {score}")

            if score < best_score:
                best_score = score
                best_server = name
                best_time = response_time

        except:
            continue

    if not best_server:
        return jsonify({"error": "All servers down"}), 500

    # ✅ UPDATE USAGE AFTER SELECTION
    usage_count[best_server] += 1

    return jsonify({
        "server_selected": best_server,
        "response_time": best_time,
        "cpu_usage": 50,
        "prediction_score": round(best_score, 4)
    })

if __name__ == '__main__':
    app.run(port=5000, threaded=True)