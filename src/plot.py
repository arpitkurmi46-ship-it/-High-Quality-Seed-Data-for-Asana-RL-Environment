import sqlite3
import pandas as pd

DB_PATH = "output/asana_simulation.sqlite"

# -------------------------------------
# LOAD synthetic data
# -------------------------------------
conn = sqlite3.connect(DB_PATH)
df_events = pd.read_sql_query("SELECT * FROM task_events", conn)
conn.close()

df_events['timestamp'] = pd.to_datetime(df_events['timestamp'], format="mixed")



# -------------------------------------
# Compute cycle time means per state
# -------------------------------------
def compute_mean_times(df):
    states = ["To Do", "In Progress", "Blocked", "Review", "Done"]
    mean_times = {}

    for s in states:
        durations = []

        for tid, group in df.groupby("task_id"):
            group = group.sort_values("timestamp")

            # find entries where new_value == s
            entries = group[group["new_value"] == s]

            for idx in entries.index:
                if idx + 1 in group.index:
                    start = group.loc[idx, "timestamp"]
                    end = group.loc[idx + 1, "timestamp"]

                    durations.append((end - start).total_seconds() / 3600)

        if len(durations) == 0:
            mean_times[s] = 1
        else:
            mean_times[s] = sum(durations) / len(durations)

    return mean_times



synthetic_means = compute_mean_times(df_events)


# -------------------------------------
# Benchmark means (industry averages)
# -------------------------------------
benchmark_means = {
    "To Do": 30,
    "In Progress": 72,
    "Blocked": 168,
    "Review": 12,
    "Done": 1
}


# -------------------------------------
# Compute relative ratios
# -------------------------------------
def compute_ratios(means, reference="In Progress"):
    base = means[reference]
    return {state: round(means[state] / base, 3) for state in means}


synthetic_ratios = compute_ratios(synthetic_means)
benchmark_ratios = compute_ratios(benchmark_means)


print("\n=== Synthetic Ratios (relative to In Progress) ===")
print(synthetic_ratios)

print("\n=== Benchmark Ratios (relative to In Progress) ===")
print(benchmark_ratios)
