from MaxHeap import MaxHeapq 
from KnapSack import knapsack_01
#from MaxHeap import MaxHeapq 
import random

class ImprovedGreedy_Scheduler:
    """
    A Simple Daily Task Scheduler Using Priority Queues

    tasks - the list of the Task() objects, that we want to schedule
    priority_queue - MaxHeapq() of the priority value for each of the tasks
    """
    # Each Task has a category. Each of the categories has a value that 
    # represents how strongly we should prioritize tasks from this category
    category_value = {"Routine" : 20, "Family" : 15, "Growth" : 15, "Friends" : 10, "Hobby" : 5, "Other" : 0}
    
    def __init__(self, tasks):
        self.tasks = tasks
        self.priority_queue = [] 

    def priority_calculation(self):
        """
        Calculates the priority of each task based on the dependencies,  
        scheduling and the category of the task

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        for task in self.tasks:
            #set priority based on the time, the sooner it is scheduled, the higher priority 
            if task.scheduled != "25:25":
                task.priority = max(task.priority, 24 * 3600 - int(task.scheduled.split(":")[0]) * 3600 - int(task.scheduled.split(":")[1]) * 60)
            # increase the priority depending on the importance of the category
            task.priority += self.category_value[task.category]
            # updates the priority of all dependencies of the current task
            self.update_dependencies_priority(task.dependencies, task.priority + 100)
        self.priority_randomization()
    
    def update_dependencies_priority(self, dependencies, value):
        
        """
        Updates the priority of the dependent task, choosing the biggest between its 
        current priority and the priority of the following task (dependant) increased by 100

        Parameters
        ----------
        dependencies: list
          list of id's of dependencies
        value: int
          the increased by 100 priority of the dependant task

        Returns
        ----------
        None
        """
        if len(dependencies) > 0:
            for dependency in dependencies:
                found = False
                for t in self.tasks:
                    if t.id == dependency:
                        found = True
                        t.priority = max(t.priority, value)
                        self.update_dependencies_priority(t.dependencies, value + 100)
                if not found:
                    dependencies.remove(dependency)

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

    def create_queue(self):
        
        """
        Create MaxHeap based on the tasks' priority

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        self.priority_queue = MaxHeapq()
        for task in self.tasks:
            self.priority_queue.heappush(task.priority)
    
    def find_priority(self, id):
        
        """
        Find the value of the Task priority based on the given id

        Parameters
        ----------
        id: int
          the id of the task

        Returns
        ----------
        int
          the priority the  task
        """
        for task in self.tasks:
            if task.id == id:
                return task.priority
        return None
        
    def print_self(self):
        
        """
        Print the all the Tasks added to the Scheduler 

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        print("Tasks added to the simple scheduler:")
        print("--------------------------------------")
        for t in self.tasks:
            print(f"➡️'{t.description}', duration = {t.duration} mins.")   
            if len(t.dependencies)>0:
                print(f"\t ⚠️ This task depends on others!")     

    def find_task(self, priority_value):
        
        """
        Find the instant of the class Task, that has indicated priority 

        Parameters
        ----------
        priority_value: int
          the value of the priority of the task

        Returns
        ----------
        Object of the Task():
            the instant of the class Task, that has indicated priority 
        """
        for task in self.tasks:
            if task.priority == priority_value:
                return task
        return None

    def new_time(self, old_time, time_passed):
        
        """
        Calculate new current time

        Parameters
        ----------
        old_time: string
          "hh:mm" that represents when the task has been started
        time_passed: int
          how many minutes is duration of the task
        
        Returns
        ----------
        str:  time when the task ends in the format "hh:mm"
        """
        h = int(old_time.split(":")[0])
        m = int(old_time.split(":")[1])
        h += time_passed // 60
        m += time_passed % 60
        if m >= 60:
            h += 1
            m -= 60
        if m < 10:
            return str(h)+":0"+str(m)
        return str(h)+":"+str(m)
    
    def time_difference(self, now, ordered):
        
        """
        Find the time_difference in minutus between current time and 
        when the next priority task is scheduled

        Parameters
        ----------
        now: string
          "hh:mm" that represents when current time
        ordered: string
          "hh:mm" when the next priority task should start

        Returns
        ----------
        int:
          minutes between the current time and the beginning of the next in the priority queue
        """
        return (int(ordered.split(":")[0]) * 60 + int(ordered.split(":")[1])) - (int(now.split(":")[0]) * 60 + int(now.split(":")[1]))
        
    def printing(self, current_task, current_time):
        """
        Prints the information about current task and updates time afer its completion

        Parameters
        ----------
        current_task: Task
          Task that is currently getting done
        current_time: string
          "hh:mm" that represents the time when current task starts

        Returns
        ----------
        string :
          "hh:mm" that represents the time after current task completion
        """
        print(f"🕰t={current_time}")
        print(f"\tstarted '{current_task.description}' for {current_task.duration} mins...")
        current_time = self.new_time(current_time, current_task.duration )
        print(f"\t✅ t={(current_time)}, task completed!")
        return current_time

    def total_time(self, dependencies, time):
        
        """
        Calculate the total time of the dependencies
        
        Parameters
        """
        if len(dependencies) == 0:
            return 0
        for dependency in dependencies:
            for task in self.tasks:
                if task.id == dependency:
                    time += task.duration
                    time += self.total_time(task.dependencies, time)
        return time
    
    def combined_total_time(self, dependencies, time, ids, queue):
        
        """
        Calculate the total time of the dependencies
        
        Parameters
        """
        if len(dependencies) == 0 or time > 16 * 60:
            return time, ids
        for dependency in dependencies:
            ids.append(dependency)
            for task in self.tasks:
                if task.id == dependency and task.priority in queue:
                    if task.scheduled != "25:25":
                        return 10000, ids
                    else:
                        time += task.duration
                    time, ids = self.combined_total_time(task.dependencies, time, ids, queue)
        return time, ids


    def filter_tasks(self, starting_time):
        """
        Filter out the tasks that are not possible to do in the given time period
        by the next rules:
        - the task is not possible to do if it is scheduled before the starting time
        - the task is not possible to do if it is scheduled after the end of the time period
        - the task is not possible to do if it has duration less than 1 minute

        Parameters
        ----------
        starting_time: string
          "hh:mm" that represents when we start the first tasks

        Returns
        ----------
        None
        """
        i = 0
        start_minutes = self.time_difference("00:00", starting_time)
        end_minutes = start_minutes + 16 * 60
        while i < len(self.tasks) - 1:
            if self.tasks[i].duration < 1: #exluding tasks that have duration less than a minute
                self.tasks.remove(self.tasks[i])
            elif self.tasks[i].scheduled != "25:25":
                scheduled_minutes = self.time_difference("00:00", self.tasks[i].scheduled)
                # exluding tasks that start or finish outside of time awake
                if scheduled_minutes < start_minutes or scheduled_minutes + self.tasks[i].duration > end_minutes:
                    self.tasks.remove(self.tasks[i])
                # exluding tasks that has prerequisites completion time larger than time available at this moment
                elif self.total_time(self.tasks[i].dependencies, 0) > self.time_difference(starting_time, self.tasks[i].scheduled):
                    self.tasks.remove(self.tasks[i])
                else:
                    i += 1
            else:
                i += 1
        
    #def multi_tasking()
    
    def run_task_scheduler(self, starting_time):
        
        """
        Runs the scheduler that calculates priorities of the given task 
        and prints them in the priority order with time considerations

        Parameters
        ----------
        starting_time: string
          "hh:mm" that represents when we start the first tasks

        Returns
        ----------
        None
        """
        current_time = starting_time
        durations_sum = 0 # how many minutes were spent in action
        tasks_done = []
        print("Running a simple scheduler:\n")
        self.filter_tasks(starting_time) # filter out the tasks that are not possible to do in the given time period
        self.priority_calculation() # calculate the priorities of the tasks
        self.create_queue() # create the priority queue
        while self.priority_queue.heap_size>0:
            current_task = self.find_task(self.priority_queue.heappop()) #get all the information about the task
            tasks_done.append(current_task.id)
            # Accomodating the case if there is a schedule
            if self.time_difference(current_time, current_task.scheduled) < 0:
                print(f"Schedule overlap happened with task {current_task.description}")
                continue
            #if the current task is scheduled for specific time, let's check if we still can do smth before the time comes
            if current_task.scheduled != "25:25":
                option = 1 #We have option to do smth in between now and time when current task is scheduled
                diff = self.time_difference(current_time, current_task.scheduled) #how many minutes we have btw now and time of the current task
                #Do as much tasks as possible in time diff, based on the priority
                print("There is ", diff, "minutes to the next task")
                #while diff > 0 and option:
                if diff > 0 and option:
                    minutes, priorities = [], []
                    items = 0
                    correspondence_to_id = {}
                    for task in self.tasks:
                        if (task.scheduled == "25:25" and task.duration <= diff and task.priority in self.priority_queue.heap):
                            if len(task.dependencies) == 0  or self.combined_total_time(task.dependencies, task.duration, [task.id], self.priority_queue.heap)[0] <= diff:
                                i = 0
                                while i < len(priorities) and priorities[i] > task.priority:
                                    i+=1
                                minutes.append(task.duration)
                                priorities.append(task.priority)
                                if i != len(priorities) - 1:
                                    minutes = minutes[:i] + [task.duration] + minutes[i:-1]
                                    priorities = priorities[:i] + [task.priority] + priorities[i:-1]
                                correspondence_to_id[items] = task.id
                                items += 1
                    if len(minutes) > 0:
                        utility, selected_items = knapsack_01(minutes, priorities, diff)
                        for item in selected_items: 
                            if priorities[item] in self.priority_queue.heap:
                                self.priority_queue.remove(priorities[item]) # remove it from the main priority queue
                                durations_sum += minutes[item]
                            current_time = self.printing(self.find_task(priorities[item]), current_time) #Print ant update current time

                current_time = current_task.scheduled #after no more tasks can be done in between, we move on the previously scheduled task
            
            durations_sum += current_task.duration
            current_time = self.printing(current_task, current_time)         
        min_passed = self.time_difference(starting_time, current_time)           
        print(f"\n🏁 Completed all planned tasks in period from {starting_time} to {current_time}! It's {min_passed} minutes passed.")
        print(f"Sum of the task durations - {durations_sum} mins")
        if min_passed == 0:
            efficiency = -1
        else:
            efficiency = round((durations_sum / min_passed) * 100, 2)
        print("Scheduler efficiency is ", efficiency)
        return efficiency

    