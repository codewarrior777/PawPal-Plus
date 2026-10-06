# 🐾 PawPal+ — Smart Pet Care Management System

A CLI-first Python application for managing pets, their care tasks, and scheduling them intelligently across multiple pets.

**Course:** AI 110 — Foundations of AI Engineering
**Project:** Project 2 (PawPal+)

---

## 📌 What It Does

PawPal+ lets a pet owner:

- Register multiple pets under their name
- Add care tasks to each pet (walks, feeding, meds, vet visits)
- View a **combined daily schedule** across all pets
- **Sort** tasks chronologically by time or by priority (high → medium → low)
- **Filter** tasks by completion status or by pet name
- **Detect scheduling conflicts** (two tasks at the same time)
- **Detect overlaps** (tasks whose 30-minute windows intersect)
- **Find the next available slot** in the day for a new task
- **Generate recurring tasks** automatically (daily or weekly)
- **Persist data** to JSON so it survives between sessions

---

## 🏗️ System Architecture

The system has four core classes (see `diagrams/README.md` for the full UML diagram):

| Class | Responsibility |
|---|---|
| **Task** | Represents a single pet care activity (description, time, due_date, completed, frequency, priority) |
| **Pet** | Stores pet details (name, species, age) and its list of tasks |
| **Owner** | Manages multiple pets and provides combined access to all tasks |
| **Scheduler** | The "brain" — sorts, filters, detects conflicts, generates recurring tasks, finds gaps |

---

## 🚀 How to Run

### Prerequisites

- Python 3.12+

### Setup

```bash
# Clone the repository
git clone https://github.com/codewarrior777/PawPal-Plus.git
cd PawPal-Plus

# Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### Run the CLI demo

```bash
python main.py
```

### Run the Streamlit UI

```bash
python -m streamlit run app.py
```

### Run the tests

```bash
python -m pytest -v
```

---

## 📋 Sample Output

Below is the output from running `main.py` — a walkthrough of the system's core features:

```
🐾 WELCOME TO PAWPAL+ DEMO | Owner: Alex 🐾
============================================================

📅 TODAY'S SCHEDULE (Sorted by Time)

╒════════╤════════════════╤════════╤══════════╤═══════════╤═════════════╕
│ Time   │ Task           │ Pet    │ Priority │ Frequency │ Status      │
╞════════╪════════════════╪════════╪══════════╪═══════════╪═════════════╡
│ 07:00  │ Morning walk   │ Cooper │ HIGH     │ daily     │ ✅ Done     │
│ 08:00  │ Playtime       │ Cooper │ MEDIUM   │ daily     │ ⏳ Pending  │
│ 08:00  │ Feed breakfast │ Prince │ HIGH     │ daily     │ ⏳ Pending  │
│ 14:00  │ Vet appointment│ Cooper │ LOW      │ once      │ ⏳ Pending  │
╘════════╧════════════════╧════════╧══════════╧═══════════╧═════════════╛

⭐ PRIORITY SCHEDULE (High → Medium → Low, then Time)

╒══════════╤════════╤════════════════╤════════╕
│ Priority │ Time   │ Task           │ Pet    │
╞══════════╪════════╪════════════════╪════════╡
│ HIGH     │ 07:00  │ Morning walk   │ Cooper │
│ HIGH     │ 08:00  │ Feed breakfast │ Prince │
│ MEDIUM   │ 08:00  │ Playtime       │ Cooper │
│ LOW      │ 14:00  │ Vet appointment│ Cooper │
╘══════════╧════════╧════════════════╧════════╛

⏳ INCOMPLETE TASKS

╒════════╤════════════════╤════════╤══════════╕
│ Time   │ Task           │ Pet    │ Priority │
╞════════╪════════════════╪════════╪══════════╡
│ 08:00  │ Playtime       │ Cooper │ MEDIUM   │
│ 14:00  │ Vet appointment│ Cooper │ LOW      │
│ 08:00  │ Feed breakfast │ Prince │ HIGH     │
╘════════╧════════════════╧════════╧══════════╛

⚠️  CONFLICTS DETECTED

╒════════╤══════════╤════════╤════════╤════════════════╤════════╤════════╕
│ Time   │ Task A   │ Pet A  │ Pri A  │ Task B         │ Pet B  │ Pri B  │
╞════════╪══════════╪════════╪════════╪════════════════╪════════╪════════╡
│ 08:00  │ Playtime │ Cooper │ MEDIUM │ Feed breakfast │ Prince │ HIGH   │
╘════════╧══════════╧════════╧════════╧════════════════╧════════╧════════╛

🐶 COOPER'S TASKS

╒════════╤════════════════╤══════════╤═══════╕
│ Time   │ Task           │ Priority │ Done? │
╞════════╪════════════════╪══════════╪═══════╡
│ 07:00  │ Morning walk   │ HIGH     │ ✅    │
│ 08:00  │ Playtime       │ MEDIUM   │ ❌    │
│ 14:00  │ Vet appointment│ LOW      │ ❌    │
╘════════╧════════════════╧══════════╧═══════╛

🕐 NEXT AVAILABLE SLOT

╒════════════╤═══════════════════════════╕
│ Duration   │ Earliest Available Start  │
╞════════════╪═══════════════════════════╡
│ 30 minutes │ 06:00                     │
│ 60 minutes │ 06:00                     │
╘════════════╧═══════════════════════════╛

🔄 RECURRING TASK GENERATION

