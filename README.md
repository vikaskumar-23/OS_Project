# CPU Scheduler Visualizer

A web-based simulation tool for Operating System CPU scheduling algorithms. This project visualizes process execution using Gantt charts and calculates Average Turnaround Time and Waiting Time.

**Author:** Vikas Kumar (2303137)

## Supported Algorithms
* First Come First Serve (FCFS)
* Shortest Job First (Non-Preemptive & Preemptive)
* Round Robin (RR)
* Priority Scheduling (Non-Preemptive)

## Prerequisites
* Python 3.x
* Flask

## Setup & Installation

1.  **Install Flask**:
    ```bash
    pip install flask
    ```

2.  **Create Project Structure**:
    Create a folder for your project and set up the following structure exactly:
    ```text
    /project_folder
    │
    ├── app.py                # Paste the Python code here
    └── templates/
        └── index.html        # Paste the HTML code here
    ```

## How to Run

1.  Open your terminal or command prompt in the project folder.
2.  Run the application:
    ```bash
    python app.py
    ```
3.  Open your web browser and navigate to:
    `http://127.0.0.1:5000`

## Usage
1.  **Add Processes**: Enter Arrival Time, Burst Time, and Priority (if applicable).
2.  **Select Algorithm**: Choose the scheduling method from the dropdown.
3.  **Set Time Quantum**: Required only for Round Robin.
4.  **Simulate**: Click to generate the Gantt Chart and results table.