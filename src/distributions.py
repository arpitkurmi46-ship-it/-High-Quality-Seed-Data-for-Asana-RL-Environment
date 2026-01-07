import random
import datetime
import math

# ===============================
# Overall task outcome weights
# ===============================
def sample_task_outcome():
    return random.choices(
        ["completed", "in_progress", "abandoned"],
        weights=[0.7, 0.2, 0.1]
    )[0]


# =========================================
# JIRA-calibrated transition probabilities
# =========================================
TRANSITIONS = {
    "To Do": {"In Progress": 1.0},

    "In Progress": {
        "Review": 0.90,     # 90% of tasks proceed normally
        "Blocked": 0.10     # Only 10% get blocked
    },

    "Review": {
        "Done": 0.85,
        "In Progress": 0.15
    },

    "Blocked": {
        "In Progress": 1.0
    },

    "Done": {}
}


# ===============================
# Reopen probability
# ===============================
REOPEN_PROB = 0.12          # matches Jira reopen rate (~12%)
MULTI_REOPEN_PROB = 0.02    # ~2% reopen more than once


def sample_next_status(current):
    possible = TRANSITIONS.get(current, {})
    if not possible:
        return None

    r = random.random()
    cumulative = 0

    for status, prob in possible.items():
        cumulative += prob
        if r <= cumulative:
            return status

    return None


# =========================================
# JIRA-calibrated cycle-time distributions
# =========================================
def sample_time_delta(event_type):

    if event_type == "to_in_progress":
        days = random.lognormvariate(math.log(0.9), 0.30)

    elif event_type == "in_progress_to_review":
        days = random.lognormvariate(math.log(2.2), 0.28)

    elif event_type == "review_to_done":
        # strong increase to match benchmark review ratio
        days = random.lognormvariate(math.log(2.8), 0.35)

    elif event_type == "blocked_to_in_progress":
        days = random.lognormvariate(math.log(4.8), 0.40)

    else:
        days = 0.5

    hours = random.randint(0, 6)
    minutes = random.randint(0, 50)

    return datetime.timedelta(days=max(0, days), hours=hours, minutes=minutes)
