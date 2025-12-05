# Vikas Kumar 2303137
# OS Project

from flask import Flask, render_template, request, jsonify
import math
from functools import reduce

app = Flask(__name__)

def get_lcm(numbers):
    if not numbers:
        return 0
    return reduce(lambda x, y: (x * y) // math.gcd(x, y), numbers)

# Standard Scheduling Algorithms

def solve_fcfs(processes):
    processes.sort(key=lambda x: x['at'])
    current_time = 0
    gantt_chart = []
    for p in processes:
        if current_time < p['at']:
            current_time = p['at']
        start_time = current_time
        completion_time = start_time + p['bt']
        p['ft'] = completion_time
        p['tat'] = p['ft'] - p['at']
        p['wt'] = p['tat'] - p['bt']
        gantt_chart.append({'id': p['id'], 'start': start_time, 'end': completion_time, 'color': p['color']})
        current_time = completion_time
    return processes, gantt_chart, []

def solve_sjf_non_preemptive(processes):
    n = len(processes)
    completed = 0
    current_time = 0
    gantt_chart = []
    for p in processes: p['done'] = False
    processes.sort(key=lambda x: x['at'])
    
    while completed < n:
        available = [p for p in processes if p['at'] <= current_time and not p['done']]
        if not available:
            next_arrival = min([p['at'] for p in processes if not p['done']])
            current_time = next_arrival
            continue
        shortest = min(available, key=lambda x: x['bt'])
        start_time = current_time
        completion_time = start_time + shortest['bt']
        shortest['ft'] = completion_time
        shortest['tat'] = shortest['ft'] - shortest['at']
        shortest['wt'] = shortest['tat'] - shortest['bt']
        shortest['done'] = True
        gantt_chart.append({'id': shortest['id'], 'start': start_time, 'end': completion_time, 'color': shortest['color']})
        completed += 1
        current_time = completion_time
    return processes, gantt_chart, []

def solve_sjf_preemptive(processes):
    n = len(processes)
    for p in processes:
        p['original_bt'] = p['bt']
        p['remaining_bt'] = p['bt']
    current_time = 0
    completed = 0
    gantt_chart = []
    last_process_id = -1
    
    while completed < n:
        available = [p for p in processes if p['at'] <= current_time and p['remaining_bt'] > 0]
        if not available:
            current_time += 1
            continue
        shortest = min(available, key=lambda x: x['remaining_bt'])
        if shortest['id'] != last_process_id:
            gantt_chart.append({'id': shortest['id'], 'start': current_time, 'end': current_time + 1, 'color': shortest['color']})
            last_process_id = shortest['id']
        else:
            gantt_chart[-1]['end'] += 1
        shortest['remaining_bt'] -= 1
        current_time += 1
        if shortest['remaining_bt'] == 0:
            completed += 1
            shortest['ft'] = current_time
            shortest['tat'] = shortest['ft'] - shortest['at']
            shortest['wt'] = shortest['tat'] - shortest['original_bt']
    return processes, gantt_chart, []

def solve_round_robin(processes, quantum):
    n = len(processes)
    processes.sort(key=lambda x: x['at'])
    for p in processes:
        p['remaining_bt'] = p['bt']
        p['original_bt'] = p['bt']
    current_time = 0
    queue = []
    gantt_chart = []
    if n > 0:
        current_time = processes[0]['at']
    i = 0
    while i < n and processes[i]['at'] <= current_time:
        queue.append(i)
        i += 1
    completed = 0
    while completed < n:
        if not queue:
            if i < n:
                current_time = processes[i]['at']
                while i < n and processes[i]['at'] <= current_time:
                    queue.append(i)
                    i += 1
            else: break
        idx = queue.pop(0)
        p = processes[idx]
        exec_time = min(quantum, p['remaining_bt'])
        gantt_chart.append({'id': p['id'], 'start': current_time, 'end': current_time + exec_time, 'color': p['color']})
        p['remaining_bt'] -= exec_time
        current_time += exec_time
        while i < n and processes[i]['at'] <= current_time:
            queue.append(i)
            i += 1
        if p['remaining_bt'] > 0:
            queue.append(idx)
        else:
            completed += 1
            p['ft'] = current_time
            p['tat'] = p['ft'] - p['at']
            p['wt'] = p['tat'] - p['original_bt']
    return processes, gantt_chart, []

def solve_priority_non_preemptive(processes):
    n = len(processes)
    completed = 0
    current_time = 0
    gantt_chart = []
    for p in processes: p['done'] = False
    processes.sort(key=lambda x: x['at'])
    while completed < n:
        available = [p for p in processes if p['at'] <= current_time and not p['done']]
        if not available:
            next_arrival = min([p['at'] for p in processes if not p['done']])
            current_time = next_arrival
            continue
        highest_priority = max(available, key=lambda x: x['pr'])
        start_time = current_time
        completion_time = start_time + highest_priority['bt']
        highest_priority['ft'] = completion_time
        highest_priority['tat'] = highest_priority['ft'] - highest_priority['at']
        highest_priority['wt'] = highest_priority['tat'] - highest_priority['bt']
        highest_priority['done'] = True
        gantt_chart.append({'id': highest_priority['id'], 'start': start_time, 'end': completion_time, 'color': highest_priority['color']})
        completed += 1
        current_time = completion_time
    return processes, gantt_chart, []

# RTOS Algorithms (RM & EDF)

def solve_rtos(processes, algo_type):
    # 1. Calculate Hyperperiod (LCM of all periods)
    periods = [p['period'] for p in processes]
    hyperperiod = get_lcm(periods)

    current_time = 0
    gantt_chart = []
    deadline_misses = []
    
    # Active jobs queue
    ready_queue = []
    
    last_process_id = -1
    
    while current_time < hyperperiod:
        
        # 1. Release new jobs at this time tick
        for i, p in enumerate(processes):
            # Check if a new period starts here (arrival time + k*period)
            if current_time >= p['at'] and (current_time - p['at']) % p['period'] == 0:
                # Add new job
                absolute_deadline = current_time + p['period']
                ready_queue.append({
                    'p_index': i,
                    'id': p['id'],
                    'deadline': absolute_deadline,
                    'rem_bt': p['bt'],
                    'color': p['color'],
                    'period': p['period'],
                    'pr': p['pr'] 
                })

        # 2. Check for Deadline Misses
        active_jobs = []
        for job in ready_queue:
            if current_time >= job['deadline']:
                deadline_misses.append({
                    'id': job['id'],
                    'time': current_time,
                    'msg': f"Process P{job['id']} missed deadline at {current_time}"
                })
                # We remove the job to visualize the failure cleanly
            else:
                active_jobs.append(job)
        ready_queue = active_jobs

        # 3. Select Job based on Algorithm
        if ready_queue:
            selected_job = None
            
            if algo_type == 'RM':
                # Fixed Priority: Higher Number = Higher Priority
                # We use max() to find the highest 'pr'. 
                # If priorities are equal, max returns the one that arrived first 
                selected_job = max(ready_queue, key=lambda x: x['pr'])
            
            elif algo_type == 'EDF':
                # Dynamic Priority: Earliest Absolute Deadline = Higher Priority
                selected_job = min(ready_queue, key=lambda x: x['deadline'])

            # Execute selected job
            if selected_job['id'] != last_process_id:
                gantt_chart.append({
                    'id': selected_job['id'], 
                    'start': current_time, 
                    'end': current_time + 1, 
                    'color': selected_job['color']
                })
                last_process_id = selected_job['id']
            else:
                gantt_chart[-1]['end'] += 1
            
            selected_job['rem_bt'] -= 1
            
            # If finished, remove from queue
            if selected_job['rem_bt'] == 0:
                ready_queue.remove(selected_job)
                last_process_id = -1 
        else:
            # CPU Idle
            if last_process_id != 'IDLE':
                gantt_chart.append({'id': 'IDLE', 'start': current_time, 'end': current_time + 1, 'color': '#eeeeee'})
                last_process_id = 'IDLE'
            else:
                gantt_chart[-1]['end'] += 1
                
        current_time += 1

    return processes, gantt_chart, deadline_misses

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    processes = data.get('processes')
    algorithm = data.get('algorithm')
    time_slice = int(data.get('time_slice', 2))
    
    # Convert inputs
    for p in processes:
        p['id'] = int(p['id'])
        p['at'] = int(p['at'])
        p['bt'] = int(p['bt'])
        p['pr'] = int(p['pr'])
        p['period'] = int(p.get('period', 0)) # Default 0 if not present
        
    result_processes = []
    gantt_chart = []
    deadline_misses = []
    
    if algorithm == 'FCFS':
        result_processes, gantt_chart, _ = solve_fcfs(processes)
    elif algorithm == 'NSJF':
        result_processes, gantt_chart, _ = solve_sjf_non_preemptive(processes)
    elif algorithm == 'PSJF':
        result_processes, gantt_chart, _ = solve_sjf_preemptive(processes)
    elif algorithm == 'RR':
        result_processes, gantt_chart, _ = solve_round_robin(processes, time_slice)
    elif algorithm == 'PR':
        result_processes, gantt_chart, _ = solve_priority_non_preemptive(processes)
    elif algorithm in ['RM', 'EDF']:
        result_processes, gantt_chart, deadline_misses = solve_rtos(processes, algorithm)

    # Stats Calculation
    # Note: For RTOS, these stats are placeholders based on the first job or kept 0
    # The visualization is the key output for RTOS.
    avg_tat = 0
    avg_wt = 0
    if algorithm not in ['RM', 'EDF'] and result_processes:
        avg_tat = sum(p['tat'] for p in result_processes) / len(result_processes)
        avg_wt = sum(p['wt'] for p in result_processes) / len(result_processes)
        
    return jsonify({
        'processes': result_processes,
        'gantt_chart': gantt_chart,
        'deadline_misses': deadline_misses,
        'avg_tat': round(avg_tat, 2),
        'avg_wt': round(avg_wt, 2),
        'is_rtos': algorithm in ['RM', 'EDF']
    })

if __name__ == '__main__':
    app.run(debug=True)
