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
- **Sort** tasks chronologically by time
- **Filter** tasks by completion status or by pet name
- **Detect scheduling conflicts** (two tasks at the same time)
- **Generate recurring tasks** automatically (daily or weekly)
- **Persist data** to JSON so it survives between sessions

---

## 🏗️ System Architecture

The system has four core classes (see `diagrams/README.md` for the full UML):

| Class | Responsibility |
|---|---|
| **Task** | Represents a single pet care activity (description, time, due_date, completed, frequency) |
| **Pet** | Stores pet details (name, species, age) and its list of tasks |
| **Owner** | Manages multiple pets and provides combined access to all tasks |
| **Scheduler** | The "brain" — sorts, filters, detects conflicts, and generates recurring tasks |

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

╒════════╤════════════════╤════════╤═════════════╤═════════════╕
│ Time   │ Task           │ Pet    │ Frequency   │ Status      │
╞════════╪════════════════╪════════╪═════════════╪═════════════╡
│ 07:00  │ Morning walk   │ Cooper │ daily       │ ✅ Done     │
├────────┼────────────────┼────────┼─────────────┼─────────────┤
│ 08:00  │ Playtime       │ Cooper │ daily       │ ⏳ Pending  │
├────────┼────────────────┼────────┼─────────────┼─────────────┤
│ 08:00  │ Feed breakfast │ Prince │ daily       │ ⏳ Pending  │
├────────┼────────────────┼────────┼─────────────┼─────────────┤
│ 14:00  │ Vet appointment│ Cooper │ once        │ ⏳ Pending  │
╘════════╧════════════════╧════════╧═════════════╧═════════════╛
...
```

See `demo_output.txt` for the full output with all 5 sections.

---

## 🎨 Professional CLI Output with `tabulate`

The CLI demo (`main.py`) uses the [`tabulate`](https://pypi.org/project/tabulate/) library to render structured ASCII tables for all major features:

| Feature | Table Format | Columns |
|---|---|---|
| Today's Schedule | `fancy_grid` | Time, Task, Pet, Frequency, Status |
| Incomplete Tasks | `fancy_grid` | Time, Task, Pet |
| Conflicts Detected | `fancy_grid` | Time, Task A, Pet A, Task B, Pet B |
| Filter by Pet | `fancy_grid` | Time, Task, Done? |
| Recurring Tasks | `fancy_grid` | Task, Due Date |

**Why `tabulate`?**
- Emojis in cells (✅ / ⏳ / ❌ / 🐾) render natively.
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

============================== 6 passed in 0.73s ==============================
```

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
├── requirements.txt        # Dependencies (streamlit, pytest, tabulate)
└── README.md               # This file
```