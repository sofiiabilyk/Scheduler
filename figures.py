import time
import random
import matplotlib.pyplot as plt
import numpy as np
from TaskClass import Task
from TaskSchedulerClass import TaskScheduler
from ImprovedGreedy_Scheduler import ImprovedGreedy_Scheduler
from DP_Scheduling import DP_Scheduler

# Configuration
STARTING_TIME = "06:00"
END_TIME = "24:00"
MAX_AVAILABLE_MINUTES = 18 * 60  # 18 hours = 1080 minutes (from 6:00 to 24:00)
MIN_TASK_DURATION = 1
MAX_TASK_DURATION = 60
CATEGORIES = ["Routine", "Family", "Growth", "Friends", "Hobby", "Other"]

def time_to_minutes(time_str):
    """Convert time string 'hh:mm' to minutes since midnight"""
    if time_str == "25:25":
        return None
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])

def minutes_to_time(minutes):
    """Convert minutes since midnight to 'hh:mm' format"""
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"

def generate_tasks(num_tasks, scheduled_percentage=0, dependency_percentage=0):
    """
    Generate a list of tasks with specified characteristics
    
    Parameters:
    -----------
    num_tasks: int
        Number of tasks to generate
    scheduled_percentage: float
        Percentage of tasks that should have scheduled times (0-1)
    dependency_percentage: float
        Percentage of tasks that should have dependencies (0-1)
    
    Returns:
    --------
    list: List of Task objects
    """
    tasks = []
    task_ids = list(range(num_tasks))
    
    # Calculate how many tasks should be scheduled and have dependencies
    num_scheduled = int(num_tasks * scheduled_percentage)
    num_with_dependencies = int(num_tasks * dependency_percentage)
    
    # Select which tasks will be scheduled
    scheduled_indices = set(random.sample(range(num_tasks), min(num_scheduled, num_tasks))) if num_scheduled > 0 else set()
    # Select which tasks will have dependencies
    dependency_indices = set(random.sample(range(num_tasks), min(num_with_dependencies, num_tasks))) if num_with_dependencies > 0 else set()
    
    # Generate scheduled times (don't worry about fitting in work period - algorithms handle that)
    start_min = time_to_minutes(STARTING_TIME)
    end_min = time_to_minutes(END_TIME)
    time_range = end_min - start_min
    
    # Create a list of scheduled times to distribute
    scheduled_times = []
    if num_scheduled > 0:
        # Distribute scheduled times throughout a wider range (can extend beyond work period)
        # Use a wider time range to allow more flexibility
        extended_range = time_range * 2  # Allow times beyond normal work period
        for i in range(num_scheduled):
            time_offset = (i * extended_range) // max(1, num_scheduled)
            scheduled_times.append(start_min + time_offset)
        random.shuffle(scheduled_times)
    
    scheduled_time_index = 0
    
    for i in range(num_tasks):
        task_id = task_ids[i]
        description = f"Task {task_id}"
        
        # Generate duration (at least 1 minute, no upper constraint)
        duration = random.randint(MIN_TASK_DURATION, MAX_TASK_DURATION)
        
        # Determine if task should be scheduled
        is_scheduled = i in scheduled_indices
        scheduled_time = "25:25"
        
        if is_scheduled and scheduled_time_index < len(scheduled_times):
            # Assign a scheduled time (don't check if it fits - algorithms handle that)
            time_slot = scheduled_times[scheduled_time_index]
            scheduled_time = minutes_to_time(time_slot)
            scheduled_time_index += 1
        
        # Determine dependencies - allow multiple dependencies, but avoid cycles
        dependencies = []
        if i in dependency_indices:
            # Create dependency on tasks with lower index (to avoid cycles)
            # Only depend on tasks that come before in the list
            possible_deps = [j for j in range(i)]
            if possible_deps:
                # Allow multiple dependencies (1 to up to 5, or all available if less than 5)
                max_deps = min(5, len(possible_deps))
                num_deps = random.randint(1, max_deps)
                dep_indices = random.sample(possible_deps, num_deps)
                dependencies = [task_ids[dep_idx] for dep_idx in dep_indices]
        
        category = random.choice(CATEGORIES)
        tasks.append(Task(
            id=task_id,
            description=description,
            duration=duration,
            dependencies=dependencies,
            scheduled=scheduled_time,
            category=category
        ))
    
    return tasks

