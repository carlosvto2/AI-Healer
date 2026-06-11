from flask import Flask, jsonify
import os

# Flask - framework with the necessary tools to build web applications and APIs
app = Flask(__name__)

DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "status": "CONNECTED"
}

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