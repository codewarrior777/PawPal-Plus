"""Module for managing pets, tasks, owners, and scheduling in PawPal+."""

import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Literal


@dataclass
class Task:
    """Represents a single pet care activity."""

    description: str
    time: str
    due_date: date
    completed: bool = False
    frequency: Literal["once", "daily", "weekly"] = "once"

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """Serialize this Task to a JSON-compatible dict."""
        return {
            "description": self.description,
            "time": self.time,
            "due_date": self.due_date.isoformat(),
            "completed": self.completed,
            "frequency": self.frequency,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Reconstruct a Task from a dict (e.g. loaded from JSON)."""
        return cls(
            description=data["description"],
            time=data["time"],
            due_date=date.fromisoformat(data["due_date"]),
            completed=data.get("completed", False),
            frequency=data.get("frequency", "once"),
        )


@dataclass
class Pet:
    """Stores pet details and associated care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new care task to the pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Retrieve all tasks associated with this pet."""
        return self.tasks

    def get_incomplete_tasks(self) -> list[Task]:
        """Retrieve pending tasks that are not yet marked as completed."""
        return [t for t in self.tasks if not t.completed]

    def to_dict(self) -> dict:
        """Serialize this Pet (and its tasks) to a JSON-compatible dict."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        """Reconstruct a Pet (and its tasks) from a dict."""
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(
            name=data["name"],
            species=data["species"],
            age=data["age"],
            tasks=tasks,
        )


@dataclass
class Owner:
    """Manages owner information and registered pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve a combined list of all tasks across all owned pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def to_dict(self) -> dict:
        """Serialize this Owner (and its pets) to a JSON-compatible dict."""
        return {
            "name": self.name,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Owner":
        """Reconstruct an Owner (and its pets) from a dict."""
        pets = [Pet.from_dict(p) for p in data.get("pets", [])]
        return cls(name=data["name"], pets=pets)


class Scheduler:
    """Provides utility methods for sorting, filtering, and checking schedules."""

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted chronologically by their time attribute."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_by_completion(
        self, tasks: list[Task], completed: bool = True
    ) -> list[Task]:
        """Filter tasks based on their completion status."""
        return [t for t in tasks if t.completed == completed]

    def filter_by_pet_name(
        self, owner: Owner, pet_name: str
    ) -> list[Task]:
        """Filter tasks belonging to a specific pet by name."""
        for pet in owner.pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def detect_conflicts(
        self, tasks: list[Task]
    ) -> list[tuple[Task, Task]]:
        """Identify and return pairs of tasks scheduled for the same time."""
        conflicts: list[tuple[Task, Task]] = []
        n = len(tasks)
        for i in range(n):
            for j in range(i + 1, n):
                if tasks[i].time == tasks[j].time:
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts

    def handle_recurring(self, task: Task) -> Task | None:
        """Generate the next iteration for recurring daily or weekly tasks."""
        if task.frequency == "daily":
            next_date = task.due_date + timedelta(days=1)
        elif task.frequency == "weekly":
            next_date = task.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=task.description,
            time=task.time,
            due_date=next_date,
            completed=False,
            frequency=task.frequency,
        )


# ----------------------------------------------------------------------
# JSON Persistence (Stretch Feature)
# ----------------------------------------------------------------------

def save_owner_to_json(owner: Owner, filepath: str) -> None:
    """
    Serialize an Owner (and all its pets and tasks) to a JSON file.

    Args:
        owner: The Owner instance to save.
        filepath: Destination file path (e.g. "data.json").
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(owner.to_dict(), f, indent=4, ensure_ascii=False)


def load_owner_from_json(filepath: str) -> Owner:
    """
    Load an Owner from a JSON file.

    If the file does not exist, returns a new empty Owner named "Alex"
    so the app can start cleanly on first run.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Owner.from_dict(data)
    except FileNotFoundError:
        return Owner(name="Alex")