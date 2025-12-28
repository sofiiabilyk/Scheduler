import matplotlib.pyplot as plt
import random
import time
from MaxHeap import MaxHeapq 
from TaskClass import Task
from TaskSchedulerClass import TaskScheduler

def available_id(ids, used_ids):
    available_ids = []
    for idd in ids:
        if idd not in used_ids:
            available_ids.append(idd)
    return available_ids

sizes = [1, 5, 10, 20, 50, 100, 150, 200, 260, 320, 395, 480]
results = []
efficiencies = []
iterations = 100
categories = ["Routine", "Family", "Growth", "Friends", "Hobby", "Other"]


for size in sizes:
    suma = 0
    efficiency = 0
    ids = []
    for i in range(size):
        ids.append(i)
    print("Ids: ", ids)
    for iteration in range(iterations):
        print("ID start - ", ids)
        tasks = []
        for task in range(size):
            used_ids = []
            lst_dependencies = ids[:]
            random.shuffle(lst_dependencies)
            print("lst_dependencies - ", lst_dependencies)
            print(ids, used_ids)
            idd = random.choice(available_id(ids, used_ids))
            description = "Task " + str(idd)
            duration = random.choice([1, 2 , 3])

            dependencies = random.choice([True, False])
            if dependencies:
                dependencies = []
                dependencies.append(lst_dependencies.pop())
                print("dependencies", dependencies)
                lst_dependencies = random.shuffle(lst_dependencies)
            else:
                dependencies = []
            
            if random.choice([True, False]):
                hh = str(random.choice(range(24)))
                if len(hh) == 1:
                    hh = "0" + hh
                mm = str(random.choice(range(60)))
                if len(mm) == 1:
                    mm = "0" + mm
                scheduled = hh + ":" + mm
            else:
                scheduled = "25:25"

            category = random.choice(categories)
            print("ID append - ", ids)
            tasks.append(Task(id = idd, description = description, duration = duration, dependencies = [], scheduled = scheduled, category = category))
        print("ID end - ", ids)
        start = time.time()
        simple_scheduler = TaskScheduler(tasks)
        efficiency += simple_scheduler.run_task_scheduler("6:00")
        end = time.time()
        suma += end - start
    print("Suma - ", suma)
    print("Efficiency - ", efficiency)
    results.append(suma / iterations)
    efficiencies.append(efficiency / iterations)

print(results)
print(efficiencies)

plt.plot(sizes, results, label = "Code Efficiency")
plt.xlabel("Size, n")
plt.ylabel("Time")
plt.legend()
plt.show()
plt.plot(sizes, efficiencies, label = "Scheduler Efficiency")
plt.xlabel("Size, n")
plt.ylabel("Efficiency")
plt.legend()
plt.show()


