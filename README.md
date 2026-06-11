# AI-Healer: Automated Infrastructure Self-Healing Engine (AIOps)

An experimental SRE/DevOps project designed to detect infrastructure failures in real-time, diagnose root causes using Local/Cloud AI Agents, and automatically orchestrate fixes through CI/CD pipelines.

## 📅 Project Status: Day 1 - Test Laboratory

Today I successfully built the sandbox environment that simulates a production application breakdown.

### Tech Stack Used Today:
* **Python (Flask):** Created the core API with a simulated state and a `/break` endpoint to trigger synthetic infrastructure failures.
* **Docker:** Packaged the application into a lightweight, containerized environment optimizing layer caching for dependencies.
* **PowerShell / CLI:** Orchestrated container lifecycles and manual failure injection.

### Current Architecture:
1. The app runs smoothly inside a Docker container (`host 0.0.0.0`).
2. A simulated configuration corruption is injected via a `POST` request to `/break`.
3. The app starts throwing `500 Internal Server Error` exceptions, generating crash tracebacks inside Docker logs.