"""Module for managing pets, tasks, owners, and scheduling in PawPal+."""

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