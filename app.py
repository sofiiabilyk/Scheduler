import streamlit as st
from TaskClass import Task
from TaskSchedulerClass import TaskScheduler
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
if 'task_message' not in st.session_state:
    st.session_state.task_message = {"type": None, "text": ""}

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
    with st.form("add_task_form", clear_on_submit=True):
        # Calculate default task ID
        default_task_id = len(st.session_state.tasks) + 1 if st.session_state.tasks else 1
        
        task_id = st.number_input("Task ID", min_value=1, value=default_task_id, step=1)
        task_description = st.text_input("Task Description", placeholder="e.g., Morning jog")
        task_duration = st.number_input("Duration (minutes)", min_value=1, value=30, step=1)
        
        st.subheader("Optional Settings")
        
        # Dependencies
        if st.session_state.tasks:
            dependency_options = [t['id'] for t in st.session_state.tasks]
            selected_dependencies = st.multiselect(
                "Dependencies (Task IDs that must be completed first)",
                dependency_options,
                help="Select task IDs that must be completed before this task"
            )
        else:
            selected_dependencies = []
            st.info("Add more tasks to set dependencies")
        
        # Scheduled time
        has_scheduled_time = st.checkbox("Has specific scheduled time?")
        if has_scheduled_time:
            scheduled_hour = st.slider("Hour", 0, 23, 9)
            scheduled_minute = st.slider("Minute", 0, 59, 0, step=5)
            scheduled_time = f"{scheduled_hour:02d}:{scheduled_minute:02d}"
        else:
            scheduled_time = "25:25"
        
        # Category
        category = st.selectbox(
            "Category",
            ["Routine", "Family", "Growth", "Friends", "Hobby", "Other"],
            index=5
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
                    st.rerun()
            else:
                st.session_state.task_message = {
                    "type": "error",
                    "text": "Please enter a task description"
                }
    
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
                
                # Create scheduler
                scheduler = TaskScheduler(task_objects)
                
                # Capture output
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                # Run scheduler
                efficiency = scheduler.run_task_scheduler(starting_time)
                
                # Restore stdout
                sys.stdout = old_stdout
                
                # Store output
                output_text = captured_output.getvalue()
                st.session_state.schedule_output = output_text
                
                st.success("Schedule generated successfully! ✅")
                
            except Exception as e:
                st.error(f"Error generating schedule: {str(e)}")
                st.exception(e)

# Display schedule output
if st.session_state.schedule_output:
    st.divider()
    st.header("📊 Generated Schedule")
    
    # Display in a nice format
    output_lines = st.session_state.schedule_output.split('\n')
    
    # Create columns for better layout
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
                st.metric("Scheduler Efficiency", line.split()[-1] + "%" if "%" not in line else line.split()[-1])
            else:
                st.text(line)
    
    # Download button for schedule
    st.download_button(
        label="📥 Download Schedule as Text",
        data=st.session_state.schedule_output,
        file_name=f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Task Scheduler - Priority-based task scheduling system</p>
        <p>Supports dependencies, scheduled times, and category-based prioritization</p>
    </div>
    """,
    unsafe_allow_html=True
)

