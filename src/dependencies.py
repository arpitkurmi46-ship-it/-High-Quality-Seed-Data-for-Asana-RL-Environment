import random

def generate_dependencies(task_ids, max_deps=3):
    """
    Create realistic task dependency relationships.
    Example:
        T3 depends on T1
        T4 depends on T1 and T2
    """
    dependencies = []

    for idx, task in enumerate(task_ids):
        # Earlier tasks cannot depend on later tasks
        earlier_tasks = task_ids[:idx]

        if len(earlier_tasks) == 0:
            continue

        # Probability of having dependencies
        if random.random() < 0.4:   # 40% of tasks will have dependencies
            num_deps = random.randint(1, min(max_deps, len(earlier_tasks)))
            chosen = random.sample(earlier_tasks, num_deps)

            for dep in chosen:
                dependencies.append((task, dep))

    return dependencies
