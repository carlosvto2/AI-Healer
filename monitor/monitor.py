import docker
import sys
import time

# Target container name defined during Day 1 runtime
CONTAINER_NAME = "mi-app-api"

def connect_to_docker(container_name: str):
    """Establishes connection to local Docker and returns the target container."""
    try:
        # Initialize the Docker client utilizing local environment variables/sockets
        client = docker.from_env()
        # Target the specific API container
        container = client.containers.get(CONTAINER_NAME)
        print(f"[*] Successfully connected to Docker. Monitoring container: {CONTAINER_NAME}")
        return container
        
    except docker.errors.NotFound:
        print("[ERROR] Container '{CONTAINER_NAME}' not found. Ensure the container is running.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[*] Monitoring intercepted by user. Exiting cleanly...")
        sys.exit(0)


def trigger_self_healing(container):
    """Executes the self recovery by sending a SIGHUP signal to the container."""
    print("[MONITOR] Triggering Self-Healing...")
    try:
        # Send signal to the container to auto-fix the problem
        container.kill(signal="SIGHUP")
        print("[HEALER] SIGHUP signal sent to container!")
    except Exception as e:
        print(f"[HEALER ERROR] Failed to send healing signal: {e}")


def process_crash_report(traceback_lines, container):
    """Handles the crash log block"""
    print("[MONITOR] Critical exception detected inside the container")
    
    # Trigger the recovery mechanism
    trigger_self_healing(container)


def start_monitoring():
    """Main loop that streams container logs and detects runtime failures."""
    container = connect_to_docker(CONTAINER_NAME)

    current_timestamp = int(time.time())

    # Ignore the old logs
    log_stream = container.logs(
        stream=True, 
        follow=True, 
        stdout=True, 
        stderr=True, 
        since=current_timestamp
    )

    in_traceback = False
    traceback_buffer = []

    for line in log_stream:
        log_line = line.decode('utf-8').strip()
        
        # --- FAILURE DETECTION LOGIC ---
        # Standard Python unhandled exceptions always begin with this specific string
        if "Traceback (most recent call last):" in log_line:
            in_traceback = True
            traceback_buffer = []  # Flush buffer
        
        # Aggregate lines from the log
        if in_traceback:
            traceback_buffer.append(log_line)
            
            # --- BREAK CONDITION ---
            # Determine the end of the traceback block by catching the error root cause.
            if "TypeError:" in log_line or "AttributeError:" in log_line:
                in_traceback = False
                process_crash_report(traceback_buffer, container)

                

if __name__ == "__main__":
    start_monitoring()