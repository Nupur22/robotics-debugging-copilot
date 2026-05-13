import json
import random
from datetime import datetime
import os

# Simulating errors 
FAILURES = [
    {"node": "/controller_server", "level": "ERROR", "msg": "Failed to make progress", "cause": "Robot is stuck or oscillating near an obstacle."},
    {"node": "/bt_navigator", "level": "WARN", "msg": "Navigation goal rejected", "cause": "The goal coordinates are outside the known map bounds."},
    {"node": "/turtlebot3_gazebo", "level": "FATAL", "msg": "Lidar plugin not responding", "cause": "The sensor simulation crashed or the topic /scan is empty."},
    {"node": "/global_costmap", "level": "ERROR", "msg": "Transform timeout: map to base_link", "cause": "The AMCL node has lost localization or the TF tree is broken."},
]

def generate_logs():
    # Make sure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    filename = "data/synthetic_logs.jsonl"
    with open(filename, 'w') as f:
        for _ in range(50):
            failure = random.choice(FAILURES)
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "node": failure["node"],
                "level": failure["level"],
                "message": failure["msg"],
                "metadata": {"root_cause": failure["cause"]}
            }
            f.write(json.dumps(log_entry) + '\n')
    print(f"Success! Generated 50 failure logs in: {os.path.abspath(filename)}")

if __name__ == "__main__":
    generate_logs()
