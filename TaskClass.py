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
    
'''
    def __lt__(self, other):
        return self.id < other.id
        '''