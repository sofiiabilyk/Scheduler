import streamlit as st
import pandas as pd
from TaskClass import Task
from TaskSchedulerClass import TaskScheduler
from ImprovedGreedy_Scheduler import ImprovedGreedy_Scheduler
from DP_Scheduling import DP_Scheduler
from datetime import datetime
import io
import sys

# Page configuration
st.set_page_config(
    page_title="Task Scheduler",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .task-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'schedule_output' not in st.session_state:
    st.session_state.schedule_output = ""
if 'schedules' not in st.session_state:
    st.session_state.schedules = {
        'simple': {'output': "", 'efficiency': 0, 'name': 'Simple Priority Scheduler'},
        'improved': {'output': "", 'efficiency': 0, 'name': 'Improved Greedy Scheduler'},
        'dp': {'output': "", 'efficiency': 0, 'name': 'DP-Based Scheduler', 'schedule_list': []}
    }
if 'selected_schedule' not in st.session_state:
    st.session_state.selected_schedule = None
if 'task_message' not in st.session_state:
    st.session_state.task_message = {"type": None, "text": ""}
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0
if 'task_description_value' not in st.session_state:
    st.session_state.task_description_value = ""

def create_task(id, description, duration, dependencies, scheduled, category):
    """Create a Task object"""
    return Task(
        id=id,
        description=description,
        duration=duration,
        dependencies=dependencies,
        scheduled=scheduled,
        category=category
    )

def format_schedule_output(captured_output, starting_time):
    """Format the scheduler output for display"""
    output_lines = captured_output.getvalue().split('\n')
    formatted_output = []
    
    for line in output_lines:
        if line.strip():
            if '🕰' in line or '✅' in line or '🏁' in line:
                formatted_output.append(f"**{line}**")
            elif 'started' in line.lower() or 'completed' in line.lower():
                formatted_output.append(f"  {line}")
            else:
                formatted_output.append(line)
    
    return '\n'.join(formatted_output)

# Header
st.markdown('<p class="main-header">📅 Task Scheduler</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Schedule your tasks efficiently with priority-based scheduling</p>', unsafe_allow_html=True)

# Sidebar for adding tasks
with st.sidebar:
    st.header("➕ Add New Task")
    
    # Use form to automatically clear fields after submission
    # Use a key that changes to force form reset after successful submission
    with st.form("add_task_form", clear_on_submit=True, key=f"task_form_{st.session_state.form_key}"):
        # Calculate default task ID
        default_task_id = len(st.session_state.tasks) + 1 if st.session_state.tasks else 1
        
        task_id = st.number_input("Task ID", min_value=1, value=default_task_id, step=1, key=f"task_id_{st.session_state.form_key}")
        
        # Task Description
        # Use session state value if available, otherwise empty
        desc_default = st.session_state.task_description_value if st.session_state.task_description_value else ""
        task_description = st.text_input(
            "Task Description", 
            value=desc_default,
            placeholder="e.g., Morning jog", 
            key=f"task_desc_{st.session_state.form_key}"
        )
        # Sync with session state
        if task_description:
            st.session_state.task_description_value = task_description
        elif not task_description and desc_default:
            st.session_state.task_description_value = ""
        
        task_duration = st.number_input("Duration (minutes)", min_value=1, value=30, step=1, key=f"task_dur_{st.session_state.form_key}")
        
        st.subheader("Optional Settings")
        
        # Dependencies
        if st.session_state.tasks:
            dependency_options = [t['id'] for t in st.session_state.tasks]
            selected_dependencies = st.multiselect(
                "Dependencies (Task IDs that must be completed first)",
                dependency_options,
                help="Select task IDs that must be completed before this task",
                key=f"deps_{st.session_state.form_key}"
            )
        else:
            selected_dependencies = []
            st.info("Add more tasks to set dependencies")
        
        # Scheduled time
        has_scheduled_time = st.checkbox("Has specific scheduled time?", key=f"sched_check_{st.session_state.form_key}")
        if has_scheduled_time:
            scheduled_hour = st.slider("Hour", 0, 23, 9, key=f"hour_{st.session_state.form_key}")
            scheduled_minute = st.slider("Minute", 0, 59, 0, step=5, key=f"min_{st.session_state.form_key}")
            scheduled_time = f"{scheduled_hour:02d}:{scheduled_minute:02d}"
        else:
            scheduled_time = "25:25"
        
        # Category
        category = st.selectbox(
            "Category",
            ["Routine", "Family", "Growth", "Friends", "Hobby", "Other"],
            index=5,
            key=f"cat_{st.session_state.form_key}"
        )
        
        # Add task button (inside form)
        submitted = st.form_submit_button("Add Task", type="primary")
        
        if submitted:
            if task_description:
                new_task = {
                    'id': task_id,
                    'description': task_description,
                    'duration': task_duration,
                    'dependencies': selected_dependencies,
                    'scheduled': scheduled_time,
                    'category': category
                }
                
                # Check if ID already exists
                if any(t['id'] == task_id for t in st.session_state.tasks):
                    st.session_state.task_message = {
                        "type": "error",
                        "text": f"Task ID {task_id} already exists! Please use a different ID."
                    }
                else:
                    st.session_state.tasks.append(new_task)
                    st.session_state.task_message = {
                        "type": "success",
                        "text": f"Task '{task_description}' added!"
                    }
                    # Clear description field
                    st.session_state.task_description_value = ""
                    # Increment form key to force form reset
                    st.session_state.form_key += 1
                    st.rerun()
            else:
                st.session_state.task_message = {
                    "type": "error",
                    "text": "Please enter a task description"
                }
    
    # Clear description button (outside form)
    if st.button("🗑️ Clear Task Description", key=f"clear_desc_btn_{st.session_state.form_key}", help="Clear the description field"):
        st.session_state.task_description_value = ""
        st.rerun()
    
    # Display message outside form (persists after form clears)
    if st.session_state.task_message["type"]:
        if st.session_state.task_message["type"] == "success":
            st.success(st.session_state.task_message["text"])
        elif st.session_state.task_message["type"] == "error":
            st.error(st.session_state.task_message["text"])
        # Clear message after displaying
        st.session_state.task_message = {"type": None, "text": ""}
    
    st.divider()
    
    # Clear all tasks
    if st.button("🗑️ Clear All Tasks", type="secondary"):
        st.session_state.tasks = []
        st.session_state.schedule_output = ""
        st.session_state.schedules = {
            'simple': {'output': "", 'efficiency': 0, 'name': 'Simple Priority Scheduler'},
            'improved': {'output': "", 'efficiency': 0, 'name': 'Improved Greedy Scheduler'},
            'dp': {'output': "", 'efficiency': 0, 'name': 'DP-Based Scheduler', 'schedule_list': []}
        }
        st.session_state.selected_schedule = None
        st.rerun()

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📋 Your Tasks")
    
    if st.session_state.tasks:
        # Display tasks
        for i, task in enumerate(st.session_state.tasks):
            with st.expander(f"Task {task['id']}: {task['description']}", expanded=False):
                st.write(f"**Duration:** {task['duration']} minutes")
                st.write(f"**Category:** {task['category']}")
                if task['scheduled'] != "25:25":
                    st.write(f"**Scheduled Time:** {task['scheduled']}")
                else:
                    st.write("**Scheduled Time:** Flexible")
                if task['dependencies']:
                    st.write(f"**Dependencies:** {', '.join(map(str, task['dependencies']))}")
                
                # Remove button
                if st.button(f"Remove", key=f"remove_{i}"):
                    st.session_state.tasks.pop(i)
                    st.session_state.schedule_output = ""
                    st.session_state.schedules = {
                        'simple': {'output': "", 'efficiency': 0, 'name': 'Simple Priority Scheduler'},
                        'improved': {'output': "", 'efficiency': 0, 'name': 'Improved Greedy Scheduler'},
                        'dp': {'output': "", 'efficiency': 0, 'name': 'DP-Based Scheduler', 'schedule_list': []}
                    }
                    st.session_state.selected_schedule = None
                    st.rerun()
        
        st.info(f"Total tasks: {len(st.session_state.tasks)}")
    else:
        st.info("👆 Add tasks using the sidebar to get started!")

with col2:
    st.header("⚙️ Schedule Settings")
    
    starting_time = st.text_input(
        "Starting Time",
        value="09:00",
        help="Enter start time in HH:MM format (24-hour)",
        placeholder="09:00"
    )
    
    # Validate starting time format
    time_valid = True
    try:
        if starting_time:
            hour, minute = starting_time.split(":")
            if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
                time_valid = False
                st.error("Invalid time format. Use HH:MM (24-hour format)")
    except:
        time_valid = False
        if starting_time:
            st.error("Invalid time format. Use HH:MM (24-hour format)")
    
    st.divider()
    
    # Generate schedule button
    if st.button("🚀 Generate Schedule", type="primary", disabled=not st.session_state.tasks or not time_valid):
        if st.session_state.tasks:
            try:
                # Convert task dictionaries to Task objects
                task_objects = []
                for task_dict in st.session_state.tasks:
                    task_obj = create_task(
                        id=task_dict['id'],
                        description=task_dict['description'],
                        duration=task_dict['duration'],
                        dependencies=task_dict['dependencies'],
                        scheduled=task_dict['scheduled'],
                        category=task_dict['category']
                    )
                    task_objects.append(task_obj)
                
                # Generate schedules using all three approaches
                with st.spinner("Generating schedules with all three algorithms..."):
                    # 1. Simple Priority Scheduler
                    try:
                        old_stdout = sys.stdout
                        sys.stdout = captured_output = io.StringIO()
                        scheduler1 = TaskScheduler(task_objects.copy())
                        efficiency1 = scheduler1.run_task_scheduler(starting_time)
                        sys.stdout = old_stdout
                        output1 = captured_output.getvalue()
                        st.session_state.schedules['simple'] = {
                            'output': output1,
                            'efficiency': efficiency1,
                            'name': 'Simple Priority Scheduler'
                        }
                    except Exception as e:
                        st.session_state.schedules['simple'] = {
                            'output': f"Error: {str(e)}",
                            'efficiency': 0,
                            'name': 'Simple Priority Scheduler'
                        }
                    
                    # 2. Improved Greedy Scheduler
                    try:
                        old_stdout = sys.stdout
                        sys.stdout = captured_output = io.StringIO()
                        scheduler2 = ImprovedGreedy_Scheduler(task_objects.copy())
                        efficiency2 = scheduler2.run_task_scheduler(starting_time)
                        sys.stdout = old_stdout
                        output2 = captured_output.getvalue()
                        st.session_state.schedules['improved'] = {
                            'output': output2,
                            'efficiency': efficiency2,
                            'name': 'Improved Greedy Scheduler'
                        }
                    except Exception as e:
                        st.session_state.schedules['improved'] = {
                            'output': f"Error: {str(e)}",
                            'efficiency': 0,
                            'name': 'Improved Greedy Scheduler'
                        }
                    
                    # 3. DP-Based Scheduler
                    try:
                        old_stdout = sys.stdout
                        sys.stdout = captured_output = io.StringIO()
                        scheduler3 = DP_Scheduler(task_objects.copy())
                        schedule_list = scheduler3.schedule_tasks(starting_time)
                        scheduler3.print_schedule()
                        sys.stdout = old_stdout
                        output3 = captured_output.getvalue()
                        
                        # Calculate efficiency for DP scheduler
                        if schedule_list:
                            total_duration = sum(task.duration for task, _ in schedule_list)
                            first_start = schedule_list[0][1]
                            last_end_time = scheduler3._add_minutes(
                                schedule_list[-1][1],
                                schedule_list[-1][0].duration
                            )
                            total_time = scheduler3.time_difference(first_start, last_end_time)
                            efficiency3 = round((total_duration / total_time * 100), 2) if total_time > 0 else 0
                        else:
                            efficiency3 = 0
                        
                        st.session_state.schedules['dp'] = {
                            'output': output3,
                            'efficiency': efficiency3,
                            'name': 'DP-Based Scheduler',
                            'schedule_list': schedule_list
                        }
                    except Exception as e:
                        st.session_state.schedules['dp'] = {
                            'output': f"Error: {str(e)}",
                            'efficiency': 0,
                            'name': 'DP-Based Scheduler',
                            'schedule_list': []
                        }
                
                st.session_state.selected_schedule = None  # Reset selection
                st.success("All 3 schedules generated successfully! ✅")
                
            except Exception as e:
                st.error(f"Error generating schedule: {str(e)}")
                st.exception(e)

# Display all three schedules
if any(st.session_state.schedules[key]['output'] for key in st.session_state.schedules):
    st.divider()
    st.header("📊 Generated Schedules")
    st.markdown("**Compare the three scheduling approaches and select your preferred one:**")
    
    # Comparison summary table
    summary_data = []
    for key in ['simple', 'improved', 'dp']:
        schedule = st.session_state.schedules[key]
        if schedule['output']:
            summary_data.append({
                'Algorithm': schedule['name'],
                'Efficiency (%)': f"{schedule['efficiency']:.2f}" if schedule['efficiency'] > 0 else "N/A",
                'Status': '✅ Generated' if schedule['efficiency'] > 0 else '❌ Error'
            })
    
    if summary_data:
        st.markdown("### 📈 Quick Comparison")
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Create tabs for each scheduler
    tab1, tab2, tab3 = st.tabs([
        f"📌 {st.session_state.schedules['simple']['name']}",
        f"⚡ {st.session_state.schedules['improved']['name']}",
        f"🎯 {st.session_state.schedules['dp']['name']}"
    ])
    
    # Tab 1: Simple Priority Scheduler
    with tab1:
        st.subheader(st.session_state.schedules['simple']['name'])
        if st.session_state.schedules['simple']['efficiency'] > 0:
            col_eff1, col_btn1 = st.columns([1, 1])
            with col_eff1:
                st.metric("Efficiency", f"{st.session_state.schedules['simple']['efficiency']:.2f}%")
            with col_btn1:
                if st.button("✅ Select This Schedule", key="select_simple", use_container_width=True):
                    st.session_state.selected_schedule = 'simple'
                    st.success("Simple Priority Scheduler selected!")
        
        output_lines = st.session_state.schedules['simple']['output'].split('\n')
        for line in output_lines:
            if line.strip():
                if '🕰' in line:
                    st.markdown(f"### {line}")
                elif '✅' in line or '🏁' in line:
                    st.success(line)
                elif 'started' in line.lower():
                    st.markdown(f"  {line}")
                elif 'completed' in line.lower():
                    st.info(line)
                elif 'efficiency' in line.lower():
                    pass  # Already shown as metric
                else:
                    st.text(line)
    
    # Tab 2: Improved Greedy Scheduler
    with tab2:
        st.subheader(st.session_state.schedules['improved']['name'])
        if st.session_state.schedules['improved']['efficiency'] > 0:
            col_eff2, col_btn2 = st.columns([1, 1])
            with col_eff2:
                st.metric("Efficiency", f"{st.session_state.schedules['improved']['efficiency']:.2f}%")
            with col_btn2:
                if st.button("✅ Select This Schedule", key="select_improved", use_container_width=True):
                    st.session_state.selected_schedule = 'improved'
                    st.success("Improved Greedy Scheduler selected!")
        
        output_lines = st.session_state.schedules['improved']['output'].split('\n')
        for line in output_lines:
            if line.strip():
                if '🕰' in line:
                    st.markdown(f"### {line}")
                elif '✅' in line or '🏁' in line:
                    st.success(line)
                elif 'started' in line.lower():
                    st.markdown(f"  {line}")
                elif 'completed' in line.lower():
                    st.info(line)
                elif 'efficiency' in line.lower():
                    pass  # Already shown as metric
                else:
                    st.text(line)
    
    # Tab 3: DP-Based Scheduler
    with tab3:
        st.subheader(st.session_state.schedules['dp']['name'])
        if st.session_state.schedules['dp']['efficiency'] > 0:
            col_eff3, col_btn3 = st.columns([1, 1])
            with col_eff3:
                st.metric("Efficiency", f"{st.session_state.schedules['dp']['efficiency']:.2f}%")
            with col_btn3:
                if st.button("✅ Select This Schedule", key="select_dp", use_container_width=True):
                    st.session_state.selected_schedule = 'dp'
                    st.success("DP-Based Scheduler selected!")
        
        output_lines = st.session_state.schedules['dp']['output'].split('\n')
        for line in output_lines:
            if line.strip():
                if line.startswith('=') or 'DP-BASED' in line:
                    st.markdown(f"**{line}**")
                elif '🕰' in line:
                    st.markdown(f"### {line}")
                elif '📋' in line or '📊' in line or '⚠️' in line:
                    st.markdown(line)
                elif 'Statistics' in line or 'Total' in line or 'Efficiency' in line:
                    st.info(line)
                else:
                    st.text(line)
    
    # Selected schedule display
    st.divider()
    if st.session_state.selected_schedule:
        st.header("⭐ Your Selected Schedule")
        selected = st.session_state.selected_schedule
        st.success(f"You have selected: **{st.session_state.schedules[selected]['name']}**")
        
        # Display selected schedule prominently
        output_lines = st.session_state.schedules[selected]['output'].split('\n')
        for line in output_lines:
            if line.strip():
                if '🕰' in line:
                    st.markdown(f"### {line}")
                elif '✅' in line or '🏁' in line:
                    st.success(line)
                elif 'started' in line.lower():
                    st.markdown(f"  {line}")
                elif 'completed' in line.lower():
                    st.info(line)
                elif '📋' in line or '📊' in line:
                    st.markdown(line)
                elif 'efficiency' in line.lower() and selected != 'dp':
                    pass
                else:
                    st.text(line)
        
        # Download button for selected schedule
        st.download_button(
            label="📥 Download Selected Schedule as Text",
            data=st.session_state.schedules[selected]['output'],
            file_name=f"schedule_{selected}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    else:
        st.info("👆 Select a schedule from the tabs above to see it displayed here and download it.")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>Task Scheduler</strong> - Advanced multi-algorithm scheduling system</p>
        <p>Three scheduling approaches: Simple Priority, Improved Greedy, and DP-Based</p>
        <p>Supports dependencies, scheduled times, and category-based prioritization</p>
    </div>
    """,
    unsafe_allow_html=True
)

