from MaxHeap import MaxHeapq 
from TaskClass import Task
from ImprovedGreedy_Scheduler import ImprovedGreedy_Scheduler
from TaskSchedulerClass import TaskScheduler
#from tests import school_day, trip_prep, group_project, edge_cases, circular_and_conflicts, mixed_statuses_and_categories, high_priority_deadlines, friends_family_mix, shuffled_order_test

task_3 = Task(id = 3, description = 'Eat Breakfast', duration = 15, dependencies = [2], scheduled = "25:25", category = "Routine")
task_4 = Task(id = 4, description = 'Take SS111 Session', duration = 80, dependencies = [1], scheduled = "25:25", category = "Growth")
task_2 = Task(id = 2, description = 'Prepare Breakfast', duration = 15, dependencies = [1], scheduled = "25:25", category = "Routine")
task_7 = Task(id = 7, description = 'Go to Shinagawa Station with the group', duration = 15, dependencies = [6], scheduled = "25:25")
task_8 = Task(id = 8, description = 'Take Shinkansen to the excursion site', duration = 180, dependencies = [7], scheduled = "25:25")
task_5 = Task(id = 5, description = 'Do my PCWs', duration = 120, dependencies = [], scheduled = "25:25", category = "Growth")
task_6 = Task(id = 6, description = 'Meet with the course group', duration = 5, dependencies = [3], scheduled = "25:25")
task_1 = Task(id = 1, description = 'Wake up & Salf Care Routine', duration = 30, dependencies = [], scheduled = "25:25", category = "Routine")

school_day = [
    Task(id=11, description='Morning jog', duration=25, dependencies=[], scheduled="07:00", category="Hobby"),
    Task(id=19, description='Recharge', duration=45, dependencies=[16], scheduled="25:25"),
    Task(id=20, description='Meditation', duration=15, dependencies=[19], scheduled="25:25"),
    Task(id=15, description='Office hours', duration=30, dependencies=[12], scheduled="14:30", category="Growth"),
    Task(id=16, description='Homework: DS problem set', duration=60, dependencies=[13], scheduled="25:25", category="Growth"),
    Task(id=17, description='Call family', duration=20, dependencies=[], scheduled="20:00", category="Family"),
    Task(id=18, description='Read for pleasure', duration=30, dependencies=[], scheduled="21:30", category="Hobby"),
    Task(id=12, description='Class: Data Structures', duration=90, dependencies=[], scheduled="09:00", category="Growth"),
    Task(id=13, description='Lab: Systems', duration=120, dependencies=[12], scheduled="11:00", category="Growth"),
    Task(id=14, description='Lunch with friends', duration=45, dependencies=[], scheduled="13:00", category="Friends"),
]

trip_prep = [
    Task(id=21, description='Buy train tickets', duration=10, dependencies=[], scheduled="08:00", category="Other"),
    Task(id=22, description='Pack clothes', duration=25, dependencies=[], scheduled="25:25", category="Routine"),
    Task(id=23, description='Charge devices', duration=15, dependencies=[], scheduled="06:30", category="Routine"),
    Task(id=24, description='Print itinerary', duration=5, dependencies=[21], scheduled="09:00", category="Other"),
    Task(id=25, description='Meet at station', duration=10, dependencies=[24], scheduled="10:15", category="Friends"),
    Task(id=26, description='Grab breakfast to-go', duration=15, dependencies=[], scheduled="09:50", category="Routine"),
    Task(id=27, description='Confirm reservations', duration=8, dependencies=[21], scheduled="25:25", category="Other"),
    Task(id=28, description='Quick tidy apartment', duration=12, dependencies=[], scheduled="06:00", category="Routine"),
    ]

my_tasks = [task_1, task_5, task_6, task_7, task_2, task_3, task_4, task_8] 
my_tasks = school_day
simple_scheduler = ImprovedGreedy_Scheduler(my_tasks)
'''
print("Length of the tasks before filtering: ", len(simple_scheduler.tasks))
for_print = []
for task in simple_scheduler.tasks:
    for_print.append(task.id)
print(sorted(for_print))
simple_scheduler.filter_tasks("9:00")
print("Length of the tasks after filtering: ", len(simple_scheduler.tasks))
for_print = []
for task in simple_scheduler.tasks:
    for_print.append(task.id)
print(sorted(for_print))
'''
simple_scheduler.run_task_scheduler("9:00")
''' '''
simple_scheduler = TaskScheduler(my_tasks)
simple_scheduler.run_task_scheduler("9:00")
#print( simple_scheduler.combined_total_time([7], 180, [8], [0]))