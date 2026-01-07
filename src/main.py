import uuid
import datetime
import random
import os

from db import get_connection, execute_script
from config import *
from generators import generate_users, generate_projects, ENG_TASKS, MARKETING_TASKS, OPS_TASKS
from dependencies import generate_dependencies
from subtasks import generate_subtasks
from simulator import simulate_task
from events import TaskEvent

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
DB_PATH = os.path.join(BASE_DIR, "output", "asana_simulation.sqlite")

ROLE_TASK_MAP = {
    "Engineer": ENG_TASKS,
    "QA": ENG_TASKS,
    "Designer": MARKETING_TASKS,
    "Marketing": MARKETING_TASKS,
    "Product Manager": OPS_TASKS,
    "Operations": OPS_TASKS
}

def safe_execute(conn, query, params, label):
    try:
        conn.execute(query, params)
    except Exception as e:
        print(f"\n❌ ERROR inserting into: {label}")
        print("Query:", query)
        print("Params:", params)
        print("Exception:", e)
        raise


def main():

    # Remove old DB
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            print("DB Browser open! Close it and rerun.")
            return

    conn = get_connection(DB_PATH)
    execute_script(conn, SCHEMA_PATH)

    # ORG
    org_id = str(uuid.uuid4())
    safe_execute(conn, "INSERT INTO organizations VALUES (?,?)",
                 (org_id, "Demo SaaS Org"), "organizations")

    # USERS
    users = generate_users(NUM_USERS)
    for u in users:
        safe_execute(conn, "INSERT INTO users VALUES (?,?,?)",
                     (u["user_id"], u["name"], u["role"]), "users")

    # PROJECTS
    projects = generate_projects(NUM_PROJECTS, org_id, START_DATE)

    for p in projects:

        safe_execute(conn, "INSERT INTO projects VALUES (?,?,?,?)",
                     (p["project_id"], p["name"], p["org_id"], p["start_date"].isoformat()), "projects")

        # Create sections
        sections = ["To Do", "In Progress", "Review", "Done"]
        section_ids = {}
        for s in sections:
            sid = str(uuid.uuid4())
            section_ids[s] = sid
            safe_execute(conn, "INSERT INTO sections VALUES (?,?,?)",
                         (sid, p["project_id"], s), "sections")

        # =====================================================
        # STAGE 1 — GENERATE AND INSERT TASK RECORDS FIRST
        # =====================================================
        task_info = {}
        all_task_ids = []

        # Parent tasks
        for _ in range(TASKS_PER_PROJECT):
            tid = str(uuid.uuid4())
            all_task_ids.append(tid)

            created = p["start_date"] + datetime.timedelta(days=random.randint(0, 10))
            name = random.choice(
                ENG_TASKS if "App" in p["name"] or "API" in p["name"] or "Backend" in p["name"]
                else MARKETING_TASKS if "Campaign" in p["name"] or "Launch" in p["name"]
                else OPS_TASKS
            )

            task_info[tid] = {
                "name": name,
                "created_at": created,
                "parent_task_id": None
            }

        # Add subtasks
        subtask_ids = []
        for parent in list(task_info.keys()):
            if random.random() < 0.4:
                st_list = generate_subtasks(parent, task_info[parent]["created_at"], task_info[parent]["name"], random.randint(2, 5))
                for st in st_list:
                    sid = st["task_id"]
                    subtask_ids.append(sid)
                    all_task_ids.append(sid)
                    task_info[sid] = st

        # NOW insert all tasks BEFORE dependencies
        for tid in all_task_ids:
            info = task_info[tid]
            safe_execute(
                conn,
                "INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?)",
                (tid,
                 p["project_id"],
                 info["name"],
                 "To Do",
                 select_assignee(info["name"], users),
                 info["created_at"].isoformat(),
                 None,
                 section_ids["To Do"],
                 info["parent_task_id"]
                 ),
                "tasks_initial"
            )

        # =====================================================
        # STAGE 2 — INSERT DEPENDENCIES (now tasks exist)
        # =====================================================
        deps = generate_dependencies(all_task_ids)
        for t, d in deps:
            safe_execute(conn,
                         "INSERT INTO task_dependencies VALUES (?,?)",
                         (t, d),
                         "task_dependencies")

        # =====================================================
        # STAGE 3 — SIMULATE AND UPDATE FINAL STATUS
        # =====================================================
        final_status_lookup = {}

        for tid in all_task_ids:

            info = task_info[tid]
            events = simulate_task(tid, info["created_at"], deps, final_status_lookup)

            final_status = events[-1].new if events else "To Do"
            final_status_lookup[tid] = final_status

            completed_at = None
            if any(e.event_type == "COMPLETED" for e in events):
                completed_at = events[-1].timestamp.isoformat()

            section_final = section_ids["Done"] if final_status == "Done" else (
                            section_ids["In Progress"] if final_status == "In Progress" else
                            section_ids["Review"] if final_status == "Review" else
                            section_ids["To Do"]
            )

            # update task record
            safe_execute(
                conn,
                """
                UPDATE tasks
                SET status=?, completed_at=?, section_id=?
                WHERE id=?
                """,
                (final_status, completed_at, section_final, tid),
                "tasks_update"
            )

            # insert events
            for e in events:
                safe_execute(
                    conn,
                    "INSERT INTO task_events VALUES (?,?,?,?,?,?)",
                    (e.event_id, e.task_id, e.event_type, e.old, e.new, e.timestamp.isoformat()),
                    "task_events"
                )

        conn.commit()

    print("Inserted tasks:", conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0])
    print("Inserted events:", conn.execute("SELECT COUNT(*) FROM task_events").fetchone()[0])

    conn.close()


def select_assignee(task_name, users):
    if task_name in ENG_TASKS:
        cat = ENG_TASKS
    elif task_name in MARKETING_TASKS:
        cat = MARKETING_TASKS
    else:
        cat = OPS_TASKS

    eligible = [u for u in users if ROLE_TASK_MAP.get(u["role"]) == cat]
    return random.choice(eligible)["user_id"] if eligible else random.choice(users)["user_id"]


if __name__ == "__main__":
    main()
