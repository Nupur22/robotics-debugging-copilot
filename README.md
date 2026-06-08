# Robotics Debugging Copilot (Nav2 & Gazebo AI Diagnostic Agent)

An intelligent, real-time debugging assistant that listens to ROS 2 navigation logs, detects failures in the navigation stack (`bt_navigator`, costmaps, planners), and leverages the Gemini API to provide actionable, plain-English solutions on an interactive web dashboard.

## 🚀 System Architecture

The project bridges the gap between robotic execution layers and large language models (LLMs) using a decoupled three-tier architecture:
1. **Robotics & Simulation Layer**: Gazebo handles physical world simulation; Nav2 orchestrates costmaps and behavior trees; RViz2 allows interactive goal placement.
2. **Data Ingestion Pipeline (`log_listener.py`)**: A native ROS 2 node that hooks directly into the logging subsystem, filtering runtime anomalies and parsing message packets.
3. **AI Diagnostic & Dashboard Engine (`app.py`)**: A lightweight web interface built with Gradio that formats incoming errors, invokes Google Gemini via the developer API, and renders markdown mitigation strategies.
## Project Demo : 


https://github.com/user-attachments/assets/a9c3e359-860a-4963-9fef-3b63b0578d1a



---

## 🛠️ Prerequisites & Environment Setup

### 1. System Requirements
- **OS**: Ubuntu 22.04 LTS (Native or WSL2)
- **ROS 2 Distribution**: Humble
- **Simulation Packages**: TurtleBot3 Gazebo, Navigation2 (`nav2_bringup`)
- **Python**: v3.10+

### 2. Python Dependency Installation
Install the necessary interface and generative modeling libraries:
```bash
pip install gradio google-generativeai onnxruntime
