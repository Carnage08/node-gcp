from flask import Flask, jsonify
from datetime import datetime, timezone
import time
import os

app = Flask(__name__)

# Store start time when the app initializes
START_TIME = time.time()


@app.route('/')
def hello():
    return "Hello from Cloud Run! System check complete."


@app.route('/analyze')
def analyze():
    # Current UTC timestamp
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Uptime in seconds
    uptime_seconds = int(time.time() - START_TIME)
    
    # Simple CPU metric using /proc/loadavg (available on Linux)
    try:
        with open('/proc/loadavg', 'r') as f:
            load_avg = float(f.read().split()[0])
        cpu_metric = round(min(load_avg * 100, 100), 2)
    except:
        cpu_metric = 0.0
    
    # Simple memory metric using /proc/meminfo
    try:
        mem_total = 0
        mem_available = 0
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if 'MemTotal' in line:
                    mem_total = int(line.split()[1])
                elif 'MemAvailable' in line:
                    mem_available = int(line.split()[1])
                if mem_total and mem_available:
                    break
        memory_metric = round((1 - mem_available / mem_total) * 100, 2) if mem_total else 0.0
    except:
        memory_metric = 0.0
    
    # Health score algorithm: weighted average
    # Lower CPU and memory = better health
    health_score = round(100 - (cpu_metric * 0.4 + memory_metric * 0.6), 2)
    health_score = max(0, min(100, health_score))  # Clamp between 0-100
    
    # Message based on health score
    if health_score >= 80:
        message = "Excellent - System running optimally"
    elif health_score >= 60:
        message = "Good - System performing well"
    elif health_score >= 40:
        message = "Fair - System under moderate load"
    elif health_score >= 20:
        message = "Poor - System experiencing high load"
    else:
        message = "Critical - System resources heavily utilized"
    
    return jsonify({
        "timestamp": timestamp,
        "uptime_seconds": uptime_seconds,
        "cpu_metric": cpu_metric,
        "memory_metric": memory_metric,
        "health_score": health_score,
        "message": message
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