def measure_execution_time(algorithm, tasks, starting_time, end_time=None):
    """
    Measure execution time of an algorithm
    
    Parameters:
    -----------
    algorithm: str
        'TaskScheduler', 'ImprovedGreedy', or 'DP'
    tasks: list
        List of Task objects
    starting_time: str
        Starting time in 'hh:mm' format
    end_time: str
        End time in 'hh:mm' format (only for DP)
    
    Returns:
    --------
    float: Execution time in seconds
    """
    # Create a deep copy of tasks to avoid modifying original
    import copy
    import sys
    from io import StringIO
    
    tasks_copy = copy.deepcopy(tasks)
    
    start_time = time.perf_counter()
    
    # Suppress print output for all algorithms
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        if algorithm == 'TaskScheduler':
            scheduler = TaskScheduler(tasks_copy)
            scheduler.run_task_scheduler(starting_time)
        elif algorithm == 'ImprovedGreedy':
            scheduler = ImprovedGreedy_Scheduler(tasks_copy)
            scheduler.run_task_scheduler(starting_time)
        elif algorithm == 'DP':
            scheduler = DP_Scheduler(tasks_copy)
            scheduler.schedule_tasks(starting_time, end_time or END_TIME)
        else:
            sys.stdout = old_stdout
            return None
    except Exception as e:
        sys.stdout = old_stdout
        # Silently handle errors - return None to skip this measurement
        return None
    finally:
        sys.stdout = old_stdout
    
    end_time_measure = time.perf_counter()
    return end_time_measure - start_time

def run_simulation(task_sizes, scheduled_percentage=0, dependency_percentage=0, num_iterations=5):
    """
    Run simulation for different task sizes
    
    Parameters:
    -----------
    task_sizes: list
        List of task counts to test
    scheduled_percentage: float
        Percentage of scheduled tasks (0-1)
    dependency_percentage: float
        Percentage of tasks with dependencies (0-1)
    num_iterations: int
        Number of iterations to average over
    
    Returns:
    --------
    dict: Dictionary with algorithm names as keys and lists of average execution times as values
    """
    results = {
        'TaskScheduler': [],
        'ImprovedGreedy': [],
        'DP': []
    }
    
    for size in task_sizes:
        print(f"Testing with {size} tasks (scheduled: {scheduled_percentage*100}%, dependencies: {dependency_percentage*100}%)...")
        
        times = {
            'TaskScheduler': [],
            'ImprovedGreedy': [],
            'DP': []
        }
        
        for iteration in range(num_iterations):
            tasks = generate_tasks(size, scheduled_percentage, dependency_percentage)
            
            for algo in ['TaskScheduler', 'ImprovedGreedy', 'DP']:
                exec_time = measure_execution_time(algo, tasks, STARTING_TIME, END_TIME)
                if exec_time is not None:
                    times[algo].append(exec_time)
        
        # Calculate averages
        for algo in results.keys():
            if times[algo]:
                avg_time = sum(times[algo]) / len(times[algo])
                results[algo].append(avg_time)
            else:
                results[algo].append(0)
    
    return results

