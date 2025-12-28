import random

class Task:
    """
    - id: int,  Task id (a reference number)   
    - description: string,  Task short description   
    - duration: int, Task duration in minutes   
    - dependencies: [int],  List of task ids that need to preceed this task  
    - status: string,  Current status of the task  
    - scheduled: string,  Time when the task should start in the format "hh:mm" 
                    if the value is "25:25" - the task is flexible time-wise
    - category: string, The user can indicate to which category (Routine, Family, 
                    Growth, Friends, Hobby, Other) the task relates to. Before executing 
                    time scheduler they also can indicate the importance of each 
                    of the categories for them personally.

   
    """
    #Initializes an instance of Task
    def __init__(self, id, description, duration,
                 dependencies = [], status="N", scheduled = "25:25", category = "Other"):
        self.id = id
        self.description = description
        self.duration = duration
        self.dependencies = dependencies
        self.status = status
        self.scheduled = scheduled
        self.priority = 0
        self.category = category
    


class MaxHeapq:
    """ 
    A class that implements properties and methods 
		that support a max priority queue data structure

		Attributes
	  ----------
	  heap : arr
	      A Python list where key values in the max heap are stored
	  heap_size: int
	      An integer counter of the number of keys present in the max heap
	  """  

    def __init__(self):    
        """
        Parameters
        ----------
        None
        """    
        self.heap       = []
        self.heap_size  = 0
        
    def left(self, i):
        """
        Takes the index of the parent node
        and returns the index of the left child node

        Parameters
        ----------
        i: int
          Index of parent node

        Returns
        ----------
        int
          Index of the left child node
        """
        return 2 * i + 1

    def right(self, i):
        """
        Takes the index of the parent node
        and returns the index of the right child node
        
        Parameters
        ----------
        i: int
            Index of parent node

        Returns
        ----------
        int
            Index of the right child node
        """
        return 2 * i + 2
		
    def parent(self, i):
        """
        Takes the index of the child node
        and returns the index of the parent node
        
        Parameters
        ----------
        i: int
            Index of child node

        Returns
        ----------
        int
            Index of the parent node
        """

        return (i - 1)//2

    def maxk(self):     
        """
        Returns the highest key in the priority queue. 
        
        Parameters
        ----------
        None

        Returns
        ----------
        int
            the highest key in the priority queue
        """
        return self.heap[0]         
  
    def heappush(self, key):  
        """
        Insert a key into a priority queue 
        
        Parameters
        ----------
        key: int
            The key value to be inserted

        Returns
        ----------
        None
        """
        # insert -inf, as it is guaranteed to be smaller than all other 
        # elements -> should be located in the end
        # to not break the max-heap property
        self.heap.append(-float("inf")) 
        self.increase_key(self.heap_size,key)
        self.heap_size+=1
        
    def increase_key(self, i, key): 
        """
        Modifies the value of a key in a max priority queue
        with a higher value
        
        Parameters
        ----------
        i: int
            The index of the key to be modified
        key: int
            The new key value

        Returns
        ----------
        None
        """
        if key < self.heap[i]:
            raise ValueError('new key is smaller than the current key')
        self.heap[i] = key
        # if the parent is smalle we should swap the elements 
        # to not break the max-heap property
        while i > 0 and self.heap[self.parent(i)] < self.heap[i]:
            j = self.parent(i)
            holder = self.heap[j]
            self.heap[j] = self.heap[i]
            self.heap[i] = holder
            i = j    
       
    def heapify(self, i):
        """
        Creates a max heap from the index given
        
        Parameters
        ----------
        i: int
            The index of the root node of the subtree to be heapify

        Returns
        ----------
        None
        """
        l = self.left(i)
        r = self.right(i)
        heap = self.heap
        #looking for the largest value among 
        # parent, right & left children 
        # to make the largest a parent
        if l <= (self.heap_size-1) and heap[l]>heap[i]:
            largest = l
        else:
            largest = i
        if r <= (self.heap_size-1) and heap[r] > heap[largest]:
            largest = r
        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            self.heapify(largest)

    def heappop(self):
        """
        returns the larest key in the max priority queue
        and remove it from the max priority queue
        
        Parameters
        ----------
        None

        Returns
        ----------
        int
            the max value in the heap that is extracted
        """
        if self.heap_size < 1:
            raise ValueError('Heap underflow: There are no keys in the priority queue ')
        maxk = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heap_size-=1
        self.heapify(0)
        return maxk

    def remove(self, key):
        """
        Removes the specified key from the max heap

        Parameters
        ----------
        key: int
            The key value to be removed

        Returns
        ----------
        None
        """
        try:
            index = self.heap.index(key)
        except ValueError:
            raise ValueError("Key not found in heap")

        # Replace with last element and heap
        self.heap[index] = self.heap[-1]
        self.heap.pop()
        self.heap_size -= 1

        # Restore heap property
        if index < self.heap_size:
            parent_index = self.parent(index)
            if index > 0 and self.heap[index] > self.heap[parent_index]:
                self.increase_key(index, self.heap[index])
            else:
                self.heapify(index)

