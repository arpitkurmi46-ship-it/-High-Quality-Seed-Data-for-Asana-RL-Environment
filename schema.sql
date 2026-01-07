PRAGMA foreign_keys = ON;

-- ORGANIZATIONS
CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT
);

-- USERS
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    role TEXT
);

-- PROJECTS
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    name TEXT,
    org_id TEXT NOT NULL,
    start_date TEXT,
    FOREIGN KEY(org_id) REFERENCES organizations(org_id)
);

-- SECTIONS
CREATE TABLE sections (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT,
    FOREIGN KEY(project_id) REFERENCES projects(project_id)
);

-- TASKS
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT,
    status TEXT,
    assignee_id TEXT,
    created_at TEXT,
    completed_at TEXT,
    section_id TEXT,
    parent_task_id TEXT,
    FOREIGN KEY(project_id) REFERENCES projects(project_id),
    FOREIGN KEY(assignee_id) REFERENCES users(user_id),
    FOREIGN KEY(section_id) REFERENCES sections(id),
    FOREIGN KEY(parent_task_id) REFERENCES tasks(id)
);


-- TASK CUSTOM FIELDS
CREATE TABLE task_custom_fields (
    id TEXT PRIMARY KEY,
    task_id TEXT,
    field_name TEXT,
    field_value TEXT,
    FOREIGN KEY(task_id) REFERENCES tasks(id)
);

-- TASK EVENTS
CREATE TABLE task_events (
    event_id TEXT PRIMARY KEY,
    task_id TEXT,
    event_type TEXT,
    old_value TEXT,
    new_value TEXT,
    timestamp TEXT,
    FOREIGN KEY(task_id) REFERENCES tasks(id)
);

-- TASK DEPENDENCIES
CREATE TABLE task_dependencies (
    task_id TEXT,
    dependency_id TEXT,
    FOREIGN KEY(task_id) REFERENCES tasks(id),
    FOREIGN KEY(dependency_id) REFERENCES tasks(id)
);

-- SUBTASKS
CREATE TABLE subtasks (
    id TEXT PRIMARY KEY,
    parent_id TEXT NOT NULL,
    name TEXT,
    status TEXT,
    created_at TEXT,
    completed_at TEXT,
    FOREIGN KEY(parent_id) REFERENCES tasks(id)
);
