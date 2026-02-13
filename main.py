from flask import Flask, jsonify
import time
import psutil
import os
from datetime import datetime

app = Flask(__name__)

# Global variable to track when the app started
# This runs ONCE when the container starts
APP_START_TIME = time.time()

HOME_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Run System Monitor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 60px 40px;
            text-align: center;
            max-width: 600px;
            width: 100%;
            animation: fadeIn 0.8s ease-in;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .logo {
            font-size: 80px;
            margin-bottom: 20px;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-10px);
            }
        }

        h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .subtitle {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 40px;
            line-height: 1.6;
        }

        .status-badge {
            display: inline-block;
            background: linear-gradient(135deg, #00b09b, #96c93d);
            color: white;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: 600;
            margin-bottom: 40px;
            font-size: 1em;
            box-shadow: 0 4px 15px rgba(0, 176, 155, 0.3);
        }

        .analyze-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 18px 50px;
            font-size: 1.2em;
            font-weight: 600;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            text-decoration: none;
            display: inline-block;
        }

        .analyze-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        }

        .analyze-btn:active {
            transform: translateY(-1px);
        }

        .features {
            margin-top: 50px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
        }

        .feature-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 15px;
            transition: transform 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
        }

        .feature-icon {
            font-size: 40px;
            margin-bottom: 10px;
        }

        .feature-title {
            color: #333;
            font-weight: 600;
            font-size: 0.9em;
        }

        .footer {
            margin-top: 40px;
            color: #999;
            font-size: 0.9em;
        }

        @media (max-width: 600px) {
            .container {
                padding: 40px 25px;
            }

            h1 {
                font-size: 2em;
            }

            .logo {
                font-size: 60px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">☁️</div>
        <h1>Cloud Run Monitor</h1>
        <p class="subtitle">Real-time system monitoring and health analysis for your containerized application</p>
        
        <div class="status-badge">
            ✅ System Check Complete
        </div>

        <a href="/analyze" class="analyze-btn">
            🔍 Analyze System
        </a>

        <div class="features">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">CPU Monitoring</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💾</div>
                <div class="feature-title">Memory Tracking</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⏱️</div>
                <div class="feature-title">Uptime Analysis</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Health Score</div>
            </div>
        </div>

        <div class="footer">
            Powered by Google Cloud Run | Flask Application
        </div>
    </div>
</body>
</html>
"""


def calculate_cpu_metric():
    """
    Custom CPU metric calculation
    Combines instant CPU usage with load average for a comprehensive score
    """
    try:
        # Get current CPU percentage (measured over 0.5 seconds)
        cpu_percent = psutil.cpu_percent(interval=0.5)
        
        # Get system load average (1 minute)
        load_avg = os.getloadavg()[0]
        
        # Get number of CPU cores
        cpu_count = os.cpu_count() or 1
        
        # Custom algorithm: weighted combination
        # 70% weight to instant CPU, 30% weight to load average
        load_normalized = (load_avg / cpu_count) * 100
        cpu_metric = (cpu_percent * 0.7) + (load_normalized * 0.3)
        
        # Ensure value is between 0 and 100
        return round(min(cpu_metric, 100), 2)
    except Exception as e:
        print(f"Error calculating CPU metric: {e}")
        return 0.0


def calculate_memory_metric():
    try:
        # Get memory information
        memory = psutil.virtual_memory()
        
        # Custom algorithm: emphasize actual used memory vs cached
        # memory.percent gives overall usage including cache
        memory_metric = memory.percent
        
        return round(memory_metric, 2)
    except Exception as e:
        print(f"Error calculating memory metric: {e}")
        return 0.0


def calculate_health_score(cpu, memory, uptime):
    """
    Custom health score algorithm (0-100)
    
    Scoring logic:
    - Start with 100 points
    - Deduct points based on CPU usage
    - Deduct points based on memory usage
    - Add bonus points for uptime milestones
    - Final score clamped between 0 and 100
    """
    score = 100
    
    # CPU penalties
    if cpu > 90:
        score -= 30  # Critical CPU usage
    elif cpu > 70:
        score -= 20  # High CPU usage
    elif cpu > 50:
        score -= 10  # Moderate CPU usage
    
    # Memory penalties
    if memory > 90:
        score -= 35  # Critical memory usage
    elif memory > 80:
        score -= 25  # High memory usage
    elif memory > 60:
        score -= 10  # Moderate memory usage
    
    # Uptime bonuses
    if uptime > 86400:  # More than 24 hours
        score += 15
    elif uptime > 3600:  # More than 1 hour
        score += 10
    elif uptime > 300:   # More than 5 minutes
        score += 5
    
    # Ensure score is between 0 and 100
    return min(max(score, 0), 100)


def generate_health_message(score):
    if score >= 90:
        return "Excellent - System running optimally"
    elif score >= 75:
        return "Good - System performing well"
    elif score >= 60:
        return "Fair - System stable with minor load"
    elif score >= 40:
        return "Warning - System experiencing moderate stress"
    else:
        return "Critical - System under heavy load, attention required"


@app.route('/')
def home():
    return render_templete_string(HOME_PAGE_HTML)


@app.route('/analyze')
def analyze(): 
    try:
        uptime_seconds = int(time.time() - APP_START_TIME)
        timestamp = datetime.utcnow().isoformat() + 'Z'
        cpu_metric = calculate_cpu_metric()
        memory_metric = calculate_memory_metric()
        health_score = calculate_health_score(cpu_metric, memory_metric, uptime_seconds)
        
        message = generate_health_message(health_score)
        return jsonify({
            'timestamp': timestamp,
            'uptime_seconds': uptime_seconds,
            'cpu_metric': cpu_metric,
            'memory_metric': memory_metric,
            'health_score': health_score,
            'message': message
        })
    
    except Exception as e:
        # Error handling - return error response
        return jsonify({
            'error': 'Failed to analyze system',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    # Run the Flask app
    # host='0.0.0.0' allows external connections
    # port=8080 is the default Cloud Run port
    app.run(host='0.0.0.0', port=8080)
