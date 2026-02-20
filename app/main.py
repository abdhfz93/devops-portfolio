from flask import Flask, jsonify
import time
import os
from prometheus_client import start_http_server, Summary, Counter, generate_latest

app = Flask(__name__)

# Define some prometheus metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Summary('app_request_latency_seconds', 'Request latency')

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=200).inc()
    return jsonify({
        "status": "UP",
        "message": "Welcome to the DevOps Portfolio API!",
        "version": "1.0.0",
        "hostname": os.uname().nodename if hasattr(os, 'uname') else "unknown"
    })

@app.route('/health')
def health():
    return jsonify({"status": "Healthy"}), 200

@app.route('/heavy')
def heavy():
    # Simulate a heavy request for testing HPA
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/heavy', http_status=200).inc()
    
    # Simple CPU intensive task
    sum(i*i for i in range(1000000))
    
    latency = time.time() - start_time
    REQUEST_LATENCY.observe(latency)
    return jsonify({"status": "Done", "latency": latency})

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    # Metrics are exposed on port 8000 by default in this script, or we can use the /metrics endpoint
    app.run(host='0.0.0.0', port=5000)
