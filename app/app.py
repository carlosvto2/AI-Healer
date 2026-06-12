from flask import Flask, jsonify
import os
import signal

# Flask - framework with the necessary tools to build web applications and APIs
app = Flask(__name__)

@app.route('/fix', methods=['POST'])
def initialize_app():
    """Initializes or resets the application configuration to a healthy state."""
    global DATABASE_CONFIG
    DATABASE_CONFIG = {
        "host": "localhost",
        "port": 5432,
        "status": "CONNECTED"
    }
    print("[APP] Application configuration initialized successfully.")

# Run initialization when the app starts
initialize_app()

def handle_reload_signal(signum, frame):
    """Signal handler to reload configuration on demand without restarting the process"""
    print("[SIGNAL] SIGHUP received! Reloading configuration...")
    initialize_app()

# Execute the function 'handle_reload_signal' when receiven a signal SIGHUP
signal.signal(signal.SIGHUP, handle_reload_signal)

@app.route('/', methods=['GET'])
def home():
    status = DATABASE_CONFIG["status"]
    return jsonify({
        "status": 200,
        "message": f"App Works!!!. Database: {status}"
    }), 200

# Call to break the app
@app.route('/break', methods=['POST'])
def break_app():
    # reference the DATABASE_CONFIG variable previously created
    global DATABASE_CONFIG
    # Sabotage the configuration to break the app
    DATABASE_CONFIG = None 
    return jsonify({
        "status": "SABOTAGED",
        "message": "App is now broken. Try to access '/' to see the mess."
    }), 200

if __name__ == '__main__':
    # Listen on all network interfaces (required for Docker port mapping)
    app.run(host='0.0.0.0', port=5000)