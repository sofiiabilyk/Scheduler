school_day = [
    Task(id=11, description='Morning jog', duration=25, dependencies=[], scheduled="07:00", category="Hobby"),
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

group_project = [
    Task(id=31, description='Plan project outline', duration=40, dependencies=[], scheduled="25:25", category="Growth"),
    Task(id=32, description='Assign roles', duration=15, dependencies=[31], scheduled="25:25", category="Growth"),
    Task(id=33, description='Implement core module', duration=180, dependencies=[32], scheduled="25:25", category="Growth"),
    Task(id=34, description='Write tests', duration=60, dependencies=[33], scheduled="25:25", category="Growth"),
    Task(id=35, description='Prepare slides', duration=45, dependencies=[31], scheduled="25:25", category="Growth"),
    Task(id=36, description='Team meeting', duration=20, dependencies=[32], scheduled="14:00", category="Friends"),
    Task(id=37, description='Peer review', duration=30, dependencies=[34,35], scheduled="25:25", category="Growth"),
    Task(id=38, description='Rehearsal', duration=20, dependencies=[37], scheduled="18:00", category="Growth"),
]

edge_cases = [
    Task(id=41, description='Instant sync (0 min)', duration=0, dependencies=[], scheduled="08:00", category="Other"),
    Task(id=42, description='Mega compute (8h)', duration=8*60, dependencies=[41], scheduled="09:00", category="Hobby"),
    Task(id=43, description='Short check', duration=5, dependencies=[], scheduled="25:25", category="Other"),  # missing dep id 99
    Task(id=44, description='Phone family', duration=10, dependencies=[], scheduled="20:00", category="Family"),
    Task(id=45, description='Evening walk', duration=30, dependencies=[], scheduled="19:30", category="Hobby"),
    Task(id=46, description='Meal prep', duration=40, dependencies=[], scheduled="25:25", category="Routine"),
    Task(id=47, description='Pay bills', duration=12, dependencies=[], scheduled="10:00", category="Other"),
    Task(id=48, description='Backup laptop', duration=25, dependencies=[47], scheduled="25:25", category="Other"),
]

circular_and_conflicts = [
    Task(id=51, description='A depends on B', duration=10, dependencies=[52], scheduled="25:25", category="Other"),
    Task(id=52, description='B depends on C', duration=10, dependencies=[53], scheduled="25:25", category="Other"),
    Task(id=53, description='C depends on A', duration=10, dependencies=[51], scheduled="25:25", category="Other"),
    Task(id=54, description='Lecture', duration=90, dependencies=[], scheduled="11:00", category="Growth"),
    Task(id=55, description='Doctor appt (conflict)', duration=30, dependencies=[], scheduled="11:00", category="Family"),
    Task(id=56, description='Coffee break', duration=15, dependencies=[], scheduled="12:30", category="Hobby"),
    Task(id=57, description='Quick errand', duration=20, dependencies=[], scheduled="13:00", category="Other"),
    Task(id=58, description='Read news', duration=10, dependencies=[], scheduled="25:25", category="Other"),
]

mixed_statuses_and_categories = [
    Task(id=61, description='Draft blog post', duration=60, dependencies=[], status="C", scheduled="25:25", category="Hobby"),
    Task(id=62, description='Edit blog post', duration=30, dependencies=[61], status="N", scheduled="25:25", category="Hobby"),
    Task(id=63, description='Respond to mentor', duration=15, dependencies=[], status="I", scheduled="09:30", category="Friends"),
    Task(id=64, description='Grocery shopping', duration=35, dependencies=[], status="N", scheduled="18:00", category="Routine"),
    Task(id=65, description='Cook dinner', duration=45, dependencies=[64], status="N", scheduled="19:00", category="Routine"),
    Task(id=66, description='Practice language', duration=25, dependencies=[], status="N", scheduled="21:00", category="Growth"),
    Task(id=67, description='Call roommate', duration=10, dependencies=[], status="N", scheduled="20:30", category="Family"),
    Task(id=68, description='Stretch & wind down', duration=15, dependencies=[], status="N", scheduled="22:15", category="Routine"),
]

high_priority_deadlines = [
    Task(id=71, description='Submit thesis draft', duration=120, dependencies=[], scheduled="09:00", category="Growth"),
    Task(id=72, description='Finalize figures', duration=60, dependencies=[71], scheduled="07:30", category="Growth"),
    Task(id=73, description='Quick revision', duration=25, dependencies=[72], scheduled="08:30", category="Growth"),
    Task(id=74, description='Print copies', duration=20, dependencies=[73], scheduled="08:50", category="Other"),
    Task(id=75, description='Send to advisor', duration=5, dependencies=[74], scheduled="09:15", category="Growth"),
    Task(id=76, description='Plan celebration', duration=40, dependencies=[75], scheduled="25:25", category="Friends"),
    Task(id=77, description='Confirm room booking', duration=10, dependencies=[], scheduled="06:30", category="Other"),
    Task(id=78, description='Breakfast & coffee', duration=20, dependencies=[], scheduled="06:00", category="Routine"),
]

friends_family_mix = [
    Task(id=81, description='Wake & call mom', duration=15, dependencies=[], scheduled="08:00", category="Family"),
    Task(id=82, description='Meet friend for coffee', duration=60, dependencies=[], scheduled="10:00", category="Friends"),
    Task(id=83, description='Museum visit', duration=120, dependencies=[82], scheduled="11:30", category="Friends"),
    Task(id=84, description='Lunch with family', duration=60, dependencies=[81], scheduled="13:00", category="Family"),
    Task(id=85, description='Guitar practice', duration=30, dependencies=[], scheduled="16:00", category="Hobby"),
    Task(id=86, description='Group chat planning', duration=10, dependencies=[82], scheduled="09:50", category="Friends"),
    Task(id=87, description='Evening movie', duration=140, dependencies=[84,83], scheduled="19:00", category="Friends"),
    Task(id=88, description='Late night journal', duration=15, dependencies=[], scheduled="23:30", category="Other"),
]

shuffled_order_test = [
    Task(id=91, description='Final meeting', duration=30, dependencies=[94], scheduled="15:00", category="Growth"),
    Task(id=92, description='Prepare slides', duration=60, dependencies=[93], scheduled="13:00", category="Growth"),
    Task(id=93, description='Collect results', duration=45, dependencies=[95], scheduled="12:00", category="Growth"),
    Task(id=94, description='Send invites', duration=10, dependencies=[92], scheduled="11:00", category="Other"),
    Task(id=95, description='Data cleaning', duration=90, dependencies=[96], scheduled="09:00", category="Growth"),
    Task(id=96, description='Experiment run', duration=120, dependencies=[], scheduled="06:00", category="Other"),
    Task(id=97, description='Rehearse talk', duration=20, dependencies=[92], scheduled="14:00", category="Growth"),
    Task(id=98, description='Post event notes', duration=25, dependencies=[91], scheduled="16:00", category="Other"),
]
