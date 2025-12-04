# Vikas Kumar 2303137
# OS Project

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# CPU Scheduling Algorithms

def solve_fcfs(processes):
    # Sort by Arrival Time
    processes.sort(key=lambda x: x['at'])
    
    current_time = 0
    gantt_chart = []
    
    for p in processes:
        # Handle CPU idle time
        if current_time < p['at']:
            current_time = p['at']
            
        start_time = current_time
        completion_time = start_time + p['bt']
        
        p['ft'] = completion_time
        p['tat'] = p['ft'] - p['at']
        p['wt'] = p['tat'] - p['bt']
        
        gantt_chart.append({
            'id': p['id'],
            'start': start_time,
            'end': completion_time,
            'color': p['color']
        })
        
        current_time = completion_time
        
    return processes, gantt_chart

def solve_sjf_non_preemptive(processes):
    n = len(processes)
    completed = 0
    current_time = 0
    gantt_chart = []
    # Add a 'completed' flag to processes
    for p in processes:
        p['done'] = False
        
    # Sort initially by arrival time to handle the first process check easily
    processes.sort(key=lambda x: x['at'])
    
    while completed < n:
        # Filter processes that have arrived and are not done
        available = [p for p in processes if p['at'] <= current_time and not p['done']]
        
        if not available:
            # If no process is available, jump to the next arrival time
            next_arrival = min([p['at'] for p in processes if not p['done']])
            current_time = next_arrival
            continue
            
        # Select process with minimum Burst Time
        shortest = min(available, key=lambda x: x['bt'])
        
        start_time = current_time
        completion_time = start_time + shortest['bt']
        
        shortest['ft'] = completion_time
        shortest['tat'] = shortest['ft'] - shortest['at']
        shortest['wt'] = shortest['tat'] - shortest['bt']
        shortest['done'] = True
        
        gantt_chart.append({
            'id': shortest['id'],
            'start': start_time,
            'end': completion_time,
            'color': shortest['color']
        })
        
        completed += 1
        current_time = completion_time
        
    return processes, gantt_chart

def solve_sjf_preemptive(processes):
    # Preemptive SJF (Shortest Remaining Time First)
    n = len(processes)
    # Store original burst time to calculate WT later because 'bt' will be decremented
    for p in processes:
        p['original_bt'] = p['bt']
        p['remaining_bt'] = p['bt']
        
    current_time = 0
    completed = 0
    gantt_chart = []
    
    # Run simulation time step by time step (or event based)
    # To keep visualization simple, we'll check status every unit of time
    # Optimization: To prevent massive loops, we can jump to next event, 
    # but unit stepping is robust for Preemptive logic.
    
    # Determine the total time roughly to prevent infinite loops in bad input
    total_burst = sum(p['bt'] for p in processes)
    # Max time roughly starts + burst
    
    last_process_id = -1
    
    while completed < n:
        # Get available processes
        available = [p for p in processes if p['at'] <= current_time and p['remaining_bt'] > 0]
        
        if not available:
            current_time += 1
            continue
            
        # Pick shortest remaining time
        shortest = min(available, key=lambda x: x['remaining_bt'])
        
        # Gantt Chart Logic: Aggregate consecutive blocks
        if shortest['id'] != last_process_id:
            # New block
            gantt_chart.append({
                'id': shortest['id'],
                'start': current_time,
                'end': current_time + 1,
                'color': shortest['color']
            })
            last_process_id = shortest['id']
        else:
            # Extend last block
            gantt_chart[-1]['end'] += 1
            
        shortest['remaining_bt'] -= 1
        current_time += 1
        
        if shortest['remaining_bt'] == 0:
            completed += 1
            shortest['ft'] = current_time
            shortest['tat'] = shortest['ft'] - shortest['at']
            shortest['wt'] = shortest['tat'] - shortest['original_bt']
            
    return processes, gantt_chart

