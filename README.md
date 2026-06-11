# AI-Driven Self-Healing Infrastructure (MVP)

A hands-on DevOps/SRE laboratory demonstrating real-time log streaming, automated failure detection, and in-memory self-healing orchestration, paving the way for an autonomous AI Healer agent.

## Architecture Overview

The project is structured into independent, decoupled components to simulate a microservices environment:

```text
ai-healer/
│
├── app/                  # Target Application
│   ├── app.py            # Flask API with chaos routes & signal handlers
│   ├── Dockerfile        # Containerization recipe
│   └── requirements.txt  # API dependencies
│
├── monitor/              # The SRE Watchdog
│   ├── monitor.py        # Real-time log streamer & signal orchestrator
│   └── requirements-monitor.txt
└── README.md

The Application (app/): A containerized Flask API running inside an isolated Docker container. It includes a simulated vulnerability (POST /break) that corrupts its memory state, and a Linux SIGHUP signal handler to trigger hot-reloads.

The Watchdog (monitor/): An independent Python automation script that hooks into the local Docker daemon socket, streams standard error logs in real-time, isolates stack traces, and orchestrates recovery without service interruption.

🚀 Getting Started & Execution Flow
To run the complete Day 2 automated self-healing pipeline, follow these steps in your terminal:

1. Provision the Target Application
Build the immutable Docker image and run the containerized API:

PowerShell
# Navigate to root, build and spin up the container
docker rm -f mi-app-api 2>$null
docker build -t ai-healer-app ./app
docker run -d -p 5000:5000 --name mi-app-api ai-healer-app
2. Launch the Watchdog Monitor
Initialize a clean Python 3 environment, install dependencies, and start real-time infrastructure surveillance:

PowerShell
cd monitor
python -m pip install -r requirements-monitor.txt
python monitor.py
Note: The monitor dynamically fetches the current timestamp to ignore past historical logs, focusing strictly on live runtime events.

3. Simulate Chaos & Verify Self-Healing
Open a secondary terminal and trigger the failure lifecycle using PowerShell:

PowerShell
# Step A: Corrupt the application configuration memory
Invoke-RestMethod -Method Post -Uri http://localhost:5000/break

# Step B: Trigger the bug by hitting the home route (Causes AttributeError)
Invoke-RestMethod -Uri http://localhost:5000/
📈 Expected Outcome
The application will experience a critical unhandled exception.

The monitor.py daemon instantly catches the Traceback lines from the Docker log stream.

The monitor isolates the payload and executes container.kill(signal="SIGHUP").

The Flask app intercepts the signal, fires initialize_app(), and heals its memory state in milliseconds.

Hit http://localhost:5000/ again—service is restored automatically with a 200 OK.