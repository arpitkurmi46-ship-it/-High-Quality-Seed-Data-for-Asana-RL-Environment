import uuid

class TaskEvent:
    def __init__(self, task_id, event_type, timestamp, old=None, new=None):
        self.event_id = str(uuid.uuid4())
        self.task_id = task_id
        self.event_type = event_type
        self.timestamp = timestamp
        self.old = old
        self.new = new