╒══════════╤════════════════╤════════════╤══════════╕
│          │ Task           │ Due Date   │ Priority │
╞══════════╪════════════════╪════════════╪══════════╡
│ Original │ Morning walk   │ 2026-10-06 │ high     │
│ Next Due │ Morning walk   │ 2026-10-07 │ high     │
╘══════════╧════════════════╧════════════╧══════════╛
```

See `demo_output.txt` for the full unredacted output.

---

## 🎨 Professional CLI Output with `tabulate`

The CLI demo (`main.py`) uses the [`tabulate`](https://pypi.org/project/tabulate/) library to render structured ASCII tables for all major features:

| Feature | Table Format | Columns |
|---|---|---|
| Today's Schedule | `fancy_grid` | Time, Task, Pet, Priority, Frequency, Status |
| Priority Schedule | `fancy_grid` | Priority, Time, Task, Pet |
| Incomplete Tasks | `fancy_grid` | Time, Task, Pet, Priority |
| Conflicts Detected | `fancy_grid` | Time, Task A, Pet A, Pri A, Task B, Pet B, Pri B |
| Filter by Pet | `fancy_grid` | Time, Task, Priority, Done? |
| Next Available Slot | `fancy_grid` | Duration, Earliest Available Start |
| Recurring Tasks | `fancy_grid` | Task, Due Date, Priority |

**Why `tabulate`?**

- Emojis in cells (✅ / ⏳ / ❌) render natively.
- The `fancy_grid` format uses Unicode box-drawing characters, far more readable than raw dashes.
- Zero-config: pass a list of rows + a headers list, get a formatted string.

---

## 💾 JSON Persistence

The Streamlit UI has **Save to JSON** and **Load from JSON** buttons in the sidebar. Data is stored in `data.json` (git-ignored).

```python
# Save the current owner + pets + tasks
save_owner_to_json(owner, "data.json")

# Load on next app start
owner = load_owner_from_json("data.json")
```

If `data.json` does not exist, a new empty owner is created automatically.

**How it works:**

- Each class implements `to_dict()` / `from_dict()` for round-trip serialization.
- `date` objects are converted to ISO strings (`"YYYY-MM-DD"`) for JSON compatibility and parsed back on load.
- The JSON file uses `indent=4` and `ensure_ascii=False` so emojis render correctly in the file.

---

## 🧠 Scheduler Algorithms

The `Scheduler` class implements seven algorithms:

| Method | Purpose | Complexity |
|---|---|---|
| `sort_by_time(tasks)` | Chronological sort by "HH:MM" string | O(n log n) |
| `sort_by_priority(tasks)` | Priority-first sort (high → medium → low), then time | O(n log n) |
| `filter_by_completion(tasks, completed)` | Return tasks matching completion status | O(n) |
| `filter_by_pet_name(owner, pet_name)` | Return tasks for a specific pet | O(pets) |
| `detect_conflicts(tasks)` | Find pairs with identical times | O(n²) |
| `detect_overlaps(tasks)` | Find pairs whose 30-min windows intersect | O(n log n) |
| `handle_recurring(task)` | Generate next occurrence for daily/weekly | O(1) |
| `find_next_available_slot(tasks, duration)` | Earliest free gap in 06:00–22:00 day | O(n log n) |

See `reflection.md` for design tradeoffs and complexity notes.

---

## 🧪 Test Results

```
$ python -m pytest -v
============================= test session starts =============================
collected 6 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED          [ 16%]
tests/test_pawpal.py::test_add_task_increases_count PASSED              [ 33%]
tests/test_pawpal.py::test_get_incomplete_tasks_filters_correctly PASSED [ 50%]
tests/test_pawpal.py::test_owner_get_all_tasks_combines_pets PASSED     [ 66%]
tests/test_pawpal.py::test_scheduler_sort_by_time PASSED                [ 83%]
tests/test_pawpal.py::test_scheduler_detect_conflicts PASSED            [100%]

============================== 6 passed in 1.11s ==============================
```

**Confidence level in the system:** ⭐⭐⭐⭐☆ (4/5) — all core behaviors are tested; edge cases for `find_next_available_slot` and `detect_overlaps` are manually verified but not automated.

---

## 🚀 Stretch Features Completed

- [x] **JSON Persistence** — Save/load the Owner, Pets, and Tasks to `data.json` via sidebar buttons. Uses `to_dict()`/`from_dict()` round-tripping with ISO dates.
- [x] **Professional UI (tabulate)** — All CLI outputs rendered as ASCII tables with `fancy_grid` format.
- [x] **Advanced Scheduling (priority)** — `sort_by_priority()` sorts by priority (high→medium→low) then by time.
- [x] **Agent Mode Algorithm** — `find_next_available_slot()` finds the earliest free 30/60-min window in the 06:00–22:00 working day. Bonus: `detect_overlaps()` identifies 30-minute window collisions.
- [x] **AI Model Comparison** — Compared ChatGPT vs Gemini on the overlapping-tasks algorithm. See `ai_interactions.md` for the full comparison table.

---

## 📁 Project Structure

```
PawPal-Plus/
├── diagrams/
│   ├── README.md           # Rendered UML diagram
│   └── uml_initial.mmd     # Mermaid source
├── tests/
│   └── test_pawpal.py      # pytest suite (6 tests)
├── app.py                  # Streamlit UI
├── main.py                 # CLI demo script
├── pawpal_system.py        # Core domain logic (4 classes + JSON persistence)
├── demo_output.txt         # Saved output of `python main.py`
├── reflection.md           # Design tradeoffs + AI collaboration notes
├── ai_interactions.md      # Agent workflow + AI model comparison
├── requirements.txt        # Dependencies (streamlit, pytest, tabulate)
└── README.md               # This file
```

---

## 🙏 Credits

Designed and built as part of AI 110 — Foundations of AI Engineering. AI assistants (ChatGPT, Gemini) were used as design collaborators; all code was reviewed, tested, and refined by the student.