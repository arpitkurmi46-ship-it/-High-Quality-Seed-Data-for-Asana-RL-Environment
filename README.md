Asana-Style Project Dataset Generator

This project creates a synthetic dataset that behaves like real project-management systems such as Asana, Jira, or Linear.
It simulates users, projects, tasks, subtasks, dependencies, and event logs using realistic workflow rules.

The dataset is generated entirely offline and does NOT use any real company data.
All values, timestamps, and records are algorithmically created for research and experimentation.

Features

Generates organizations, users, projects

Creates tasks + optional subtasks

Builds dependencies between tasks

Simulates task lifecycles through:

To Do

In Progress

Review

Blocked

Done

Produces detailed event logs (status changes)

Models realistic delays between events

Assigns tasks based on role matching

Stores everything in a clean SQLite database

Option to benchmark against industry-standard Jira metrics

Project Structure
asana_sim/
│
├── src/
│   ├── main.py                # Main script (generate database)
│   ├── simulator.py           # Lifecycle simulation engine
│   ├── generators.py          # Users, projects, task names
│   ├── distributions.py       # Time delay & probability models
│   ├── dependencies.py        # Dependency generator
│   ├── subtasks.py            # Subtask generator
│   ├── events.py              # TaskEvent class
│   ├── db.py                  # Database connection helpers
│   ├── config.py              # Global configuration
│   └── benchmark_compare.py   # Compare to benchmark metrics
│
├── schema.sql                 # SQLite schema
├── output/
│   └── asana_simulation.sqlite  # Generated dataset
│
└── README.md

Installation

Clone or download the repository

Install dependencies:

pip install -r requirements.txt


(Optional) Create and activate a virtual environment:

python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Mac/Linux

How to Generate the Dataset

Run:

python src/main.py


If successful, you will see:

Inserted tasks: 950+
Inserted events: 4800+


Your SQLite file will appear at:

output/asana_simulation.sqlite

How the Simulation Works
1. Generate Users + Projects

Users are assigned realistic roles (Engineer, QA, PM, etc.)
Projects include names and start dates.

2. Create Tasks

Each project receives a set of tasks.
Tasks are categorised into:

Engineering

Marketing

Operations

3. Add Subtasks

About 40% of tasks automatically receive subtasks (2–5 each).

Each subtask:

Inherits the task category

Receives a new creation timestamp

Is assigned to an appropriate user

4. Generate Dependencies

Random valid dependencies are created while preventing:

Cycles

Self-dependencies

Missing references

5. Simulate Task Lifecycle

Each task moves through realistic states:

To Do → In Progress → Review → Done
              ↘
              Blocked → In Progress


Events include:

CREATED

STATUS_CHANGE

BLOCKED

REOPENED

COMPLETED

Timestamps follow realistic Jira-like statistical distributions.

Database Structure
organizations
Field	Description
org_id	Organization ID
name	Organization name
users
Field	Description
user_id	Unique identifier
name	Username
role	Job role
projects
Field	Description
project_id	Project ID
name	Project name
org_id	Linked organization
start_date	Start timestamp
tasks
Field	Description
id	Unique task ID
project_id	Parent project
name	Task title
status	Final status
assignee_id	Assigned user
created_at	Creation timestamp
completed_at	Completion timestamp
section_id	Board column
parent_task_id	Subtask relationship
task_events

Represents every status change.

Field	Description
event_id	Event ID
task_id	Task reference
event_type	Type of transition
old_value	Previous status
new_value	New status
timestamp	When change happened

Benchmark Analysis (Optional)

To compare synthetic vs benchmark:

python src/benchmark_compare.py


You will see:

Transition probabilities

Mean cycle times

Reopen rate

Blocked rate

These numbers verify that the dataset behaves realistically.

Customization

Update values inside config.py:

NUM_USERS = 25
NUM_PROJECTS = 10
TASKS_PER_PROJECT = 100
START_DATE = datetime.date(2024, 1, 1)


You can easily generate thousands of tasks by increasing these numbers.

Safety

All data is synthetic

No external API access

No personal information

Works fully offline