def test_maxheapq():

    """
        Tests the class MaxHeapq

        Parameters
        ----------
        None

        Returns
        ----------
        None
    """

    print("Running test cases...")

    print("Test 1: Basic insertion and max retrieval")
    h = MaxHeapq()
    h.heappush(10)
    h.heappush(20)
    h.heappush(5)
    print(h.maxk() == 20)
    
    print("Test 2: Pop max and check heap property")
    print(h.heappop() == 20)
    print(h.maxk() ==  10)

    print("Test 3: pudh more values in and remove the key")
    h.heappush(17)
    h.heappush(23)
    h.heappush(4)
    print(h.heap)
    h.remove(23)
    print(h.heap)  # Should not contain 10


    print("All tests passed!")

#test_maxheapq()


class TaskScheduler:
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
                for t in self.tasks:
                    if t.id == dependency:
                        t.priority = max(t.priority, value)
                        self.update_dependencies_priority(t.dependencies, value + 100)

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
    
    def difference(self, now, ordered):
        
        """
        Find the difference in minutus between current time and 
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
        print("Running a simple scheduler:\n")
        self.priority_calculation()
        self.create_queue()
        while self.priority_queue.heap_size>0:
            current_task = self.find_task(self.priority_queue.heappop()) #get all the information about the task
            # Accomodating the case if there is a schedule overlap
            if self.difference(current_time, current_task.scheduled) < 0:
                print(f"Schedule overlap happened with task {current_task.description}")
                continue
            #if the current task is scheduled for specific time, let's check if we still can do smth before the time comes
            if current_task.scheduled != "25:25":
                option = 1 #We have option to do smth in between now and time when current task is scheduled
                diff = self.difference(current_time, current_task.scheduled) #how many minutes we have btw now and time of the current task
                #Do as much tasks as possible in time diff, based on the priority
                while diff > 0 and option:
                    alternative_queue = MaxHeapq() #heap of the options we have
                    # create priority queue for tasks that fit within diff time
                    for task in self.tasks:
                        if task.scheduled == "25:25" and task.duration <= diff and task.priority in self.priority_queue.heap:
                            #before adding it to the heap of tasks we can do
                            #check if all dependencies are done
                            completed_dependencies = 1
                            for dependency in task.dependencies:
                                if self.find_priority(dependency) in self.priority_queue.heap or dependency == current_task.id:
                                    completed_dependencies = 0
                            if completed_dependencies:
                                alternative_queue.heappush(task.priority)
                    if alternative_queue.heap_size == 0: #if no tasks can be done in time diff
                        option = 0
                    else:
                        #proceed with the top-priority task that fits within schedule
                        self.priority_queue.remove(alternative_queue.heap[0]) # remove it from the main priority queue
                        current_time = self.printing(self.find_task(alternative_queue.heappop()), current_time) #Print ant update current time
                        diff = self.difference(current_time, current_task.scheduled)
                current_time = current_task.scheduled #after no more tasks can be done in between, we move on the previously scheduled task

            current_time = self.printing(current_task, current_time)         
                    
        print(f"\n🏁 Completed all planned tasks in period from {starting_time} to {current_time}!")

task_1 = Task(id = 1, description = 'Wake up & Salf Care Routine', duration = 30, dependencies = [], scheduled = "25:25", category = "Routine")
task_2 = Task(id = 2, description = 'Prepare Breakfast', duration = 15, dependencies = [1], scheduled = "25:25", category = "Routine")
task_3 = Task(id = 3, description = 'Eat Breakfast', duration = 15, dependencies = [2], scheduled = "25:25", category = "Routine")
task_4 = Task(id = 4, description = 'Take SS111 Session', duration = 90, dependencies = [1], scheduled = "10:00", category = "Growth")
task_5 = Task(id = 5, description = 'Do my PCWs', duration = 120, dependencies = [], scheduled = "25:25", category = "Growth")
task_6 = Task(id = 6, description = 'Meet with the course group', duration = 5, dependencies = [], scheduled = "12:00")
task_7 = Task(id = 7, description = 'Go to Shinagawa Station with the group', duration = 15, dependencies = [6], scheduled = "12:15")
task_8 = Task(id = 8, description = 'Take Shinkansen to the excursion site', duration = 180, dependencies = [7], scheduled = "16:24")

my_tasks = [task_1, task_5, task_6, task_7, task_2, task_3, task_4, task_8] 
simple_scheduler = TaskScheduler(my_tasks)
simple_scheduler.run_task_scheduler("6:00")



