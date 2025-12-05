# CPU & RTOS Scheduler Visualizer 📊

This project is a web-based simulation tool built with **Flask** (Python) and **JavaScript** for visualizing various CPU and Real-Time Operating System (RTOS) scheduling algorithms.

## ✨ Features

* **Algorithms Implemented (7):**
    * **CPU:** FCFS, Non-Preemptive SJF (NSJF), Preemptive SJF (PSJF), Round Robin (RR), Non-Preemptive Priority (PR).
    * **RTOS:** Fixed Priority (RM), Earliest Deadline First (EDF).
* **Input Parameters:** Process ID, Arrival Time (AT/Offset), Burst Time (BT/Capacity), Priority (for PR/RM), Period (T) (for RM/EDF).
* **Core Output Metrics:** Dynamic **Gantt Chart** visualization, Completion Time (FT), Turnaround Time (TAT), Waiting Time (WT), and Average Metrics.
* **RTOS Specific:** Calculates the **Hyperperiod (LCM)** for the Gantt chart length and explicitly reports **Deadline Misses** (for RM/EDF).

## 🚀 Setup and Run

1.  **Dependencies:** Ensure you have Python and Flask installed.
    ```bash
    pip install Flask
    ```
2.  **Run:** Execute the main Python application (`app.py`).
    ```bash
    python app.py
    ```
3.  **Access:** Open your web browser and navigate to the local server address.
    ```
    [http://127.0.0.1:5000/]
    ```

## 🛠 Project Structure

| File | Description |
| :--- | :--- |
| `app.py` | Main Flask backend. Contains API endpoints and core scheduling logic (solvers for all 7 algorithms). |
| `index.html` | Frontend interface (HTML, CSS/Bootstrap, JavaScript). Handles process input, simulation API calls, and renders the results and the interactive Gantt chart. |
