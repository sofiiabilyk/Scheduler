from TaskClass import Task
from KnapSack import knapsack_01
import random

class DP_Scheduler:
    """
    A Dynamic Programming-based Task Scheduler
    
    This scheduler uses a DP approach to optimally fill gaps between scheduled tasks
    by treating each gap as a knapsack problem where we maximize priority value
    within the available time capacity.
    
    Attributes:
        tasks: List of Task objects to schedule
        category_value: Dictionary mapping categories to priority values
        scheduled_tasks: List of tasks with fixed scheduled times
        flexible_tasks: List of tasks without fixed scheduled times
        schedule: Final schedule with task assignments
    """
    
    # Category priority values - can be customized
    category_value = {"Routine": 20, "Family": 15, "Growth": 15, "Friends": 10, "Hobby": 5, "Other": 0}
    
    def __init__(self, tasks):
        """
        Initialize the DP Scheduler
        
        Parameters:
        ----------
        tasks: list
            List of Task objects to schedule
        """
        self.tasks = tasks.copy()
        self.scheduled_tasks = []
        self.flexible_tasks = []
        self.schedule = []  # List of (task, start_time) tuples
        self.completed_tasks = []  # Track completed task IDs
    
    def time_to_minutes(self, time_str):
        """
        Convert time string "hh:mm" to minutes since midnight
        
        Parameters:
        ----------
        time_str: str
            Time in format "hh:mm"
            
        Returns:
        ----------
        int: Minutes since midnight
        """
        if time_str == "25:25":
            return None
        parts = time_str.split(":")
        return int(parts[0]) * 60 + int(parts[1])
    
    def minutes_to_time(self, minutes):
        """
        Convert minutes since midnight to "hh:mm" format
        
        Parameters:
        ----------
        minutes: int
            Minutes since midnight
            
        Returns:
        ----------
        str: Time in format "hh:mm"
        """
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"
    
    def time_difference(self, start_time, end_time):
        """
        Calculate time difference in minutes between two times
        
        Parameters:
        ----------
        start_time: str
            Start time in "hh:mm" format
        end_time: str
            End time in "hh:mm" format
            
        Returns:
        ----------
        int: Difference in minutes
        """
        start_min = self.time_to_minutes(start_time)
        end_min = self.time_to_minutes(end_time)
        if start_min is None or end_min is None:
            return None
        return end_min - start_min
    
    #also filter those which prerequisitues were unrealistic
    def filter_unrealistic_tasks(self, starting_time, end_time="24:00"):
        """
        Clear all tasks that are unrealistic to get done
        
        Filters out tasks that:
        - Are scheduled before starting_time or after end_time
        - Have dependencies that cannot be completed in time
        - Have duration less than 1 minute
        - Cannot fit within the available time window
        
        Parameters:
        ----------
        starting_time: str
            Start time in "hh:mm" format
        end_time: str
            End time in "hh:mm" format (default: "24:00")
            
        Returns:
        ----------
        None
        """
        start_min = self.time_to_minutes(starting_time)
        end_min = self.time_to_minutes(end_time)
        
        filtered_tasks = []
        
        for task in self.tasks:
            # Filter tasks with invalid duration
            if task.duration < 1:
                continue
            
            # Check if task has a fixed schedule
            if task.scheduled != "25:25":
                task_start = self.time_to_minutes(task.scheduled)
                task_end = task_start + task.duration
                
                # Filter if scheduled outside time window
                if task_start < start_min or task_end > end_min:
                    continue
                
                # Check if dependencies can be completed in time
                dep_time = self._calculate_dependency_time(task, start_min)
                if dep_time > (task_start - start_min):
                    continue
            
            filtered_tasks.append(task)
        
        self.tasks = filtered_tasks
    
    def _calculate_dependency_time(self, task, start_min):
        """
        Calculate total time needed for all dependencies of a task
        
        Parameters:
        ----------
        task: Task
            Task object
        start_min: int
            Start time in minutes
            
        Returns:
        ----------
        int: Total minutes needed for dependencies
        """
        if not task.dependencies:
            return 0
        
        total_time = 0
        visited = set()
        
        def dfs_deps(dep_ids):
            nonlocal total_time
            for dep_id in dep_ids:
                if dep_id in visited:
                    continue
                visited.add(dep_id)
                
                for t in self.tasks:
                    if t.id == dep_id:
                        total_time += t.duration
                        if t.dependencies:
                            dfs_deps(t.dependencies)
                        break
        
        dfs_deps(task.dependencies)
        return total_time
    
    def set_priorities(self):
        """
        Set and define priorities for all tasks
        
        Priority is calculated based on:
        - Scheduled time (earlier = higher priority)
        - Category importance
        - Dependencies (tasks that others depend on get higher priority)
        
        Returns:
        ----------
        None
        """
        # Reset priorities
        for task in self.tasks:
            task.priority = 0
        
        # Set priority based on scheduled time
        for task in self.tasks:
            if task.scheduled != "25:25":
                scheduled_min = self.time_to_minutes(task.scheduled)
                # Earlier tasks get higher priority (inverse of time)
                task.priority = 24 * 60 - scheduled_min
        
        # Add category-based priority
        for task in self.tasks:
            task.priority += self.category_value.get(task.category, 0)
        
        # Boost priority for tasks that others depend on
        for task in self.tasks:
            # Check if any other task depends on this one
            for other_task in self.tasks:
                if task.id in other_task.dependencies:
                    task.priority += 100
                    break
        
        # Recursively update dependency priorities
        for task in self.tasks:
            if task.dependencies:
                self._update_dependency_priorities(task.dependencies, task.priority + 100)
        
        self.priority_randomization()
    
    def priority_randomization(self):
        
        """
        In order to have only unique values of priorities, add random float in the range [0;1) 
        & check uniqueness of priority

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        unique_values = []
        for task in self.tasks:
            add = random.random()
            while task.priority + add in unique_values:
                add = random.random()
            task.priority += add
            unique_values.append(task.priority)
    
    def _update_dependency_priorities(self, dependencies, value):
        """
        Recursively update priorities of dependent tasks
        
        Parameters:
        ----------
        dependencies: list
            List of task IDs that are dependencies
        value: float
            Priority value to assign
        """
        for dep_id in dependencies:
            for task in self.tasks:
                if task.id == dep_id:
                    task.priority = max(task.priority, value)
                    if task.dependencies:
                        self._update_dependency_priorities(task.dependencies, value + 100)
                    break
    
    def identify_scheduled_tasks(self):
        """
        Separate tasks into scheduled (fixed time) and flexible (no fixed time)
        
        Returns:
        ----------
        None
        """
        self.scheduled_tasks = []
        self.flexible_tasks = []
        
        for task in self.tasks:
            if task.scheduled != "25:25":
                self.scheduled_tasks.append(task)
            else:
                self.flexible_tasks.append(task)
        
        # Sort scheduled tasks by their scheduled time
        self.scheduled_tasks.sort(key=lambda t: self.time_to_minutes(t.scheduled))
    
    def find_gaps(self, starting_time, end_time="24:00"):
        """
        Find time gaps between scheduled tasks
        
        Parameters:
        ----------
        starting_time: str
            Start time in "hh:mm" format
        end_time: str
            End time in "hh:mm" format
            
        Returns:
        ----------
        list: List of tuples (gap_start, gap_end, gap_duration_minutes)
        """
        gaps = []
        start_min = self.time_to_minutes(starting_time)
        end_min = self.time_to_minutes(end_time)
        
        if not self.scheduled_tasks:
            # No scheduled tasks, one big gap
            gap_duration = end_min - start_min
            if gap_duration > 0:
                gaps.append((starting_time, end_time, gap_duration))
            return gaps
        
        # Gap before first scheduled task
        first_task_start = self.time_to_minutes(self.scheduled_tasks[0].scheduled)
        if first_task_start > start_min:
            gap_duration = first_task_start - start_min
            gaps.append((starting_time, self.scheduled_tasks[0].scheduled, gap_duration))
        
        # Gaps between scheduled tasks
        current_end = first_task_start + self.scheduled_tasks[0].duration
        
        for i in range(1, len(self.scheduled_tasks)):
            next_task_start = self.time_to_minutes(self.scheduled_tasks[i].scheduled)
            
            if current_end < next_task_start:
                gap_duration = next_task_start - current_end
                gap_start = self.minutes_to_time(current_end)
                gap_end = self.scheduled_tasks[i].scheduled
                gaps.append((gap_start, gap_end, gap_duration))
            
            # Update current_end to after this scheduled task
            task_end = next_task_start + self.scheduled_tasks[i].duration
            current_end = max(current_end, task_end)
        
        # Gap after last scheduled task
        if current_end < end_min:
            gap_duration = end_min - current_end
            gap_start = self.minutes_to_time(current_end)
            gaps.append((gap_start, end_time, gap_duration))
        
        return gaps
    
    def fill_gap_with_knapsack(self, gap_start, gap_duration, available_tasks):
        """
        Fill a time gap using knapsack problem approach
        
        Selects tasks that maximize total priority within the gap duration
        
        Parameters:
        ----------
        gap_start: str
            Start time of the gap in "hh:mm" format
        gap_duration: int
            Duration of gap in minutes
        available_tasks: list
            List of Task objects that can be scheduled in this gap
            
        Returns:
        ----------
        list: List of Task objects selected to fill the gap
        """
        if gap_duration <= 0 or not available_tasks:
            return []
        
        # Filter tasks that can fit in the gap and have dependencies satisfied
        candidate_tasks = []
        for task in available_tasks:
            # Check if task fits in gap
            if task.duration > gap_duration:
                continue
            
            # Check if dependencies are already completed
            if self._dependencies_satisfied(task):
                candidate_tasks.append(task)
        
        if not candidate_tasks:
            return []
        
        # Prepare knapsack inputs
        weights = [task.duration for task in candidate_tasks]
        values = [task.priority for task in candidate_tasks]
        
        
        # Solve knapsack problem
        max_value, selected_indices = knapsack_01(weights, values, gap_duration)
        
        # Get selected tasks
        selected_tasks = [candidate_tasks[i] for i in selected_indices]
        
        # Sort selected tasks by priority (highest first)
        selected_tasks.sort(key=lambda t: t.priority, reverse=True)
        
        return selected_tasks
    
    def _dependencies_satisfied(self, task):
        """
        Check if all dependencies of a task are already completed
        
        Parameters:
        ----------
        task: Task
            Task object to check
            
        Returns:
        ----------
        bool: True if all dependencies are satisfied
        """
        if not task.dependencies:
            return True
        for dep_id in task.dependencies:
            if dep_id not in self.completed_tasks:
                return False
        return True
    
    def schedule_tasks(self, starting_time, end_time="24:00"):
        """
        Main scheduling function using DP approach
        
        Steps:
        1. Filter unrealistic tasks
        2. Set priorities
        3. Identify scheduled tasks
        4. Find gaps between scheduled tasks
        5. Fill gaps using knapsack problem
        
        Parameters:
        ----------
        starting_time: str
            Start time in "hh:mm" format
        end_time: str
            End time in "hh:mm" format (default: "24:00")
            
        Returns:
        ----------
        list: List of tuples (task, start_time) representing the schedule
        """
        # Step 1: Filter unrealistic tasks
        self.filter_unrealistic_tasks(starting_time, end_time)
        
        # Step 2: Set priorities
        self.set_priorities()
        
        # Step 3: Identify scheduled and flexible tasks
        self.identify_scheduled_tasks()
        
        # Step 4: Find gaps
        gaps = self.find_gaps(starting_time, end_time)
        
        # Step 5: Build schedule
        self.schedule = []
        self.completed_tasks = []
        available_flexible = self.flexible_tasks.copy()
        
        # Create a mapping of gaps to the scheduled task that comes after them
        # This helps us know which scheduled task to mark as completed after filling a gap
        gap_to_scheduled_task = {}
        scheduled_task_index = 0
        
        for gap_start, gap_end, gap_duration in gaps:
            # Find the scheduled task that starts at gap_end (if any)
            scheduled_task_after_gap = None
            for task in self.scheduled_tasks:
                if task.scheduled == gap_end:
                    scheduled_task_after_gap = task
                    break
            gap_to_scheduled_task[(gap_start, gap_end, gap_duration)] = scheduled_task_after_gap
        
        # Fill gaps with flexible tasks using knapsack
        for gap_start, gap_end, gap_duration in gaps:
            # Get tasks available for this gap
            gap_tasks = [t for t in available_flexible if t.id not in self.completed_tasks]
            
            # Fill gap using knapsack
            selected_tasks = self.fill_gap_with_knapsack(gap_start, gap_duration, gap_tasks)
            
            # Schedule selected tasks sequentially
            current_gap_time = gap_start
            while self.time_difference(current_gap_time,  gap_end) > 0 and len(selected_tasks) > 0:
                for task in selected_tasks: 
                    self.schedule.append((task, current_gap_time))
                    self.completed_tasks.append(task.id)
                    current_gap_time = self._add_minutes(current_gap_time, task.duration)
                    # Remove from available flexible tasks
                    available_flexible = [t for t in available_flexible if t.id != task.id]
                gap_tasks = [t for t in available_flexible if t.id not in self.completed_tasks]
                selected_tasks = self.fill_gap_with_knapsack(current_gap_time, self.time_difference(current_gap_time, gap_end), gap_tasks)
            
            # After filling the gap, mark the scheduled task that comes after this gap as completed
            scheduled_task_after_gap = gap_to_scheduled_task[(gap_start, gap_end, gap_duration)]
            if scheduled_task_after_gap:
                # Add the scheduled task to the schedule
                self.schedule.append((scheduled_task_after_gap, scheduled_task_after_gap.scheduled))
                self.completed_tasks.append(scheduled_task_after_gap.id)
                # Remove from available flexible tasks if it was there
                available_flexible = [t for t in available_flexible if t.id != scheduled_task_after_gap.id]
        
        # Handle scheduled tasks that don't have a gap before them
        # (e.g., if a scheduled task starts immediately after another)
        for task in self.scheduled_tasks:
            if task.id not in self.completed_tasks:
                # This scheduled task doesn't have a gap before it, so add it now
                self.schedule.append((task, task.scheduled))
                self.completed_tasks.append(task.id)
                available_flexible = [t for t in available_flexible if t.id != task.id]
        
        # Sort schedule by start time
        self.schedule.sort(key=lambda x: self.time_to_minutes(x[1]))
        
        return self.schedule
    
    def _add_minutes(self, time_str, minutes):
        """
        Add minutes to a time string
        
        Parameters:
        ----------
        time_str: str
            Time in "hh:mm" format
        minutes: int
            Minutes to add
            
        Returns:
        ----------
        str: New time in "hh:mm" format
        """
        time_min = self.time_to_minutes(time_str)
        new_min = time_min + minutes
        return self.minutes_to_time(new_min)
    
    def print_schedule(self):
        """
        Print the generated schedule
        
        Returns:
        ----------
        None
        """
        if not self.schedule:
            print("No schedule generated. Call schedule_tasks() first.")
            return
        
        print("\n" + "="*60)
        print("DP-BASED TASK SCHEDULE")
        print("="*60)
        
        total_duration = 0
        for task, start_time in self.schedule:
            end_time = self._add_minutes(start_time, task.duration)
            total_duration += task.duration
            print(f"🕰 {start_time} - {end_time} ({task.duration} min)")
            print(f"   📋 {task.description} [ID: {task.id}]")
            print(f"   📊 Priority: {task.priority:.2f} | Category: {task.category}")
            if task.dependencies:
                print(f"   ⚠️  Depends on: {task.dependencies}")
            print()
        
        if self.schedule:
            first_start = self.schedule[0][1]
            last_end = self._add_minutes(self.schedule[-1][1], self.schedule[-1][0].duration)
            total_time = self.time_difference(first_start, last_end)
            efficiency = (total_duration / total_time * 100) if total_time > 0 else 0
            
            print("="*60)
            print(f"📈 Statistics:")
            print(f"   Total tasks scheduled: {len(self.schedule)}")
            print(f"   Total task duration: {total_duration} minutes")
            print(f"   Time span: {first_start} - {last_end} ({total_time} minutes)")
            print(f"   Efficiency: {efficiency:.2f}%")
            print("="*60)
    
    def get_schedule(self):
        """
        Get the current schedule
        
        Returns:
        ----------
        list: List of tuples (task, start_time)
        """
        return self.schedule


# Example usage
if __name__ == "__main__":
    from Scheduler import school_day, trip_prep
    # Example with trip_prep tasks
    print("Testing DP Scheduler with trip_prep tasks:\n")
    dp_scheduler = DP_Scheduler(trip_prep)
    schedule = dp_scheduler.schedule_tasks("06:00", "24:00")
    dp_scheduler.print_schedule()

