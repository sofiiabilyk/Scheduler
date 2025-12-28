# Task Scheduler 📅

A priority-based task scheduling system that helps you organize your daily tasks efficiently. The scheduler considers task dependencies, scheduled times, and category-based prioritization to create an optimal schedule.

## Features

- **Priority-based Scheduling**: Automatically prioritizes tasks based on categories, dependencies, and scheduled times
- **Task Dependencies**: Define tasks that must be completed before others
- **Flexible Scheduling**: Set specific times for tasks or leave them flexible
- **Category Support**: Organize tasks by categories (Routine, Family, Growth, Friends, Hobby, Other)
- **Web Interface**: Beautiful, user-friendly web interface built with Streamlit

## Live Web Application

🚀 **Access the app**: [Deploy on Streamlit Cloud](#deployment-instructions) (Free!)

## How to Use

### Using the Web Interface

1. Add tasks using the sidebar:
   - Enter Task ID (unique identifier)
   - Add task description
   - Set duration in minutes
   - Optionally set dependencies (other task IDs that must be completed first)
   - Optionally set a specific scheduled time
   - Choose a category

2. Set your starting time

3. Click "Generate Schedule" to get your optimized task schedule

### Using the Python API

```python
from TaskClass import Task
from TaskSchedulerClass import TaskScheduler

# Create tasks
task1 = Task(id=1, description="Wake up", duration=30, category="Routine")
task2 = Task(id=2, description="Breakfast", duration=15, dependencies=[1], category="Routine")

# Create scheduler
scheduler = TaskScheduler([task1, task2])

# Run scheduler
scheduler.run_task_scheduler("09:00")
```

## Installation

### For Local Development

1. Clone the repository:
```bash
git clone https://github.com/sofiiabilyk/Scheduler.git
cd Scheduler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

## Deployment Instructions

### Deploy to Streamlit Cloud (Free) 🌟

1. **Push your code to GitHub** (already done! ✅)

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
   - Sign up/Sign in with your GitHub account
   - Click "New app"
   - Select your repository: `sofiiabilyk/Scheduler`
   - Set Main file path: `app.py`
   - Click "Deploy!"

3. **Your app will be live at**: `https://your-app-name.streamlit.app`

That's it! Your app is now accessible to anyone via the link, completely free!

### Alternative Free Hosting Options

- **Render**: Deploy as a web service (requires minor Flask/FastAPI wrapper)
- **Railway**: Similar to Render, easy deployment
- **HuggingFace Spaces**: If you want to use Gradio instead

## Project Structure

```
.
├── app.py                    # Streamlit web application
├── TaskClass.py              # Task class definition
├── TaskSchedulerClass.py     # Main scheduler logic
├── MaxHeap.py                # Priority queue implementation
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Task Categories & Priorities

The scheduler assigns priorities based on categories:
- **Routine**: 20 points
- **Family**: 15 points
- **Growth**: 15 points
- **Friends**: 10 points
- **Hobby**: 5 points
- **Other**: 0 points

Tasks with dependencies get additional priority boosts, and scheduled tasks are prioritized based on their time.

## License

This project is open source and available for personal and educational use.