def solve_round_robin(processes, quantum):
    n = len(processes)
    # Sort by arrival time to queue them correctly initially
    processes.sort(key=lambda x: x['at'])
    
    for p in processes:
        p['remaining_bt'] = p['bt']
        p['original_bt'] = p['bt']
    
    current_time = 0
    queue = []
    gantt_chart = []
    
    # Initialize queue with first process(es)
    # We need to keep track of indices to modify the actual objects
    
    # Push initial processes arriving at time 0 (or min time)
    if n > 0:
        min_at = processes[0]['at']
        current_time = min_at
        
        # Add all processes that arrive at the very start
        i = 0
        while i < n and processes[i]['at'] <= current_time:
            queue.append(i)
            i += 1
    
    completed = 0
    # Track which processes have been added to queue to avoid duplicates
    # 'i' tracks the index of the next process to arrive from the sorted list
    
    while completed < n:
        if not queue:
            # If queue is empty but processes remain, jump to next arrival
            if i < n:
                current_time = processes[i]['at']
                while i < n and processes[i]['at'] <= current_time:
                    queue.append(i)
                    i += 1
            else:
                # Should not happen if logic is correct
                break
                
        idx = queue.pop(0)
        p = processes[idx]
        
        # Execute for quantum or remaining burst
        exec_time = min(quantum, p['remaining_bt'])
        
        gantt_chart.append({
            'id': p['id'],
            'start': current_time,
            'end': current_time + exec_time,
            'color': p['color']
        })
        
        p['remaining_bt'] -= exec_time
        current_time += exec_time
        
        # Check for new arrivals during this execution
        while i < n and processes[i]['at'] <= current_time:
            queue.append(i)
            i += 1
            
        # If process not finished, re-queue
        if p['remaining_bt'] > 0:
            queue.append(idx)
        else:
            completed += 1
            p['ft'] = current_time
            p['tat'] = p['ft'] - p['at']
            p['wt'] = p['tat'] - p['original_bt']
            
    return processes, gantt_chart

def solve_priority_non_preemptive(processes):
    # Higher number = Higher priority (Common convention, can be flipped)
    # Assuming standard non-preemptive priority with arrival time consideration
    
    n = len(processes)
    completed = 0
    current_time = 0
    gantt_chart = []
    for p in processes:
        p['done'] = False
        
    processes.sort(key=lambda x: x['at'])
    
    while completed < n:
        available = [p for p in processes if p['at'] <= current_time and not p['done']]
        
        if not available:
            next_arrival = min([p['at'] for p in processes if not p['done']])
            current_time = next_arrival
            continue
            
        # Select process with max Priority value (Highest Priority)
        # Breaking ties with Arrival Time
        highest_priority = max(available, key=lambda x: x['pr'])
        
        start_time = current_time
        completion_time = start_time + highest_priority['bt']
        
        highest_priority['ft'] = completion_time
        highest_priority['tat'] = highest_priority['ft'] - highest_priority['at']
        highest_priority['wt'] = highest_priority['tat'] - highest_priority['bt']
        highest_priority['done'] = True
        
        gantt_chart.append({
            'id': highest_priority['id'],
            'start': start_time,
            'end': completion_time,
            'color': highest_priority['color']
        })
        
        completed += 1
        current_time = completion_time
        
    return processes, gantt_chart



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    processes = data.get('processes')
    algorithm = data.get('algorithm')
    time_slice = int(data.get('time_slice', 2))
    
    # Convert inputs to integers where needed
    for p in processes:
        p['id'] = int(p['id'])
        p['at'] = int(p['at'])
        p['bt'] = int(p['bt'])
        p['pr'] = int(p['pr'])
        
    result_processes = []
    gantt_chart = []
    
    if algorithm == 'FCFS':
        result_processes, gantt_chart = solve_fcfs(processes)
    elif algorithm == 'NSJF':
        result_processes, gantt_chart = solve_sjf_non_preemptive(processes)
    elif algorithm == 'PSJF':
        result_processes, gantt_chart = solve_sjf_preemptive(processes)
    elif algorithm == 'RR':
        result_processes, gantt_chart = solve_round_robin(processes, time_slice)
    elif algorithm == 'PR':
        result_processes, gantt_chart = solve_priority_non_preemptive(processes)
        
    # Calculate Averages
    if result_processes:
        avg_tat = sum(p['tat'] for p in result_processes) / len(result_processes)
        avg_wt = sum(p['wt'] for p in result_processes) / len(result_processes)
    else:
        avg_tat = 0
        avg_wt = 0
        
    return jsonify({
        'processes': result_processes,
        'gantt_chart': gantt_chart,
        'avg_tat': round(avg_tat, 2),
        'avg_wt': round(avg_wt, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)