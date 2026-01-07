import random
import datetime
from events import TaskEvent
from distributions import (
    sample_next_status,
    sample_time_delta,
    REOPEN_PROB,
    MULTI_REOPEN_PROB
)

def simulate_task(task_id, created_at, deps, final_status_lookup):

    events = []
    status = "To Do"
    now = created_at

    events.append(TaskEvent(task_id, "CREATED", now, None, status))

    MAX_TRANSITIONS = 20
    transitions = 0
    reopened_once = False

    while transitions < MAX_TRANSITIONS:

        transitions += 1
        next_status = sample_next_status(status)

        if next_status is None:
            break

        # Determine delay type
        if status == "To Do" and next_status == "In Progress":
            evt = "to_in_progress"
        elif status == "In Progress" and next_status == "Review":
            evt = "in_progress_to_review"
        elif status == "Review" and next_status == "Done":
            evt = "review_to_done"
        elif status == "Blocked" and next_status == "In Progress":
            evt = "blocked_to_in_progress"
        else:
            evt = "generic"

        # --------------------------------------
        # SPECIAL RULE: DO NOT ADD DELAY FOR DONE
        # --------------------------------------
        if next_status == "Done":
            # No delay added here!
            events.append(TaskEvent(task_id, "STATUS_CHANGE", now, status, "Done"))
            status = "Done"
        else:
            # Add delay normally
            delay = sample_time_delta(evt)

            try:
                now = now + delay
            except OverflowError:
                now = now + datetime.timedelta(days=1)

            events.append(TaskEvent(task_id, "STATUS_CHANGE", now, status, next_status))
            status = next_status

        # --------------------------------------
        # HANDLE REOPEN LOGIC
        # --------------------------------------
        if status == "Done":

            # First reopen chance
            if random.random() < REOPEN_PROB:
                now += datetime.timedelta(hours=random.randint(1, 3))  # smaller delay
                events.append(TaskEvent(task_id, "REOPENED", now, "Done", "In Progress"))
                status = "In Progress"
                reopened_once = True
                continue

            # Second reopen chance
            if reopened_once and random.random() < MULTI_REOPEN_PROB:
                now += datetime.timedelta(hours=random.randint(1, 2))  # smaller delay
                events.append(TaskEvent(task_id, "REOPENED", now, "In Progress", "Review"))
                status = "Review"
                continue

            # Permanently completed
            events.append(TaskEvent(task_id, "COMPLETED", now, "Review", "Done"))
            break

    return events
