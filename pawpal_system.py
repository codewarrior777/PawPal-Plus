"""Module for managing pets, tasks, owners, and scheduling in PawPal+."""

from dataclasses import dataclass, field
from datetime import date
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
        raise NotImplementedError


@dataclass
class Pet:
    """Stores pet details and associated care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new care task to the pet's task list."""
        raise NotImplementedError

    def get_tasks(self) -> list[Task]:
        """Retrieve all tasks associated with this pet."""
        raise NotImplementedError

    def get_incomplete_tasks(self) -> list[Task]:
        """Retrieve pending tasks that are not yet marked as completed."""
        raise NotImplementedError


@dataclass
class Owner:
    """Manages owner information and registered pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        raise NotImplementedError

    def get_all_tasks(self) -> list[Task]:
        """Retrieve a combined list of all tasks across all owned pets."""
        raise NotImplementedError


class Scheduler:
    """Provides utility methods for sorting, filtering, and checking schedules."""

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted chronologically by their time attribute."""
        raise NotImplementedError

    def filter_by_completion(
        self, tasks: list[Task], completed: bool = True
    ) -> list[Task]:
        """Filter tasks based on their completion status."""
        raise NotImplementedError

    def filter_by_pet_name(
        self, owner: Owner, pet_name: str
    ) -> list[Task]:
        """Filter tasks belonging to a specific pet by name."""
        raise NotImplementedError

    def detect_conflicts(
        self, tasks: list[Task]
    ) -> list[tuple[Task, Task]]:
        """Identify and return pairs of tasks scheduled for the same time."""
        raise NotImplementedError

    def handle_recurring(self, task: Task) -> Task | None:
        """Generate the next iteration for recurring daily or weekly tasks."""
        raise NotImplementedError