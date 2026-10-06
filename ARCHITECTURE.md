# Architecture Decision Records (ADRs) — PawPal+

This document captures the key architectural decisions made during the design and implementation of PawPal+.

---

## ADR-001: Four-class design with dataclasses

**Status:** Accepted

**Context:**
The system needs to model pets, tasks, owners, and scheduling logic. The Mermaid UML from Phase 1 specified four classes: `Task`, `Pet`, `Owner`, `Scheduler`.

**Decision:**
- Use `@dataclass` for `Task`, `Pet`, `Owner` (data-focused classes).
- Use a plain class for `Scheduler` (behavior-focused service class).

**Rationale:**
- Dataclasses give us `__init__`, `__repr__`, and `__eq__` for free, eliminating boilerplate for pure-data classes.
- The `Scheduler` class contains algorithms, not data — a dataclass would add nothing.
- The four-class split keeps data (Task/Pet/Owner) separate from behavior (Scheduler), which makes the algorithms unit-testable in isolation.

**Consequences:**
- ✅ Tests can pass plain `list[Task]` to `Scheduler` methods without setting up an `Owner`/`Pet` hierarchy.
- ⚠️ Methods like `filter_by_pet_name` take an `Owner` (not just tasks) — a minor coupling tradeoff to support pet-name-based filtering.

---

## ADR-002: `st.session_state` for state persistence in Streamlit

**Status:** Accepted

**Context:**
Streamlit re-executes the entire script top-to-bottom on every user interaction. Plain variables lose their value between reruns.

**Decision:**
Store the `Owner` and `Scheduler` instances in `st.session_state`.

**Rationale:**
- `session_state` is the official Streamlit mechanism for cross-rerun persistence.
- Storing the entire `Owner` object (not individual fields) keeps serialization simple and keeps the domain model intact.

**Consequences:**
- ✅ Adding pets / tasks persists across UI interactions.
- ✅ JSON save/load integrates naturally by replacing `session_state.owner`.
- ⚠️ The "Reset System" button must explicitly reset `session_state.owner`.

---

## ADR-003: JSON over CSV for persistence

**Status:** Accepted

**Context:**
The stretch feature requires persistent storage of pets and tasks between runs. Options: JSON, CSV, SQLite.

**Decision:**
Use JSON with `indent=4` and `ensure_ascii=False`.

**Rationale:**
- JSON natively handles **nested structures** (Owner → Pets → Tasks), unlike CSV.
- Emojis in task descriptions render correctly with `ensure_ascii=False`.
- No external DB dependency; the file is human-readable and versionable.
- CSV would require flattening the hierarchy and writing custom join logic.
- SQLite would work but is overkill for a single-owner CLI-first app.

**Consequences:**
- ✅ Simple `to_dict()` / `from_dict()` round-trip on each class.
- ✅ ISO-8601 dates survive serialization without a custom encoder.
- ⚠️ No atomic writes or concurrency safety — acceptable for single-user desktop app.

---

## ADR-004: Priority-based sort as a tuple sort key

**Status:** Accepted

**Context:**
Tasks have a `priority` field (`high` / `medium` / `low`). We need to sort by priority, and within the same priority, by time.

**Decision:**
Use a priority-to-integer mapping and a tuple sort key:

```python
_PRIORITY_ORDER: ClassVar[dict[str, int]] = {"high": 0, "medium": 1, "low": 2}

def sort_by_priority(self, tasks):
    return sorted(tasks, key=lambda t: (self._PRIORITY_ORDER[t.priority], t.time))