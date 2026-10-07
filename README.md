# 🐾 PawPal+ — Smart Pet Care Management System

[![Live Demo](https://img.shields.io/badge/demo-LIVE-brightgreen?style=for-the-badge&logo=streamlit)](https://pawpal-plus-esqzqdlgrnnjsezv6a7r4f.streamlit.app)
[![Tests](https://img.shields.io/badge/tests-28%20passing-brightgreen)](https://github.com/codewarrior777/PawPal-Plus/actions)
[![Lint](https://github.com/codewarrior777/PawPal-Plus/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/codewarrior777/PawPal-Plus/actions/workflows/lint.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/codewarrior777/PawPal-Plus)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://github.com/codewarrior777/PawPal-Plus)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/codewarrior777/PawPal-Plus)

A CLI-first Python application for managing pets, their care tasks, and scheduling them intelligently across multiple pets.

**Course:** AI 110 — Foundations of AI Engineering
**Project:** Project 2 (PawPal+)

---

## 🌐 Try It Live

**[▶ Open PawPal+ on Streamlit Cloud](https://pawpal-plus-esqzqdlgrnnjsezv6a7r4f.streamlit.app)**

No installation needed — just click and use it in your browser.

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

### Run tests with coverage

```bash
python -m pytest --cov=pawpal_system --cov-report=term-missing
```

### Install as a package (optional)

```bash
pip install -e .
pawpal    # runs the CLI demo from anywhere
```

---

## 📋 Sample Output

Below is the output from running `main.py` — a walkthrough of the system's core features:

```
🐾 WELCOME TO PAWPAL+ DEMO | Owner: Gustavo 🐾
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

## 📊 Dashboard (Streamlit UI)

The sidebar shows live stats:

- **Total Tasks** — count of all tasks across all pets.
- **Bar chart** — task distribution by priority (HIGH / MEDIUM / LOW).
- **Bar chart** — task distribution per pet.

Powered by Streamlit's built-in `st.bar_chart()`. No extra charting library needed.

---

## 🧠 Scheduler Algorithms

The `Scheduler` class implements eight algorithms:

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
See `benchmark.py` for empirical measurements of each algorithm's scaling.

---

## 📈 Algorithm Benchmarks

`benchmark.py` measures each algorithm at n = 10, 100, 500, 1000, 2000 tasks:

```
╒══════════════════════════════╤════════╤═════════╤═════════╤══════════╤══════════╕
│ Algorithm                    │ n=10   │ n=100   │ n=500   │ n=1000   │ n=2000   │
╞══════════════════════════════╪════════╪═════════╪═════════╪══════════╪══════════╡
│ sort_by_time                 │ 0.00   │ 0.01    │ 0.15    │ 0.25     │ 0.67     │
│ sort_by_priority             │ 0.00   │ 0.04    │ 0.26    │ 0.57     │ 1.80     │
│ detect_conflicts (O(n²))     │ 0.01   │ 0.43    │ 9.19    │ 36.53    │ 148.00   │
│ detect_overlaps (O(n log n)) │ 0.02   │ 0.48    │ 8.21    │ 36.05    │ 120.27   │
│ find_next_available_slot     │ 0.01   │ 0.08    │ 0.54    │ 0.74     │ 1.64     │
╘══════════════════════════════╧════════╧═════════╧═════════╧══════════╧══════════╛
```

The **O(n²) explosion** of `detect_conflicts` at n=2000 (148 ms vs <2 ms for the others) empirically confirms the theoretical complexity.

---

## 🧪 Test Results

28 tests, 100% coverage on `pawpal_system.py`:

```
$ python -m pytest --cov=pawpal_system --cov-report=term-missing -v
============================= test session starts =============================
collected 28 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED          [  3%]
tests/test_pawpal.py::test_task_default_priority_is_medium PASSED       [  7%]
tests/test_pawpal.py::test_task_default_frequency_is_once PASSED        [ 10%]
tests/test_pawpal.py::test_task_to_dict_roundtrip PASSED                [ 14%]
tests/test_pawpal.py::test_add_task_increases_count PASSED              [ 17%]
tests/test_pawpal.py::test_get_incomplete_tasks_filters_correctly PASSED [ 21%]
tests/test_pawpal.py::test_pet_to_dict_roundtrip PASSED                 [ 25%]
tests/test_pawpal.py::test_owner_get_all_tasks_combines_pets PASSED     [ 28%]
tests/test_pawpal.py::test_owner_get_all_tasks_empty PASSED             [ 32%]
tests/test_pawpal.py::test_owner_to_dict_roundtrip PASSED               [ 35%]
tests/test_pawpal.py::test_scheduler_sort_by_time PASSED                [ 39%]
tests/test_pawpal.py::test_sort_by_priority_high_before_low PASSED      [ 42%]
tests/test_pawpal.py::test_sort_by_priority_ties_broken_by_time PASSED  [ 46%]
tests/test_pawpal.py::test_filter_by_completion PASSED                  [ 50%]
tests/test_pawpal.py::test_filter_by_pet_name PASSED                    [ 53%]
tests/test_pawpal.py::test_filter_by_pet_name_returns_empty_for_unknown PASSED [ 57%]
tests/test_pawpal.py::test_detect_conflicts_finds_duplicates PASSED     [ 60%]
tests/test_pawpal.py::test_detect_conflicts_empty_list PASSED           [ 64%]
tests/test_pawpal.py::test_detect_overlaps_within_30_min_window PASSED  [ 67%]
tests/test_pawpal.py::test_detect_overlaps_no_overlap_exact_boundary PASSED [ 71%]
tests/test_pawpal.py::test_handle_recurring_daily PASSED                [ 75%]
tests/test_pawpal.py::test_handle_recurring_weekly PASSED               [ 78%]
tests/test_pawpal.py::test_handle_recurring_once_returns_none PASSED    [ 82%]
tests/test_pawpal.py::test_find_next_available_slot_returns_first_gap PASSED [ 85%]
tests/test_pawpal.py::test_find_next_available_slot_after_dense_morning PASSED [ 89%]
tests/test_pawpal.py::test_find_next_available_slot_returns_none_when_full PASSED [ 92%]
tests/test_pawpal.py::test_json_save_and_load_roundtrip PASSED          [ 96%]
tests/test_pawpal.py::test_json_load_missing_file_returns_empty PASSED  [100%]

---------- coverage: platform win32, python 3.14.0-final-0 -----------
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
pawpal_system.py    116      0   100%
-----------------------------------------------
TOTAL               116      0   100%
============================== 28 passed in 1.40s ==============================
```

**Confidence level in the system:** ⭐⭐⭐⭐⭐ (5/5) — every line of `pawpal_system.py` is covered by an automated test.

---

## 🔄 Continuous Integration

This project runs tests and linting on every push via GitHub Actions:

- **Tests workflow** — runs the full pytest suite on Python 3.12 and 3.13, verifies ≥95% coverage.
- **Lint workflow** — runs `ruff check` and `ruff format --check`.

Both workflows are shown as badges at the top of this README.

Pre-commit hooks (`.pre-commit-config.yaml`) enforce the same checks locally before each commit.

---

## 🚀 Stretch Features Completed

- [x] **JSON Persistence** — Save/load the Owner, Pets, and Tasks to `data.json` via sidebar buttons. Uses `to_dict()`/`from_dict()` round-tripping with ISO dates.
- [x] **Professional UI (tabulate)** — All CLI outputs rendered as ASCII tables with `fancy_grid` format.
- [x] **Advanced Scheduling (priority)** — `sort_by_priority()` sorts by priority (high→medium→low) then by time.
- [x] **Agent Mode Algorithm** — `find_next_available_slot()` finds the earliest free 30/60-min window in the 06:00–22:00 working day. Bonus: `detect_overlaps()` identifies 30-minute window collisions.
- [x] **AI Model Comparison** — Compared ChatGPT vs Gemini on the overlapping-tasks algorithm. See `ai_interactions.md` for the full comparison table.

### Bonus Polish (Portfolio-Grade)

- [x] **Live Deployment** — Public URL on Streamlit Community Cloud
- [x] **GitHub Actions CI** — Tests + lint on Python 3.12 & 3.13
- [x] **Pre-commit hooks** — Ruff, trailing whitespace, EOF, yaml, mixed line endings
- [x] **Ruff** — Linter + formatter, 100% clean
- [x] **`pyproject.toml`** — Installable package with `pawpal` CLI entry point
- [x] **ARCHITECTURE.md** — 6 Architecture Decision Records (ADRs)
- [x] **benchmark.py** — Empirical algorithm complexity comparison
- [x] **MIT LICENSE** + **CONTRIBUTING.md**
- [x] **First-run onboarding** — Dynamic owner name with persistence

---

## 📁 Project Structure

```
PawPal-Plus/
├── .github/
│   └── workflows/
│       ├── tests.yml          # CI: pytest on Python 3.12 + 3.13
│       └── lint.yml           # CI: ruff check + format
├── .streamlit/
│   └── config.toml            # Streamlit theme + config
├── diagrams/
│   ├── README.md              # Rendered UML diagram
│   └── uml_initial.mmd        # Mermaid source
├── tests/
│   └── test_pawpal.py         # pytest suite (28 tests, 100% coverage)
├── app.py                     # Streamlit UI (deployed live)
├── main.py                    # CLI demo script
├── pawpal_system.py           # Core domain logic (4 classes + JSON persistence)
├── benchmark.py               # Algorithm benchmark script
├── demo_output.txt            # Saved output of `python main.py`
├── reflection.md              # Design tradeoffs + AI collaboration notes
├── ai_interactions.md         # Agent workflow + AI model comparison
├── ARCHITECTURE.md            # 6 Architecture Decision Records
├── CONTRIBUTING.md            # Development workflow guide
├── LICENSE                    # MIT License
├── pyproject.toml             # Package metadata + CLI entry point
├── requirements.txt           # Dependencies
├── ruff.toml                  # Ruff linter config
├── .pre-commit-config.yaml    # Pre-commit hooks
├── .gitignore
└── README.md                  # This file
```

---

## 🙏 Credits

Designed and built as part of **AI 110 — Foundations of AI Engineering**. AI assistants (ChatGPT, Gemini) were used as design collaborators; all code was reviewed, tested, and refactored by the student.