def create_figure(task_sizes, results, title, filename):
    """
    Create and save a figure with all three algorithm curves and complexity reference lines
    
    Parameters:
    -----------
    task_sizes: list
        List of task counts
    results: dict
        Dictionary with algorithm execution times
    title: str
        Figure title
    filename: str
        Filename to save the figure
    """
    plt.figure(figsize=(12, 5))
    
    # Find the maximum and minimum values across all algorithm results (not complexity lines)
    max_time = 0
    min_time = float('inf')
    for algo in results.values():
        if algo:
            max_time = max(max_time, max(algo))
            min_time = min(min_time, min([t for t in algo if t > 0]))
    
    # If no data, use a default scale
    if max_time == 0:
        max_time = 1
    if min_time == float('inf'):
        min_time = 0.001
    
    # Calculate y-axis limits to focus on algorithm data with some padding
    # Add 10% padding above and below the data range
    y_padding = (max_time - min_time) * 0.1 if max_time > min_time else max_time * 0.1
    y_min = max(0, min_time - y_padding)
    y_max = max_time + y_padding
    
    # Convert task_sizes to numpy array for calculations
    n = np.array(task_sizes)
    
    # Calculate scaling factors so complexity lines show their growth patterns
    # Scale them so they start at similar values but grow at different rates
    # This way they don't all end at the same point
    if len(task_sizes) > 0 and max_time > 0:
        min_n = task_sizes[0]
        max_n = task_sizes[-1]
        
        # Scale each complexity so they start at a similar baseline
        # but grow at their natural rates, making them end at different points
        baseline_time = min_time if min_time > 0 else max_time * 0.1
        
        # For O(n): scale so it grows linearly
        # Make it reach about 0.3 * max_time at max_n
        c_n = (max_time * 0.3) / max_n if max_n > 0 else 0.001
        
        # For O(n log n): scale so it grows faster
        # Make it reach about 0.5 * max_time at max_n
        c_nlogn = (max_time * 0.5) / (max_n * np.log2(max_n + 1)) if max_n > 0 else 0.001
        
        # For O(n²): scale so it grows quadratically
        # Make it reach about 0.7 * max_time at max_n
        c_n2 = (max_time * 0.7) / (max_n ** 2) if max_n > 0 else 0.001
        
        # For O(n³): scale so it grows cubically
        # Make it reach about max_time at max_n (or extend beyond if needed)
        c_n3 = (max_time * 1.0) / (max_n ** 3) if max_n > 0 else 0.001
        
        # Adjust if any line would be too small at the start
        if min_n > 0:
            min_val_n = c_n * min_n
            min_val_nlogn = c_nlogn * min_n * np.log2(min_n + 1)
            min_val_n2 = c_n2 * (min_n ** 2)
            min_val_n3 = c_n3 * (min_n ** 3)
            
            # Ensure all start at a reasonable minimum
            min_allowed = baseline_time * 0.5
            if min_val_n < min_allowed and c_n > 0:
                c_n = min_allowed / min_n
            if min_val_nlogn < min_allowed and c_nlogn > 0:
                c_nlogn = min_allowed / (min_n * np.log2(min_n + 1))
            if min_val_n2 < min_allowed and c_n2 > 0:
                c_n2 = min_allowed / (min_n ** 2)
            if min_val_n3 < min_allowed and c_n3 > 0:
                c_n3 = min_allowed / (min_n ** 3)
    else:
        # Default scaling if no data
        c_n = 0.001
        c_nlogn = 0.001
        c_n2 = 0.001
        c_n3 = 0.001
    
    # Plot complexity reference lines (dotted, lighter colors)
    # These will now end at different points showing their growth patterns
    plt.plot(n, c_n * n, '--', color='gray', alpha=0.5, linewidth=1.5, label='O(n)', zorder=1)
    plt.plot(n, c_nlogn * n * np.log2(n + 1), '--', color='lightblue', alpha=0.6, linewidth=1.5, label='O(n log n)', zorder=1)
    plt.plot(n, c_n2 * n ** 2, '--', color='lightcoral', alpha=0.6, linewidth=1.5, label='O(n²)', zorder=1)
    plt.plot(n, c_n3 * n ** 3, '--', color='lightgreen', alpha=0.6, linewidth=1.5, label='O(n³)', zorder=1)
    
    # Plot each algorithm with updated legend names (on top of complexity lines)
    plt.plot(task_sizes, results['TaskScheduler'], 'o-', label='Greedy Approach Part I', linewidth=2, markersize=6, zorder=2)
    plt.plot(task_sizes, results['ImprovedGreedy'], 's-', label='Greedy Approach Part II', linewidth=2, markersize=6, zorder=2)
    plt.plot(task_sizes, results['DP'], '^-', label='DP Approach', linewidth=2, markersize=6, zorder=2)
    
    # Set y-axis limits to zoom in on algorithm data
    plt.ylim(y_min, y_max)
    
    plt.xlabel('Number of Tasks', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(fontsize=9, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save figure
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved figure: {filename}")
    plt.close()

def main():
    """Main function to run all simulations and create figures"""
    # Task sizes: points every 25 tasks, starting from 25
    # Maximum should respect available time (each task at least 1 minute)
    # But we'll cap at a reasonable number for performance
    max_tasks = min(MAX_AVAILABLE_MINUTES, 500)  # Cap at 500 tasks for reasonable runtime
    task_sizes = list(range(25, max_tasks + 1, 25))
    
    print(f"Task sizes to test: {task_sizes}")
    print(f"Maximum available time: {MAX_AVAILABLE_MINUTES} minutes")
    
    # Figure 1: Just tasks, no scheduled tasks, no dependencies
    print("\n" + "="*60)
    print("Figure 1: No scheduled tasks, no dependencies")
    print("="*60)
    results1 = run_simulation(task_sizes, scheduled_percentage=0, dependency_percentage=0, num_iterations=50)
    create_figure(task_sizes, results1, 
                  "Time Complexity: No Scheduled Tasks, No Dependencies",
                  "figure1_no_scheduled_no_dependencies.png")
    
    # Figure 2: No dependencies, 10% scheduled tasks
    print("\n" + "="*60)
    print("Figure 2: No dependencies, 10% scheduled tasks")
    print("="*60)
    results2 = run_simulation(task_sizes, scheduled_percentage=0.1, dependency_percentage=0, num_iterations=50)
    create_figure(task_sizes, results2,
                  "Time Complexity: 10% Scheduled Tasks, No Dependencies",
                  "figure2_10pct_scheduled_no_dependencies.png")
    
    # Figure 3: No dependencies, 50% scheduled tasks
    print("\n" + "="*60)
    print("Figure 3: No dependencies, 50% scheduled tasks")
    print("="*60)
    results3 = run_simulation(task_sizes, scheduled_percentage=0.5, dependency_percentage=0, num_iterations=50)
    create_figure(task_sizes, results3,
                  "Time Complexity: 50% Scheduled Tasks, No Dependencies",
                  "figure3_50pct_scheduled_no_dependencies.png")
    
    # Figure 4: No dependencies, 90% scheduled tasks
    print("\n" + "="*60)
    print("Figure 4: No dependencies, 90% scheduled tasks")
    print("="*60)
    results4 = run_simulation(task_sizes, scheduled_percentage=0.9, dependency_percentage=0, num_iterations=50)
    create_figure(task_sizes, results4,
                  "Time Complexity: 90% Scheduled Tasks, No Dependencies",
                  "figure4_90pct_scheduled_no_dependencies.png")
    
    # Figure 5: No scheduled tasks, 10% tasks with dependencies
    print("\n" + "="*60)
    print("Figure 5: No scheduled tasks, 10% tasks with dependencies")
    print("="*60)
    results5 = run_simulation(task_sizes, scheduled_percentage=0, dependency_percentage=0.1, num_iterations=50)
    create_figure(task_sizes, results5,
                  "Time Complexity: No Scheduled Tasks, 10% Tasks with Dependencies",
                  "figure5_no_scheduled_10pct_dependencies.png")
    
    # Figure 6: No scheduled tasks, 50% tasks with dependencies
    print("\n" + "="*60)
    print("Figure 6: No scheduled tasks, 50% tasks with dependencies")
    print("="*60)
    results6 = run_simulation(task_sizes, scheduled_percentage=0, dependency_percentage=0.5, num_iterations=50)
    create_figure(task_sizes, results6,
                  "Time Complexity: No Scheduled Tasks, 50% Tasks with Dependencies",
                  "figure6_no_scheduled_50pct_dependencies.png")
    
    # Figure 7: No scheduled tasks, 90% tasks with dependencies
    print("\n" + "="*60)
    print("Figure 7: No scheduled tasks, 90% tasks with dependencies")
    print("="*60)
    results7 = run_simulation(task_sizes, scheduled_percentage=0, dependency_percentage=0.9, num_iterations=50)
    create_figure(task_sizes, results7,
                  "Time Complexity: No Scheduled Tasks, 90% Tasks with Dependencies",
                  "figure7_no_scheduled_90pct_dependencies.png")
    
    # Figure 8: 50% scheduled tasks, 10% tasks with dependencies
    print("\n" + "="*60)
    print("Figure 8: 50% scheduled tasks, 10% tasks with dependencies")
    print("="*60)
    results8 = run_simulation(task_sizes, scheduled_percentage=0.5, dependency_percentage=0.1, num_iterations=50)
    create_figure(task_sizes, results8,
                  "Time Complexity: 50% Scheduled Tasks, 10% Tasks with Dependencies",
                  "figure8_50pct_scheduled_10pct_dependencies.png")
    
    # Figure 9: 50% scheduled tasks, 50% tasks with dependencies
    print("\n" + "="*60)
    print("Figure 9: 50% scheduled tasks, 50% tasks with dependencies")
    print("="*60)
    results9 = run_simulation(task_sizes, scheduled_percentage=0.5, dependency_percentage=0.5, num_iterations=50)
    create_figure(task_sizes, results9,
                  "Time Complexity: 50% Scheduled Tasks, 50% Tasks with Dependencies",
                  "figure9_50pct_scheduled_50pct_dependencies.png")
    
    # Figure 10: 50% scheduled tasks, 90% tasks with dependencies
    print("\n" + "="*60)
    print("Figure 10: 50% scheduled tasks, 90% tasks with dependencies")
    print("="*60)
    results10 = run_simulation(task_sizes, scheduled_percentage=0.5, dependency_percentage=0.9, num_iterations=50)
    create_figure(task_sizes, results10,
                  "Time Complexity: 50% Scheduled Tasks, 90% Tasks with Dependencies",
                  "figure10_50pct_scheduled_90pct_dependencies.png")
    
    print("\n" + "="*60)
    print("All figures created successfully!")
    print("="*60)

if __name__ == "__main__":
    main()

