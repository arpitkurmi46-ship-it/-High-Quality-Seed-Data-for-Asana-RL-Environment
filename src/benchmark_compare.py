import sqlite3
import pandas as pd
import numpy as np
from collections import Counter, defaultdict

DB_PATH = "output/asana_simulation.sqlite"

def load_events():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM task_events ORDER BY timestamp", conn)
    conn.close()

    # Use actual column names from your table
    df["new_state"] = df["new_value"]
    df["old_state"] = df["old_value"]

    return df


def compute_transition_probs(df):
    transitions = Counter()
    totals = Counter()

    for task_id, group in df.groupby("task_id"):
        group = group.sort_values("timestamp")

        statuses = list(group["new_state"])

        for i in range(len(statuses) - 1):
            s1 = statuses[i]
            s2 = statuses[i + 1]
            transitions[(s1, s2)] += 1
            totals[s1] += 1

    probs = {k: transitions[k] / totals[k[0]] for k in transitions}
    return probs


def compute_cycle_times(df):
    durations = defaultdict(list)

    for task_id, group in df.groupby("task_id"):
        group = group.sort_values("timestamp")

        prev_status = None
        prev_time = None

        for _, row in group.iterrows():
            if prev_status is not None:
                delta = pd.to_datetime(row["timestamp"]) - pd.to_datetime(prev_time)
                durations[prev_status].append(delta.total_seconds() / 3600)

            prev_status = row["new_state"]
            prev_time = row["timestamp"]

    stats = {
        status: (np.mean(times), np.std(times))
        for status, times in durations.items() if len(times) > 0
    }
    return stats


def compute_reopen_rate(df):
    return len(df[df["event_type"] == "REOPENED"]) / df["task_id"].nunique()


def compute_block_rate(df):
    return len(df[df["new_state"] == "Blocked"]) / df["task_id"].nunique()


def main():
    df = load_events()

    print("\n=== TRANSITION PROBABILITIES ===")
    print(compute_transition_probs(df))

    print("\n=== CYCLE TIMES (hours) ===")
    print(compute_cycle_times(df))

    print("\n=== REOPEN RATE ===")
    print(compute_reopen_rate(df))

    print("\n=== BLOCK RATE ===")
    print(compute_block_rate(df))


if __name__ == "__main__":
    main()
