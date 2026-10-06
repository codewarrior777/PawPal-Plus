# AI Interactions Log — PawPal+

> Documents how AI assistants were used across the PawPal+ project.

---

## Agent Workflow (Stretch Feature 4)

**Task given to the agent (Gemini):**

```
I need a THIRD algorithmic capability for my Scheduler class that goes
beyond sorting and filtering. Propose a "next available time slot" finder.

Method signature:
find_next_available_slot(self, tasks: list[Task], duration_minutes: int = 30) -> str

- Input: a list of tasks (each with .time in "HH:MM" format)
- Output: the earliest time (as "HH:MM") when there are no tasks scheduled
  for duration_minutes consecutive minutes, starting from 06:00
- Working day: 06:00 to 22:00
- Approach: convert times to minutes-since-midnight, sort, walk through
  the gaps, return the first gap that fits
- Keep it simple — no external libraries
```

**What the agent (Gemini) did:**

1. Proposed a clean algorithm using minutes-since-midnight conversion.
2. Assumed each existing task occupies 30 minutes (Task has no duration field).
3. Handled the working-day boundary (06:00 to 22:00).
4. Handled the edge case of no available slot ("None available today").
5. Added a detailed docstring with Args/Returns.

**What I had to verify or fix manually:**

- **Verified** the algorithm against a hand-computed case: tasks at 07:00 and 08:00 → expected result 06:00 (first free gap). The function returned `06:00`. ✅
- **Documented the 30-minute assumption** in both the docstring and `reflection.md`. This is a limitation — the Scheduler doesn't know task durations, so it uses a fixed 30-minute block for gap calculations.
- **Integrated the method** into `main.py` as Feature 6 with a new table showing next available slots for 30-min and 60-min queries.

**Files modified:**

- `pawpal_system.py` — Added `Scheduler.find_next_available_slot()`
- `main.py` — Added Feature 6 (NEXT AVAILABLE SLOT table)
- `demo_output.txt` — Regenerated with the new section

---

## AI Model Comparison (Stretch Feature 5)

**Task given to both models:**

```
I have a Python class called Scheduler for a pet care app with these methods:
sort_by_time, sort_by_priority, filter_by_completion, filter_by_pet_name,
detect_conflicts, handle_recurring, find_next_available_slot.

Each Task has: description, time ("HH:MM"), due_date, completed,
frequency ("once"|"daily"|"weekly"), priority ("high"|"medium"|"low").

I want to add a NEW method that detects overlapping tasks — where one task's
start time falls within another's duration window. Assume every task takes
30 minutes.

Propose the method signature and a Python implementation.
```

### Model A — Gemini

```python
def find_overlapping_tasks(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
    """Detects pairs of tasks that overlap in time, assuming each task takes 30 minutes.

    Args:
        tasks: List of Task objects, each with a .time attribute in "HH:MM" format.

    Returns:
        A list of tuples, where each tuple contains two overlapping Task objects.
    """
    def time_to_minutes(time_str: str) -> int:
        hrs, mins = map(int, time_str.split(":"))
        return hrs * 60 + mins

    overlapping_pairs = []
    sorted_tasks = sorted(tasks, key=lambda t: time_to_minutes(t.time))

    for i in range(len(sorted_tasks)):
        start_a = time_to_minutes(sorted_tasks[i].time)
        end_a = start_a + 30
        for j in range(i + 1, len(sorted_tasks)):
            start_b = time_to_minutes(sorted_tasks[j].time)
            if start_b >= end_a:
                break
            overlapping_pairs.append((sorted_tasks[i], sorted_tasks[j]))
    return overlapping_pairs
```

### Model B — ChatGPT

```python
def detect_overlaps(self, tasks: list["Task"]) -> list[tuple["Task", "Task"]]:
    """Return pairs of tasks whose 30-minute time windows overlap."""
    overlaps = []

    def to_minutes(time_str: str) -> int:
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

    sorted_tasks = sorted(tasks, key=lambda task: to_minutes(task.time))

    for i, task_a in enumerate(sorted_tasks):
        start_a = to_minutes(task_a.time)
        end_a = start_a + 30
        for task_b in sorted_tasks[i + 1:]:
            start_b = to_minutes(task_b.time)
            if start_b >= end_a:
                break
            if start_b >= start_a:
                overlaps.append((task_a, task_b))
    return overlaps
```

### Comparison Table

| Aspect | Gemini (`find_overlapping_tasks`) | ChatGPT (`detect_overlaps`) |
|---|---|---|
| **Method name** | Verbose, less consistent with existing API | Concise, matches existing `detect_conflicts` |
| **Loop style** | `range(len(...))` + index access | `enumerate()` + slicing (more Pythonic) |
| **Type hints** | Direct `list[Task]` | Quoted `list["Task"]` (unnecessary forward ref) |
| **Redundant checks** | None | Has `if start_b >= start_a:` — always true after sort |
| **Docstring** | Detailed (Args / Returns) | One line only |
| **Early break optimization** | ✅ Uses `if start_b >= end_a: break` | ✅ Same |
| **Correctness** | ✅ Both produce identical results | ✅ Same |

### Final Student Decision

I chose a **hybrid** of the two:

- **Method name** from ChatGPT — `detect_overlaps` matches the existing `detect_conflicts` naming convention.
- **Loop style** from ChatGPT — `enumerate()` + slicing is more idiomatic Python than `range(len())`.
- **Docstring** from Gemini — included full Args/Returns so the method is self-documenting.
- **Removed** ChatGPT's redundant `if start_b >= start_a:` check — after sorting, this condition is always true, so it just adds noise.

**Which model was "better"?**

- **ChatGPT** produced more Pythonic code (`enumerate` + slicing).
- **Gemini** produced a better docstring and did not include the redundant check.

Neither was perfect on its own. The best result came from combining the strengths of each and verifying the behavior with a hand-traced example.

---

## Test Generation (Base Requirement)

**Prompt used:**

```
I need pytest tests for my PawPal+ system with these classes: Task, Pet,
Owner, Scheduler. Write 6 tests covering: mark_complete, add_task,
get_incomplete_tasks, get_all_tasks, sort_by_time, detect_conflicts.
Use date.today() for due_date. Import from pawpal_system.
```

**AI-suggested tests (all passing):**

| # | Test | Verifies |
|---|---|---|
| 1 | `test_mark_complete_changes_status` | `Task.mark_complete()` sets `completed = True` |
| 2 | `test_add_task_increases_count` | `Pet.add_task()` appends to `tasks` |
| 3 | `test_get_incomplete_tasks_filters_correctly` | Incomplete filter excludes completed tasks |
| 4 | `test_owner_get_all_tasks_combines_pets` | `Owner.get_all_tasks()` returns combined list |
| 5 | `test_scheduler_sort_by_time` | `Scheduler.sort_by_time()` returns chronological order |
| 6 | `test_scheduler_detect_conflicts` | `Scheduler.detect_conflicts()` finds same-time pairs |

**Verification:** `python -m pytest -v` → 6 passed in 1.11s.