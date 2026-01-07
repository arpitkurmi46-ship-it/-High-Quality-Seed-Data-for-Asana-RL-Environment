import uuid
import random
import datetime

def generate_subtasks(parent_task_id, parent_created_at, task_name, count=3):
    """
    Generate subtasks for a single parent task.
    """
    subtasks = []

    for i in range(count):
        sub_id = str(uuid.uuid4())

        # Subtasks are created shortly after the parent
        created_at = parent_created_at + datetime.timedelta(hours=random.randint(1, 24))

        subtask_name = f"{task_name} - Subtask {i+1}"

        subtasks.append({
            "task_id": sub_id,
            "name": subtask_name,
            "created_at": created_at,
            "parent_task_id": parent_task_id
        })

    return subtasks
